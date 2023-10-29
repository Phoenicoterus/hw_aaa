import unittest


def fit_transform(*args: str) -> list[tuple[str, list[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows


class TestOneHot(unittest.TestCase):
    def test_hello_world(self):
        actual = fit_transform('Hello world!')
        expected = [('Hello world!', [1])]
        self.assertEqual(actual, expected)

    def test_apple(self):
        actual = fit_transform('apple')
        expected = [('apple', [1])]
        self.assertEqual(actual, expected)

    def test_banana(self):
        actual = fit_transform('banana')
        expected = [('banana', [1])]
        self.assertEqual(actual, expected)

    def test_sandwich(self):
        actual = fit_transform('sandwich')
        self.assertIsNotNone(actual)

    def test_empty(self):
        with self.assertRaises(TypeError):
            fit_transform()


if __name__ == '__main__':
    unittest.main()
