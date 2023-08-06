from itertools import chain
import pandas as pd
import numpy as np


class TimeSeries(object):

    def __init__(self, dataframe, boundary, resolution):
        dataframe = self.transform_datetimes(dataframe)
        dataframe = self.transform_window_to_point(dataframe)
        dataframe.set_index('datetime', inplace=True)
        dataframe.sort(inplace=True)
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
        # Gaps calculation
        # In a given dataframe, calculate gap groups
        period = int(seconds / 2)
        hour = 60 * 60

        # Store the original integer index
        df_base = dataframe.reset_index()
        df_base['_index'] = df_base.index

        # Get the dataframe at seconds resolution
        df_period = df_base.set_index('datetime').asfreq('S')

        # Find all NULL elements in our dataframe
        df_nulls = df_base[df_base[field].isnull()].set_index('datetime')

        # Shift the NULL elements to the start of their frame
        df_nulls = df_nulls.shift(-period, freq='S')

        # Store the period integer index
        df_index = df_period.reset_index()
        df_index['_index2'] = df_index.index
        df_index.set_index('datetime', inplace=True)

        # Obtain the period elements matched to NULLs
        df_period_nulls = df_index[df_index['_index'].isin(df_nulls['_index'])]

        # Obtain the indexes for the gap elements
        elements =\
            list(set(chain(*[[y for y in range(
                x - seconds + hour,
                x + seconds)]
                for x in df_period_nulls['_index2']])))
        return df_index[df_index['_index2'].isin(elements)][dataframe.columns]

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
