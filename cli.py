import requests
import bs4
from saavn_downloader import *
import sys
import urllib.request
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
}
def download(url, filename):
    if not os.path.exists(filename):    
        print('Downloading '+filename)
        urllib.request.urlretrieve(url, filename)
    else:
        print('File already exists. Skipping file...')
def get_song():
    base_path = './songs'
    base_url = 'https://www.saavn.com/search/'
    query = input('Enter search query:')
    url = base_url + query

    #Scraping Saavn for first result
    req = requests.get(url, headers = headers)
    soup = bs4.BeautifulSoup(req.text,"lxml")
    links = soup.find_all("a")
    song_link = None
    for link in links:
        if link.has_attr('href')and ('s/song/' in link['href']):
            print(link['href'])
            song_link = link['href']
            break
    if song_link is None:
        print("Error finding song. Exiting...")
        sys.exit(0)
    downloader = SaavnDownloader(song_link)
    songs = downloader.get_songs()
    song = songs[0]
    download(song['url'],base_path+'/'+song['title']+'-'+song['artists']+'.mp3')
def get_album():
    base_path = './songs'
    album_link = input('Please enter Album URL-\n')
    album_name = input('Please enter Album Name\n(Your album will be stored under ./songs/<ALBUM_NAME>)\n')
    base_path = base_path +'/'+album_name

    #Making Album directory if not exists
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    downloader = SaavnDownloader(album_link)
    songs = downloader.get_songs()
    for song in songs:
        download(song['url'],base_path+'/'+song['title']+'-'+song['artists']+'.mp3')
def main():
    choice = input('Do you want to download a song - s or an album - a\n')
    if choice.upper() == 'A':
        #Album
        get_album()
    elif choice.upper() == 'S':
        #Song
        get_song()
    else:
        print('Incorrect choice.Exiting...')
    
if __name__ == '__main__':
    main()