import requests
from bs4 import BeautifulSoup
from pprint import pprint

result = {}
filename = 'lexicon.json'


def downloadInfo(URL):
    req = requests.get(URL)
    req.encoding = 'gb18030'
    soup = BeautifulSoup(req.text, 'lxml')
    tmp = soup.find_all('p')

    order = ''
    family = ''
    genus = ''
    species = ''

    for i in tmp:
        if i.br and '&gt' in str(i):
            info = i.getText().split()
            order, family, genus = info[0], info[2], info[4]
            species = soup.title.getText().split()[1]
            break

    return (species, order, family, genus)


def main():
    for i in range(1, 1330):
        # print(i)
        url = 'http://www.cnbird.org.cn/shouce/b' + str(i) + '.htm'
        print('\rNOW PROCESSING: ' + str(i) + '/' + str(1329) + ' {:.2%}'.format(i/1329), end='')
        data = downloadInfo(url)
        result[data[0]] = data[1] + ' ' + data[2] + ' ' + data[3]

    print('DONE!')
    pprint(result)

    import json

    with open(filename, 'w') as file:
        json.dump(result, file, ensure_ascii=False)

def fromFile(filename):
    opt = {}

    with open(filename, 'r') as file:
        '''class_name = ''
        order = ''
        family = ''
        genus = '''''
        species = ''

        for line in file.readlines():
            data = line.split(';')
            species = data[0]
            info = data[1].strip()
            opt[species] = info
            #class_name, order, family, genus = data[0], data[1], data[2], data[3]

    import json

    json.dump(opt, open('tmp.json', 'w'), ensure_ascii=False)
    
    return opt





if __name__ == '__main__':
    print(fromFile('data.txt'))
