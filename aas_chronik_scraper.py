from time import sleep
import os
import json

import requests
from bs4 import BeautifulSoup
import pandas as pd

#%%

SLEEPTIME_SEC = 1     # delay between requests
MAX_PAGES = None         # set for debugging; otherwise set to None
OUTPUT_CSV = 'collected_data.csv'

#%%

def fetch_page(pagenum):
    postdata = {
        'action': 'facetwp_refresh',
        'data[facets]': '{"yearly":[],"monthly":[],"region":[],"city":[],"load_more":[%d]}' % pagenum,
        'data[http_params][uri]': 'chronik',
        'data[http_params][lang]': 'de',
        'data[template]': 'wp',
        'data[extras][sort]': 'default',
        'data[soft_refresh]': '1',
        'data[is_bfcache]': '1',
        'data[first_load]': '0',
        'data[paged]': str(pagenum)
    }

    resp = requests.post('https://www.amadeu-antonio-stiftung.de/chronik/', data=postdata)

    if resp.ok:
        respdata = resp.json()
        assert respdata['settings']['pager']['page'] == pagenum
        return respdata
    else:
        raise RuntimeError('requesting chronical page %d failed' % pagenum)


def fetch_article(url):
    resp = requests.get(url)

    if not resp.ok:
        raise RuntimeError(f'requesting article from {url} failed')

    data = {
        'url': url
    }

    soup = BeautifulSoup(resp.content, 'html.parser')
    fullarticle = soup.select_one('article.chronicle')
    data['title'] = fullarticle.select_one('h1').text

    author_elem = fullarticle.select_one('span.author')
    data['author'] = author_elem.text
    data['author_url'] = author_elem.select_one('a')['href']

    postedon_elem = fullarticle.select_one('span.posted-on')
    data['date'] = postedon_elem.select_one('time')['datetime']

    possible_location_elem = postedon_elem.next_sibling
    if hasattr(possible_location_elem, 'text') and possible_location_elem.text.strip().startswith(','):
        data['location'] = possible_location_elem.text.strip()[1:].strip()
    else:
        data['location'] = None

    data['text'] = '\n\n'.join(p.text.strip() for p in fullarticle.select('.entry-content p'))

    sources_urls = []
    sources_texts = []
    for a_elem in fullarticle.select('.socials div.text-grey-light a'):
        sources_urls.append(a_elem['href'])
        sources_texts.append(a_elem.text.strip())

    data['sources_urls'] = '; '.join(sources_urls)
    data['sources_texts'] = '; '.join(sources_texts)

    return data


#%%

if os.path.exists(OUTPUT_CSV):
    print(f'loading already existing data from {OUTPUT_CSV}')
    df = pd.read_csv(OUTPUT_CSV)
    print(f'> loaded {len(df)} rows')
else:
    df = None

pages_left = True
page = 1
total_pages = None

while pages_left:
    print(f'page {page}/{total_pages}')

    rawdatafile = f'rawdata/page{page}.json'

    if os.path.exists(rawdatafile):
        print(f'> loading page data from file {rawdatafile}')
        with open(rawdatafile, 'r') as f:
            respdata = json.load(f)
    else:
        print(f'> fetching page data from website')
        respdata = fetch_page(page)

        print(f'> storing page data to file {rawdatafile}')
        with open(rawdatafile, 'w') as f:
            json.dump(respdata, f)

    page_soup = BeautifulSoup(respdata['template'], 'html.parser')
    chron_items = page_soup.select('article.chronicle')
    print(f'> got {len(chron_items)} articles on page')
    collected_data = []
    for item in chron_items:
        headline_elem = item.select_one('h2 a')
        if not headline_elem:
            print('> no headline for this item; skipping')
            continue

        item_url = headline_elem['href']

        if df is not None and item_url in set(df['url']):
            print(f'> already fetched data from {item_url}; skipping')
        else:
            print(f'> fetching article data from {item_url}')
            articledata = fetch_article(item_url)
            if articledata:
                collected_data.append(articledata)

            sleep(SLEEPTIME_SEC)

    newdata = pd.DataFrame(collected_data)
    df = pd.concat((df, newdata))

    print(f'> collected {len(df)} articles so far; storing to {OUTPUT_CSV}')
    df.to_csv(OUTPUT_CSV, index=False)

    total_pages = respdata['settings']['pager']['total_pages']

    page += 1
    pages_left = page <= (MAX_PAGES or total_pages)

#%%

print('done.')
