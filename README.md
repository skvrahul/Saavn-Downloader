Saavn Downloader(Forked from drt420/Saavn-Downloader)
====

This is a CLI Downloader for Saavn which lets you download entire playlists or even individual songs(by searching for the title).This builds on top of the upstream branch by adding the following features:   

* Actually downloading the MP3 file using UrlLib
* Adding search functionality letting you download individual songs.
* Naming the song files using title and artist
====
You need Python, BeautifulSoup4 and urllib installed for the script to work.

I used python3 but you can use python2, just make changes in the print statements and urllib import statements.

Python3			- https://www.python.org/download/releases/3.0/
BeautifulSoup4	- https://www.crummy.com/software/BeautifulSoup/bs4/doc/

Usage
====
<pre>python3 saavn_downloader.py</pre>
You can choose to either download a single song or an entire album/playlist.   
Enter `s` for Song and `a` for Album   
For song, enter the title of the song and the program searches Saavn for the song and automatically downloads the first result, so make sure your query is appropriate and precise.  

For album, enter the url of the album or playlist from the saavn website eg. http://www.saavn.com/s/album/blah-blah   
OR   
http://www.saavn.com/p/playlist/blah-blah



Future Additions
====

* ID3 Metadata/Tagging 
* Displaying search results and allowing user to choose from them.


