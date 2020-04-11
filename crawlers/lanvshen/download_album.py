from lxml import etree
import re
import os

from iutil.requests2.fetch import get_url_text, get_url_binary


MAX_IMAGES_PER_ALBUM = 100
MAX_CONTINUOUS_FAIL_CNT = 3

ptn_ending_space = re.compile(r'\s+$')
ptn_inner_multi_space = re.compile(r'\s\s+')
ptn_arrow_jointer = re.compile(r'\s*>\s*')
ptn_key_value_splitter = re.compile(r'[：:]\s+')
ptn_line_leader = re.compile(r'^', re.M)

image_url_ptn = 'https://img.hywly.com/a/1/%s/%s.jpg'
DATA_ROOT = '/mnt/data/crawler/lanvshen'
IMAGES_ROOT = os.path.join(DATA_ROOT, 'images')
INFO_ROOT = os.path.join(DATA_ROOT, 'desc')


if not os.path.exists(IMAGES_ROOT):
    os.makedirs(IMAGES_ROOT)
if not os.path.exists(INFO_ROOT):
    os.makedirs(INFO_ROOT)


def get_dom_texts(dom, xpath_ptn):
    node = dom.xpath(xpath_ptn)
    texts = [i.strip() for i in node[0].itertext() if i.strip()]
    return texts


def fetch_album(album_id, task_manager):
    url = 'https://www.lanvshen.com/a/%s/' % album_id
    html = get_url_text(url)

    if html is None:
        return
    # print(html[:100])
    task_manager.feed_tasks(html)

    dom = etree.HTML(html)
    meta_text = '\n'.join(get_dom_texts(dom, '/html/body/div[2]'))
    tags_text = ' '.join(get_dom_texts(dom, '/html/body/div[6]'))

    meta_text = tags_text + '\n' + meta_text

    # simple formatter
    meta_text = ptn_ending_space.sub('', meta_text)
    meta_text = ptn_inner_multi_space.sub('\n', meta_text)
    meta_text = ptn_arrow_jointer.sub(' > ', meta_text)
    meta_text = ptn_key_value_splitter.sub(': ', meta_text)
    meta_text = ptn_line_leader.sub('# ', meta_text)

    # print(meta_text)
    # image_urls = []

    continuous_failed_cnt = 0
    for i in range(MAX_IMAGES_PER_ALBUM):

        seq = i + 1
        image_url = image_url_ptn % (album_id, seq)
        if i and i % 100 == 0:
            print('fetching image %s. %s' % (seq, image_url))

        content, ext = get_url_binary(image_url)
        if content is None:
            continuous_failed_cnt += 1
            if continuous_failed_cnt >= MAX_CONTINUOUS_FAIL_CNT:
                print('MAX_CONTINUOUS_FAIL_CNT, %s downloaded' % (seq - MAX_CONTINUOUS_FAIL_CNT))
                break
        else:
            continuous_failed_cnt = 0
            image_filename = os.path.join(IMAGES_ROOT, 'album_%08d_seq_%04d.%s' % (int(album_id), seq, ext.strip('.')))
            with open(image_filename, 'wb') as fw:
                fw.write(content)


if __name__ == '__main__':
    demo_urls = [
        '22610',  # 'https://www.lanvshen.com/a/22610/',  # single model
        '32322',  # 'https://www.lanvshen.com/a/32322/',  # two model
    ]
    for demo_url in demo_urls:
        print('======')
        fetch_album(demo_url)
