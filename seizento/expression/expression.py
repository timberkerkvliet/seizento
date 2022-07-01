from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Set, Any, TYPE_CHECKING, Callable, Optional

from seizento.data_tree import DataTree
from seizento.identifier import Identifier
from seizento.path import Path, PathComponent
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.service.expression_service import PathEvaluator


@dataclass(frozen=True)
class Constraint:
    values: Dict[Identifier, str]

    def can_merge(self, other: Constraint) -> bool:
        return set(other.values.keys()).isdisjoint(self.values.keys())

    def merge(self, other: Constraint) -> Constraint:
        if not self.can_merge(other):
            raise ValueError

        return Constraint(values={**self.values, **other.values})

    def pop_parameter(self, parameter: Identifier) -> Constraint:
        return Constraint(
            values={k: v for k, v in self.values.items() if k != parameter}
        )

    def __hash__(self):
        return hash(tuple(self.values.items()))


NO_CONSTRAINT = Constraint(values={})


@dataclass(frozen=True)
class EvaluationResult:
    results: Dict[Constraint, Any]

    def get_one(self):
        if len(set(self.results.keys())) != 1:
            raise Exception

        return self.results[NO_CONSTRAINT]

    def merge(self, other: EvaluationResult, merge_function: Callable) -> EvaluationResult:
        new_results = self.results
        for other_constraint, other_value in other.results.items():
            new_results = {
                constraint.merge(other_constraint): merge_function(value, other_value)
                for constraint, value in new_results.items()
                if constraint.can_merge(other_constraint)
            }

        return EvaluationResult(results=new_results)

    def aggregate(self, parameter: Identifier, aggregate_function: Callable) -> Dict[Optional[str], EvaluationResult]:
        result: Dict[Optional[str], EvaluationResult] = {}

        for constraint, value in self.results.items():
            key = constraint.values[parameter] if parameter not in constraint.values else None
            new_result = EvaluationResult(results={constraint.pop_parameter(parameter): value})

            if key not in result:
                result[key] = new_result
            else:
                result[key] = result[key].merge(
                    other=new_result,
                    merge_function=aggregate_function
                )

        return result


class Expression(ABC):
    @abstractmethod
    def get_schema(self, schemas: Dict[Path, Schema]) -> Schema:
        pass

    @abstractmethod
    async def evaluate(
        self,
        evaluator: PathEvaluator,
        constraint: Constraint
    ) -> EvaluationResult:
        pass

    @abstractmethod
    def get_path_references(self) -> Set[Path]:
        pass

    @abstractmethod
    def supports_child_at(self, component: PathComponent) -> bool:
        pass

    @abstractmethod
    def to_tree(self) -> DataTree:
        pass
