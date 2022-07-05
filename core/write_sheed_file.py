import os
import pandas as pd

def write_seedfile(path_file, list_tables):
    root = str(os.path.abspath(path_file))
    try:
        df_seed=pd.read_csv(r''+root)
        for df in list_tables:
            if len(df.merge(df_seed)) != len(df):
                df.to_csv(r''+root, mode='a', index=False, header=False,sep=',',decimal=',')
        return True
    except:
        return False
