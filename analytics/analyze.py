from dataclasses import asdict
import re
import time
import json
import urllib
import argparse
from sys import exit
from typing import Dict, Iterable, List, MutableMapping, Optional, Sequence, Tuple

import openpyxl
from stanfordcorenlp import StanfordCoreNLP

from analytics.lib.tree import NlpNode as Node
from analytics.lib.data_types import PoachingData, Source, SOURCES, LEXICON, SourceData, SourceInfo

full_text = ''
data = []
nlp = None


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


def get_location(data) -> Tuple[Optional[str], str, bool]:
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


def get_sentence(data) -> List[str]:
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


def get_species_info(text) -> MutableMapping[str, str]:

    appeared_species = {}

    #from ast import literal_eval

    for species in LEXICON.keys():
        if species in text:
            appeared_species[species] = LEXICON[species]

    return appeared_species


def get_buy_sources(tree_dict: Dict[str, List[Node]]) -> List[SourceInfo]:
    sources = []
    # Find sources details for type '收购'
    for node in Node.traverser(tree_dict, SOURCES[Source.BUY.value]):
        # For the token (keywords like '收购') located, we go up in the tree by 4 levels to search
        # within a context of interest
        context_node = node.up(4)
        # "PP" generally corresponds to locations, dates, and etc.
        pp_nodes = context_node.dfs(annotation="PP", count=2, before=node)
        highlights = set()
        for pp_node in pp_nodes:
            highlights.add(pp_node)
            np_node = pp_node.dfs_one(annotation="NP")
            if np_node:
                highlights.add(np_node)
                sources.append(SourceInfo(type=Source.BUY, occasion=np_node.text))
    return sources    


def get_sell_sources(tree_dict: Dict[str, List[Node]]) -> List[SourceInfo]:
    sources = []
    for node in Node.traverser(tree_dict, SOURCES[Source.SELL.value]):
        if node.annotation != "VV":
            continue
        context_node = node.up(3)
        sell_source = SourceInfo(Source.SELL)

        np_node = context_node.dfs_one(annotation="NP")
        if np_node:
            prep_node = context_node.dfs_one(text="给", after=node)
            if prep_node:
                sell_source.buyer = np_node.text

        pre_pp_node = context_node.dfs_one(annotation="PP", before=node)
        if pre_pp_node:
            np_node = pre_pp_node.dfs_one(annotation="NP")
            if np_node:
                sell_source.occasion = np_node.text
        sources.append(sell_source)
    return sources


def get_transport_sources(tree_dict: Dict[str, List[Node]]) -> List[SourceInfo]:
    sources = []
    for node in Node.traverser(tree_dict, SOURCES[Source.TRANSPORT.value]):
        context_node = node.up(3)
        transport_source = SourceInfo(Source.TRANSPORT)
        from_symbol = context_node.dfs_one(text=("从", "自"))
        dest_symbol = context_node.dfs_one(text=("到", "至"))

        if from_symbol:
            from_node = context_node.dfs_one(annotation="NP", after=from_symbol, before=dest_symbol)
            if from_node:
                transport_source.occasion = from_node.text
        if dest_symbol:
            dest_node = context_node.dfs_one(annotation="NP", after=dest_symbol)
            if dest_node:
                transport_source.destination = dest_node.text

        sources.append(transport_source)
    return sources


def get_hunt_sources(tree_dict: Dict[str, List[Node]]) -> List[SourceInfo]:
    sources = []
    for node in Node.traverser(tree_dict, SOURCES[Source.HUNT.value]):
        context_node = node.up(5)
        hunt_source = SourceInfo(Source.HUNT)

        occasion_symbol = context_node.dfs_one(annotation="P", text="在", before=node)
        if occasion_symbol:
            occasion_node = occasion_symbol.up(1).dfs_one(annotation={"NP", "VP"})
            if occasion_node:
                hunt_source.occasion = occasion_node.text

        method_symbol = context_node.dfs_one(text="方式", before=node)
        if method_symbol:
            method_nodes = context_node.dfs(annotation="VV", before=method_symbol)
            for node in method_nodes:
                print(f"method:{node.text}")

        sources.append(hunt_source)
    return sources


def get_sources_info(data: Sequence[str], title: Optional[str], sentence: Sequence[str], names: List[str]) -> List[SourceData]:
    # preprocess the title
    defendant_sources_info = {name: SourceData(name=name) for name in names}
    name_exp = str(names)[1:len(str(names)) - 1].replace(', ', '|').replace('\'','')
    # title_list = re.sub(r'(((被告人)?(' + name_exp + ')(、)?)+)', r'\n\1', title if title is not None else "").split()

    # (sources_info, missings) = fetch_sources_from_text(names, title_list)

    # if(len(missings) > 0):
    #     (result, _) = fetch_sources_from_text(missings, sentence)
    #     sources_info += result
    
    def update_defendant_source_info(names: Iterable[str], data: Iterable[SourceInfo]) -> None:
        for source in data:
            if source.is_empty():
                continue
            for name in names:
                if source.type in (Source.BUY, Source.HUNT):
                    defendant_sources_info[name].input.append(source)
                else:
                    defendant_sources_info[name].output.append(source)

    # Lookup lines in which the subject's name appears
    for line in data:
        names_mentioned = [name for name in names if name in line]

        if len(names_mentioned) > 0:
            _, tree_dict = nlp_parse(line)
            sources = get_buy_sources(tree_dict) + get_sell_sources(tree_dict) + get_transport_sources(tree_dict) + get_hunt_sources(tree_dict)
            update_defendant_source_info(names_mentioned, sources)

    return list(defendant_sources_info.values())


def fetch_sources_from_text(names: List[str], lines: Iterable[str]) -> Tuple[List[SourceData], List[str]]:
    result = []
    _names = names.copy()

    for name in _names:
        info = SourceData(name=name)
        for line in lines:
            if name in line:
                input_ = get_input_sources(line)
                output = get_output_sources(line)

                if len(input_) > 0:
                    info.input = input_

                if len(output) > 0:
                    info.output = output

        if len(info.input) > 0 or len(info.output) > 0:
            result.append(info)
            _names.remove(name)

    return (result, _names)


def nlp_parse(text) -> Tuple[Node, Dict[str, List[Node]]]:
    assert nlp is not None
    parse_res = nlp.parse(text)

    node = Node(None, parse_res)
    return (node, node.tree_dict)


def get_input_sources(text) -> List[SourceInfo]:
    result = []

    # Determine the input method according to the charges
    if Source.BUY.value in text:
        result.append(SourceInfo(type=Source.BUY))

    if Source.HUNT.value in text:
        result.append(SourceInfo(type=Source.HUNT))

    return result


def get_output_sources(text: str) -> List[SourceInfo]:
    result = []

    # Determine the output method according to the charges
    if Source.SELL.value in text:
        SourceInfo(type=Source.SELL)

    if Source.TRANSPORT.value in text:
        SourceInfo(type=Source.TRANSPORT)

    return result


def from_open_law(file: str, limit: Optional[int] = None) -> List[PoachingData]:
    result: List[PoachingData] = []
    book = openpyxl.load_workbook(file)

    sheet = book.active

    max_row = sheet.max_row
    if limit and limit < max_row:
        max_row = limit + 1
    
    for i in range(2, max_row + 1):
        '''
        G:  location
        J:  defendant
        R:  defendant info
        AD: sentence
        V:  details
        A:  title
        B:  number
        '''

        print('\rNOW PROCESSING: ' + str(i - 1) + '/' + str(max_row - 1), end='')
        poaching_data = PoachingData(data_id=f"OpenLaw #{i - 1}")
        result.append(poaching_data)

        defendant: str = sheet['J' + str(i)].value
        if not defendant:
            continue

        poaching_data.defendants = [name for name in defendant.split('、') if len(name) <= 4]

        # print(sheet['G' + str(i)])
        poaching_data.location = sheet['G' + str(i)].value

        for name in poaching_data.defendants:
            raw_info = sheet['R' + str(i)].value.replace('。、', '。\n').split()
            poaching_data.defendant_info.append(get_info(raw_info, name))

        poaching_data.sentence = sheet['AD' + str(i)].value.replace(':、', '：\n').replace('：、', '：\n').replace('。、', '。\n').split()

        poaching_data.species_info = get_species_info(sheet['V' + str(i)].value)

        poaching_data.title = sheet['A' + str(i)].value

        poaching_data.number = sheet['B' + str(i)].value

        poaching_data.sources_info = get_sources_info(sheet['V' + str(i)].value.split('。、'), poaching_data.title, poaching_data.sentence, poaching_data.defendants)

    return result


def from_file(file: str):
    global full_text

    result = []

    with open(file, 'r', encoding='utf-8') as doc:
        data = [line for line in [line.strip() for line in doc.readlines()] if line]
        full_text = "".join(data)

        poaching_data = PoachingData(data_id=doc.name)

        poaching_data.defendants = get_name(data)

        poaching_data.location, _, _ = get_location(data)

        for name in poaching_data.defendants:
            person_info = get_info(data, name)
            poaching_data.defendant_info.append(person_info)

        poaching_data.sentence = get_sentence(data)

        poaching_data.species_info = get_species_info(full_text)

        result.append(poaching_data)

    return result


def main(file: str, opt_file: str, limit: Optional[int] = None):
    if file[-5:] == '.xlsx':
        print('DETECTED: OpenLaw data')
        result = from_open_law(file, limit)
        if opt_file:
            with open(opt_file, 'w', encoding='utf-8') as opt:
                json.dump([asdict(data) for data in result], opt, ensure_ascii=False)

    else:
        print('DETECTED: file')
        result = from_file(file)
        if opt_file:
            with open(opt_file, 'w') as opt:
                json.dump([asdict(data) for data in result], opt, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze the given data")

    parser.add_argument("target", nargs="+", help="The files to be analyzed")
    parser.add_argument("--host", "-x", default="127.0.0.1", help="The host of the nlp server (default: 127.0.0.1)")
    parser.add_argument("--port", "-p", default=9000, type=int, help="The port number of the nlp server (default: 9000)")
    parser.add_argument("--out", "-o", help="The destination of the generated file (optional)")
    parser.add_argument("--server", "-s", help="The path to the Stanford CoreNLP Server (optional)")
    parser.add_argument("--limit", "-l", type=int, help="The maximum number of entries to be processed in each file (optional)")

    args = parser.parse_args()

    init_nlp_server(args.host, args.port, args.server)

    starttime = time.time()

    for file in args.target:
        main(file, args.out, args.limit)

    endtime = time.time()

    print('\nUSED: ' + str(endtime - starttime) + 's')
