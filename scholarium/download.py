import argparse
import requests

LOGIN_URL = 'https://scholarium.at/nutzer/anmelden/'

BASIC_URL = 'https://scholarium.at/warenkorb/bestellungen'


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


if __name__ == '__main__':
    main()
