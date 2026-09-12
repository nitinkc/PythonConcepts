import asyncio
import unittest

from examples.concurrency.execution_models import run_async, run_threaded
from examples.fundamentals.collections import merge_profiles, unique_in_order
from examples.functions.imports_and_main import describe_execution
from examples.gui.widgets import Order, create_order_form, format_order
from examples.object_oriented.calculator import Calculator
from examples.reliability.capitalization import capitalize_words


class ExampleTests(unittest.TestCase):
    def test_collections(self):
        self.assertEqual(merge_profiles({"a": 1}, {"a": 2}), {"a": 2})
        self.assertEqual(unique_in_order([1, 2, 1]), [1, 2])

    def test_import_description(self):
        self.assertIn("entry point", describe_execution("__main__"))
        self.assertIn("imported", describe_execution("examples.module"))

    def test_calculator(self):
        calculator = Calculator()
        self.assertEqual(calculator.add(1, 2, 3), 6)
        self.assertEqual(calculator.subtract(5, 2), 3)
        self.assertEqual(calculator.multiply(3, 4), 12)
        with self.assertRaises(TypeError):
            calculator.add(1, "2")

    def test_capitalization(self):
        self.assertEqual(capitalize_words("python concepts"), "Python Concepts")
        self.assertIsNone(capitalize_words(None))
        with self.assertRaises(TypeError):
            capitalize_words(42)

    def test_gui_widgets(self):
        order = Order(quantity=2, category="books", notes="Gift wrap")
        self.assertEqual(format_order(order), "Submitted 2 books item(s). Notes: Gift wrap")
        self.assertEqual(type(create_order_form()).__name__, "VBox")

    def test_concurrent_io_examples(self):
        self.assertEqual(run_threaded([1, 2, 3]), [1, 2, 3])
        self.assertEqual(asyncio.run(run_async([1, 2, 3])), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
