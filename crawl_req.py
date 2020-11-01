import aiohttp
import asyncio
from bs4 import BeautifulSoup
import lxml.html

HOST = 'https://habr.com/ru'


async def request_callback(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                text = await asyncio.create_task(response.text())

                await asyncio.create_task(get(text))
                await asyncio.wait(text)
        finally:
            async with session.get(HOST + url) as response:
                text = await asyncio.create_task(response.text())

                await asyncio.create_task(get(text))
                await asyncio.wait(text)


#    asyncio.as_completed(
async def get(html):
    raw_html = BeautifulSoup(html, 'html.parser')
    full_links = [link.get('href') for link in raw_html.select("body a")]

    task = [asyncio.ensure_future(request_callback(link1)) for link1 in set(full_links)]

    await extract(raw_html, html)
    await asyncio.wait(task)


async def extract(content, html_):
    try:
        xpath_html = lxml.html.fromstring(html_)
        h1_extract = xpath_html.xpath('//h1/text()')[0]
        h2_extract = content.find('h2').get_text(strip=True)
        #text_all_extract=content.get_text(strip=False)

    except Exception as e:
        return e
    await responses(h1_extract, h2_extract)


async def responses(output1, output2):
    #    data = {'Заголовок H1': output1, 'Заголовок H2': output2, 'Текст': output3}
    data = {'Заголовок H1': output1, 'Заголовок H2': output2}
    print('%s' % data)
    return data


async def main():
    url = HOST + '/'
    await request_callback(url)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
