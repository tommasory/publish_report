import requests
import pyuser_agent
from bs4 import BeautifulSoup

UA = pyuser_agent.UA()

class WebRequests():

    def __init__(self):
        self._headers = {"User-Agent" : UA.chrome}

    def request_header(self):
        return self._headers

    def request_server(self, url : str):
        '''Convert the URL to a SOUP object.
        :param url: (str): URL to consult.
        :return: (dict): Query return plus success status.
        '''
        try:
            gate = requests.get(url, headers=self.request_header())
            code = gate.status_code
            if code == 200:
                soup = BeautifulSoup(gate.text, 'html.parser')
                return True, soup
            message = f'Server response {code}.'
        except:
            message = 'Unexpected error in request_server function'
        return False, message