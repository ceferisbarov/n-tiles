"""Module containing the code for problem definitions."""

import copy

from src.solvers import BacktrackingSolver
from src.domain import Domain
from src.constraints import Constraint
from typing import Optional, Union, Sequence, Callable

class Problem:
    """Class used to define a problem and retrieve solutions."""

    def __init__(self, solver=None):
        """Initialization method.

        Args:
            solver (instance of a :py:class:`Solver`): Problem solver to use (default is :py:class:`BacktrackingSolver`)
        """
        self._solver = solver or BacktrackingSolver()
        self._constraints = []
        self._variables = {}

    def addVariable(self, variable, domain):
        """Add a variable to the problem.

        Example:
            >>> problem = Problem()
            >>> problem.addVariable("a", [1, 2])
            >>> problem.getSolution() in ({'a': 1}, {'a': 2})
            True

        Args:
            variable (hashable object): Object representing a problem
                variable
            domain (list, tuple, or instance of :py:class:`Domain`): Set of items
                defining the possible values that the given variable may
                assume
        """
        if variable in self._variables:
            msg = "Tried to insert duplicated variable %s" % repr(variable)
            raise ValueError(msg)
        if isinstance(domain, Domain):
            domain = copy.deepcopy(domain)
        elif hasattr(domain, "__getitem__"):
            domain = Domain(domain)
        else:
            msg = "Domains must be instances of subclasses of the Domain class"
            raise TypeError(msg)
        if not domain:
            raise ValueError("Domain is empty")
        self._variables[variable] = domain

    def addConstraint(self, constraint: Union[Constraint, Callable], variables: Optional[Sequence] = None):
        """Add a constraint to the problem."""
        if not isinstance(constraint, Constraint):
            if callable(constraint):
                constraint = Constraint(constraint)
            else:
                msg = "Constraints must be instances of subclasses " "of the Constraint class"
                raise ValueError(msg)
        self._constraints.append((constraint, variables))
        
    def getSolution(self):
        """Find and return a solution to the problem."""
        
        domains, constraints, vconstraints = self._getArgs()
        if not domains:
            return None
        return self._solver.getSolution(domains, constraints, vconstraints)
    
    def getSolutions(self):
        """Find and return all solutions to the problem."""

        domains, constraints, vconstraints = self._getArgs()
        if not domains:
            return []
        return self._solver.getSolutions(domains, constraints, vconstraints)

    def _getArgs(self):
        domains = self._variables.copy()
        allvariables = domains.keys()
        constraints = []
        for constraint, variables in self._constraints:
            if not variables:
                variables = list(allvariables)
            constraints.append((constraint, variables))
        vconstraints = {}
        for variable in domains:
            vconstraints[variable] = []
        for constraint, variables in constraints:
            for variable in variables:
                vconstraints[variable].append((constraint, variables))
        for constraint, variables in constraints[:]:
            constraint.preProcess(variables, domains, constraints, vconstraints)
        for domain in domains.values():
            domain.resetState()
            if not domain:
                return None, None, None

        return domains, constraints, vconstraints