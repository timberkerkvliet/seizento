from __future__ import annotations

from dataclasses import dataclass

from typing import Dict, Any

from seizento.path import Path, PathComponent, PlaceHolder


class InvalidDataTree(Exception):
    pass


@dataclass(frozen=True)
class DataTree:
    values: Dict[Path, Any]

    def __post_init__(self):
        for path in self.values.keys():
            if path.empty:
                continue

            if not path.remove_last() in self.values.keys():
                raise InvalidDataTree

    def delete_subtree(self, path: Path) -> DataTree:
        return DataTree(
            values={
                tree_path: v for tree_path, v in self.values.items()
                if not tree_path >= path
            }
        )

    def set_subtree(self, path: Path, subtree: DataTree) -> DataTree:
        return DataTree(
            values={
                **{
                    tree_path: v for tree_path, v in self.values.items()
                    if not tree_path >= path
                },
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
    def values_per_component(self) -> Dict[PathComponent, Dict[Path, Dict]]:
        categorized: Dict[PathComponent, Dict[Path, Dict]] = {}
        for path, value in self.values.items():
            if path.empty:
                continue

            component = path.first_component

            if component not in categorized:
                categorized[component] = {}

            categorized[component][path] = value

        return categorized

    @property
    def subtrees(self) -> Dict[PathComponent, DataTree]:
        return {
            component: DataTree(
                values={
                    path.remove_first(): data
                    for path, data in values.items()
                }
            )
            for component, values in self.values_per_component.items()
        }

    def get_subtree(self, path: Path) -> DataTree:
        result = self
        for component in path:
            subtrees = result.subtrees
            if component in subtrees:
                result = subtrees[component]
            elif PlaceHolder() in subtrees:
                result = subtrees[PlaceHolder()]
            else:
                raise KeyError

        return result
