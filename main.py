import tweepy
from core.scraping import Scraping
from datetime import datetime as dt
from core.read_pdf import extract_tables_file
from core.write_sheed_file import write_seedfile
from core.generator import GeneratingImages

CONSUMER_KEY="sJ7jTV0G940R41xRrq8gRvpsS"
CONSUMER_SECRET="ZZmmZg942j3wGLnHMlV1xnhkwyv9IgUEpoQe4whJQiVrYvvqJO"
ACCESS_TOKEN="1512196084218712070-zzVWXk1Ftse0tj0zHOiEqUU0Huk8bN"
ACCESS_TOKEN_SECRET="kKoTayt4n08beZSE9G3q77XBQGh5oIBwhj7WxAyTAbJ6B"

CONFIGURATION_FILE_PATH = "core/static/settings.json"
REPORTING_LOG_PATH = "core/static/reports.json"
SEED_FILE_PATH = "core/static/csv_seed.csv"

DATE = dt.today()

def start_connection_twitter():
    '''Authenticate to Twitter'''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # Create API object
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Authentication OK")
        return True, api
    except:
        print("Error during authentication with Twitter API")
        return False, None

def main():
    scraping = Scraping(CONFIGURATION_FILE_PATH, REPORTING_LOG_PATH)
    status_api, api = start_connection_twitter()
    scraping.get_report_file()
    if status_api and scraping.status:
        print(f"Extract tables from PDF report file")
        status_ext, df_list = extract_tables_file(scraping.file_path)
        print(f"Updating the seed file with a new report")
        status_seed = write_seedfile(SEED_FILE_PATH, df_list)
        if status_ext and status_seed:
            print("Construction of images")
            image_directory_path = f"core/img/{scraping.report_name}"
            generator_obj = GeneratingImages()
            generator_obj.const_images(image_directory_path, SEED_FILE_PATH)
            if generator_obj.status:
                print("Create twitter post")
                media_ids = [api.media_upload(url).media_id for url in generator_obj.list_images]
                tweet='Texto de prueba'
                post_result = api.update_status(status=tweet, media_ids=media_ids)
                print("Post completed successfully\n")

if __name__ == "__main__":
    print(f"\n[{DATE}] : EXECUTION REPORT")
    main()