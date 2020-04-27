import requests
from bs4 import BeautifulSoup
from pprint import pprint

result = {}
filename = 'result.txt'

def download_info(URL):
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
            # print(info)
            order, family, genus = info[0], info[2], info[4]
            species = soup.title.getText().split()[1]
            break

    return (species, order, family, genus)

def main():
    for i in range(1, 1330):
        print(i)
        url = 'http://www.cnbird.org.cn/shouce/b' + str(i) + '.htm'
        data = download_info(url)
        result[data[0]] = data[1] + ' ' + data[2] + ' ' + data[3]
    
    print('DONE!')
    pprint(result)

    with open(filename, 'w') as file:
        file.write(str(result))




if __name__ == '__main__':
    main()
