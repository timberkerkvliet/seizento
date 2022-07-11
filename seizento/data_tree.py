from __future__ import annotations

from dataclasses import dataclass, field

from typing import Dict, Any

from seizento.path import Path, PathComponent, EMPTY_PATH, IndexPlaceHolder, LiteralComponent, \
    PropertyPlaceHolder


@dataclass(frozen=True)
class DataTree:
    root_data: Any
    subtrees: Dict[PathComponent, DataTree] = field(default_factory=dict)

    def get_all_paths(self) -> Dict[Path, Any]:
        result = {EMPTY_PATH: self.root_data}

        for component, subtree in self.subtrees.items():
            result.update(
                {
                    path.insert_first(component): data
                    for path, data in subtree.get_all_paths().items()
                }
            )

        return result

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

        new_subtree = self.subtrees[path.first_component]\
            .set_subtree(path=path.remove_first(), subtree=subtree)

        return DataTree(
            root_data=self.root_data,
            subtrees={
                **self.subtrees,
                path.first_component: new_subtree
            }
        )

    def get_subtree(self, path: Path) -> DataTree:
        result = self
        for component in path:
            subtrees = result.subtrees
            if component in subtrees:
                result = subtrees[component]
            elif IndexPlaceHolder() in subtrees and isinstance(component, LiteralComponent) and component.value.isdigit():
                result = subtrees[IndexPlaceHolder()]
            elif PropertyPlaceHolder() in subtrees and isinstance(component, LiteralComponent):
                result = subtrees[PropertyPlaceHolder()]
            else:
                raise KeyError

        return result


def tree_from_paths(all_paths: Dict[Path, Any]) -> DataTree:
    children = {path.first_component for path in all_paths if len(path) == 1}

    return DataTree(
        root_data=all_paths[EMPTY_PATH],
        subtrees={
            component: tree_from_paths(
                all_paths={
                    path.remove_first(): data
                    for path, data in all_paths.items()
                    if len(path) > 0 and path.first_component == component
                }
            )
            for component in children
        }
    )
