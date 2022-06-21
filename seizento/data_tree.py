from __future__ import annotations

from dataclasses import dataclass

from typing import Dict

from seizento.path import Path, PathComponent


@dataclass(frozen=True)
class DataTree:
    values: Dict[Path, Dict]

    def delete_subtree(self, path: Path) -> DataTree:
        return DataTree(
            values={
                tree_path: v for tree_path, v in self.values.items()
                if tree_path.extends(path)
            }
        )

    def set_subtree(self, path: Path, subtree: DataTree) -> DataTree:
        result = self.delete_subtree(path=path)
        return DataTree(
            values={
                **result.values,
                **{
                    path + tree_path: value
                    for tree_path, value in subtree.values.items()
                }
            }
        )

    @property
    def root_data(self):
        root_values = [value for path, value in self.values.items() if path.empty]
        if len(root_values) != 1:
            raise Exception

        return root_values[0]

    @property
    def subtrees(self) -> Dict[PathComponent, DataTree]:
        result = {}
        for path, value in self.values.items():
            if path.empty:
                continue

            component = path.first_component

            if component not in result:
                result[component] = DataTree(values={})

            result[component] = result[component].add(path=path.remove_first(), value=value)

        return result

    def get_subtree(self, path: Path) -> DataTree:
        result = self
        for component in path:
            result = result.subtrees[component]

        return result
