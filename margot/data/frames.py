from inspect import getmembers
from datetime import datetime

import pandas as pd

from margot.data.column import BaseColumn
from margot.data.features import BaseFeature
from margot.data.symbols import Symbol
from margot.data.ratio import Ratio


class MargotDataFrame(object):
    """An Ensemble brings together symbols, columns and features.

    Args:
        object ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """

    def __init__(self, env: dict = {}):
        """Initiate."""
        self.env = env

        self.symbols = [
            name for name,
            ref in getmembers(self, lambda m: isinstance(m, Symbol))]

        self.features = [
            name for name,
            ref in getmembers(self, lambda m: isinstance(m, BaseFeature))]

        self.ratios = [
            name for name,
            ref in getmembers(self, lambda m: isinstance(m, Ratio))]
        super().__init__()

    def to_pandas(self, when: datetime = None) -> pd.DataFrame:
        """Return a pandas Dataframe representing this MargotDataFrame.

        Args:
            when (datetime, optional): slice to only show data that was
            available at when. 
            That is, the EOD from the previous day.
            Defaults to None.

        Returns:
            pd.DataFrame: [description]
        """
        # Get the elements one at a time, to pandas them and ensemble.
        df1 = pd.concat([getattr(self, name).to_pandas()
                        for name in self.symbols], axis=1)

        df2 = pd.DataFrame({('margot', name): getattr(self, name).get_series()
                            for name in self.ratios + self.features})

        df = pd.concat([df1, df2], axis=1)

        if when:
            df = df.to_pandas().shift()[:when]
    
        return df

    def refresh(self):
        """Refresh all Symbols in this DataFrame."""
        for member in self.symbols:
            getattr(self, member).refresh() 

    @property
    def start_date(self):
        """Attribute.

        The first available value of the 
        time-series index.

        Returns:
            Timestamp: a pandas timestamp.
        """
        return self.to_pandas().index.min()

    @property
    def end_date(self):
        """Attribute.

        The last available value of the 
        time-series index.

        Returns:
            Timestamp: a pandas timestamp.
        """
        return self.to_pandas().index.max()
