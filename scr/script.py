import pandas as pd
from scipy import stats
import plotly.express as px
import numpy as np

input_excel = 'train-FIN_ANA_DATA .xls'

class CreditRiskAnalyzer:
    def __init__(self, input_dir:str):
        self.input_dir = input_dir
        self.dataframe = pd.read_excel(input_dir)
        self.columns_info = {i:{'datatype':self.dataframe[i].dtypes.name,
                                'n_nulls':list(self.dataframe.isnull().sum())[n]} 
                                for n, i in enumerate(self.dataframe.columns)}
        self.review_null_values()
        self.values = self.dataframe['QUALITY_OF_LOAN'].value_counts()
        self.dataframe['DEFAULT'] = np.where(self.dataframe['QUALITY_OF_LOAN'] == 'B', 1, 0)
        self.risk_distribution = self.dataframe['DEFAULT'].value_counts(normalize=True)
    
    def save_clean_dataset(self):
        self.dataframe.to_csv('clean_dataset.csv')
    
    def review_null_values(self):
        self.dataframe['INSTALL_SIZE'] = self.dataframe['INSTALL_SIZE'].fillna(self.dataframe['INSTALL_SIZE'].median())
        self.dataframe['CLIENT_TYPE'] = self.dataframe['CLIENT_TYPE'].fillna('Unknown')
        self.dataframe['COMPENSATION_CHARGED'] = self.dataframe['COMPENSATION_CHARGED'].fillna('N')
        self.dataframe = self.dataframe.dropna(subset=['INF_MARITAL_STATUS', 'INF_GENDER'])
        self.columns_info = {i:{'datatype':self.dataframe[i].dtypes.name,
                                'n_nulls':list(self.dataframe.isnull().sum())[n]} 
                                for n, i in enumerate(self.dataframe.columns)}
    
    def probability_calculation_bygroup(self, column_name:str):
        return self.dataframe.groupby(column_name)['DEFAULT'].mean().sort_values(ascending=False)
    
    def total_elements_bygroup(self, column_name:str):
        return self.dataframe[column_name].value_counts()
    
    def mean_calculation_bydefault(self, column_value:str):
        return self.dataframe.groupby('DEFAULT')[column_value].mean().sort_values(ascending=False)

    def apply_kruskal_test(self, column_value:str):
        groups_y = [self.dataframe[self.dataframe['DEFAULT'] == value][column_value] for value in self.dataframe['DEFAULT'].unique()]
        r = stats.kruskal(*groups_y)
        return r
    
    def plot_graph_box(self, column_value:str, scale:bool = False, save:bool = False): 
        if scale:
            fig = px.box(self.dataframe, x='DEFAULT', y=column_value, points='all', log_y=True)
        else:
            fig = px.box(self.dataframe, x='DEFAULT', y=column_value, points='all')
        if save:
            fig.write_image(f'boxes_{column_value}.png')
        fig.show()