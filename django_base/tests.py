from django.test import SimpleTestCase

from .utils import (
    pascal_case_to_snake_case, default_related_names,
)


class TestPascalToSnake(SimpleTestCase):
    def test_a(self):
        test_str = 'SimpleTest'
        expected = 'simple_test'
        self.assertEqual(
            pascal_case_to_snake_case(test_str),
            expected,
        )
