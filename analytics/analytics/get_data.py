from pprint import pprint
from typing import Any

import requests
from bs4 import BeautifulSoup

result: Any = {}
filename = "lexicon.json"


def download_info(URL):
    req = requests.get(URL)
    req.encoding = "gb18030"
    soup = BeautifulSoup(req.text, "lxml")
    tmp = soup.find_all("p")

    order = ""
    family = ""
    genus = ""
    species = ""

    for i in tmp:
        if i.br and "&gt" in str(i):
            info = i.getText().split()
            order, family, genus = info[0], info[2], info[4]
            species = soup.title.getText().split()[1]
            break

    return (species, order, family, genus)


def main():
    for i in range(1, 1330):
        # print(i)
        url = "http://www.cnbird.org.cn/shouce/b" + str(i) + ".htm"
        print(
            "\rNOW PROCESSING: "
            + str(i)
            + "/"
            + str(1329)
            + " {:.2%}".format(i / 1329),
            end="",
        )
        data = download_info(url)
        result[data[0]] = data[1] + " " + data[2] + " " + data[3]

    print("DONE!")
    pprint(result)

    import json

    with open(filename, "w") as file:
        json.dump(result, file, ensure_ascii=False)


def from_file(filename):
    opt = {}

    with open(filename, "r") as file:
        """class_name = ''
        order = ''
        family = ''
        genus = """ ""
        species = ""

        for line in file.readlines():
            print(line)
            data = line.split(";")
            species = data[0]
            info = data[1].strip()
            opt[species] = info
            # class_name, order, family, genus = data[0], data[1], data[2], data[3]

    import json

    json.dump(opt, open("tmp.json", "w"), ensure_ascii=False)

    return opt


def from_excel(filename):
    import re

    import openpyxl

    data = {}
    book = openpyxl.load_workbook(filename)

    sheet = book.active

    max_row = sheet.max_row

    data = []

    for i in range(3, max_row + 1):
        # for i in range(15, 16):
        print("\rNOW PROCESSING: " + str(i - 2) + "/" + str(max_row - 2), end="")

        class_name = "哺乳纲"
        order = sheet["C" + str(i)].value
        family = sheet["E" + str(i)].value
        genus = str(sheet["J" + str(i)].value).replace("\ufeff", "")
        species = sheet["G" + str(i)].value

        text = str(
            species + ";" + class_name + " " + order + " " + family + " " + genus
        )
        text = re.sub(r"\d", "", text).replace("（", "").replace("）", "")

        data.append(text)

    with open("tmp.txt", "w") as file:
        for i in data:
            file.write(i + "\n")


if __name__ == "__main__":
    from_excel("/Users/henry3510/OneDrive/Project/mammal.xlsx")
    print(from_file("/Users/henry3510/OneDrive/Project/tmp.txt"))
