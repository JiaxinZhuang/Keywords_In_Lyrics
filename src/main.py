from Lyrics_Download import Music
from Classifier import Classifier

if __name__=='__main__':
    top = 50
    classifier = Classifier()
    music = Music(singer_id=6452)
    get_lyric = music.get_lyrics_Of_singer()
    index = 1
    while True:
        try:
            sentences = next(get_lyric)
            classifier.update(sentences)
            print('\ntop:{}'.format(top))
            print(classifier.most_common(top))
            print('\n')
            index = index + 1
        except StopIteration:
            print('No songs any more')
            break
    print('----------Conclusion----------')
    print('## 统计歌曲数目：{}'.format(index))
    print('## top:{} 词（去虚词代词）'.format(top))
    print('## {}'.format(classifier.most_common(top)))

