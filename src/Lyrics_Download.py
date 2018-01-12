import requests
from bs4 import BeautifulSoup
import time
from collections import defaultdict
import sqlite3
import sys
import ast
import pickle
import os

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_ntes_nnid=7eced19b27ffae35dad3f8f2bf5885cd,1476521011210; _ntes_nuid=7eced19b27ffae35dad3f8f2bf5885cd; usertrack=c+5+hlgB7TgnsAmACnXtAg==; Province=025; City=025; NTES_PASSPORT=6n9ihXhbWKPi8yAqG.i2kETSCRa.ug06Txh8EMrrRsliVQXFV_orx5HffqhQjuGHkNQrLOIRLLotGohL9s10wcYSPiQfI2wiPacKlJ3nYAXgM; P_INFO=hourui93@163.com|1476523293|1|study|11&12|jis&1476511733&mail163#jis&320100#10#0#0|151889&0|g37_client_check&mailsettings&mail163&study&blog|hourui93@163.com; _ga=GA1.2.1405085820.1476521280; JSESSIONID-WYYY=fb5288e1c5f667324f1636d020704cab2f27ee915622b114f89027cbf60c38be2af6b9cbef2223c1f2581e3502f11b86efd60891d6f61b6f783c0d55114f8269fa801df7352f5cc4c8259876e563a6bd0212b504a8997723a0593b21d5b3d9076d4fa38c098be68e3c5d36d342e4a8e40c1f73378cec0b5851bd8a628886edbdd23a7093%3A1476623819662; _iuqxldmzr_=25; __utma=94650624.1038096298.1476521011.1476610320.1476622020.10; __utmb=94650624.14.10.1476622020; __utmc=94650624; __utmz=94650624.1476521011.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'DNT': '1',
    'Host': 'music.163.com',
    'Pragma': 'no-cache',
    'Referer': 'http://music.163.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}

class Music():
    def __init__(self, singer_id, singer_name, headers=headers):
        self.headers = headers
        self.singer_id = singer_id
        self.singer_name = singer_name
        self.neteasemusic_home_url = "https://music.163.com"
        self.neteasemusic_album_by_artist = "http://music.163.com/artist/album"
        self.neteasemusic_album = "http://music.163.com/album"
        self.neteasemusic_song = "http://music.163.com/api/song/media"
        #self.params_get_ablum_id = {id:self.singer_id}
        #self.params_get_song_id = dict()
        #self.params_get_lyric = dict()
        self.songs_path = '../data/songs_of_{}.txt'.format(self.singer_name)
        self.database_songs = '../data/songids_of_{}'.format(self.singer_id)
        self.database_lyrics = '../data/lyrics_of_{}'.format(self.singer_id)
        #self.connect_sqlite3_database()

        #self.singer_name = singer_name

    #def get_singer_id_by_name(self):
    #    requests.get(

    #def __del__(self):
        #self.conn.commit()
        #self.conn.close()

    def connect_sqlite3_database(self):
        self.conn = sqlite3.connect(self.database_path)
        c = self.conn.cursor()
        return c

    def connect_and_get_respond(self, url, params, headers):
       respond = requests.get(url, params=params, headers=headers)
       soup = BeautifulSoup(respond.content.decode(), 'html.parser')
       return soup

    def get_album_id_by_singer_id(self, singer_id):
        print('----------{} begin----------'.format(sys._getframe().f_code.co_name))
        params_get_ablum_id = {'id':singer_id, 'limit':200}
        soup = self.connect_and_get_respond(self.neteasemusic_album_by_artist, params = params_get_ablum_id, headers = self.headers)
        body = soup.body
        sets = body.find_all('div', class_='u-cover u-cover-alb3')
        # {album_id:album_name}
        albums = defaultdict()

        for item in sets:
            album_id = item.find('a').get('href').replace('/album?id=', '')
            album_name = item.get('title')
            albums[album_id] = album_name
            print("{}:{}".format(album_id, album_name))

        print('----------{} end----------\n'.format(sys._getframe().f_code.co_name))
        return albums

    def get_song_id_by_album_id(self, album_id):
        print('----------{} begin----------'.format(sys._getframe().f_code.co_name))
        params_get_song_id = defaultdict()
        params_get_song_id['id'] = album_id
        soup = self.connect_and_get_respond(self.neteasemusic_album, params = params_get_song_id, headers = headers)
        body = soup.body
        sets = body.find('ul', attrs={'class': 'f-hide'}).find_all('li')
        songs = defaultdict()

        for item in sets:
            song_name = item.getText()
            song_id = item.a.get('href').replace('/song?id=', '')
            songs[song_id] = song_name
            print('{}:{}'.format(song_id, song_name))

        print('----------{} end----------\n'.format(sys._getframe().f_code.co_name))
        return songs

    def get_lyric_by_song_id(self, song_id):
        print('----------{} begin----------'.format(sys._getframe().f_code.co_name))
        params_get_lyrics = defaultdict()
        params_get_lyrics['id'] = song_id
        soup = self.connect_and_get_respond(self.neteasemusic_song, params = params_get_lyrics, headers = headers)
        body = soup.text
        lyrics = []

        #print(body)
        #print(type(body))

        replace_symbol = ['-','…','\'','"','~',',','，','.','。','?','？',':',
'：','!','！','[',']','（','）','(', ')']

        if body.find('nolyric') == -1:
            try:
                temp = ast.literal_eval(body)
            except ValueError:
                return lyrics

            if 'lyric' not in temp.keys():
                return lyrics
            temp = temp['lyric'].split('\n')
            for item in temp:
                item.strip()
                item = item.split(']')
                if (len(item)) > 1:
                    item = item[-1]
                    if item.find('：') == -1:
                        for exword in replace_symbol:
                            item = item.replace(exword, '')
                        lyrics.append(item)
            #    lyrics += sets
        #print(lyrics)
        print('----------{} end----------\n'.format(sys._getframe().f_code.co_name))
        return lyrics

    def get_lyrics_Of_singer(self):
        print('----------{} begin----------'.format(sys._getframe().f_code.co_name))
        lyrics = []
        songs = defaultdict()
        if os.path.exists(self.database_songs) == False:
            albums = self.get_album_id_by_singer_id(self.singer_id)
            for album_id, album_name in albums.items():
                song = self.get_song_id_by_album_id(album_id)
                for song_id, song_name in song.items():
                    if len(song_name.split('(')) == 1:
                        temp = list(songs)
                        if song_name not in temp:
                            songs[song_id] = song_name
            with open(self.database_songs, 'wb') as f:
                pickle.dump(songs, f)
        else:
            with open(self.database_songs, 'rb') as f:
                songs = pickle.load(f)

        self.songs_size = len(songs)
        index = 1.0
        length = 50

        if os.path.exists(self.database_lyrics) == False:
            with open(self.songs_path, 'w') as f:
                with open(self.database_lyrics, 'wb') as ff:
                    for song_id, song_name in songs.items():
                        print('{:>3}/{} {:>}{} {}'.format(int(index), self.songs_size,'='*(int)(index/self.songs_size*length), '>', song_name))
                        f.write(song_name+'\n')
                        time.sleep(5)
                        lyric = self.get_lyric_by_song_id(song_id)
                        lyrics.append(lyric)
                        index = index + 1
                        yield lyric
                        #print('歌曲数目： {}'.format(len(lyrics)))
                    pickle.dump(lyrics, ff)
        else:
            with open(self.database_lyrics, 'rb') as f:
                lyrics = pickle.load(f)
                for lyric in lyrics:
                    yield lyric
        print('----------{} end----------\n'.format(sys._getframe().f_code.co_name))

    def get_songs_size(self):
        return self.songs_size

if __name__=='__main__':
    music = Music(singer_id=6452)
    #music.get_lyric_by_song_id(26609713)
    music.get_lyrics_Of_singer()
