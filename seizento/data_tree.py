from __future__ import annotations

from dataclasses import dataclass, field

from typing import Dict, Any

from seizento.path import Path, PathComponent, PlaceHolder, EMPTY_PATH


class InvalidDataTree(Exception):
    pass


@dataclass(frozen=True)
class DataTree:
    root_data: Any
    subtrees: Dict[PathComponent, DataTree] = field(default_factory=dict)

    def delete_subtree(self, path: Path) -> DataTree:
        if path == EMPTY_PATH:
            raise ValueError

        subtrees = {
            component: subtree for component, subtree in self.subtrees.items()
            if component != path.first_component
        }

        if len(path) > 1 and path.first_component in self.subtrees:
            subtrees[path.first_component] = self.subtrees[path.first_component].delete_subtree(path=path.remove_first())

        return DataTree(root_data=self.root_data, subtrees=subtrees)

    def set_subtree(self, path: Path, subtree: DataTree) -> DataTree:
        if path == EMPTY_PATH:
            raise ValueError

        if len(path) == 1:
            return DataTree(
                root_data=self.root_data,
                subtrees={
                    **self.subtrees,
                    path.first_component: subtree
                }
            )

        return DataTree(
            root_data=self.root_data,
            subtrees={
                **self.subtrees,
                path.first_component: self.subtrees[path.first_component].set_subtree(path=path.remove_first(), subtree=subtree)
            }
        )

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
