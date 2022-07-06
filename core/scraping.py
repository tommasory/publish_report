from .tools import *
from .web_requests import WebRequests

WR = WebRequests()

class Scraping:

    def __init__(self, file_path="", report_log_path=""):
        self.file_path = file_path
        self.report_log_path = report_log_path
        self._status_json, self._settings = read_json_file(self.file_path)
        self.report_name = ""
        self.report_path = ""
        self.status = False

    def get_settings(self):
        '''Get configuration variable'''
        return self._settings

    def get_last_report(self):
        '''Get last report url
        :return: (str) : Report URL.
        '''
        reports = []
        soup = ""
        function_status = self._status_json
        if function_status:
            try:
                function_status = False
                status, soup = WR.request_server_bs4(self.get_settings()["url"])
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
                status, soup = WR.request_server_bs4(response)
                if status:
                    file_list = soup.find_all(self.get_settings()["file"]["label"],class_=self.get_settings()["file"]["class"])
                    if len(file_list) != 0:
                        path_file = file_list[0].a.get('href')
                        self.download_pdf_file(path_file)
                    else:
                        message("There is no file path for this report")
                else:
                    message(soup)
            except:
                message("An unexpected code error occurred")

    def download_pdf_file(self, path_file):
        '''Download a PDF report from the web
        :param path_file: Report URL.
        :return: None
        '''
        try:
            status, response = WR.request_server(path_file)
            if status:
                file_name = path_file.rsplit('/',1)[1]
                aux_report_path = f'core/static/{file_name}'
                open(aux_report_path, 'wb').write(response.content)
                message("Report downloaded successfully")
                self.report_name = file_name.rsplit("-",1)[0]
                self.file_path = aux_report_path
                self.verify_report_publication()
            else:
                print(response)
        except:
            message("PDF download failed")

    def verify_report_publication(self):
        ''' check if the latest report can be published
        :return: Status
        '''
        status, reports = read_json_file(self.report_log_path)
        if status:
            try:
                report = reports[self.report_name]
                if report["pub_status"] == "off":
                    message(f"This report is not yet published - [{self.report_name}]")
                    self.status = True
                else:
                    message(f"This report has already been published - [{self.report_name}]")
            except KeyError:
                message(f"This report is not yet published - [{self.report_name}]")
                reports[self.report_name] = {"pub_status":"off"}
                status, response = write_json_file(self.report_log_path, reports)
                if not status:
                    message(response)
                else:
                    self.status = True