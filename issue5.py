import json
import urllib.request
import unittest
from unittest.mock import Mock, MagicMock

API_URL = 'http://worldclockapi.com/api/json/utc/now'
YMD_SEP = '-'
DMY_SEP = '.'
YMD_SEP_INDEX = 4
DMY_SEP_INDEX = 2
YMD_YEAR_SLICE = slice(0, 4)
DMY_YEAR_SLICE = slice(6, 10)


def what_is_year_now() -> int:
    """
    Получает текущее время из API-worldclock и извлекает из поля 'currentDateTime' год

    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2019-03-01
      * DD.MM.YYYY - 01.03.2019
    """
    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)

    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)


class TestWhatIsYearNow(unittest.TestCase):
    def test_ymd(self):
        mock_url = MagicMock()
        mock_url.__enter__.return_value.read.return_value = '{"currentDateTime": "2022-01-01"}'
        mock = MagicMock(return_value=mock_url)
        with unittest.mock.patch('urllib.request.urlopen', mock):
            result = what_is_year_now()
        self.assertEqual(result, 2022)

    def test_dmy(self):
        mock_url = MagicMock()
        mock_url.__enter__.return_value.read.return_value = '{"currentDateTime": "01.01.2021"}'
        mock = MagicMock(return_value=mock_url)
        with unittest.mock.patch('urllib.request.urlopen', mock):
            result = what_is_year_now()
        self.assertEqual(result, 2021)

    def test_invalid_format(self):
        mock_url = MagicMock()
        mock_url.__enter__.return_value.read.return_value = '{"currentDateTime": "Hello world"}'
        mock = MagicMock(return_value=mock_url)
        with unittest.mock.patch('urllib.request.urlopen', mock):
            with self.assertRaises(ValueError):
                what_is_year_now()


if __name__ == '__main__':
    unittest.main()
