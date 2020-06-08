import pandas as pd


class Ratio(object):
    """Ratio of two series.

    Ratio = numerator / denomnator of two series.

    Args:
        numerator (str): the series to numerate the ratio
        denominator (str): the series to denominate the ratio
        label (str): give it a name for your dataframe. e.g. current_ratio
    """

    def __init__(self, numerator, denominator, label, **kwargs):
        """Initiate. See class for args."""
        self.numerator = numerator
        self.denominator = denominator
        self.series = None
        self.label = label
        self.__dict__.update(kwargs)

        if not self.numerator and self.denominator:
            raise AttributeError(
                "You must supply both a numerator and denominator")
        self.series = self.numerator.get_series().divide(self.denominator.get_series())

    def get_series(self):
        return self.series.rename(self.label)

    def to_pandas(self):
        return self.get_series().to_frame()
