import json

import aiosqlite
from aiosqlite import Connection

from seizento.path import Path
from seizento.data_tree import DataTree
from seizento.repository import DataTreeStoreTransaction
from seizento.serializers.path_serializer import serialize_path, parse_path


class SQLiteDataTreeStoreTransaction(DataTreeStoreTransaction):
    def __init__(self, connection: Connection, ensured_table: bool):
        self._connection = connection
        self._ensured_table = ensured_table

    async def __aenter__(self):
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

    async def __aexit__(self, *args):
        await self._connection.commit()
        await self._connection.__aexit__(*args)

    async def get_tree(self, path: Path) -> DataTree:
        result = await self._connection.execute(
            """
            SELECT data FROM data WHERE path = ?
            """,
            serialize_path(path)
        )
        root_data_result = await result.fetchone()
        if root_data_result is None:
            raise KeyError

        root_data = json.loads(root_data_result[0])

        components_result = await self._connection.execute(
            "SELECT path FROM data WHERE path LIKE ?",
            serialize_path(path) + '/%[^/]'
        )

        subpaths = {parse_path(row[0]) for row in await components_result.fetchall()}

        return DataTree(
            root_data=root_data,
            subtrees={
                subpath.last_component: await self.get_tree(path=subpath)
                for subpath in subpaths
            }
        )

    async def set_tree(self, path: Path, tree: DataTree) -> None:
        await self.delete_tree(path)

        await self._connection.execute(
            "INSERT INTO data (path, data) VALUES (?, ?)",
            (serialize_path(path), json.dumps(tree.root_data))
        )
        for component, subtree in tree.subtrees.items():
            await self.set_tree(path=path.append(component), tree=subtree)

    async def delete_tree(self, path: Path) -> None:
        await self._connection.execute(
            "DELETE FROM data WHERE path=? OR path LIKE ?",
            (serialize_path(path), serialize_path(path) + '/%')
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

