import requests
import pyuser_agent
from bs4 import BeautifulSoup

UA = pyuser_agent.UA()

class WebRequests:

    def __init__(self):
        self._headers = {"User-Agent" : UA.random}

    def request_header(self):
        return self._headers

    def request_server_bs4(self, url : str):
        '''Convert the URL to a SOUP object.
        :param url: (str): URL to consult.
        :return: (dict): Query return plus success status.
        '''
        try:
            response = requests.get(url, headers=self.request_header())
            code = response.status_code
            if code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return True, soup
            message = f'Server response {code}.'
        except:
            message = 'Unexpected error in request_server function'
        return False, message

    def request_server(self, url : str):
        '''Convert url to https response.
        :param url: (str): URL to consult.
        :return: (dict): Query return plus success status.
        '''
        try:
            response = requests.get(url, headers=self.request_header())
            code = response.status_code
            if code == 200:
                return True, response
            message = f'Server response {code}.'
        except:
            message = 'Unexpected error in request_server function'
        return False, message