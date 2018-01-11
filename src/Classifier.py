import Lyrics_Download
import jieba
from collections import Counter

class Classifier():
    def __init__(self):
        self.counter = Counter([])

    def update(self, sentences):
        seg_list = self.chinese_text_segementation(sentences)
        self.counter.update(seg_list)

    def most_common(self, num):
        if len(self.counter) >= num:
            return self.counter.most_common(num)

    def chinese_text_segementation(self, sentences):
        seg_list = []
        for item in sentences:
            seg_list += jieba.cut(item, cut_all=False)
        return seg_list
