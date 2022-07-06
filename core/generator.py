import os
import itertools
import pandas as pd
import plotly.express as px
from datetime import datetime
from core.tools import read_json_file, message

class ImageGenerator:

    def __init__(self, build_file_path:str, image_file_path:str, seed_file_path:str):
        self.build_file_path = build_file_path
        self.image_file_path = image_file_path
        self.seed_file_path = seed_file_path
        self.list_images = []
        self.status = False

    def get_combination_list(self):
        ''' Genera una combinación de los diferentes filtros para crear las imágenes.
        :return:  Status, List
        '''
        status, list_json = read_json_file(self.build_file_path)
        list_comb = []
        list_aux = []
        if status:
            for v in list_json.values():
                list_aux.append(v)
            try:
                for combinacion in itertools.product(list_aux[0], list_aux[1], list_aux[2]):
                    list_comb.append(combinacion)
                return True, list_comb
            except:
                message("Could not extract the configuration file to build the images")
                pass
        return False, list_comb

    def create_list_images(self):
        '''create a list of images
        :param image_file_path: image file path
        :param seed_file_path: seed file path
        :return: Status
        '''
        self.list_images = []
        if not os.path.exists(self.image_file_path):
            os.makedirs(self.image_file_path)

        status, list_comb = self.get_combination_list()
        if status:
            for comb in list_comb:
                try:
                    self.generate_graph(comb[0], comb[1], comb[2])
                    message(f"Generating image : {comb}")
                except:
                    message(f"Error building image : {comb}")

        self.status = len(self.list_images) != 0

    def generate_graph(self, country,filter_1,filter_2):
        '''Genera una imagen apartir de un pais y dos filtros
        :param country: Pais del cual quiero generar la grafica
        :param filter_1: row filter
        :param filter_2: column filter
        :return: Status
        '''
        date=str(datetime.today().strftime('%Y-%m-%d'))
        name=date+'_'+country+'_'+filter_2+'.png'
        df=pd.read_csv(r''+self.seed_file_path)

        if country!='multiple':
            df_filter=df[(df['country']==country) & (df['Unnamed: 0']==filter_1)].reset_index(drop=True)

            df_filter=df_filter.loc[df_filter['Cars'] != '-', :]
            df_filter=df_filter.loc[df_filter['Cumulative'] != '-', :]
            df_filter=df_filter.loc[df_filter['2021_week'] != '-', :]
            df_filter=df_filter.loc[df_filter['Avg/wk'] != '-', :]
            df_filter=df_filter.loc[df_filter['2021_Y-t-d'] != '-', :]

            df_filter['Cars'] = df_filter['Cars'].str.replace(',','')
            df_filter['Cumulative'] = df_filter['Cumulative'].str.replace(',','')
            df_filter['2021_week'] = df_filter['2021_week'].str.replace('%','')
            df_filter['Avg/wk'] = df_filter['Avg/wk'].str.replace('%','')
            df_filter['2021_Y-t-d'] = df_filter['2021_Y-t-d'].str.replace('%','')
            df_filter=df_filter.loc[df_filter[filter_2].str.contains(r'[^\x00-\x7F]+') == False]
            df_filter[[filter_2]]=df_filter[[filter_2]].astype(float)
            df_filter=df_filter.sort_values("date").reset_index(drop=True)
            fig = px.line(df_filter, x='date', y=filter_2,title=filter_2,markers=True)
            fig.update_xaxes(type='category')
        else:
            df=df[df['Unnamed: 0']==filter_1]
            df['Cars'] = df['Cars'].str.replace(',','')
            df['Cumulative'] = df['Cumulative'].str.replace(',','')
            df['2021_week'] = df['2021_week'].str.replace('%','')
            df['Avg/wk'] = df['Avg/wk'].str.replace('%','')
            df['2021_Y-t-d'] = df['2021_Y-t-d'].str.replace('%','')

            df=df.loc[df[filter_2].str.contains(r'[^\x00-\x7F]+') == False]
            df = df.sort_values("date").reset_index(drop=True)
            df[[filter_2]]=df[[filter_2]].astype(float)
            fig = px.line(df, x='date', y=filter_2,color='country',title=filter_2+' for country',markers=True)

        image_path = f"{self.image_file_path}/{name}"
        fig.write_image(r''+image_path)
        self.list_images.append(image_path)