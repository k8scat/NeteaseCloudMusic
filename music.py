import requests
from urllib.parse import quote
import json

headers = {
    'authority': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}


def music(id, name=None):
    """ 通过歌曲ID下载歌曲 """
    
    save_dir = 'musics/'
    url = 'http://music.163.com/song/media/outer/url?id=' + str(id) + '.mp3'
    r = requests.get(url, headers=headers)
    file = save_dir + (str(id) if name is None else name) + '.mp3'
    with open(file, 'wb') as f:
        f.write(r.content)


def lyric(id, name=None):
    """ 通过歌曲ID下载歌词 """
    
    save_dir = 'lyrics/'
    url = 'http://music.163.com/api/song/media?id=' + str(id)
    r = requests.get(url, headers=headers)
    content = json.loads(r.content.decode('utf-8'))
    if content['code'] == 200:
        file = save_dir + (str(id) if name is None else name) + '.txt'
        with open(file, 'w') as f:
            l = content.get('lyric', None)
            if l is not None:
                f.write(l)
            else:
                print('No lyric')


def search(s, offset=0, limit=10, t=1):
    """ 
    搜索歌曲获取ID
    
    s: 歌曲名
    offset: 偏移量
    limit: 获取歌曲数
    t: 类型(歌曲：1、专辑：10、歌手：100、歌单：1000、用户：1002、mv：1004)
    """
    base_limit = 100
    
    url = 'http://music.163.com/api/search/pc'
    data = {
        's': s,
        'offset': offset,
        'limit': limit,
        'type': t
    }
    r = requests.post(url, data, headers=headers)
    content = json.loads(r.content.decode('utf-8'))
    song_count = content['result']['songCount']
    print(f'搜索结果条数: {song_count}')
    songs = content['result']['songs']
    for song in songs:
        artists = []
        for artist in song['artists']:
            artists.append(artist['name'])
        print(f"id: {song['id']} - 歌名: {song['name']} | 歌手: {','.join(artists)}")
    

if __name__ == "__main__":
    search('Only if you want to')
    music(2530439, name='Only If You Want To')
    lyric(2530439, name='Only If You Want To')
