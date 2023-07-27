import pandas as pd
from scipy.stats.stats import kendalltau
from typing import *


class CorrelationTools:
    def __init__(self):
        self.low_correlations: Dict[str, float]
        self.high_correlations: Dict[str, float]

    def read_excel(self, file) -> pd.DataFrame:
        """
        Read an Excel file and return its contents as a pandas DataFrame.

        Parameters:
        file (str): The path to the Excel file.

        Returns:
        pd.DataFrame: A DataFrame containing the data from the Excel file.
        """
        return pd.read_excel(file)

    def calculate_correlation(self, data: pd.DataFrame, method: str) -> pd.DataFrame:
        """
        Calculate the correlation matrix using the specified method.

        Parameters:
            data (pd.DataFrame): The input data.
            method (str): The method to calculate correlation (e.g., 'pearson', 'kendall', 'spearman').

        Returns:
            pd.DataFrame: The correlation matrix.
        """
        return data.corr(numeric_only=True, method=method)

    def filter_correlations(
        self, data_corr: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Filter the correlation matrix into two dictionaries containing low and high correlations.

        Parameters:
            data_corr (pd.DataFrame): The correlation matrix.

        Returns:
            Tuple[Dict[str, Dict[str, float]], Dict[str, Dict[str, float]]]: A tuple containing two dictionaries,
            the first one with low correlations and the second one with high correlations.
        """
        df_filtered_low = data_corr[(data_corr < 0.5) & (data_corr > -0.5)].fillna(0)
        df_filtered_high = data_corr[(data_corr > 0.5) | (data_corr < -0.5)].fillna(0)
        return df_filtered_low, df_filtered_high

    def filter_low_high_corr(self, file, method_chosen="pearson") -> None:
        """
        Read data from an Excel file, calculate correlation, and filter low and high correlations.

        Parameters:
            file (str): The path to the Excel file containing the data.
            method_chosen (str, optional): The method to calculate correlation (default is 'pearson').

        Returns:
            None
        """
        data = self.read_excel(file)
        data_corr = self.calculate_correlation(data, method_chosen)
        df_filtered_low, df_filtered_high = self.filter_correlations(data_corr)
        self.low_correlations = df_filtered_low.to_dict()
        self.high_correlations = df_filtered_high.to_dict()
        self._clean_correlation_dict(self.low_correlations)
        self._clean_correlation_dict(self.high_correlations)

    def _clean_correlation_dict(self, correlation_dict: dict) -> None:
        """
        Go through the correlation_dict and remove 0 and repeating values.

        Parameters:
            correlation_dict (dict): dict of correlated data.
        Returns:
            None
        """
        keys_to_delete = []

        for key1 in correlation_dict:
            sub_dict = correlation_dict[key1]
            for key2 in sub_dict:
                if sub_dict[key2] == 0.0 or key1 == key2:
                    keys_to_delete.append((key1, key2))

        for key in keys_to_delete:
            del correlation_dict[key[0]][key[1]]

    # How to add typing here
    def get_low_corr(self):
        if self.is_empty(self.low_correlations):
            return pd.DataFrame.from_dict(self.low_correlations).to_html()
        return "No low correlation found"

    # How to add typing here
    def get_high_corr(self):
        if self.is_empty(self.high_correlations):
            return pd.DataFrame.from_dict(self.high_correlations).to_html()
        return "No high correlation found"

    @staticmethod
    def is_empty(correlation_dict: Dict[str, float]) -> bool:
        values_list = []
        for i in correlation_dict:
            for x in correlation_dict[i]:
                values_list.append(x)
        return bool(values_list)
