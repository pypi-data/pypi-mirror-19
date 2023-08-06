#!/usr/bin/env python
import os
import re
import requests
from bs4 import BeautifulSoup


class Nibelis:
    base_url = 'https://client.nibelis.com/servlet'

    def __init__(self, output, filename_format):
        self.session = requests.Session()
        self.output = output
        self.filename_format = filename_format

    def absolute_url(self, path):
        """Transform a URL or path to an absolute URL"""
        if '://' in path:
            return path
        return '{0}/{1}'.format(self.base_url, path)

    def get(self, path):
        return self.session.get(self.absolute_url(path))

    def get_soup(self, path):
        """Fetch a path or URL as a BeautifulSoup object"""
        r = self.session.get(self.absolute_url(path))
        r.raise_for_status()
        return BeautifulSoup(r.content, 'html5lib')

    def post(self, path, data):
        return self.session.post(self.absolute_url(path), data=data)

    def login(self, user, password):
        data = {
                'ACTION': 'ACCUEIL',
                'MAJ': 'O',
                'MP:LOGI_PERS_CONN': "{MP:LOGI_PERS_CONN}",
                'MP:LOGI_LOGI': user,
                'MP:LOGI_PASS': password,
                }
        r = self.post('SA_GestionLoginAccueil', data)
        r.raise_for_status()
        if 'Set-Cookie' in r.headers:
            raise RuntimeError("login failed")

    def download_bulletins(self):
        soup = self.get_soup('Gestion?CONVERSATION=SA_GestionDonneesPersonnelles&ACTION=MODI&MAJ=N')
        table = soup.find('form', id='FORM_PRIN').find('table').find('tbody')
        bulletins = [row.find_all('td')[-1].find('input')['value'] for row in table.find_all('tr')]
        if not bulletins:
            print("no bulletins found")
            return
        print("%d bulletins found, last: %s" % (len(bulletins), bulletins[-1]))

        for bulletin in bulletins:
            m = re.match(r'^(?P<user>\d+):(?P<day>\d\d)/(?P<month>\d\d)/(?P<year>\d\d\d\d)$', bulletin)
            output_file = os.path.join(self.output, self.filename_format % m.groupdict())
            if os.path.exists(output_file):
                continue  # already downloaded
            print("downloading %s to %s" % (bulletin, output_file))
            r = self.get('BulletinPdf?PARAM=%s' % bulletin)
            r.raise_for_status()
            with open(output_file, 'wb') as f:
                f.write(r.content)


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Download pay slips from Nibelis website")
    parser.add_argument('-o', '--output', metavar='DIR', default='.',
            help="download directory (default: %(default)s)")
    parser.add_argument('-u', '--user',
            help="user name (default: prompted)")
    parser.add_argument('-p', '--password',
            help="password (default: prompted)")
    parser.add_argument('--filename-format', metavar='FORMAT', default='salaire-%(year)s-%(month)s.pdf',
            help="format of output filenames (default: %(default)s)")
    args = parser.parse_args()

    if args.user is None:
        args.user = raw_input('Username: ')
    if args.password is None:
        import getpass
        args.password = getpass.getpass("Password: ")

    nibelis = Nibelis(args.output, args.filename_format)
    nibelis.login(args.user, args.password)
    nibelis.download_bulletins()



if __name__ == '__main__':
    main()

