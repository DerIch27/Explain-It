import pywikibot.pagegenerators as pg
import wikitextparser as wtp
import pywikibot
import csv
import io
import re

class RandomWordGenerator:
    def __init__(self):
        self.site = pywikibot.Site('de', 'wiktionary')
        self.generator = pg.RandomPageGenerator(None, self.site)
    def get(self):
        for page in self.generator:
            for tmpl in wtp.parse(page.text).templates:
                if tmpl.name in ['Grundformverweis Dekl', 'Grundformverweis Konj']:
                    page = pywikibot.Page(self.site, tmpl.get_arg('1').string.lstrip('|'))
                    break
            title = page.title()
            if title.startswith('Flexion:'):
                title = title[8:]
            elif title.startswith('Reim:Deutsch:') or title.startswith('Benutzer:') or \
                title.startswith('Kategorie:') or title.startswith('Wiktionary:') or \
                    title.startswith('Diskussion:') or title.endswith('/Gerundivum') or \
                        title.startswith('Vorlage:') or title.startswith('Kategorie Diskussion:') or \
                            title.startswith('Benutzer Diskussion:'):
                continue
            if re.search('[a-zA-Z]', title) is None: continue
            return title
        

try:
    filename = 'src/assets/data/german_standard.csv'
    generator = RandomWordGenerator()
    while True:
        title = generator.get()
        print()
        res = input(title + ' : ')
        if res == '':
            continue
        with io.open(filename, 'a', encoding='utf8', newline='') as file:
            csv.writer(file).writerow([title]+[i.lstrip(' ') for i in res.split(',') if i.strip()!=''])
except KeyboardInterrupt:
    pass