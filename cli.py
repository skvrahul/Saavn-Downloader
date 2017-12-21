import requests
import bs4
from saavn_downloader import *
import sys
import urllib.request
import string
import eyed3
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
}
def download_album_art(url,filename):
    if not os.path.exists(filename+'.jpg'):
        print('Downloading cover art...')
        urllib.request.urlretrieve(url, filename+'.jpg')
    else:
        print('Cover art already exists')
def song_select(song_links):
    # n = len(songs)
    # for i,song in enumerate(songs):
    #     print('{}) {} - {}'.format(i, song['title'], song['artists']))
    # sel = input('Enter the number of the song you want to download(0 to '+str(n)+')')
    # return int(sel)
    n = len(song_links)    
    for i, link in enumerate(song_links):
        title = '????'
        if link.has_attr('title'):
            title = link.contents[0]
        print('{}) {}'.format(i, title))
    sel = input('Enter the number of the song you want to download(0 to '+str(n)+')')
    return int(sel)
    
def download(url, filename, song):
    if not os.path.exists(filename+'.mp3'):    
        print('Downloading '+song['title']+'-'+song['artists'])
        urllib.request.urlretrieve(url, filename+'.mp3')
        download_album_art(song['thumbnail'], filename)
    else:
        print('File already exists. Skipping file...')
        return
    audiofile = eyed3.load(filename+'.mp3')
    if(audiofile is None):
        return
    audiofile.tag.artist = song['artists']
    audiofile.tag.album = song['album']
    audiofile.tag.title = song['title']
    audiofile.tag.release_date = song['year']
    thumbnail = open(filename+'.jpg', "rb").read()
    audiofile.tag.images.set(3, thumbnail,"image/jpeg",u"")
    audiofile.tag.save()
    print('Done!')
def get_song():
    base_path = './songs'
    base_url = 'https://www.saavn.com/search/'
    query = input('Enter search query:')
    url = base_url + query

    #Scraping Saavn for first result
    req = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(req.text, "lxml")
    links = soup.find_all("a")
    song_link = None
    song_links = []
    for link in links:
        if link.has_attr('href')and ('s/song/' in link['href']):
            song_links.append(link)

    #Selecting a song from the results    
    song_link = song_links[song_select(song_links)]['href']
    print('Downloading from:'+song_link)
    downloader = SaavnDownloader(song_link)
    songs = downloader.get_songs()
    song = songs[0]
    #Removing '/' from file name and album and downloading the file
    download(song['url'], base_path+'/'+(song['title']).replace('/', '') , song)
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
        #Removing '/' from file name and album and downloading the file
        download(song['url'],base_path+'/'+(song['title']).replace('/', '') ,song)
def main():
    choice = input('Do you want to download a song - s or an album/playlist - a\n')
    if choice.upper() == 'A' or choice.upper()=='P':
        #Album
        get_album()
    elif choice.upper() == 'S':
        #Song
        get_song()
    else:
        print('Incorrect choice.Exiting...')
    
if __name__ == '__main__':
    main()