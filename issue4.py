import pytest


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


def test_hello_world():
    assert fit_transform('Hello world!') == [('Hello world!', [1])]


def test_single_input():
    assert fit_transform('apple') == [('apple', [1])]


def test_multiple_inputs():
    assert fit_transform('apple', 'banana', 'cucumber', 'apple', 'strawberry') == [
        ('apple', [0, 0, 0, 1]), ('banana', [0, 0, 1, 0]), ('cucumber', [0, 1, 0, 0]), ('apple', [0, 0, 0, 1]),
        ('strawberry', [1, 0, 0, 0])]


def test_str_number():
    assert fit_transform('0') == [('0', [1])]


def test_empty_input():
    with pytest.raises(TypeError):
        fit_transform()


if __name__ == '__main__':
    pytest.main()
