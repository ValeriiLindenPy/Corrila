import pandas as pd
from scipy.stats.stats import kendalltau


class FileHandler:
    @staticmethod
    def read_excel(file):
        return pd.read_excel(file)


class CorrelationCalculator:
    @staticmethod
    def calculate_correlation(data, method):
        return data.corr(numeric_only=True, method=method)


class CorrelationFilter:
    @staticmethod
    def filter_correlations(data_corr):
        df_filtered_low = data_corr[(data_corr < 0.5) & (
            data_corr > -0.5)].fillna(0)
        df_filtered_high = data_corr[(data_corr > 0.5) | (
            data_corr < -0.5)].fillna(0)
        return df_filtered_low, df_filtered_high


class CorrelationTools:
    def __init__(self):
        self.low_correlations = None
        self.high_correlations = None

    def filter_low_high_corr(self, file, method_chosen='pearson'):
        data = FileHandler.read_excel(file)
        data_corr = CorrelationCalculator.calculate_correlation(
            data, method_chosen)
        df_filtered_low, df_filtered_high = CorrelationFilter.filter_correlations(
            data_corr)
        self.low_correlations = df_filtered_low.to_dict()
        self.high_correlations = df_filtered_high.to_dict()
        self._clean_correlation_dict(self.low_correlations)
        self._clean_correlation_dict(self.high_correlations)

    def _clean_correlation_dict(self, correlation_dict):
        keys_to_delete = []

        for key1 in correlation_dict:
            sub_dict = correlation_dict[key1]
            for key2 in sub_dict:
                if sub_dict[key2] == 0.0 or key1 == key2:
                    keys_to_delete.append((key1, key2))

        for key in keys_to_delete:
            del correlation_dict[key[0]][key[1]]

    def get_low_corr(self):
        if self.is_empty(self.low_correlations):
            return pd.DataFrame.from_dict(self.low_correlations).to_html()
        return 'No low correlation found'

    def get_high_corr(self):
        if self.is_empty(self.high_correlations):
            return pd.DataFrame.from_dict(self.high_correlations).to_html()
        return 'No high correlation found'

    @staticmethod
    def is_empty(dic):
        values_list = []
        for i in dic:
            for x in dic[i]:
                values_list.append(x)
        return bool(values_list)
