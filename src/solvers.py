"""Module containing the code for the problem solvers."""

from typing import List

class BacktrackingSolver:
    """Problem solver with backtracking capabilities."""

    def getSolutionIter(self, domains: dict, constraints: List[tuple], vconstraints: dict):  # noqa: D102
        assignments = {}

        queue = []

        while True:
            # Mix the Degree and Minimum Remaing Values (MRV) heuristics
            lst = [(-len(vconstraints[variable]), len(domains[variable]), variable) for variable in domains]
            lst.sort()
            for item in lst:
                if item[-1] not in assignments:
                    # Found unassigned variable
                    variable = item[-1]
                    values = domains[variable][:]
                    pushdomains = [domains[x] for x in domains if x not in assignments and x != variable]
                    break
            else:
                # No unassigned variables. We've got a solution. Go back
                # to last variable, if there's one.
                yield assignments.copy()
                if not queue:
                    return
                variable, values, pushdomains = queue.pop()
                if pushdomains:
                    for domain in pushdomains:
                        domain.popState()

            while True:
                # We have a variable. Do we have any values left?
                if not values:
                    # No. Go back to last variable, if there's one.
                    del assignments[variable]
                    while queue:
                        variable, values, pushdomains = queue.pop()
                        if pushdomains:
                            for domain in pushdomains:
                                domain.popState()
                        if values:
                            break
                        del assignments[variable]
                    else:
                        return

                # Got a value. Check it.
                assignments[variable] = values.pop()

                if pushdomains:
                    for domain in pushdomains:
                        domain.pushState()

                for constraint, variables in vconstraints[variable]:
                    if not constraint(variables, domains, assignments, pushdomains):
                        # Value is not good.
                        break
                else:
                    break

                if pushdomains:
                    for domain in pushdomains:
                        domain.popState()

            # Push state before looking for next variable.
            queue.append((variable, values, pushdomains))

    def getSolution(self, domains: dict, constraints: List[tuple], vconstraints: dict):  # noqa: D102
        iter = self.getSolutionIter(domains, constraints, vconstraints)
        try:
            return next(iter)
        except StopIteration:
            return None

    def getSolutions(self, domains: dict, constraints: List[tuple], vconstraints: dict):  # noqa: D102
        return list(self.getSolutionIter(domains, constraints, vconstraints))
