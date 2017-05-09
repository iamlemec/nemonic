# tiddlywiki parser

import os
import re
import unicodedata
from bs4 import BeautifulSoup

tablen = 4
tab = tablen*' '

def parse_block(block):
    title = block['title']

    tags = re.findall(r'\[\[([^\]]+)\]\]', block.get('tags', ''))

    text = block.pre.text
    text = re.sub(r'\*+', lambda x: tab*(len(x.group())-1)+'-', text) # for lists

    return {
        'title': title,
        'tags': tags,
        'text': text
    }

def normalize(s):
    s = s.lower()
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode()
    s = re.sub(r'[ \-]', '_', s)
    s = re.sub(r'[^a-z0-9_]', '', s)
    s = re.sub(r'_{2,}', '_', s)
    return s

def format_block(info, tags=[]):
    title = normalize(info['title'])

    body = ''
    body += '!' + info['title'] + '\n'
    body += '\n'
    body += ' '.join(['#' + normalize(x) for x in info['tags'] + tags]) + '\n'
    body += '\n'
    body += info['text']

    return title, body

def store_block(info, dname, tags=[]):
    title, body = format_block(info, tags=tags)
    fpath = os.path.join(dname, title)
    with open(fpath, 'w+') as fout:
        fout.write(body)

def generate_blocks(fin, max_blocks=None):
    with open(fin) as fid:
        tree = BeautifulSoup(fid.read())
        store = tree.find(id='storeArea')
        for i, block in enumerate(store.find_all('div')):
            yield parse_block(block)
            if max_blocks is not None and i >= max_blocks:
                break

def parse_document(fin, dout, tags=[], max_blocks=None):
    for info in generate_blocks(fin, max_blocks=max_blocks):
        store_block(info, dout, tags=tags)

