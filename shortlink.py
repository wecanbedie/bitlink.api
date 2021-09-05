import os
import requests
import argparse

from urllib.parse import urlparse
from dotenv import load_dotenv



def count_clicks(token_header, link):
    parsed_url = urlparse(link)
    path = parsed_url.path
    netloc = parsed_url.netloc
    summary_click_check_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}{}/clicks/summary'
    response = requests.get(summary_click_check_url.format(netloc, path), headers=token_header)
    response.raise_for_status()
    return response.json()['total_clicks']


def shorten_link(token_header, link):
    shorten_link_create = 'https://api-ssl.bitly.com/v4/bitlinks'
    payload = {'long_url': link}
    response = requests.post(shorten_link_create, headers=token_header, json=payload)
    response.raise_for_status()
    return response.json()['link']


def check_bitly(token_header, link):
    parsed_url = urlparse(link)
    path = parsed_url.path
    netloc = parsed_url.netloc
    check_bitlink = 'https://api-ssl.bitly.com/v4/bitlinks/{}{}'
    response = requests.get(check_bitlink.format(netloc, path), headers=token_header)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    token_header = {'Authorization': 'Bearer {}'.format(bitly_token)}
    parser = argparse.ArgumentParser(description='Сокращает ссылки и считает количество кликов ')
    parser.add_argument('link', type=str, help='Введите ссылку для сокращения')
    link = parser.parse_args().link
    try:
        if check_bitly(token_header, link):
            shared_clicks = count_clicks(token_header, link)
            print('Количество кликов: ', shared_clicks)
        else:
            shorten_link_create = shorten_link(token_header, link)
            print('Битлинк:', shorten_link_create)
    except requests.exceptions.HTTPError:
        print('Ссылка не является действительной')
