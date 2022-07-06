import os
import tweepy
import shutil
import pandas as pd
from core.tools import *
from core.scraping import Scraping
from core.read_pdf import extract_tables_file
from core.generator import ImageGenerator

# system_variables
status, sv = read_json_file("core/static/system_variables.json")

def clean_records(image_file_path, file_path, build_file_path, report_name):
    '''clean generated files'''
    message("Clean generated files\n")
    try:
        shutil.rmtree(image_file_path)

        status, reports = read_json_file(build_file_path)
        if status:
            reports[report_name]["pub_status"] = "on"
            write_json_file(build_file_path, reports)

    except OSError as error:
        message(f'Error removing directory : {error}')

    except KeyError as error:
        message(f'Error changing report status')



def write_seedfile(path_file, list_tables):
    message("Updating the seed file with a new report")

    try:
        df_seed=pd.read_csv(r''+path_file)
        for df in list_tables:
            if len(df.merge(df_seed)) != len(df):
                df.to_csv(r''+path_file, mode='a', index=False, header=False,sep=',',decimal=',')
        return True
    except:
        message("CSV file update failed")
        return False

def start_connection_twitter():
    '''Authenticate to Twitter'''
    auth = tweepy.OAuthHandler(sv["consumer_key"], sv["consumer_secret"])
    auth.set_access_token(sv["access_token"], sv["access_token_secret"])
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        message("Authentication OK")
        return True, api
    except:
        message("Error during authentication with Twitter API")
        return False, None

def main():
    scraping = Scraping(sv["configuration_file_path"], sv["reporting_log_path"])
    status_api, api = start_connection_twitter()
    scraping.get_report_file()
    if status_api and scraping.status:
        status_ext, df_list = extract_tables_file(scraping.file_path)
        status_seed = write_seedfile(sv["seed_file_path"], df_list)
        if status_ext and status_seed:
            message("Construction of images")
            generator_obj = ImageGenerator(sv["build_file_path"], f"{sv['image_directory_path']}/{scraping.report_name}", sv["seed_file_path"])
            generator_obj.create_list_images()
            if generator_obj.status:
                try:
                    message("Create twitter post")
                    media_ids = [api.media_upload(url).media_id for url in generator_obj.list_images]
                    api.update_status(status='Texto de prueba', media_ids=media_ids)
                    message("Post completed successfully")
                    clean_records(generator_obj.image_file_path, scraping.file_path, sv["reporting_log_path"], scraping.report_name)
                except:
                    message("Tweet posting failed\n")

if __name__ == "__main__":
    message("EXECUTION REPORT")
    main()