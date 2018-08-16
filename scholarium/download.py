import argparse
import requests

from bs4 import BeautifulSoup

LOGIN_URL = 'https://scholarium.at/nutzer/anmelden/'

ORDERS_URL = 'https://scholarium.at/warenkorb/bestellungen'


class ScholieSource:

    def __init__(self, soup):
        self.soup = soup

    def title(self):
        return self.soup.find(class_='bestellung_titel').find('a').text


class ScholariumWebpage:

    def __init__(self):
        self.session = requests.session()

    def login(self, username, password):
        csrftoken = self._fetch_csrftoken()
        self.session.post(
                LOGIN_URL,
                data={
                    'csrfmiddlewaretoken': csrftoken,
                    'identification': username,
                    'password': password
                })

    def fetch_available_scholien(self):
        res = self.session.get(ORDERS_URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        content_tables = soup.find_all('table', class_='bestellung_item')
        sources = []
        for table in content_tables:
            for tr in table.find_all('tr'):
                if tr.find(text='Büchlein'):
                    source = ScholieSource(tr)
                    sources.append(source)
        return sources

    def download(self, source):
        pass

    def _fetch_csrftoken(self):
        res = self.session.get('https://scholarium.at')
        return res.cookies.get('csrftoken')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('email',
                        help='Your e-mail for https://scholarium.at')
    parser.add_argument('password',
                        help='Your password for https://scholarium.at')
    args = parser.parse_args()
    page = ScholariumWebpage()
    page.login(args.email, args.password)
    print('Looking for available Scholien')
    scholien_sources = page.fetch_available_scholien()
    if len(scholien_sources) > 0:
        print('Found:')
        for src in scholien_sources:
            print(src.title())
    page.download(scholien_sources)


if __name__ == '__main__':
    main()
