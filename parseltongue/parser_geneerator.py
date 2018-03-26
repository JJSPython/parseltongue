from bs4 import BeautifulSoup
import json
import os
import ast


class GetTagWithText:
    def __init__(self, html, text, num=0):
        self.html = html
        self.num = num if num == 0 else num-1
        self.text = text

    def get_tag(self):
        tag_array = []
        if self.num > 0:
            check_num = 0
            for tag_str in self.html.find_all(True):
                if tag_str.get_text() == self.text:
                    if check_num > 0:
                        tag_str.string = self.text + str(check_num)
                        check_num += 1
                    else:
                        check_num += 1
        self.text = self.text if self.num == 0 else self.text + str(self.num)
        for tags in self.html.find(text=self.text).parents:
            first_tag = str(tags).splitlines()[0]
            tag = BeautifulSoup(first_tag, "lxml").find("body").contents[0]
            if len(self.html.find_all(attrs=tag.attrs)) == 1:
                tag_array.append({'tag': tag.name, 'attr': tag.attrs})
                break
            else:
                tag_array.append({'tag': tag.name, 'attr': tag.attrs})
        return list(reversed(tag_array))


def replace_all(text):
    rep_map = {'[': '', ']': '', '\'': '', ',': '', ' ': '.'}
    for x, y in rep_map.items():
        text = text.replace(x, y)
    return text


def dict_to_select(text):
    if text != {}:
        select_text = ''
        for k, v in text.items():
            if k == "class":
                select_text = "." + replace_all(str(v))
            else:
                select_text = "[" + str(k) + "=" + replace_all(str(v)) + "]"
        return select_text
    else:
        return ''


def html_tag_to_json(get_tag_array):
    select_array = []
    for get_tag in get_tag_array:
        select_array.append({"select": get_tag['tag'] + dict_to_select(get_tag['attr'])})
    return select_array


class Setting:
    def __init__(self, html, file_name=''):
        self.html = BeautifulSoup(html, "lxml")
        self.name = file_name
        self.tag_str = []
        self.table_str = []

    def set_tag(self, *texts):
        tag_array = []
        for txt in texts:
            get_tag_array = GetTagWithText(self.html, txt).get_tag()
            select_array = html_tag_to_json(get_tag_array)
            tag_array.append({"tag": select_array})
        self.tag_str += tag_array

    def set_tag_map(self, maps):
        maps = ast.literal_eval(maps)
        tag_array = []
        for t, n in maps.items():
            get_tag_array = GetTagWithText(self.html, t, n).get_tag()
            select_array = html_tag_to_json(get_tag_array)
            tag_array.append({"tag": select_array})
        self.tag_str += tag_array

    def set_table(self, *texts):
        text_array = []
        for text in texts:
            text_array.append({"text": text})
        self.table_str = text_array

    def to_json(self):
        json_str = json.dumps({"tags": self.tag_str, "table": self.table_str}, separators=(',', ':'))
        '''with open(self.name+".json", "w+") as write_f:
            write_f.write(json_str)'''
        return json_str


class GetJson:
    def __init__(self, file):
        self.file = file

    def to_string(self):
        if os.path.isfile(self.file + ".json"):
            with open(self.file + ".json", "r")as read_f:
                json_str = read_f.read()
            return str(json_str)
        else:
            print(self.file + "不存在")


class JsonToGetText:
    def __init__(self, html, json_str):
        self.html = BeautifulSoup(html, "lxml")
        self.json = json_str

    def get_tag_text(self):
        tag_text = []
        for get_tags in ast.literal_eval(self.json)['tags']:
            for get_tag in get_tags['tag']:
                select_str = ''
                select_str += get_tag['select']+" "
            for text in self.html.select(select_str):
                tag_text.append(text.string)
        return tag_text

    def get_table_text(self):
        table_array = []
        for texts in ast.literal_eval(self.json)['table']:
            text = texts['text']
            for ele in self.html.find_all("table"):
                for txt in ele.stripped_strings:
                    if txt == text:
                        element_string = ele
            arrays = []
            for ele_tr in element_string.select("tr"):
                array = []
                for ele_td in ele_tr.select("td"):
                    array.append(ele_td.text)
                arrays.append(array)
            table_array.append(arrays)
        return table_array