# -*- coding: utf8 -*-

"""
Eines per a la connexió a bases de dades relacionals (Oracle i MariaDB)
i la manipulació de les seves dades i estructures.
"""

import os
import random
import subprocess
import time

import cx_Oracle
import MySQLdb.cursors

from .constants import (APP_CHARSET, IS_PYTHON_3, TMP_FOLDER,
                        MARIA_CHARSET, MARIA_COLLATE, MARIA_STORAGE)
from .aes import AESCipher
from .services import DB_INSTANCES, DB_CREDENTIALS
from .textfile import TextFile


class Database(object):
    """
    Classe principal. S'instancia per cada connexió a una base de dades.
    Tots els mètodes es poden utilitzar per Oracle i MariaDB
    si no s'especifica el contrari.
    """

    def __init__(self, instance, schema, retry=None):
        """
        Inicialització de paràmetres i connexió a la base de dades.
        En cas d'error, intenta cada (retry) segons.
        """
        attributes = DB_INSTANCES[instance]
        self.engine = attributes['engine']
        self.host = attributes['host']
        self.port = attributes['port']
        if self.engine == 'my':
            self.local_infile = attributes['local_infile']
            self.user, self.password = DB_CREDENTIALS[instance]
            self.database = schema
        elif self.engine == 'ora':
            self.sid = attributes.get('sid', None)
            self.service_name = attributes.get('service_name', None)
            self.user, self.password = DB_CREDENTIALS[instance][schema]
        self.available = False
        while not self.available:
            try:
                self.connect()
            except Exception as e:
                if '1049' in str(e):
                    self.connect(existent=False)
                    self.recreate_database()
                elif retry:
                    time.sleep(retry)
                else:
                    raise
            else:
                self.available = True

    def connect(self, existent=True):
        """Desencripta password i connecta a la base de dades."""
        password = AESCipher().decrypt(self.password) if self.password else ''
        if self.engine == 'my':
            self.connection = MySQLdb.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=password,
                db=self.database if existent else 'information_schema',
                cursorclass=MySQLdb.cursors.SSCursor,
                charset=APP_CHARSET,
                use_unicode=IS_PYTHON_3,
                local_infile=1 * self.local_infile
            )
        elif self.engine == 'ora':
            if self.sid:
                self.dsn = cx_Oracle.makedsn(self.host, self.port, self.sid)
            else:
                self.dsn = cx_Oracle.makedsn(self.host,
                                             self.port,
                                             service_name=self.service_name)
            self.connection = cx_Oracle.connect(self.user, password, self.dsn)

    def execute(self, sql):
        """Executa una sentència SQL."""
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        self.cursor.close()
        self.connection.commit()

    def recreate_database(self):
        """Elimina i torna a crear una base de dades (MariaDB)."""
        self.execute('drop database if exists {}'.format(self.database))
        sql = 'create database {} character set {} collate {}'
        self.execute(sql.format(self.database, MARIA_CHARSET, MARIA_COLLATE))
        self.execute('use {}'.format(self.database))

    def create_table(self, table, columns,
                     pk=None, partitions=None, remove=False):
        """Crea una taula a la base de dades."""
        if remove:
            try:
                self.execute('drop table {}'.format(table))
            except:
                pass
        if pk:
            if self.engine == 'my':
                spec = '({}, PRIMARY KEY ({}))'.format(', '.join(columns),
                                                       ', '.join(pk))
            elif self.engine == 'ora':
                spec = '({}, CONSTRAINT {}_pk PRIMARY KEY ({}))'.format(
                    ', '.join(columns),
                    table,
                    ', '.join(pk))
        else:
            spec = '({})'.format(', '.join(columns))
        if self.engine == 'my':
            this = ' engine {} character set {} collate {}'
            spec += this.format(MARIA_STORAGE, MARIA_CHARSET, MARIA_COLLATE)
        if partitions:
            this = ' partition by hash (id) partitions {}'
            spec += this.format(partitions)
        try:
            self.execute('create table {} {}'.format(table, spec))
        except Exception as e:
            s = str(e)
            if not any([word in s for word in ('1050', 'ORA-00955')]):
                raise e

    def get_all(self, sql):
        """
        Crea un generator que retorna d'un en un tots els registres
        obtinguts per una sentència SQL.
        """
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        for row in self.cursor:
            yield row
        self.cursor.close()

    def get_many(self, sql, n):
        """
        Crea un generator que retorna de n en n tots els registres
        obtinguts per una sentència SQL.
        """
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        while True:
            result = self.cursor.fetchmany(n)
            if not result:
                break
            yield result
        self.cursor.close()

    def get_one(self, sql):
        """Retorna un registre d'una sentència SQL."""
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        resul = self.cursor.fetchone()
        self.cursor.close()
        return resul

    def list_to_table(self, iterable, table, partition=None):
        """Insereix un iterable a una taula."""
        if self.engine == 'my':
            rand = random.randrange(0, 2 ** 64)
            filename = '{}/{}_{}.txt'.format(TMP_FOLDER, table, rand)
            partition = 'PARTITION ({})'.format(partition) if partition else ''
            delimiter = '@,'
            endline = '|;'
            with TextFile(filename) as file:
                file.write_iterable(iterable, delimiter, endline)
            sql = "LOAD DATA {local} INFILE '{filename}' \
                   ignore INTO TABLE {table} {partition} \
                   CHARACTER SET {charset} \
                   FIELDS TERMINATED BY '{delimiter}' \
                   LINES TERMINATED BY '{endline}'"
            sql = sql.format(
                local='LOCAL' if self.local_infile else '',
                filename=filename,
                table=table,
                partition=partition,
                charset=APP_CHARSET,
                delimiter=delimiter,
                endline=endline
            )
            self.execute(sql)
            os.remove(filename)
        elif self.engine == 'ora':
            values = [':{}'.format(i + 1) for i in range(len(iterable[0]))]
            values = ', '.join(values)
            self.cursor = self.connection.cursor()
            sql = 'insert into {} VALUES ({})'
            self.cursor.prepare(sql.format(table, values))
            self.cursor.executemany(None, iterable)
            self.cursor.close()
            self.connection.commit()

    def get_table_owner(self, table):
        """Retorna el propietari i el nom original d'una taula (Oracle)."""
        table = table.upper()
        try:
            sql = "select table_name from user_tables \
                   where table_name = '{}'"
            table, = self.get_one(sql.format(table))
            owner, = self.get_one('select user from dual')
        except TypeError:
            try:
                sql = "select table_owner, table_name from user_synonyms \
                       where synonym_name = '{}'"
                owner, table = self.get_one(sql.format(table))
                try:
                    sql = "select table_owner, table_name from all_synonyms \
                           where owner = '{}' and synonym_name = '{}'"
                    owner, table = self.get_one(sql.format(owner, table))
                except TypeError:
                    pass
            except TypeError:
                try:
                    sql = "select table_owner, table_name from all_synonyms \
                           where owner = 'PUBLIC' and synonym_name = '{}'"
                    owner, table = self.get_one(sql.format(table))
                except TypeError:
                    sql = "select owner, table_name from all_tables \
                           where table_name = '{}'"
                    owner, table = self.get_one(sql.format(table))
        return owner, table

    def get_table_count(self, table):
        """Retorna el número de registres d'una taula."""
        if self.engine == 'my':
            sql = "select table_rows from information_schema.tables \
                   where table_schema = '{}' and table_name = '{}'"
            sql = sql.format(self.database, table)
        elif self.engine == 'ora':
            owner, table = self.get_table_owner(table)
            sql = "select nvl(num_rows, 0) from all_tables \
                   where owner = '{}' and table_name = '{}'"
            sql = sql.format(owner.upper(), table.upper())
        rows, = self.get_one(sql)
        return rows

    def get_table_partitions(self, table):
        """
        Retorna un diccionari amb les particions d'una taula
        i el seu número de registres.
        """
        if self.engine == 'my':
            sql = "select partition_name, table_rows \
                   from information_schema.partitions \
                   where table_schema = '{}' and table_name = '{}' \
                   and partition_name is not null"
            sql = sql.format(self.database, table)
        elif self.engine == 'ora':
            owner, table = self.get_table_owner(table)
            sql = "select partition_name, nvl(num_rows, 0) \
                   from all_tab_partitions \
                   where table_owner = '{}' and table_name = '{}'"
            sql = sql.format(owner.upper(), table.upper())
        partitions = {}
        for partition, rows in self.get_all(sql):
            partitions[partition] = rows
        return partitions

    def get_table_columns(self, table):
        if self.engine == 'my':
            sql = "select column_name from information_schema.columns \
                   where table_schema = '{}' and table_name = '{}' \
                   order by ordinal_position".format(self.database, table)
        elif self.engine == 'ora':
            owner, table_real = self.get_table_owner(table)
            sql = "select column_name from all_tab_columns \
                   where owner = '{}' and table_name='{}' \
                   order by column_id".format(owner.upper(),
                                              table_real.upper())
        columns = [column for column, in self.get_all(sql)]
        return columns

    def get_column_information(self, column, table, desti='my'):
        if self.engine == 'my':
            sql = "select column_type, data_type, character_maximum_length, \
                   numeric_precision from information_schema.columns \
                   where table_schema = '{}' and table_name = '{}' \
                   and column_name = '{}'".format(self.database, table, column)
            done, type, char, num = self.get_one(sql)
            length, precision, scale = None, None, None
        elif self.engine == 'ora':
            owner, table_real = self.get_table_owner(table)
            sql = "select data_type, data_length, data_precision, data_scale \
                   from all_tab_columns \
                   where owner = '{}' and table_name = '{}' \
                   and column_name = '{}'".format(owner.upper(),
                                                  table_real.upper(),
                                                  column.upper())
            type, length, precision, scale = self.get_one(sql)
            done, char, num = None, None, None
            words_in = ('DAT', 'VAL_D_V')
            words_out = ('EDAT',)
            if type == 'NUMBER' and \
               any([word in column.upper() for word in words_in]) and \
               not any([word in column.upper() for word in words_out]):
                type = 'DATE_J'
        param = {'column': column, 'length': length,
                 'precision': precision, 'scale': scale,
                 'done': done, 'char': char, 'num': num}
        conv = {('my', 'date', 'my', 'create'): '{column} {done}',
                ('my', 'date', 'my', 'query'):
                    "date_format({column}, '%Y%m%d')",
                ('my', 'date', 'ora', 'create'): '{column} date',
                ('my', 'date', 'ora', 'query'): column,
                ('my', 'int', 'my', 'create'): '{column} {done}',
                ('my', 'int', 'my', 'query'): column,
                ('my', 'int', 'ora', 'create'): '{column} number({num})',
                ('my', 'int', 'ora', 'query'): column,
                ('my', 'double', 'my', 'create'): '{column} {done}',
                ('my', 'double', 'my', 'query'): column,
                ('my', 'double', 'ora', 'create'): '{column} number({num})',
                ('my', 'double', 'ora', 'query'): column,
                ('my', 'varchar', 'my', 'create'): '{column} {done}',
                ('my', 'varchar', 'my', 'query'): column,
                ('my', 'varchar', 'ora', 'create'):
                    '{column} varchar2({char})',
                ('my', 'varchar', 'ora', 'query'): column,
                ('ora', 'DATE', 'my', 'create'): '{column} date',
                ('ora', 'DATE', 'my', 'query'):
                    "to_char({column}, 'YYYYMMDD')",
                ('ora', 'DATE', 'ora', 'create'): '{column} date',
                ('ora', 'DATE', 'ora', 'query'): column,
                ('ora', 'DATE_J', 'my', 'create'): '{column} date',
                ('ora', 'DATE_J', 'my', 'query'):
                    "to_char(to_date({column}, 'J'), 'YYYYMMDD')",
                ('ora', 'DATE_J', 'ora', 'create'): '{column} date',
                ('ora', 'DATE_J', 'ora', 'query'): "to_date({column}, 'J')",
                ('ora', 'NUMBER', 'my', 'create'):
                    '{column} int' if scale == 0 else '{column} double',
                ('ora', 'NUMBER', 'my', 'query'):
                    '{column} number({precision}, {scale})',
                ('ora', 'NUMBER', 'ora', 'create'):
                    '{column} number({precision}, {scale})',
                ('ora', 'NUMBER', 'ora', 'query'): column,
                ('ora', 'VARCHAR2', 'my', 'create'):
                    "{column} varchar({length})",
                ('ora', 'VARCHAR2', 'my', 'query'):
                    'ltrim(rtrim({column}))' if length > 49 else column,
                ('ora', 'VARCHAR2', 'ora', 'create'):
                    '{column} varchar2({length})',
                ('ora', 'VARCHAR2', 'ora', 'query'): column}
        resul = {key: conv[(self.engine, type, desti, key)].format(**param)
                 for key in ('create', 'query')}
        return resul

    def disconnect(self):
        """Desconnecta de la base de dades."""
        self.connection.close()

    def __enter__(self):
        """Context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager."""
        self.disconnect()
