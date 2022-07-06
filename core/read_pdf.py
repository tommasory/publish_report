from .tools import message
from tabula import read_pdf


def extract_table(file):
    #read_pdf es una función de la libreria tabula que permite extraer tablas desde archivos pdf, el
    #parámetro 'pages' con el valor 'all' permite que nos concentremos en todo el pdf pues se podría hacer filtros
    #por pagina que se desea extraer. Esta función retorna una lista de dataframes de todas las tablas encontradas en el pdf
    df_pageall = read_pdf(file,pages='all')
    k=0
    l_indexTrue=[]
    l_indexFalse=[]
    #Como todas las tablas no son de interés para nuestro proposito, creamos un filtro que solo traiga las tablas de longitud 14
    #que son las de nuestro interés para generar los gráficos
    #l_indexTrue alamacenara los indices de la lista que cumplen con la condición anterior y l_indexFalse los que no
    for df in df_pageall:
        if len(df)==14:
            l_indexTrue.append(k)
        else:
            l_indexFalse.append(k)
        k=k+1
    #Ahora borramos de la lista global df_pageall los indices que no cumplieron con la condición, retornando un df_pageall
    #con los dataframes que cumplen con la condición
    for idx in sorted(l_indexFalse, reverse = True):
        del df_pageall[idx]

    return df_pageall

def separate_columns(df):
    #Por defecto
    cars=[]
    year=[]
    cumulative=[]
    avg_wk=[]

    for i in range(len(df)):
        idx_emptyWeek=df['This Week'][i].find(' ')
        idx_emptyYear=df['Year-To-Date'][i].find(' ')

        cars.append(df['This Week'][i][:idx_emptyWeek])
        year.append(df['This Week'][i][idx_emptyWeek+1:])

        cumulative.append(df['Year-To-Date'][i][:idx_emptyYear])
        avg_wk.append(df['Year-To-Date'][i][idx_emptyYear+1:])

    df['Cars']=cars
    df['2021_week']=year
    df['Cumulative']=cars
    df['Avg/wk']=year

    df=df.drop(['This Week','Year-To-Date'],axis=1)
    df=df.drop([0],axis=0)
    df=df.rename(columns={'Unnamed: 1':'2021_Y-t-d'})
    df.reset_index().drop(["index"], axis=1)
    return df[['Unnamed: 0','Cars','2021_week','Cumulative','Avg/wk','2021_Y-t-d']]

def extract_tables_file(file):
    message("Extract tables from PDF report file")
    try:
        dict_country={0:'U.S',1:'Canadian',2:'Mexican',3:'North_american'}
        date_file=file[-26:][:10]
        df_list=extract_table(file)
        i=0
        for df in df_list:
            df=separate_columns(df)
            df_list[i]=df
            df['country']=[dict_country[i]]*len(df)
            df['date']=[date_file]*len(df)
            i=i+1
        if len(df_list) != 0:
            message(f"Successful extraction of information from {len(df_list)} tables")
            return True, df_list
    except:
        message("Error extracting information from report")
    return False, None
