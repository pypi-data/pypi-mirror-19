import argparse
from datetime import datetime, timedelta
import json

from tests import test_dataframe
from timeseries import TimeSeries


"""
Fixtures for large datasets (i.e minute) needs to be generated for tests.
This utility produces a JSON file which can then be checked manually.
"""


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def obtain_rows(data, start, end, resolution):
    timeseries = TimeSeries(data, timedelta(hours=4), resolution)
    return timeseries.query(start, end, resolution).to_records().tolist()


def serialize_to_file(rows, filename):
    with open(filename, 'w') as fh:
        # JSON custom formatting, due to the output needs to be human editable
        #   (dumps kwarg indent is not sufficient)
        fh.write('[')
        for i, row in enumerate(rows):
            fh.write('\n\t\t{0}'.format(json.dumps(row, cls=DateTimeEncoder)))
            if not i == len(rows) - 1:
                fh.write(',')
        fh.write('\n]')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('start')
    parser.add_argument('end')
    parser.add_argument('data')
    parser.add_argument('resolution', choices=['S', 'H'])
    parser.add_argument('output')
    args = parser.parse_args()

    data = getattr(test_dataframe, args.data)
    start = args.start
    end = args.end
    resolution = args.resolution
    filename = args.output

    rows = obtain_rows(data, start, end, resolution)
    serialize_to_file(rows, filename)
