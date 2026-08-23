from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from calculator import Calculator, CalculationError
from solver import MathSolver, SolverError


class DXDCalculatorUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(12),
            **kwargs,
        )

        self.calculator = Calculator()
        self.solver = MathSolver()

        self._build_header()
        self._build_display()
        self._build_buttons()

    def _build_header(self):
        header = Label(
            text="D X D Calculations",
            font_size=dp(24),
            bold=True,
            size_hint_y=None,
            height=dp(45),
        )
        self.add_widget(header)

    def _build_display(self):
        self.input_box = TextInput(
            hint_text="Enter a mathematical expression...",
            multiline=False,
            font_size=dp(24),
            size_hint_y=None,
            height=dp(60),
            write_tab=False,
        )

        self.input_box.bind(
            on_text_validate=lambda *_: self.calculate()
        )

        self.add_widget(self.input_box)

        self.result = Label(
            text="Ready",
            font_size=dp(20),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(70),
        )

        self.result.bind(
            size=lambda instance, value: setattr(
                instance, "text_size", value
            )
        )

        self.add_widget(self.result)

    def _build_buttons(self):
        scroll = ScrollView()

        grid = GridLayout(
            cols=4,
            spacing=dp(6),
            size_hint_y=None,
        )

        grid.bind(minimum_height=grid.setter("height"))

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "(", ")",
            "pi", "e", "^", "%",
            "sqrt(", "sin(", "cos(", "tan(",
            "log(", "ln(", "abs(", "=", 
            "C", "⌫", "x²", "1/x",
        ]

        for text in buttons:
            button = Button(
                text=text,
                font_size=dp(18),
                size_hint_y=None,
                height=dp(55),
            )

            button.bind(
                on_press=self.button_pressed
            )

            grid.add_widget(button)

        scroll.add_widget(grid)
        self.add_widget(scroll)

    def button_pressed(self, button):
        value = button.text

        if value == "=":
            self.calculate()

        elif value == "C":
            self.input_box.text = ""
            self.result.text = "Ready"

        elif value == "⌫":
            self.input_box.text = self.input_box.text[:-1]

        elif value == "x²":
            self.input_box.text += "^2"

        elif value == "1/x":
            self.input_box.text = (
                f"1/({self.input_box.text})"
            )

        else:
            self.input_box.insert_text(value)

    def calculate(self):
        expression = self.input_box.text.strip()

        if not expression:
            self.result.text = "Enter an expression."
            return

        try:
            answer = self.calculator.calculate(
                expression
            )

            self.result.text = f"= {answer}"

        except CalculationError as error:
            self.result.text = f"Error: {error}"

        except Exception:
            self.result.text = "Invalid mathematical expression."


class DXDCalculationsApp(App):
    def build(self):
        self.title = "D X D Calculations"

        # Keep the application portrait-oriented.
        Window.softinput_mode = "below_target"

        return DXDCalculatorUI()


if __name__ == "__main__":
    DXDCalculationsApp().run()
