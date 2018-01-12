from Lyrics_Download import Music
from Classifier import Classifier
import sys
import time

def classifier_print(top_list):
    index = 1
    for (song, value) in top_list:
        print('### Top {}:{}; ###### COUNT:{}'.format(index, song, value))
        index = index + 1


if __name__=='__main__':
    if len(sys.argv) != 3:
        print('Parameter must include singer name and id')
        sys.exit(-1)
    singer_name = sys.argv[1]
    singer_id = int(sys.argv[2])
    top = 50
    classifier = Classifier()
    music = Music(singer_id=6452)
    get_lyric = music.get_lyrics_Of_singer()
    start = time.clock()
    while True:
        try:
            sentences = next(get_lyric)
            classifier.update(sentences)
            print('\ntop:{}'.format(top))
            print(classifier.most_common(top))
            print('\n')
        except StopIteration:
            print('No songs any more')
            break
    end = time.clock()
    print('Time costs {}'.format(end-start))
    print('----------Conclusion----------')
    print(singer_name)
    print('## 统计歌曲数目：{}'.format(music.get_songs_size()))
    print('## top:{} 词（去虚词）'.format(top))
    classifier_print(classifier.most_common(top))

