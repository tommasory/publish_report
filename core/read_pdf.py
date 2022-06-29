from tabula import read_pdf

def extract_table(file):
    df_pageall = read_pdf(file,pages='all')
    k=0
    l_indexTrue=[]
    l_indexFalse=[]
    for df in df_pageall:
        if len(df)==14:
            l_indexTrue.append(k)
        else:
            l_indexFalse.append(k)
        k=k+1
    for idx in sorted(l_indexFalse, reverse = True):
        del df_pageall[idx]
    return df_pageall

def separate_columns(df):
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

def tuning_df():
    path_file = "core/latest_report.pdf"
    # try:
    df_list=extract_table(path_file)
    i=0
    for df in df_list:
        df=separate_columns(df)
        df_list[i]=df
        i=i+1
    if len(df_list) != 0:
        print("Successful information extraction")
        return True, df_list
    # except:
    #     print("Error extracting information from report")
    # return False, None
