1#!/usr/bin/python3
# coded by Arun Kumar Shreevastave - 25 Oct 2016

from bs4 import BeautifulSoup
import os
import requests
from json import JSONDecoder
import base64

from pyDes import *
class SaavnDownloader:
    def __init__(self, url):
        self.url = url
        
    def get_songs(self):
        proxy_ip = ''
        # set http_proxy from environment
        if('http_proxy' in os.environ):
            proxy_ip = os.environ['http_proxy']
        proxies = {
        'http': proxy_ip,
        'https': proxy_ip,
        }
        # proxy setup end here

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
        }
        base_url = 'http://h.saavncdn.com'
        json_decoder = JSONDecoder()

        # Key and IV are coded in plaintext in the app when decompiled
        # and its preety insecure to decrypt urls to the mp3 at the client side
        # these operations should be performed at the server side.
        des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0" , pad=None, padmode=PAD_PKCS5)
        try:
            res = requests.get(self.url, proxies=proxies, headers=headers)
        except Exception as e:
            print(str(e))
            sys.exit()
        soup = BeautifulSoup(res.text,"lxml")

        # Encrypted url to the mp3 are stored in the webpage
        songs_json = soup.find_all('div',{'class':'hide song-json'})
        song_dicts = []
        for song in songs_json:
            song_dict = {}
            obj = json_decoder.decode(song.text)
            song_dict['album'] = obj['album']
            song_dict['artists'] = obj['singers']
            song_dict['year'] = obj['year']
            song_dict['title'] = obj['title']
            song_dict['thumbnail'] = obj['image_url']       
            enc_url = base64.b64decode(obj['url'].strip())
            dec_url = des_cipher.decrypt(enc_url,padmode=PAD_PKCS5).decode('utf-8')
            dec_url = base_url + dec_url.replace('mp3:audios','') + '.mp3'
            song_dict['url'] = dec_url
            song_dicts.append(song_dict)
        return song_dicts            
