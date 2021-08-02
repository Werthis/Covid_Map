import pycountry
import plotly.express as px
import pandas as pd

class CovMap():

    def __init__(self):
        self.list_of_countries = []
        self.dict_of_country_code = {}

    def get_dataset(self):
        self.url_dataset = r'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
        self.cov_19_data_frame = pd.read_csv(self.url_dataset)
        return self.cov_19_data_frame

    def make_list_of_countries(self):   
        self.list_of_countries = self.cov_19_data_frame['Country'].unique().tolist()
        return self.list_of_countries

    def make_dict_of_country_code(self):
        for country in self.list_of_countries:
            try:
                country_data = pycountry.countries.search_fuzzy(country)
                country_code = country_data[0].alpha_3
                self.dict_of_country_code.update({country : country_code})
            except:
                self.dict_of_country_code.update({country : ' '})

    def fill_dataset_with_iso(self):
        for i, j in self.dict_of_country_code.items():
            self.cov_19_data_frame.loc[(self.cov_19_data_frame.Country == i), 'country_code'] = j

    def make_choropleth_map(self, pick='Confirmed'):
        self.pick = pick
        self.cov_map = px.choropleth(
            data_frame = self.cov_19_data_frame,
            locations = 'country_code',
            color = self.pick,
            hover_name = 'Country',
            color_continuous_scale = 'Redor',
            animation_frame = 'Date'          
            )
        self.cov_map.show()


class MakeMap():

    def __init__(self):
        m = CovMap()
        m.get_dataset()
        m.make_list_of_countries()
        m.make_dict_of_country_code()
        m.fill_dataset_with_iso()
        m.make_choropleth_map()


class GuiCommunication():

    def gui_communication(self, gui_pick='Deaths'):
        self.gui_pick = gui_pick
        m = CovMap()
        m.get_dataset()
        m.make_list_of_countries()
        m.make_dict_of_country_code()
        m.fill_dataset_with_iso()
        m.make_choropleth_map(self.gui_pick)
        
if __name__ == "__main__":
    m = MakeMap()
