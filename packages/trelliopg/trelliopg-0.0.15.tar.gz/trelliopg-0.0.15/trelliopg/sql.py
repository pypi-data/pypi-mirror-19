import functools
import itertools
import os
import sys

from asyncpg.connection import Connection
from asyncpg.pool import Pool, create_pool

PY_36 = sys.version_info >= (3, 6)

try:
    import ujson as json
except ImportError:
    import json


def get_db_settings(config_file=None):
    if not config_file:
        config_file = os.environ.get('CONFIG_FILE')

    if not config_file:
        config_file = './config.json'

    with open(config_file) as f:
        settings = json.load(f)

        if 'DATABASE_SETTINGS' not in settings.keys():
            raise KeyError('"DATABASE_SETTINGS" key not found in config file')

    return settings['DATABASE_SETTINGS']


def get_db_adapter(settings=None, config_file=None):
    if not settings:
        settings = get_db_settings(config_file)

    db_adapter = DBAdapter(**settings)
    return db_adapter


def async_atomic(func):
    '''
    first argument will be a conn object
    :param func:
    :return:
    '''
    _db_adapter = get_db_adapter()

    @functools.wraps(func)
    async def wrapped(self, *args, **kwargs):
        conn = None
        for i in itertools.chain(args, kwargs.values()):
            if type(i) is Connection:
                conn = i
                break
        if not conn:
            pool = await _db_adapter.get_pool()
            async with pool.acquire() as conn:
                async with conn.transaction():
                    return await func(self, conn, *args, **kwargs)
        else:
            async with conn.transaction():
                return await func(self, *args, **kwargs)

    return wrapped


def async_atomic_func(func):
    _db_adapter = get_db_adapter()

    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        conn = None
        for i in itertools.chain(args, kwargs.values()):
            if type(i) is Connection:
                conn = i
                break
        if not conn:
            pool = await _db_adapter.get_pool()
            async with pool.acquire() as conn:
                async with conn.transaction():
                    return await func(conn, *args, **kwargs)
        else:
            async with conn.transaction():
                return await func(*args, **kwargs)

    return wrapped


class Borg(object):
    __shared_state = dict()

    def __init__(self):
        self.__dict__ = self.__shared_state


class DBAdapter(Borg):
    INSERT = """INSERT INTO {table} ({columns}) VALUES ({values}) returning *;"""
    SELECT = """select * from {table}"""
    UPDATE = """update {table} set {values} {where} returning *"""
    DELETE = """delete from {table} {where}"""
    WHERE = """ where {key} = '{value}'"""

    def __init__(self, database: str = '', user: str = '', password: str = '', host: str = 'localhost',
                 port: int = 5432, min_size=10, max_size=50, max_queries=50000, setup=None, loop=None, **kwargs):

        super(DBAdapter, self).__init__()

        self._params = dict()
        self._params['database'] = database
        self._params['user'] = user
        self._params['password'] = password
        self._params['host'] = host
        self._params['port'] = port
        self._params['min_size'] = min_size
        self._params['max_size'] = max_size
        self._params['max_queries'] = max_queries
        self._params['setup'] = setup
        self._params['loop'] = loop
        self._params.update(kwargs)

        self.pool = None

        if PY_36:
            self._compat()

    async def get_pool(self) -> Pool:
        if not self.pool:
            self.pool = await create_pool(**self._params)
        return self.pool

    async def insert(self, con: Connection = None, table: str = '', value_dict: dict = None):

        columns = ",".join(value_dict.keys())
        placeholder = ",".join(['${}'.format(i) for i in range(1, len(value_dict) + 1)])

        query = self.INSERT.format(table=table, columns=columns, values=placeholder)

        if not con:
            pool = await self.get_pool()
            async with pool.acquire() as con:
                async with con.transaction():
                    result = await con.fetchrow(query, *value_dict.values())
        else:
            async with con.transaction():
                result = await con.fetchrow(query, *value_dict.values())

        return result

    async def update(self, con: Connection = None, table: str = '', where_dict: dict = None,
                     **update_params: dict) -> list:

        values = ','.join(["{}='{}'".format(k, v) for k, v in update_params.items()])
        where = ' and'.join([self.WHERE.format(key=k, value=v) for k, v in where_dict.items()])
        query = self.UPDATE.format(table=table, values=values, where=where)

        if not con:
            pool = await self.get_pool()
            async with pool.acquire() as con:
                async with con.transaction():
                    results = await con.fetch(query)
        else:
            async with con.transaction():
                results = await con.fetch(query)

        return results

    async def delete(self, con: Connection = None, table: str = '', where_dict: dict = None):
        where = ' and'.join([self.WHERE.format(key=k, value=v) for k, v in where_dict.items()])
        query = self.DELETE.format(table=table, where=where)

        if not con:
            pool = await self.get_pool()
            async with pool.acquire() as con:
                async with con.transaction():
                    await con.execute(query)
        else:
            async with con.transaction():
                await con.execute(query)

    async def execute(self, con: Connection = None, query: str = ''):
        if not con:
            pool = await self.get_pool()
            async with pool.acquire() as con:
                async with con.transaction():
                    await con.execute(query)
        else:
            async with con.transaction():
                await con.execute(query)

    async def select(self, table: str, offset=0, limit=100, order_by='created desc') -> list:
        query = self.SELECT.format(table=table)
        query += ' order by $1 offset $2 limit $3'

        pool = await self.get_pool()
        async with pool.acquire() as con:
            stmt = await con.prepare(query)
            results = await stmt.fetch(order_by, offset, limit)

        return results

    async def where(self, table: str, offset=0, limit=100, order_by='created desc', **where_dict: dict) -> list:
        param_count = len(where_dict)

        query = self.SELECT.format(table=table)
        query += ' where '
        query += ' and'.join(['{} = ${}'.format(column, i) for i, column in enumerate(where_dict.keys(), start=1)])
        query += ' order by ${} offset ${} limit ${}'.format(param_count + 1, param_count + 2, param_count + 3)

        pool = await self.get_pool()
        async with pool.acquire() as con:
            stmt = await con.prepare(query)
            params = list(where_dict.values()) + [order_by, offset, limit]
            results = await stmt.fetch(*params)

        return results

    def _compat(self):
        ld = {}
        s = '''async def iterate(self, query: str):
            pool = await self.get_pool()
            async with pool.acquire() as con:
                async with con.transaction():
                    async for record in con.cursor(query):
                        yield record'''

        exec(s, None, ld)
        for name, value in ld.items():
            setattr(DBAdapter, name, value)
