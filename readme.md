# Readme

***

Download Lyrics from web of particular singer and account for keywords 



## Dependencies

* requests: For getting html
* bs4: For retrieving
* jieba: For text segmentation
* Python3 



## Installation

```
pip3 install -t requirement.txt
```



## Running

```bash
python3 main.py "Singer_name" "id_in_netease_music_url" "top_10?" 
```

You should add three more parameters,  singer_name in Chinese,  singer_id in netease_music url and how many key words do you want to count. Eg.

```
python3 main.py "陈奕迅" 2116 20
```



## Principle

1. Web Spider 
2. Chinese text segmentation 





## Reference

1. [jieba chinese text segmentation](https://github.com/fxsjy/jieba)
2. [PaperWeekly](http://rsarxiv.github.io/)
3. [zhihu how to learn web spider](https://www.zhihu.com/question/20899988)

