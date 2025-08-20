#!/usr/bin/env python3
"""
Smart Calculator
A modern calculator application with advanced features and memory functions.

Features:
- Basic and scientific operations
- Memory functions (M+, M-, MR, MC)
- Calculation history
- Keyboard shortcuts
- Expression evaluation with error handling

Author: Aditya Pagare
Email: adityapaagare619@gmail.com
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import ast
import operator
import json
from pathlib import Path
from datetime import datetime


class CalculatorEngine:
    """Handles calculation logic and expression evaluation."""

    # Safe operations mapping
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.BitXor: operator.xor,
        ast.USub: operator.neg,
    }

    # Mathematical functions
    FUNCTIONS = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log10,
        'ln': math.log,
        'sqrt': math.sqrt,
        'abs': abs,
        'ceil': math.ceil,
        'floor': math.floor,
        'round': round,
    }

    def __init__(self):
        self.memory = 0.0
        self.history = []
        self.load_history()

    def evaluate_expression(self, expression):
        """Safely evaluate mathematical expression."""
        try:
            # Replace mathematical constants and functions
            expression = expression.replace('π', str(math.pi))
            expression = expression.replace('e', str(math.e))
            expression = expression.replace('√', 'sqrt')
            expression = expression.replace('²', '**2')
            expression = expression.replace('³', '**3')

            # Parse and evaluate
            tree = ast.parse(expression, mode='eval')
            result = self._eval_node(tree.body)

            # Store in history
            self.add_to_history(expression, result)
            return result

        except (ValueError, ZeroDivisionError, TypeError, SyntaxError) as e:
            raise ValueError(f"Invalid expression: {str(e)}")

    def _eval_node(self, node):
        """Recursively evaluate AST nodes."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):  # For Python < 3.8
            return node.n
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op = self.OPERATORS.get(type(node.op))
            if op:
                return op(left, right)
            else:
                raise ValueError(f"Unsupported operation: {type(node.op)}")
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op = self.OPERATORS.get(type(node.op))
            if op:
                return op(operand)
            else:
                raise ValueError(f"Unsupported unary operation: {type(node.op)}")
        elif isinstance(node, ast.Call):
            func_name = node.func.id
            if func_name in self.FUNCTIONS:
                args = [self._eval_node(arg) for arg in node.args]
                return self.FUNCTIONS[func_name](*args)
            else:
                raise ValueError(f"Unknown function: {func_name}")
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")

    def add_to_memory(self, value):
        """Add value to memory."""
        self.memory += value

    def subtract_from_memory(self, value):
        """Subtract value from memory."""
        self.memory -= value

    def recall_memory(self):
        """Recall value from memory."""
        return self.memory

    def clear_memory(self):
        """Clear memory."""
        self.memory = 0.0

    def add_to_history(self, expression, result):
        """Add calculation to history."""
        self.history.append({
            'expression': expression,
            'result': result,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        # Keep only last 50 entries
        if len(self.history) > 50:
            self.history = self.history[-50:]

        self.save_history()

    def save_history(self):
        """Save history to file."""
        try:
            history_file = Path("data/history.json")
            history_file.parent.mkdir(exist_ok=True)
            with open(history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception:
            pass  # Fail silently for history save

    def load_history(self):
        """Load history from file."""
        try:
            history_file = Path("data/history.json")
            if history_file.exists():
                with open(history_file, 'r') as f:
                    self.history = json.load(f)
        except Exception:
            self.history = []


class CalculatorApp:
    """Main calculator application with GUI."""

    def __init__(self, root):
        self.root = root
        self.root.title("Smart Calculator")
        self.root.geometry("400x600")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)

        # Initialize calculator engine
        self.calc = CalculatorEngine()

        # Display variables
        self.display_var = tk.StringVar(value="0")
        self.expression = ""
        self.last_operation = None
        self.should_reset = False

        # Create GUI
        self.setup_styles()
        self.create_widgets()
        self.bind_keyboard()

        # Focus on window for keyboard input
        self.root.focus_set()

    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')

        # Button styles
        style.configure('Number.TButton', font=('Arial', 14), padding=10)
        style.configure('Operator.TButton', font=('Arial', 14, 'bold'), padding=10)
        style.configure('Function.TButton', font=('Arial', 10), padding=5)
        style.configure('Memory.TButton', font=('Arial', 10, 'bold'), padding=5)

    def create_widgets(self):
        """Create and arrange GUI widgets."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Display
        self.create_display(main_frame)

        # Memory and function buttons
        self.create_memory_functions(main_frame)

        # Main keypad
        self.create_keypad(main_frame)

        # History panel
        self.create_history_panel(main_frame)

    def create_display(self, parent):
        """Create calculator display."""
        display_frame = ttk.Frame(parent)
        display_frame.grid(row=0, column=0, columnspan=6, sticky=(tk.W, tk.E), pady=(0, 10))

        # Main display
        display_label = ttk.Label(
            display_frame,
            textvariable=self.display_var,
            font=('Arial', 20, 'bold'),
            background='white',
            foreground='black',
            relief='sunken',
            padding=10,
            anchor='e'
        )
        display_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Expression display
        self.expr_var = tk.StringVar()
        expr_label = ttk.Label(
            display_frame,
            textvariable=self.expr_var,
            font=('Arial', 10),
            foreground='gray',
            anchor='e'
        )
        expr_label.grid(row=1, column=0, sticky=(tk.W, tk.E))

        display_frame.columnconfigure(0, weight=1)

    def create_memory_functions(self, parent):
        """Create memory and function buttons."""
        mem_frame = ttk.Frame(parent)
        mem_frame.grid(row=1, column=0, columnspan=6, sticky=(tk.W, tk.E), pady=(0, 5))

        # Memory buttons
        memory_buttons = [
            ("MC", self.memory_clear),
            ("MR", self.memory_recall),
            ("M+", self.memory_add),
            ("M-", self.memory_subtract),
            ("MS", self.memory_store)
        ]

        for i, (text, command) in enumerate(memory_buttons):
            btn = ttk.Button(mem_frame, text=text, command=command,
                             style='Memory.TButton', width=5)
            btn.grid(row=0, column=i, padx=1)

        # Function buttons
        func_frame = ttk.Frame(parent)
        func_frame.grid(row=2, column=0, columnspan=6, sticky=(tk.W, tk.E), pady=(0, 5))

        function_buttons = [
            ("sin", lambda: self.append_function("sin")),
            ("cos", lambda: self.append_function("cos")),
            ("tan", lambda: self.append_function("tan")),
            ("log", lambda: self.append_function("log")),
            ("ln", lambda: self.append_function("ln")),
            ("√", lambda: self.append_function("sqrt"))
        ]

        for i, (text, command) in enumerate(function_buttons):
            btn = ttk.Button(func_frame, text=text, command=command,
                             style='Function.TButton', width=5)
            btn.grid(row=0, column=i, padx=1)

    def create_keypad(self, parent):
        """Create main calculator keypad."""
        keypad_frame = ttk.Frame(parent)
        keypad_frame.grid(row=3, column=0, columnspan=6, pady=5)

        # Button layout
        buttons = [
            ['C', 'CE', '⌫', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]

        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                    cmd = lambda t=text: self.append_number(t)
                    style = 'Number.TButton'
                elif text in ['+', '−', '×', '÷', '=']:
                    cmd = lambda t=text: self.handle_operator(t)
                    style = 'Operator.TButton'
                elif text == 'C':
                    cmd = self.clear_all
                    style = 'Operator.TButton'
                elif text == 'CE':
                    cmd = self.clear_entry
                    style = 'Operator.TButton'
                elif text == '⌫':
                    cmd = self.backspace
                    style = 'Operator.TButton'
                elif text == '±':
                    cmd = self.toggle_sign
                    style = 'Operator.TButton'

                width = 12 if text == '0' else 6
                btn = ttk.Button(keypad_frame, text=text, command=cmd,
                                 style=style, width=width)

                colspan = 2 if text == '0' else 1
                btn.grid(row=i, column=j, columnspan=colspan, padx=1, pady=1, sticky='ew')

    def create_history_panel(self, parent):
        """Create calculation history panel."""
        history_frame = ttk.LabelFrame(parent, text="History", padding=5)
        history_frame.grid(row=4, column=0, columnspan=6, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        # History listbox
        self.history_listbox = tk.Listbox(history_frame, height=6, font=('Courier', 9))
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=scrollbar.set)

        self.history_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Bind double-click to use result
        self.history_listbox.bind('<Double-Button-1>', self.use_history_result)

        # Clear history button
        clear_btn = ttk.Button(history_frame, text="Clear History", command=self.clear_history)
        clear_btn.grid(row=1, column=0, pady=(5, 0))

        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)

        # Load initial history
        self.update_history_display()

    def bind_keyboard(self):
        """Bind keyboard shortcuts."""
        self.root.bind('<Key>', self.handle_keypress)
        self.root.bind('<Return>', lambda e: self.handle_operator('='))
        self.root.bind('<KP_Enter>', lambda e: self.handle_operator('='))
        self.root.bind('<Escape>', lambda e: self.clear_all())
        self.root.bind('<BackSpace>', lambda e: self.backspace())

    def handle_keypress(self, event):
        """Handle keyboard input."""
        key = event.char

        if key.isdigit() or key == '.':
            self.append_number(key)
        elif key in ['+', '-', '*', '/', '=']:
            op_map = {'+': '+', '-': '−', '*': '×', '/': '÷', '=': '='}
            self.handle_operator(op_map.get(key, key))
        elif key.lower() == 'c':
            self.clear_all()

    def append_number(self, number):
        """Append number to display."""
        current = self.display_var.get()

        if self.should_reset or current == "0":
            if number == ".":
                self.display_var.set("0.")
            else:
                self.display_var.set(number)
            self.should_reset = False
        else:
            if number == "." and "." in current:
                return  # Don't allow multiple decimal points
            self.display_var.set(current + number)

        self.update_expression_display()

    def append_function(self, func_name):
        """Append function to expression."""
        self.expression += f"{func_name}("
        self.display_var.set(f"{func_name}(")
        self.update_expression_display()

    def handle_operator(self, operator):
        """Handle operator button press."""
        current = self.display_var.get()

        if operator == '=':
            try:
                # Build complete expression
                if self.expression and not self.expression.endswith(current):
                    full_expr = self.expression + current
                else:
                    full_expr = current

                # Convert display operators to math operators
                full_expr = full_expr.replace('×', '*').replace('÷', '/').replace('−', '-')

                result = self.calc.evaluate_expression(full_expr)
                self.display_var.set(str(result))
                self.expression = ""
                self.should_reset = True
                self.update_history_display()

            except ValueError as e:
                messagebox.showerror("Error", str(e))
                self.clear_all()
        else:
            # Convert operator for expression
            op_map = {'×': '*', '÷': '/', '−': '-', '+': '+'}
            math_op = op_map.get(operator, operator)

            if self.should_reset:
                self.expression = current + math_op
                self.should_reset = False
            else:
                self.expression += current + math_op

            self.display_var.set("0")

        self.update_expression_display()

    def clear_all(self):
        """Clear all input and expression."""
        self.display_var.set("0")
        self.expression = ""
        self.should_reset = False
        self.update_expression_display()

    def clear_entry(self):
        """Clear current entry."""
        self.display_var.set("0")

    def backspace(self):
        """Remove last character."""
        current = self.display_var.get()
        if len(current) > 1:
            self.display_var.set(current[:-1])
        else:
            self.display_var.set("0")

    def toggle_sign(self):
        """Toggle positive/negative sign."""
        current = self.display_var.get()
        if current != "0":
            if current.startswith("-"):
                self.display_var.set(current[1:])
            else:
                self.display_var.set("-" + current)

    def memory_clear(self):
        """Clear memory."""
        self.calc.clear_memory()
        messagebox.showinfo("Memory", "Memory cleared")

    def memory_recall(self):
        """Recall value from memory."""
        value = self.calc.recall_memory()
        self.display_var.set(str(value))
        self.should_reset = True

    def memory_add(self):
        """Add current value to memory."""
        try:
            current = float(self.display_var.get())
            self.calc.add_to_memory(current)
            messagebox.showinfo("Memory", f"Added {current} to memory")
        except ValueError:
            messagebox.showerror("Error", "Invalid number")

    def memory_subtract(self):
        """Subtract current value from memory."""
        try:
            current = float(self.display_var.get())
            self.calc.subtract_from_memory(current)
            messagebox.showinfo("Memory", f"Subtracted {current} from memory")
        except ValueError:
            messagebox.showerror("Error", "Invalid number")

    def memory_store(self):
        """Store current value in memory."""
        try:
            current = float(self.display_var.get())
            self.calc.memory = current
            messagebox.showinfo("Memory", f"Stored {current} in memory")
        except ValueError:
            messagebox.showerror("Error", "Invalid number")

    def update_expression_display(self):
        """Update expression display."""
        if self.expression:
            # Convert math operators back to display operators
            display_expr = self.expression.replace('*', '×').replace('/', '÷').replace('-', '−')
            self.expr_var.set(display_expr)
        else:
            self.expr_var.set("")

    def update_history_display(self):
        """Update history listbox."""
        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.calc.history[-10:]):  # Show last 10
            expr = entry['expression']
            result = entry['result']
            self.history_listbox.insert(0, f"{expr} = {result}")

    def use_history_result(self, event):
        """Use result from history."""
        selection = self.history_listbox.curselection()
        if selection:
            item = self.history_listbox.get(selection[0])
            result = item.split(" = ")[-1]
            self.display_var.set(result)
            self.should_reset = True

    def clear_history(self):
        """Clear calculation history."""
        if messagebox.askyesno("Clear History", "Clear all calculation history?"):
            self.calc.history = []
            self.calc.save_history()
            self.update_history_display()


def main():
    """Main function to run the calculator."""
    root = tk.Tk()
    app = CalculatorApp(root)

    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()