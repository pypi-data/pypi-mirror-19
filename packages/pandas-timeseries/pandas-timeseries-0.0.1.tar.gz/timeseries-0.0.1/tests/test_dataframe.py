from collections import namedtuple
from datetime import timedelta
import json

import arrow
import pandas as pd

from timeseries import TimeSeries

RangeRow = namedtuple('RangeRow', 'valid_from, valid_to, value')
MultipleRangeRow = namedtuple('MultipleRangeRow',
                              'valid_from, valid_to, value1, value2')
PointRow = namedtuple('PointRow', 'datetime, value')

# Complete data
data_A0 = [
    RangeRow('2016-12-01T00:00:00Z', '2016-12-01T04:00:00Z', 10),
    RangeRow('2016-12-01T04:00:00Z', '2016-12-01T08:00:00Z', 30),
    RangeRow('2016-12-01T08:00:00Z', '2016-12-01T12:00:00Z', 60),
    RangeRow('2016-12-01T12:00:00Z', '2016-12-01T16:00:00Z', 60),
    RangeRow('2016-12-01T16:00:00Z', '2016-12-01T20:00:00Z', 40),
    RangeRow('2016-12-01T20:00:00Z', '2016-12-02T00:00:00Z', 50),
]

# Non-numeric content
data_A1 = [
    RangeRow('2016-12-01T00:00:00Z', '2016-12-01T04:00:00Z', 'A'),
    RangeRow('2016-12-01T04:00:00Z', '2016-12-01T08:00:00Z', 'F'),
    RangeRow('2016-12-01T08:00:00Z', '2016-12-01T12:00:00Z', 'C'),
    RangeRow('2016-12-01T12:00:00Z', '2016-12-01T16:00:00Z', 'B'),
    RangeRow('2016-12-01T16:00:00Z', '2016-12-01T20:00:00Z', 'D'),
    RangeRow('2016-12-01T20:00:00Z', '2016-12-02T00:00:00Z', 'A'),
]

# Multiple with non-numeric content
data_A2 = [
    MultipleRangeRow('2016-12-01T00:00:00Z', '2016-12-01T04:00:00Z', 10, 'A'),
    MultipleRangeRow('2016-12-01T04:00:00Z', '2016-12-01T08:00:00Z', 30, 'F'),
    MultipleRangeRow('2016-12-01T08:00:00Z', '2016-12-01T12:00:00Z', 60, 'C'),
    MultipleRangeRow('2016-12-01T12:00:00Z', '2016-12-01T16:00:00Z', 60, 'B'),
    MultipleRangeRow('2016-12-01T16:00:00Z', '2016-12-01T20:00:00Z', 40, 'D'),
    MultipleRangeRow('2016-12-01T20:00:00Z', '2016-12-02T00:00:00Z', 50, 'A'),
]

# Missing window at the start
data_B0 = [
    RangeRow('2016-12-01T04:00:00Z', '2016-12-01T08:00:00Z', 30),
    RangeRow('2016-12-01T08:00:00Z', '2016-12-01T12:00:00Z', 60),
    RangeRow('2016-12-01T12:00:00Z', '2016-12-01T16:00:00Z', 60),
    RangeRow('2016-12-01T16:00:00Z', '2016-12-01T20:00:00Z', 40),
    RangeRow('2016-12-01T20:00:00Z', '2016-12-02T00:00:00Z', 50),
]

# Missing window in the middle
data_B1 = [
    RangeRow('2016-12-01T00:00:00Z', '2016-12-01T04:00:00Z', 10),
    RangeRow('2016-12-01T04:00:00Z', '2016-12-01T08:00:00Z', 30),
    RangeRow('2016-12-01T12:00:00Z', '2016-12-01T16:00:00Z', 60),
    RangeRow('2016-12-01T16:00:00Z', '2016-12-01T20:00:00Z', 40),
    RangeRow('2016-12-01T20:00:00Z', '2016-12-02T00:00:00Z', 50),
]

# Missing window at the end
data_B2 = [
    RangeRow('2016-12-01T00:00:00Z', '2016-12-01T04:00:00Z', 10),
    RangeRow('2016-12-01T04:00:00Z', '2016-12-01T08:00:00Z', 30),
    RangeRow('2016-12-01T08:00:00Z', '2016-12-01T12:00:00Z', 60),
    RangeRow('2016-12-01T12:00:00Z', '2016-12-01T16:00:00Z', 60),
    RangeRow('2016-12-01T16:00:00Z', '2016-12-01T20:00:00Z', 40),
]

# Gaps between windows
data_C = [
    RangeRow('2016-12-01T00:00:00Z', '2016-12-01T04:00:00Z', 10),
    RangeRow('2016-12-01T08:00:00Z', '2016-12-01T12:00:00Z', 60),
    RangeRow('2016-12-01T16:00:00Z', '2016-12-01T20:00:00Z', 40),
]

# No data
data_D = [
]

# Multiple columns
data_E = [
    MultipleRangeRow('2016-12-01T00:00:00Z', '2016-12-01T04:00:00Z', 10, 20),
    MultipleRangeRow('2016-12-01T04:00:00Z', '2016-12-01T08:00:00Z', 30, 10),
    MultipleRangeRow('2016-12-01T08:00:00Z', '2016-12-01T12:00:00Z', 60, 0),
    MultipleRangeRow('2016-12-01T12:00:00Z', '2016-12-01T16:00:00Z', 60, 50),
    MultipleRangeRow('2016-12-01T16:00:00Z', '2016-12-01T20:00:00Z', 40, 70),
    MultipleRangeRow('2016-12-01T20:00:00Z', '2016-12-02T00:00:00Z', 50, 90),
]

# Multiple with non-numeric content
data_F = [
    MultipleRangeRow('2016-12-01T00:00:00Z', '2016-12-01T04:00:00Z', 10, 'A'),
    MultipleRangeRow('2016-12-01T04:00:00Z', '2016-12-01T08:00:00Z', 30, 'F'),
    MultipleRangeRow('2016-12-01T08:00:00Z', '2016-12-01T12:00:00Z', 60, 'C'),
    MultipleRangeRow('2016-12-01T12:00:00Z', '2016-12-01T16:00:00Z', 60, 'B'),
    MultipleRangeRow('2016-12-01T16:00:00Z', '2016-12-01T20:00:00Z', 40, 'D'),
    MultipleRangeRow('2016-12-01T20:00:00Z', '2016-12-02T00:00:00Z', 50, 'A'),
]


def encode_expected(data):
    return [(arrow.get(x[0]).datetime.replace(tzinfo=None), *x[1:])
            for x in data]


def load_params_from_json(json_path):
    with open(json_path) as f:
        return json.load(f)


def assertTimeSeriesExpected(data, columns, expected, start, end, resolution):
    expected = encode_expected(expected)
    # XXX: Hardcoded boundary of 4
    timeseries = TimeSeries.from_list(data, columns, timedelta(hours=4),
                                      resolution)
    output = timeseries.query(start, end, resolution)
    output = output.where(pd.notnull(output), None)
    assert output.to_records().tolist() == expected


def test_A0_query_hour_4_20():
    expected = [['2016-12-01T04:00:00', 20.0],
                ['2016-12-01T05:00:00', 25.0],
                ['2016-12-01T06:00:00', 30.0],
                ['2016-12-01T07:00:00', 37.5],
                ['2016-12-01T08:00:00', 45.0],
                ['2016-12-01T09:00:00', 52.5],
                ['2016-12-01T10:00:00', 60.0],
                ['2016-12-01T11:00:00', 60.0],
                ['2016-12-01T12:00:00', 60.0],
                ['2016-12-01T13:00:00', 60.0],
                ['2016-12-01T14:00:00', 60.0],
                ['2016-12-01T15:00:00', 55.0],
                ['2016-12-01T16:00:00', 50.0],
                ['2016-12-01T17:00:00', 45.0],
                ['2016-12-01T18:00:00', 40.0],
                ['2016-12-01T19:00:00', 42.5],
                ['2016-12-01T20:00:00', 45.0]
                ]
    assertTimeSeriesExpected(data_A0, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'H')


def test_A0_query_minute_4_20():
    expected = encode_expected(
        load_params_from_json('tests/fixtures/timeseries_A0_minute.json'))
    assertTimeSeriesExpected(data_A0, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'S')


def test_A0_query_hour_8_12():
    expected = [['2016-12-01T08:00:00', 45.0],
                ['2016-12-01T09:00:00', 52.5],
                ['2016-12-01T10:00:00', 60.0],
                ['2016-12-01T11:00:00', 60.0],
                ['2016-12-01T12:00:00', 60.0],
                ]
    assertTimeSeriesExpected(data_A0, RangeRow._fields, expected,
                             '2016-12-01T08:00:00Z', '2016-12-01T12:00:00Z',
                             'H')


def test_A0_query_hour_6_10():
    expected = [
        ['2016-12-01T06:00:00', 30.0],
        ['2016-12-01T07:00:00', 37.5],
        ['2016-12-01T08:00:00', 45.0],
        ['2016-12-01T09:00:00', 52.5],
        ['2016-12-01T10:00:00', 60.0],
    ]
    assertTimeSeriesExpected(data_A0, RangeRow._fields, expected,
                             '2016-12-01T06:00:00Z', '2016-12-01T10:00:00Z',
                             'H')


def test_A0_query_hour_6_8():
    expected = [
        ['2016-12-01T06:00:00', 30.0],
        ['2016-12-01T07:00:00', 37.5],
        ['2016-12-01T08:00:00', 45.0],
    ]
    assertTimeSeriesExpected(data_A0, RangeRow._fields, expected,
                             '2016-12-01T06:00:00Z', '2016-12-01T08:00:00Z',
                             'H')


def test_A0_query_hour_7_9():
    expected = [
        ['2016-12-01T07:00:00', 37.5],
        ['2016-12-01T08:00:00', 45.0],
        ['2016-12-01T09:00:00', 52.5],
    ]
    assertTimeSeriesExpected(data_A0, RangeRow._fields, expected,
                             '2016-12-01T07:00:00Z', '2016-12-01T09:00:00Z',
                             'H')


def test_A0_query_hour_6_7():
    expected = [
        ['2016-12-01T06:00:00', 30.0],
        ['2016-12-01T07:00:00', 37.5],
    ]
    assertTimeSeriesExpected(data_A0, RangeRow._fields, expected,
                             '2016-12-01T06:00:00Z', '2016-12-01T07:00:00Z',
                             'H')


def test_A0_query_hour_6_6():
    expected = [
        ['2016-12-01T06:00:00', 30.0],
    ]
    assertTimeSeriesExpected(data_A0, RangeRow._fields, expected,
                             '2016-12-01T06:00:00Z', '2016-12-01T06:00:00Z',
                             'H')


def test_A0_query_hour_7_7():
    expected = [
        ['2016-12-01T07:00:00', 37.5],
    ]
    assertTimeSeriesExpected(data_A0, RangeRow._fields, expected,
                             '2016-12-01T07:00:00Z', '2016-12-01T07:00:00Z',
                             'H')


def test_A1_query_hour_4_20():
    expected = [
        ['2016-12-01T04:00:00', None],
        ['2016-12-01T05:00:00', None],
        ['2016-12-01T06:00:00', 'F'],
        ['2016-12-01T07:00:00', None],
        ['2016-12-01T08:00:00', None],
        ['2016-12-01T09:00:00', None],
        ['2016-12-01T10:00:00', 'C'],
        ['2016-12-01T11:00:00', None],
        ['2016-12-01T12:00:00', None],
        ['2016-12-01T13:00:00', None],
        ['2016-12-01T14:00:00', 'B'],
        ['2016-12-01T15:00:00', None],
        ['2016-12-01T16:00:00', None],
        ['2016-12-01T17:00:00', None],
        ['2016-12-01T18:00:00', 'D'],
        ['2016-12-01T19:00:00', None],
        ['2016-12-01T20:00:00', None],
    ]
    assertTimeSeriesExpected(data_A1, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'H')


def test_A2_query_hour_4_20():
    expected = [
        ['2016-12-01T04:00:00', 20.0, None],
        ['2016-12-01T05:00:00', 25.0, None],
        ['2016-12-01T06:00:00', 30.0, 'F'],
        ['2016-12-01T07:00:00', 37.5, None],
        ['2016-12-01T08:00:00', 45.0, None],
        ['2016-12-01T09:00:00', 52.5, None],
        ['2016-12-01T10:00:00', 60.0, 'C'],
        ['2016-12-01T11:00:00', 60.0, None],
        ['2016-12-01T12:00:00', 60.0, None],
        ['2016-12-01T13:00:00', 60.0, None],
        ['2016-12-01T14:00:00', 60.0, 'B'],
        ['2016-12-01T15:00:00', 55.0, None],
        ['2016-12-01T16:00:00', 50.0, None],
        ['2016-12-01T17:00:00', 45.0, None],
        ['2016-12-01T18:00:00', 40.0, 'D'],
        ['2016-12-01T19:00:00', 42.5, None],
        ['2016-12-01T20:00:00', 45.0, None],
    ]
    assertTimeSeriesExpected(data_A2, MultipleRangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'H')


def test_B0_query_hour_4_20():
    expected = [
                ['2016-12-01T04:00:00', None],
                ['2016-12-01T05:00:00', None],
                ['2016-12-01T06:00:00', 30.0],
                ['2016-12-01T07:00:00', 37.5],
                ['2016-12-01T08:00:00', 45.0],
                ['2016-12-01T09:00:00', 52.5],
                ['2016-12-01T10:00:00', 60.0],
                ['2016-12-01T11:00:00', 60.0],
                ['2016-12-01T12:00:00', 60.0],
                ['2016-12-01T13:00:00', 60.0],
                ['2016-12-01T14:00:00', 60.0],
                ['2016-12-01T15:00:00', 55.0],
                ['2016-12-01T16:00:00', 50.0],
                ['2016-12-01T17:00:00', 45.0],
                ['2016-12-01T18:00:00', 40.0],
                ['2016-12-01T19:00:00', 42.5],
                ['2016-12-01T20:00:00', 45.0]
                ]
    assertTimeSeriesExpected(data_B0, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'H')
    expected = encode_expected(expected)


def test_B0_query_minute_4_20():
    expected = encode_expected(
        load_params_from_json('tests/fixtures/timeseries_B0_minute.json'))
    assertTimeSeriesExpected(data_B0, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'S')


def test_B1_query_hour_4_20():
    expected = [['2016-12-01T04:00:00', 20.0],
                ['2016-12-01T05:00:00', 25.0],
                ['2016-12-01T06:00:00', 30.0],
                ['2016-12-01T07:00:00', None],
                ['2016-12-01T08:00:00', None],
                ['2016-12-01T09:00:00', None],
                ['2016-12-01T10:00:00', None],
                ['2016-12-01T11:00:00', None],
                ['2016-12-01T12:00:00', None],
                ['2016-12-01T13:00:00', None],
                ['2016-12-01T14:00:00', 60.0],
                ['2016-12-01T15:00:00', 55.0],
                ['2016-12-01T16:00:00', 50.0],
                ['2016-12-01T17:00:00', 45.0],
                ['2016-12-01T18:00:00', 40.0],
                ['2016-12-01T19:00:00', 42.5],
                ['2016-12-01T20:00:00', 45.0]
                ]
    assertTimeSeriesExpected(data_B1, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'H')


def test_B1_query_minute_4_20():
    expected = encode_expected(
        load_params_from_json('tests/fixtures/timeseries_B1_minute.json'))
    assertTimeSeriesExpected(data_B1, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'S')


def test_B2_query_hour_4_20():
    expected = [
                ['2016-12-01T04:00:00', 20.0],
                ['2016-12-01T05:00:00', 25.0],
                ['2016-12-01T06:00:00', 30.0],
                ['2016-12-01T07:00:00', 37.5],
                ['2016-12-01T08:00:00', 45.0],
                ['2016-12-01T09:00:00', 52.5],
                ['2016-12-01T10:00:00', 60.0],
                ['2016-12-01T11:00:00', 60.0],
                ['2016-12-01T12:00:00', 60.0],
                ['2016-12-01T13:00:00', 60.0],
                ['2016-12-01T14:00:00', 60.0],
                ['2016-12-01T15:00:00', 55.0],
                ['2016-12-01T16:00:00', 50.0],
                ['2016-12-01T17:00:00', 45.0],
                ['2016-12-01T18:00:00', 40.0],
                ['2016-12-01T19:00:00', None],
                ['2016-12-01T20:00:00', None]
                ]
    assertTimeSeriesExpected(data_B2, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'H')
    expected = encode_expected(expected)


def test_B2_query_minute_4_20():
    expected = encode_expected(
        load_params_from_json('tests/fixtures/timeseries_B2_minute.json'))
    assertTimeSeriesExpected(data_B2, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'S')


def test_C_query_hour_4_20():
    expected = [['2016-12-01T04:00:00', None],
                ['2016-12-01T05:00:00', None],
                ['2016-12-01T06:00:00', None],
                ['2016-12-01T07:00:00', None],
                ['2016-12-01T08:00:00', None],
                ['2016-12-01T09:00:00', None],
                ['2016-12-01T10:00:00', 60.0],
                ['2016-12-01T11:00:00', None],
                ['2016-12-01T12:00:00', None],
                ['2016-12-01T13:00:00', None],
                ['2016-12-01T14:00:00', None],
                ['2016-12-01T15:00:00', None],
                ['2016-12-01T16:00:00', None],
                ['2016-12-01T17:00:00', None],
                ['2016-12-01T18:00:00', 40.0],
                ['2016-12-01T19:00:00', None],
                ['2016-12-01T20:00:00', None]
                ]
    assertTimeSeriesExpected(data_C, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'H')


def test_C_query_minute_4_20():
    expected = encode_expected(
        load_params_from_json('tests/fixtures/timeseries_C_minute.json'))
    assertTimeSeriesExpected(data_C, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'S')


def test_D_hour_query_4_20():
    expected = [['2016-12-01T04:00:00', None],
                ['2016-12-01T05:00:00', None],
                ['2016-12-01T06:00:00', None],
                ['2016-12-01T07:00:00', None],
                ['2016-12-01T08:00:00', None],
                ['2016-12-01T09:00:00', None],
                ['2016-12-01T10:00:00', None],
                ['2016-12-01T11:00:00', None],
                ['2016-12-01T12:00:00', None],
                ['2016-12-01T13:00:00', None],
                ['2016-12-01T14:00:00', None],
                ['2016-12-01T15:00:00', None],
                ['2016-12-01T16:00:00', None],
                ['2016-12-01T17:00:00', None],
                ['2016-12-01T18:00:00', None],
                ['2016-12-01T19:00:00', None],
                ['2016-12-01T20:00:00', None]
                ]
    assertTimeSeriesExpected(data_D, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'H')


def test_D_query_minute_4_20():
    expected = encode_expected(
        load_params_from_json('tests/fixtures/timeseries_D_minute.json'))
    assertTimeSeriesExpected(data_D, RangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'S')


def test_E_query_hour_4_20():
    expected = [['2016-12-01T04:00:00', 20.0, 15],
                ['2016-12-01T05:00:00', 25.0, 12.5],
                ['2016-12-01T06:00:00', 30.0, 10],
                ['2016-12-01T07:00:00', 37.5, 7.5],
                ['2016-12-01T08:00:00', 45.0, 5],
                ['2016-12-01T09:00:00', 52.5, 2.5],
                ['2016-12-01T10:00:00', 60.0, 0],
                ['2016-12-01T11:00:00', 60.0, 12.5],
                ['2016-12-01T12:00:00', 60.0, 25],
                ['2016-12-01T13:00:00', 60.0, 37.5],
                ['2016-12-01T14:00:00', 60.0, 50],
                ['2016-12-01T15:00:00', 55.0, 55],
                ['2016-12-01T16:00:00', 50.0, 60],
                ['2016-12-01T17:00:00', 45.0, 65],
                ['2016-12-01T18:00:00', 40.0, 70],
                ['2016-12-01T19:00:00', 42.5, 75],
                ['2016-12-01T20:00:00', 45.0, 80]
                ]
    assertTimeSeriesExpected(data_E, MultipleRangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'H')


def test_F_query_hour_4_20():
    expected = [['2016-12-01T04:00:00', 20.0, None],
                ['2016-12-01T05:00:00', 25.0, None],
                ['2016-12-01T06:00:00', 30.0, 'F'],
                ['2016-12-01T07:00:00', 37.5, None],
                ['2016-12-01T08:00:00', 45.0, None],
                ['2016-12-01T09:00:00', 52.5, None],
                ['2016-12-01T10:00:00', 60.0, 'C'],
                ['2016-12-01T11:00:00', 60.0, None],
                ['2016-12-01T12:00:00', 60.0, None],
                ['2016-12-01T13:00:00', 60.0, None],
                ['2016-12-01T14:00:00', 60.0, 'B'],
                ['2016-12-01T15:00:00', 55.0, None],
                ['2016-12-01T16:00:00', 50.0, None],
                ['2016-12-01T17:00:00', 45.0, None],
                ['2016-12-01T18:00:00', 40.0, 'D'],
                ['2016-12-01T19:00:00', 42.5, None],
                ['2016-12-01T20:00:00', 45.0, None]
                ]
    assertTimeSeriesExpected(data_F, MultipleRangeRow._fields, expected,
                             '2016-12-01T04:00:00Z', '2016-12-01T20:00:00Z',
                             'H')
