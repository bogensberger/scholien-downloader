import argparse
import requests

from os.path import join, abspath
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = 'https://scholarium.at'
LOGIN_URL = urljoin(BASE_URL, '/nutzer/anmelden/')

ORDERS_URL = urljoin(BASE_URL, '/warenkorb/bestellungen')


DEFAULT_TARGET_DIR = join(abspath('.'), 'downloads')


class ScholieSource:

    def __init__(self, soup):
        self.soup = soup

    def title(self):
        return self.soup.find(class_='bestellung_titel').find('a').text

    def filename(self, base_path=None):
        if base_path is None:
            base_path = DEFAULT_TARGET_DIR
        name = '{}.{}'.format(self.title().lower(),
                              self._file_ending())
        name = name.replace('/', '_').replace(' ', '_')
        return join(base_path, name)

    def form_data(self):
        form = self.soup.find('form')
        data = {
            input.get('name'): input.get('value')
            for input in form.find_all('input')
            if input.get('name')
        }
        return form.get('action'), data

    def _file_ending(self):
        return self.soup.find_all('span')[1].text.lower()


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
                if tr.find(text='Büchlein') and \
                        (tr.find(text='Mobi') or tr.find(text='Epub')):
                    source = ScholieSource(tr)
                    sources.append(source)
        return sources

    def download(self, sources):
        for source in sources:
            action, data = source.form_data()
            url = urljoin(BASE_URL, action)
            print("Downloading {}".format(source.filename()))
            res = self.session.post(url, data)
            with open(source.filename(), 'wb') as f:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

    def _fetch_csrftoken(self):
        res = self.session.get(BASE_URL)
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
