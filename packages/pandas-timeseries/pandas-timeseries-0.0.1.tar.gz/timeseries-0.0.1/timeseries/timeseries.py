import pandas as pd
import numpy as np


class TimeSeries(object):

    def __init__(self, dataframe, boundary, resolution):
        dataframe = self.transform_datetimes(dataframe)
        dataframe = self.transform_window_to_point(dataframe)
        dataframe.set_index('datetime', inplace=True)
        dataframe = self.transform_dataframe(dataframe, boundary)
        self.dataframe = dataframe.where(pd.notnull(dataframe), None)\
            .asfreq(resolution)

    @classmethod
    def from_dataframe(cls, dataframe, boundary, resolution='S'):
        return cls(dataframe, boundary, resolution)

    @classmethod
    def from_list(cls, data, columns, boundary, resolution='S'):
        dataframe = pd.DataFrame(data, columns=columns)
        return cls(dataframe, boundary, resolution)

    @staticmethod
    def transform_datetimes(dataframe):
        for f in ['valid_from', 'valid_to', 'datetime']:
            if f not in dataframe:
                continue
            dataframe[f] = dataframe[f].astype('datetime64[ns]')
        return dataframe

    @staticmethod
    def transform_window_to_point(dataframe):
        if 'valid_from' not in dataframe or 'valid_to' not in dataframe:
            return dataframe

        dataframe['datetime'] = dataframe['valid_from'].apply(pd.to_datetime)\
            + abs(dataframe['valid_to'] - dataframe['valid_from']) / 2.0
        del dataframe['valid_from']
        del dataframe['valid_to']

        return dataframe

    @classmethod
    def transform_dataframe(cls, dataframe, boundary):
        if dataframe.empty:
            return dataframe

        seconds = int(boundary.seconds)
        # XXX: Add test
        if not seconds:
            return dataframe

        # Interpolation should only occur on numeric types
        dtypes = [np.dtype('int64'), np.dtype('float64')]
        fields = [k for k, v in dataframe.dtypes.iteritems()
                  if v in dtypes]
        nonnumeric_fields = [k for k, _ in dataframe.dtypes.iteritems()
                             if k not in fields]

        dataframe_period = dataframe.asfreq('{0}S'.format(seconds))
        dataframe_interp = dataframe[fields].resample('S').interpolate()
        dataframe_nonnumeric = dataframe[nonnumeric_fields]
        dataframe = dataframe_interp.combine_first(dataframe_nonnumeric)

        mask = dataframe.copy()
        mask[fields] = True
        mask[nonnumeric_fields] = True
        for field in fields:
            gaps = cls.dataframe_gaps(dataframe_period[[field]], field,
                                      seconds)
            gaps[field] = False
            mask[[field]] = gaps[[field]].combine_first(mask[[field]])
        for field in nonnumeric_fields:
            mask[[field]] = mask[[field]].astype('bool')
        return dataframe[mask]

    @staticmethod
    def dataframe_gaps(dataframe, field, seconds):
        dataframe_nulls = dataframe[dataframe[field].isnull()]
        dataframe_gaps = dataframe_nulls.copy()
        for i in range(0, len(dataframe_nulls)):
            gap = dataframe_nulls[i:i+1]
            gap = (gap.shift(-60*60 - (seconds/2), freq='S') + gap +
                   gap.shift((seconds/2)+60*60, freq='S')).asfreq('S')
            dataframe_gaps = dataframe_gaps + gap
        return dataframe_gaps

    def query(self, start, end, resolution):
        dataframe = self.dataframe.copy()
        start = np.datetime64(start)
        end = np.datetime64(end)
        if start not in dataframe.index:
            dataframe.loc[start] = None
        if end not in dataframe.index:
            dataframe.loc[end] = None
        dataframe.index = dataframe.index.astype('datetime64[ns]')
        dataframe.sort_index(inplace=True)
        dataframe = dataframe.asfreq(resolution)
        return dataframe[start:end]
