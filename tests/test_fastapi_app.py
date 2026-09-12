import unittest

from pydantic import ValidationError

from examples.web.fastapi_app import ItemIn, create_item, health


class FastApiAppTests(unittest.TestCase):
    def test_health(self):
        self.assertEqual(health(), {"status": "ok"})

    def test_create_item(self):
        item = create_item(ItemIn(name="Book", price=10))
        self.assertEqual(item.name, "Book")
        self.assertEqual(item.id, 1)

    def test_rejects_invalid_item(self):
        with self.assertRaises(ValidationError):
            ItemIn(name="", price=0)


if __name__ == "__main__":
    unittest.main()
