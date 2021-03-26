import pandas as pd

from .base import Command
from ..community import community, communities


class List(Command):

    def run(self, name=None, groups=False, all=False, summary=False, out=None):
        name = name or 'all'
        df = self.build_dataframe(name)
        if out:
            df.to_csv(out)
        elif all:
            print(df)
        elif groups:
            print(df.Group.unique())
        elif summary:
            print(df.nunique().to_string())
        else:
            print(df.Community.unique())

    def build_dataframe(self, name):
        df = pd.DataFrame(columns=['Community', 'Group', 'Schema', 'Service', 'URL', 'OAI Set', 'Productive'])
        pd.set_option('display.max_rows', None)
        for identifier in communities(name):
            com = community(identifier)
            df = df.append({
                'Community': com.NAME,
                'Group': com.IDENTIFIER,
                'Schema': com.SCHEMA,
                'Service': com.SERVICE_TYPE,
                'URL': com.URL,
                'OAI Set': com.OAI_SET,
                'Productive': com.PRODUCTIVE,
                 },
                ignore_index=True)
        # df.set_index('Group', inplace=True)
        df = df.sort_values(by=['Community', 'Group'])
        df_sorted = pd.DataFrame(
            data=df.values,
            columns=df.columns)
        return df_sorted
