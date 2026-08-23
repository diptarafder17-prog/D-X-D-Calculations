import ast
import math
import operator


class CalculationError(Exception):
    """Raised when an expression cannot be calculated."""


class Calculator:

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    CONSTANTS = {
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
    }

    FUNCTIONS = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "log": math.log10,
        "ln": math.log,
        "abs": abs,
        "floor": math.floor,
        "ceil": math.ceil,
        "exp": math.exp,
        "degrees": math.degrees,
        "radians": math.radians,
    }

    def calculate(self, expression):
        expression = expression.strip()

        if not expression:
            raise CalculationError(
                "Expression is empty."
            )

        expression = self._normalize(expression)

        try:
            tree = ast.parse(
                expression,
                mode="eval"
            )
        except SyntaxError:
            raise CalculationError(
                "Invalid expression."
            )

        try:
            result = self._evaluate(tree.body)
        except ZeroDivisionError:
            raise CalculationError(
                "Cannot divide by zero."
            )
        except (ValueError, OverflowError):
            raise CalculationError(
                "Mathematical domain error."
            )

        if isinstance(result, float):
            if not math.isfinite(result):
                raise CalculationError(
                    "Result is not finite."
                )

            if result.is_integer():
                return int(result)

            return round(result, 12)

        return result

    @staticmethod
    def _normalize(expression):
        return (
            expression
            .replace("×", "*")
            .replace("÷", "/")
            .replace("−", "-")
            .replace("^", "**")
        )

    def _evaluate(self, node):

        if isinstance(node, ast.Constant):
            if isinstance(
                node.value,
                (int, float)
            ):
                return node.value

            raise CalculationError(
                "Unsupported constant."
            )

        if isinstance(node, ast.BinOp):
            operation = self.OPERATORS.get(
                type(node.op)
            )

            if operation is None:
                raise CalculationError(
                    "Unsupported operator."
                )

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operation = self.OPERATORS.get(
                type(node.op)
            )

            if operation is None:
                raise CalculationError(
                    "Unsupported unary operator."
                )

            return operation(
                self._evaluate(node.operand)
            )

        if isinstance(node, ast.Name):
            if node.id in self.CONSTANTS:
                return self.CONSTANTS[node.id]

            raise CalculationError(
                f"Unknown value: {node.id}"
            )

        if isinstance(node, ast.Call):
            if not isinstance(
                node.func,
                ast.Name
            ):
                raise CalculationError(
                    "Invalid function."
                )

            function_name = node.func.id

            function = self.FUNCTIONS.get(
                function_name
            )

            if function is None:
                raise CalculationError(
                    f"Unknown function: {function_name}"
                )

            if len(node.args) > 5:
                raise CalculationError(
                    "Too many arguments."
                )

            arguments = [
                self._evaluate(argument)
                for argument in node.args
            ]

            return function(*arguments)

        raise CalculationError(
            "Unsupported mathematical expression."
        )
