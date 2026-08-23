import sympy as sp


class SolverError(Exception):
    """Raised when symbolic mathematics fails."""


class MathSolver:

    def __init__(self):
        self.allowed_locals = {
            "x": sp.Symbol("x"),
            "y": sp.Symbol("y"),
            "z": sp.Symbol("z"),
            "pi": sp.pi,
            "e": sp.E,
        }

    def parse(self, expression):
        try:
            return sp.sympify(
                expression,
                locals=self.allowed_locals
            )
        except Exception as error:
            raise SolverError(
                f"Invalid expression: {error}"
            )

    def simplify(self, expression):
        return sp.simplify(
            self.parse(expression)
        )

    def expand(self, expression):
        return sp.expand(
            self.parse(expression)
        )

    def factor(self, expression):
        return sp.factor(
            self.parse(expression)
        )

    def solve_equation(
        self,
        equation,
        variable="x"
    ):
        if "=" not in equation:
            raise SolverError(
                "Equation must contain '='."
            )

        left, right = equation.split(
            "=",
            1
        )

        symbol = sp.Symbol(variable)

        try:
            equation_object = sp.Eq(
                self.parse(left),
                self.parse(right)
            )

            return sp.solve(
                equation_object,
                symbol
            )

        except Exception as error:
            raise SolverError(
                f"Unable to solve equation: {error}"
            )

    def derivative(
        self,
        expression,
        variable="x"
    ):
        symbol = sp.Symbol(variable)

        return sp.diff(
            self.parse(expression),
            symbol
        )

    def integral(
        self,
        expression,
        variable="x"
    ):
        symbol = sp.Symbol(variable)

        return sp.integrate(
            self.parse(expression),
            symbol
        )

    def limit(
        self,
        expression,
        variable="x",
        point=0
    ):
        symbol = sp.Symbol(variable)

        return sp.limit(
            self.parse(expression),
            symbol,
            point
        )

    def matrix(self, values):
        try:
            return sp.Matrix(values)
        except Exception as error:
            raise SolverError(
                f"Invalid matrix: {error}"
  )
