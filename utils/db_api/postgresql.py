from typing import Union

import asyncpg
from asyncpg import Pool, Connection
from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS Users (
        user_id BIGINT PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        purchase_counter INTEGER DEFAULT 0 NOT NULL,
        reward_counter INTEGER DEFAULT 0 NOT NULL
        );
        '''
        await self.execute(sql, execute=True)

    async def add_user(self, user_id, full_name):
        sql = 'INSERT INTO Users (user_id, full_name) VALUES ($1, $2);'
        await self.execute(sql, user_id, full_name, execute=True)

    async def purchase_counter_request(self, user_id):
        sql = 'SELECT purchase_counter FROM Users WHERE user_id=$1;'
        return await self.execute(sql, user_id, fetchval=True)

    async def reward_counter_request(self, user_id):
        sql = 'SELECT reward_counter FROM Users WHERE user_id=$1;'
        return await self.execute(sql, user_id, fetchval=True)

    async def get_reward_from_db(self, user_id):
        sql = 'SELECT reward_counter FROM Users WHERE user_id=$1;'
        reward_counter = (await self.execute(sql, user_id, fetchval=True)) - 1
        sql = 'UPDATE Users SET reward_counter=$1 WHERE user_id=$2;'
        await self.execute(sql, reward_counter, user_id, execute=True)

    async def add_reward_auto(self, user_id):
        sql = 'SELECT purchase_counter FROM Users WHERE user_id=$1;'
        purchase_counter = await self.execute(sql, user_id, fetchval=True)
        if purchase_counter >= 5:
            purchase_counter -= 5
            sql = 'UPDATE Users SET purchase_counter=$1 WHERE user_id=$2;'
            await self.execute(sql, purchase_counter, user_id, execute=True)
            sql = 'SELECT reward_counter FROM Users WHERE user_id=$1;'
            reward_counter = await self.execute(sql, user_id, fetchval=True)
            reward_counter += 1
            sql='UPDATE Users SET reward_counter=$1 WHERE user_id=$2;'
            await self.execute(sql, reward_counter, user_id, execute=True)
            return True
        else:
            return False

    async def add_purchase_to_db(self, amount, user_id):
        sql = 'SELECT purchase_counter FROM Users WHERE user_id=$1;'
        purchase_counter = await self.execute(sql, user_id, fetchval=True)
        purchase_counter += amount
        sql = 'UPDATE Users SET purchase_counter=$1 WHERE user_id=$2;'
        await self.execute(sql, purchase_counter, user_id, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql = ' AND '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def select_all_users(self):
        sql = 'SELECT * FROM Users;'
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = 'SELECT * FROM Users WHERE '
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = 'SELECT COUNT(*) FROM Users'
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = 'UPDATE Users SET username=$1 WHERE telegram_id=$2'
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute('DELETE FROM Users WHERE TRUE', execute=True)

    async def drop_users(self):
        await self.execute('DROP TABLE Users', execute=True)
