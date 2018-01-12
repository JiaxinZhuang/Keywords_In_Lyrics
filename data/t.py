import pickle
import sys

sid = sys.argv[1]
with open('lyrics_of_{}'.format(sid), 'rb') as f:
    data = pickle.load(f)

cdata = []
replace_symbol = ['-','…','\'','"','~',',','，','.','。','?','？',':',
'：','!','！','[',']','（','）','(', ')']
for song in data:
    temp = []
    for item in song:
        if item.find('[') == -1:
            item = item.strip()
            for exword in replace_symbol:
                item = item.replace(exword,'')
            temp.append(item)
    cdata.append(temp)

with open('lyrics_of_{}'.format(sid), 'wb') as f:
    pickle.dump(cdata, f)
