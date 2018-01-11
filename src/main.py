from Lyrics_Download import Music
from Classifier import Classifier

if __name__=='__main__':
    top = 30
    classifier = Classifier()
    music = Music(singer_id=6452)
    get_lyric = music.get_lyrics_Of_singer()
    while True:
        try:
            sentences = next(get_lyric)
            classifier.update(sentences)
            print('top:{}'.format(top))
            print(classifier.most_common(top))
        except StopIteration:
            print('No songs any more')
            break
    print('top:{}'.format(top))
    print(Classifier.most_common(top))

