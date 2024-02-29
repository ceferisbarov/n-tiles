from typing import Callable, List, Sequence

class Constraint:
    def __init__(self, func: Callable, assigned: bool = True):
        self._func = func
        self._assigned = assigned

    def __call__(
        self,
        variables: Sequence,
        domains: dict,
        assignments: dict,
        forwardcheck=False,
        _unassigned="Unassigned",
    ):
        parms = list()
        missing = 0
        for x in variables:
            if x in assignments:
                parms.append(assignments[x])
            else:
                parms.append(_unassigned)
                missing += 1

        # if there are unassigned variables, do a forward check before executing the restriction function
        if missing > 0:
            return (self._assigned or self._func(*parms)) and (
                not forwardcheck or missing != 1 or self.forwardCheck(variables, domains, assignments)
            )
        return self._func(*parms)


    def preProcess(self, variables: Sequence, domains: dict, constraints: List[tuple], vconstraints: dict):
        """Preprocess variable domains."""

        if len(variables) == 1:
            variable = list(variables)[0]
            domain = domains[variable]
            for value in domain[:]:
                if not self(variables, domains, {variable: value}):
                    domain.remove(value)
            constraints.remove((self, variables))
            vconstraints[variable].remove((self, variables))

    def forwardCheck(self, variables: Sequence, domains: dict, assignments: dict, _unassigned="Unassigned"):
        """Helper method for generic forward checking."""
        unassignedvariable = _unassigned
        for variable in variables:
            if variable not in assignments:
                if unassignedvariable is _unassigned:
                    unassignedvariable = variable
                else:
                    break
        else:
            if unassignedvariable is not _unassigned:
                # Remove from the unassigned variable domain's all
                # values which break our variable's constraints.
                domain = domains[unassignedvariable]
                if domain:
                    for value in domain[:]:
                        assignments[unassignedvariable] = value
                        if not self(variables, domains, assignments):
                            domain.hideValue(value)
                    del assignments[unassignedvariable]
                if not domain:
                    return False
        return True
