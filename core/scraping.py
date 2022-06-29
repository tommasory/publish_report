from .web_requests import WebRequests

WR = WebRequests()
SETTINGS = {
    "url" : "https://www.aar.org",
    "reports" : {
        "label" : "li",
        "class" : "news-item"
    },
    "file" : {
        "label" : "span",
        "class" : "button"
    }
}

class Scraping:

    def __init__(self):
        self._status, self._settings = True, SETTINGS

    def get_settings(self):
        '''Get configuration variable'''
        return self._settings

    def get_last_report(self):
        '''Get last report url
        :return: (str) : Report URL.
        '''
        reports = []
        soup = ""
        function_status = self._status
        if function_status:
            try:
                function_status = False
                status, soup = WR.request_server(self.get_settings()["url"])
                if status:
                    report_list = soup.find_all(self.get_settings()["reports"]["label"],class_=self.get_settings()["reports"]["class"])
                    for report in report_list:
                        reports.append(report.a.get('href'))
                    if len(reports) != 0:
                        return True, reports[0]
                    soup = "No reports found on current configurations."
            except:
                soup = "An unexpected code error occurred"
        return function_status, soup

    def get_report_file(self):
        '''PDF report path
        :return: (str) : Report URL.
        '''
        function_status, response = self.get_last_report()
        if function_status:
            try:
                function_status = False
                status, soup = WR.request_server(response)
                if status:
                    file_list = soup.find_all(self.get_settings()["file"]["label"],class_=self.get_settings()["file"]["class"])
                    if len(file_list) != 0:
                        path_file = file_list[0].a.get('href')
                        return True, path_file
                    print("There is no file path for this report")
                else:
                    print(soup)
            except:
                print("An unexpected code error occurred")

        return function_status, None