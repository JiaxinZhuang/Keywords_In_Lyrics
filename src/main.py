from Lyrics_Download import Music
from Classifier import Classifier
import sys
import time

def classifier_print(top_list):
    index = 1
    counts_star = 178
    max_value = max([value for song,value in top_list])
    for (song, value) in top_list:
        if len(song) == 2:
            print('### Top {: >2}:{:^5}; {}{} COUNT:{}'.format(index, song, '='*((int)(float(value/max_value)*counts_star)),'>',  value))
        else:
            print('### Top {: >2}:{:^6}; {}{} COUNT:{}'.format(index, song, '='*((int)(float(value/max_value)*counts_star)),'>',  value))
        index = index + 1


if __name__=='__main__':
    if len(sys.argv) != 4:
        print('Parameter must include singer name and id and top num')
        sys.exit(-1)
    singer_name = sys.argv[1]
    singer_id = int(sys.argv[2])
    top = int(sys.argv[3])
    classifier = Classifier()
    music = Music(singer_id=singer_id, singer_name=singer_name)
    get_lyric = music.get_lyrics_Of_singer()
    start = time.clock()
    while True:
        try:
            sentences = next(get_lyric)
            classifier.update(sentences)
            #print('\ntop:{}'.format(top))
            #print(classifier.most_common(top))
            #print('\n')
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

