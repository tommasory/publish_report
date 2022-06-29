import tweepy
from core.scraping import Scraping
from datetime import datetime as dt
from core.read_pdf import tuning_df

CONSUMER_KEY="sJ7jTV0G940R41xRrq8gRvpsS"
CONSUMER_SECRET="ZZmmZg942j3wGLnHMlV1xnhkwyv9IgUEpoQe4whJQiVrYvvqJO"
ACCESS_TOKEN="1512196084218712070-zzVWXk1Ftse0tj0zHOiEqUU0Huk8bN"
ACCESS_TOKEN_SECRET="kKoTayt4n08beZSE9G3q77XBQGh5oIBwhj7WxAyTAbJ6B"

DATE = dt.today()

def start_connection_twitter():
    # Authenticate to Twitter
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
    scraping = Scraping()
    status_api, api = start_connection_twitter()
    status_pdf, pdf = scraping.get_report_file()
    if status_api and status_pdf:
        status_ext, df_list = tuning_df()
        if status_ext:
            print("Create twitter post")
            response = api.update_status(f"{DATE}\nReport : {pdf}")
            for table in df_list:
                print(table)
                print('- '*50)
            print("Post completed successfully\n")

if __name__ == "__main__":
    print(f"\n[{DATE}] : EXECUTION REPORT")
    main()