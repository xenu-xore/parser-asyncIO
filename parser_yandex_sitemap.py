from multiprocessing import Pool
import requests
import bs4
import csv
import lxml.html

HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
}

HOST = 'marketyandex'
SITEMAP = '/path-to-sitemap/sitemap-model_reviews-000.xml'


class Crawl(object):
    def data(self):
        """Сбор URL из sitemap для дальнейшего обхода в behavior(data_urls)"""
        try:
            c = requests.get(SITEMAP, allow_redirects=True, headers=HEADERS, timeout=1)
            soup = bs4.BeautifulSoup(c.content, 'html.parser')
            list_urls_s = [i.get_text() for i in soup.find_all('loc')]
            print(list_urls_s)
            return list_urls_s
        finally:

            with open(SITEMAP , 'r') as f:
                soup = bs4.BeautifulSoup(f, 'html.parser')
                list_urls_s = [i.get_text() for i in soup.find_all('loc')]
                return list_urls_s

    def behavior(self, data_urls, timeout=1):
        """Поведение(обработка) полученых из data() URL"""
        self.data_urls = data_urls

        try:
            r = requests.get(self.data_urls, allow_redirects=False, headers=HEADERS, timeout=timeout)
            soup1 = bs4.BeautifulSoup(r.content, 'html.parser')
            lxml_xpath = lxml.html.fromstring(r.content)

            description = lxml_xpath.xpath('//meta[@name="description"]/@content')[0]
            title = lxml_xpath.xpath('//title/text()')[0]
            h1 = soup1.find('h1').get_text()
            text = soup1.get_text(strip=False)
            url = r.url
            status = r.status_code

            dicts = {'status': status, 'h1': h1, 'description': description, 'title': title, 'url': url, 'text': text}
            print(dicts)
        except:
            dicts = {'status': 'None', 'h1': 'None', 'description': 'None', 'title': 'None', 'url': data_urls,
                     'text': 'None'}
            print(dicts)
            pass

        self.csv_writer(dicts)
        return None

    def csv_writer(self, data):
        self.data = data
        """Запись полученых данных из behavior(data_urls)"""
        with open(HOST + '.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow((self.data['status'], self.data['h1'], self.data['description'], self.data['title'], \
                             self.data['url'], self.data['text']))
            f.close()


def PoolCrawl(n):
    M = Crawl()
    Data = M.data()
    pool = Pool(n)
    pool.map(M.behavior, Data)


if __name__ == "__main__":
    PoolCrawl(10)