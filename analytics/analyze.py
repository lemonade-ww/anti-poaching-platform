import re
import time
import json
import urllib
import argparse
from sys import exit
from enum import Enum
from typing import Container, Dict, List, Optional, Set, Tuple, Union

import openpyxl
from stanfordcorenlp import StanfordCoreNLP
from pprint import pprint

full_text = ''
data = []
nlp = None
QueryT = Optional[Union[str, Container[str]]]

class Source(Enum):
    BUY = '收购'
    HUNT = '猎捕'
    SELL = '出售'
    TRANSPORT = '运输'


def init_nlp_server(host: str, port: int, server_path: Optional[str] = None):
    global nlp
    if not host.startswith(("http://", "https://")):
        host = f"http://{host}"
    url = f"{host}:{port}"

    try:
        urllib.request.urlopen(url)

    except urllib.error.URLError:
        print(f'Cannot connect to the server via {url}...')

        if server_path:
            print(f"Trying to lanuch the server located at {server_path}")
            try:
                from psutil import AccessDenied
                nlp = StanfordCoreNLP(server_path,
                                    lang='zh', port=port)
            except AccessDenied:
                print('ACCESS DENIED, PLEASE RUN AS ROOT')
            except OSError as err:
                print(err)

        print("Exiting now...")
        exit(1)

    print(f'USING EXISTING SERVER ON {url}')
    nlp = StanfordCoreNLP(host, lang='zh', port=port)


def get_name(data):
    keyword = '被告人'
    name = None
    name_dict = {}

    for line in data:
        keyword_location = line.find(keyword)
        if keyword_location == -1:
            continue

        check_range = line[keyword_location:len(
            line)].replace('）', '')  # just in case

        # try to match names from previous results
        '''for possible_name in name_list:
            # print(check_range[len(pattern):len(name)+len(pattern)])
            if check_range[len(pattern):len(possible_name)+len(pattern)] == possible_name:
                return'''
  
        ner_result = nlp.ner(check_range)
        if ner_result[1][1] == 'PERSON':  # ner_result[0] is keyword

            name = ner_result[1][0]

            if not name_dict.__contains__(name):
                name_dict[name] = 1

            else:
                name_dict[name] += 1

    return name_dict


def get_info(data, name):
    info = {'name': name, 'gender': None, 'birth': None, 'race': None,
            'education_level': None, 'is_valid_person': True, 'all_found': False}

    gender = {'男': '男', '女': '女', '男性': '男', '女性': '女'}
    splited_text = []
    # print(data)

    for line in data:
        if name not in line:
            continue

        ner_result = nlp.ner(line)

        if 'DATE' in str(ner_result):

            for i in ner_result:
                if i[1] == 'DEMONYM' or i[1] == 'NATIONALITY':  # find race info
                    if '族' in i[0]:
                        info['race'] = i[0]
                        break

            splited_text = line.split('。')[0].split('，')

            gender_found = False
            birth_found = False
            education_level_found = False
            for i in splited_text:
                if gender_found and birth_found and education_level_found:
                    break

                if i in gender:
                    info['gender'] = gender[i]
                    gender_found = True

                if '生' in i and not birth_found:
                    ner_result = nlp.ner(i)
                    birth = ''
                    for j in ner_result:
                        if j[1] == 'DATE':
                            birth += j[0]

                    if birth and re.compile('[0-9]+').findall(birth):
                        info['birth'] = birth
                        birth_found = True

                if '文化' in i or '文盲' in i and not education_level_found:
                    info['education_level'] = i
                    education_level_found = True

            break

    from collections import Counter

    if Counter(info.values())[None] == len(info) - 2:
        info['is_valid_person'] = False

    if not Counter(info.values())[None]:
        info['all_found'] = True

    return info


def get_all_name_occurrences(text, names):
    name_list = list(names.keys())
    name_occurrences = {}
    for name in name_list:
        name_occurrences[name] = text.count(name)

    return name_occurrences


def get_location(data):
    place = '公诉机关'
    is_detected = True

    for line in data:
        if place not in line:
            continue

        ner_result = nlp.ner(line)
        location = ''

        for item in ner_result:
            if item[1] == 'ORGANIZATION':
                location += item[0]

        if not location:
            is_detected = False

            from string import punctuation
            punc = '，。、【 】 “”：；（）《》‘’「」？！()、%^>℃：.”“^-——=&#@￥' + punctuation

            location = line[line.find(
                place) + len(place):len(line)].strip(punc)

        return (location, line, is_detected)

    return (None, None, is_detected)


def get_sentence(data):
    sentence = []
    data_reversed = list(reversed(data))
    number = 0

    for number in range(0, len(data_reversed)):
        if data_reversed[number][len(data_reversed[number])-5:] == '判决如下：':
            break

    for i in range(number, 0-1, -1):
        if not data_reversed[i].strip():
            break

        '''text = data_reversed[i]
        ner_result = nlp.ner(text)
        if ner_result[0][1] != 'NUMBER' and text[0] != '（' and text[0:2] != '被告人':
            break'''
        sentence.append(data_reversed[i])

    return sentence


def get_species_info(text):

    appeared_species = {}

    #from ast import literal_eval

    with open('./lexicon.json', 'r', encoding='utf-8') as file:
        #data = literal_eval(file.read())
        data = json.load(file)

    for species in data.keys():
        if species in text:
            appeared_species[species] = data[species]

    return appeared_species


def get_sources_info(data: str, title: str, sentence: str, names: str):
    # preprocess the title
    name_exp = str(names)[1:len(str(names)) - 1].replace(', ', '|').replace('\'','')
    title_list = re.sub(r'(((被告人)?(' + name_exp + ')(、)?)+)', r'\n\1', title).split()

    (sources_info, missings) = fetch_sources_from_text(names, title_list)

    if(len(missings) > 0):
        (result, __) = fetch_sources_from_text(missings, sentence)
        for info in result:
            sources_info.append(info)

    # Lookup lines in which the subject's name appears
    for line in data:
        found = False

        for name in names:
            if name in line:
                found = True
                break

        if found:
            _, tree_dict = nlp_parse(line)

            with open('src_keywords.json', 'r', encoding='utf8') as f:
                sources_keywords = json.load(f)
                # Find sources details for type '收购'
                for keyword in sources_keywords[Source.BUY.value]:
                    for node in tree_dict.get(keyword, []):
                        # For the token (keywords like '收购') located, we go up in the tree by 4 levels to search
                        # within a context of interest
                        context_node = node.up(4)

                        # "PP" generally corresponds to locations, dates, and etc.
                        pp_nodes = context_node.dfs(annotation="PP", count=2, before=node)
                        highlights = set()
                        result = []
                        for pp_node in pp_nodes:
                            highlights.add(pp_node)
                            np_node = pp_node.dfs_one(annotation="NP")
                            if np_node:
                                highlights.add(np_node)
                                result.append(np_node.text)
                        if result:
                            print(result)

                for keyword in sources_keywords[Source.SELL.value]:
                    for node in tree_dict.get(keyword, []):
                        if node.annotation != "VV":
                            continue
                        context_node = node.up(3)
                        result = {"occasion": [], "buyer": []}

                        np_node = context_node.dfs_one(annotation="NP")
                        if np_node:
                            prep_node = context_node.dfs_one(text="给", after=node)
                            if prep_node:
                                result["buyer"].append(np_node.text)

                        pp_node = context_node.dfs_one(annotation="PP", before=node)
                        if pp_node:
                            np_node = pp_node.dfs_one(annotation="NP")
                            if np_node:
                                result["occasion"].append(np_node.text)

                        if result["occasion"] or result["buyer"]:
                            print(result)

                for keyword in sources_keywords[Source.TRANSPORT.value]:
                    for node in tree_dict.get(keyword, []):
                        context_node = node.up(3)
                        result = []

                        #print(context_node.text)

                for keyword in sources_keywords[Source.HUNT.value]:
                    for node in tree_dict.get(keyword, []):
                        context_node = node.up(4)
                        result = []

                        pp_node = context_node.dfs_one(annotation="P", text="在", before=node)
                        if pp_node:
                            np_node = pp_node.up(1).dfs_one(annotation={"NP", "VP"})
                            if np_node:
                                result.append(np_node.text)
                        if result:
                            print(result)

    return sources_info


def fetch_sources_from_text(names_, lines):
    result = []
    names = names_.copy()

    for name in names_:
        info = {'name': name, 'input': [], 'output': []}
        for line in lines:
            if name in line:
                input_ = get_input_sources(line)
                output = get_output_sources(line)

                if len(input_) > 0:
                    info['input'] = input_

                if len(output) > 0:
                    info['output'] = output

        if len(info['input']) > 0 or len(info['output']) > 0:
            result.append(info)
            names.remove(name)

    return (result, names)


class Node:
    def __init__(self, parent: Optional["Node"], text: str, tree_dict: Optional[Dict[str, List["Node"]]] = None):
        self.parent: Optional[Node] = parent
        self.children: List[Node] = []
        self.annotation: str = "UD"
        self.tree_dict: Dict[str, List[Node]] = tree_dict if tree_dict is not None else {}

        # Build a tree with nodes from the phrase-structure tree of the text
        left_stack = []
        for i in range(len(text)):
            if text[i] == '(':
                left_stack.append(i)

            if text[i] == ')':
                left_index = left_stack.pop()

                if len(left_stack) == 0:
                    result = re.search(r'\(([A-Z]+) ((?!\().+?)?[\(\)]', text[left_index:i + 1])
                    self.full_text = text
                    assert result is not None
                    self.annotation = result.group(1)
                    try:
                        self.text = result.group(2)
                        if self.tree_dict.get(self.text) is None:
                            self.tree_dict[self.text] = []
                        self.tree_dict[self.text].append(self)
                    except:
                        pass

                if len(left_stack) == 1:
                    self.children.append(Node(self, text[left_index:i + 1], self.tree_dict))

        if self.text is None:
            prepared_text = []
            for child in self.children:
                prepared_text.append(child.text)
            self.text = "".join(prepared_text)

    def match(self, text: QueryT = None, annotation: QueryT = None) -> bool:
        """A helper funtion to see if the current node match the given conditionals
        When both text and annotation are None, this function always returns True"""
        target_text = {text} if isinstance(text, str) else text
        target_annotation = {annotation} if isinstance(annotation, str) else annotation
        return (target_text is None or self.text in target_text) and (target_annotation is None or self.annotation in target_annotation)

    def tree_to_str(self, highlights: Optional[Set["Node"]] = None) -> str:
        stack = [(0, self)]
        result = []

        def space(level: int) -> str:
            return "".join(["  " for _ in range(level)])

        while len(stack) > 0:
            level, cur_node = stack.pop()
            s = "*" if highlights and cur_node in highlights else ""
            cur_text = f"{space(level)}{s}{cur_node.annotation}{f' {cur_node.text}' if len(cur_node.children) == 0 else ''}{s}"
            if len(cur_node.children) == 1:
                stack.append((0, cur_node.children[0]))
                result.append(f"{cur_text} ")
            else:
                for child in reversed(cur_node.children):
                    stack.append((level + 1, child))
                result.append(f"{cur_text}\n")

        return "".join(result)

    def __repr__(self) -> str:
        return f"Node {self.annotation} \"{self.text[:20]}{'...' if len(self.text) > 20 else ''}\""
    
    def __str__(self) -> str:
        return f"({self.annotation}{f' {self.text}' if self.text else ''})"

    def up(self, level: int) -> "Node":
        """Trace upwards to a parent of the current node.
        When level=0, return the node itself"""
        assert level >= 0
        cur_node = self
        while level > 0:
            if not cur_node.parent:
                return cur_node
            cur_node = cur_node.parent
            level -= 1
        return cur_node

    def dfs_one(self, *, text: QueryT = None, annotation: QueryT = None, before: Optional["Node"] = None, after: Optional["Node"] = None) -> Optional["Node"]:
        """A helper function to look up only one node"""
        result = self.dfs(text=text, annotation=annotation, before=before, after=after)
        return result[0] if len(result) > 0 else None

    def dfs(self, *, text: QueryT = None, annotation: QueryT = None, count: int = 1, before: Optional["Node"] = None, after: Optional["Node"] = None) -> List["Node"]:
        """Conduct a depth first search for the first nth children matching the given conditionals"""
        stack: List[Node] = [self]
        result: List[Node] = []
        is_after = after is None

        def loop(cur_node: Node) -> bool:
            """A helper function to help us conveniently break the outer while loop"""
            for node in cur_node.children:
                if node.match(text, annotation):
                    result.append(node)
                    return False
                if len(result) >= count:
                    return False
            return True

        while len(stack) > 0:
            cur_node = stack.pop()

            if cur_node is before:
                return result

            if is_after and not loop(cur_node):
                break

            if cur_node is after:
                is_after = True

            for node in reversed(cur_node.children):
                stack.append(node)

        return result


def nlp_parse(text) -> Tuple[Node, Dict[str, List[Node]]]:
    assert nlp is not None
    parse_res = nlp.parse(text)

    node = Node(None, parse_res)
    return (node, node.tree_dict)


def get_input_sources(text):
    result = []

    # Determine the input method according to the charges
    if '收购' in text:
        result.append({'type': '收购', 'details': {'occasion': None, 'seller': None}})

    if '猎捕' in text:
        result.append({'type': '猎捕', 'details': {'method': None}})

    return result


def get_output_sources(text):
    result = []

    # Determine the output method according to the charges
    if '出售' in text:
        result.append({'type': '出售', 'details': {'occasion': None, 'buyer': None}})

    if '运输' in text:
        result.append({'type': '运输', 'details': {'vehicle': None}})

    return result


def from_open_law(file):
    data = {}
    book = openpyxl.load_workbook(file)

    sheet = book.active

    max_row = sheet.max_row
    
    for i in range(2, max_row + 1):
    # for i in range(15, 16):
        '''
        G:  location
        J:  defendant
        R:  defendant info
        AD: sentence
        V:  details
        A:  title
        B:  number
        '''

        print('\rNOW PROCESSING: ' + str(i - 1) + '/' + str(max_row), end='')
        detail = {}

        defendant = sheet['J' + str(i)].value
        if not defendant:
            data[i-1] = {}
            continue

        defendant = defendant.split('、')
        for j in defendant:
            if len(j) > 4:
                defendant.remove(j)
        detail['defendant'] = defendant

        # print(sheet['G' + str(i)])
        location = sheet['G' + str(i)].value
        detail['location'] = location

        defendant_info = []
        for name in defendant:
            #tmp = []
            tmp = sheet['R' + str(i)].value.replace('。、', '。\n').split()
            defendant_info.append(get_info(tmp, name))
        detail['defendant_info'] = defendant_info

        sentence = sheet['AD' + str(i)].value.replace(':、',
                                                      '：\n').replace('：、', '：\n').replace('。、', '。\n').split()
        detail['sentence'] = sentence

        species_info = get_species_info(sheet['V' + str(i)].value)
        detail['species_info'] = species_info

        title = sheet['A' + str(i)].value
        detail['title'] = title

        number = sheet['B' + str(i)].value
        detail['number'] = number

        sources_info = get_sources_info(sheet['V' + str(i)].value.split('。、'), title, sentence, defendant)
        detail['sources_info'] = sources_info

        data[i-1] = detail

    return data


def from_file(file):
    global full_text

    detail = {}

    with open(file, 'r', encoding='utf-8') as doc:
        for line in doc.readlines():
            if line.strip():
                full_text += line
                data.append(line.strip())

        defendant = get_name(data)
        detail['defendant'] = defendant

        location = get_location(data)

        detail['location'] = location

        defendant_info = []
        for name in defendant:
            person_info = get_info(data, name)
            defendant_info.append(person_info)

        detail['defendant_info'] = defendant_info

        sentence = get_sentence(data)
        detail['sentence'] = sentence

        species_info = get_species_info(full_text)
        detail['species_info '] = species_info

    return detail


def main(file, opt_file):
    if file[-5:] == '.xlsx':
        print('DETECTED: OpenLaw data')
        result = from_open_law(file)
        #pprint(result)
        if opt_file:
            with open(opt_file, 'w', encoding='utf-8') as opt:
                json.dump(result, opt, ensure_ascii=False)

    else:
        print('DETECTED: file')
        result = from_file(file)
        pprint(result)
        if opt_file:
            with open(opt_file, 'w') as opt:
                json.dump(result, opt, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze the given data")

    parser.add_argument("target", nargs="+", help="The files to be analyzed")
    parser.add_argument("--host", "-x", default="127.0.0.1", help="The host of the nlp server (default: 127.0.0.1)")
    parser.add_argument("--port", "-p", default=9000, type=int, help="The port number of the nlp server (default: 9000)")
    parser.add_argument("--out", "-o", help="The destination of the generated file (optional)")
    parser.add_argument("--server", "-s", help="The path to the Stanford CoreNLP Server (optional)")

    args = parser.parse_args()

    init_nlp_server(args.host, args.port, args.server)

    starttime = time.time()

    for file in args.target:
        main(file, args.out)

    endtime = time.time()

    print('\nUSED: ' + str(endtime - starttime) + 's')
