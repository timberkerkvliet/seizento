from __future__ import annotations

import json

import aiosqlite
from aiosqlite import Connection

from seizento.path import Path
from seizento.data_tree import DataTree, tree_from_paths
from seizento.repository import DataTreeStoreTransaction
from seizento.serializers.path_serializer import serialize_path, parse_path


class SQLiteDataTreeStoreTransaction(DataTreeStoreTransaction):
    def __init__(self, connection: Connection, ensured_table: bool):
        self._connection = connection
        self._ensured_table = ensured_table

    async def __aenter__(self) -> SQLiteDataTreeStoreTransaction:
        await self._connection.__aenter__()
        if not self._ensured_table:
            await self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS data (
                    path TEXT,
                    data TEXT,
                    PRIMARY KEY (path)
                )
                """
            )

        return self

    async def __aexit__(self, *args):
        await self._connection.commit()
        await self._connection.__aexit__(*args)

    @staticmethod
    def child_pattern(path: Path) -> str:
        if len(path) == 0:
            return '_%'

        return serialize_path(path) + '/%'

    async def get_tree(self, path: Path) -> DataTree:
        result = await self._connection.execute(
            """
            SELECT path, data FROM data WHERE path = ? OR path LIKE ?
            """,
            (serialize_path(path), self.child_pattern(path))
        )
        all_paths = {
            parse_path(row[0]).remove_from_start(len(path)): json.loads(row[1])
            for row in await result.fetchall()
        }

        return tree_from_paths(all_paths)

    async def set_tree(self, path: Path, tree: DataTree) -> None:
        await self.delete_tree(path)

        all_paths = tree.get_all_paths()

        await self._connection.executemany(
            "INSERT INTO data (path, data) VALUES (?, ?)",
            [
                (serialize_path(path + tree_path), json.dumps(data))
                for tree_path, data in all_paths.items()
            ]
        )

    async def delete_tree(self, path: Path) -> None:
        await self._connection.execute(
            "DELETE FROM data WHERE path=? OR path LIKE ?",
            (serialize_path(path), self.child_pattern(path))
        )


class SQLiteDataTreeStore:
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._ensured_table = False

    def get_transaction(self) -> SQLiteDataTreeStoreTransaction:
        return SQLiteDataTreeStoreTransaction(
            connection=aiosqlite.connect(self._db_path),
            ensured_table=self._ensured_table
        )
