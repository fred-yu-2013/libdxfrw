# -*- coding: utf-8 -*-

"""
This file use to gather texts for the data exported from dxf file.
    usage: he_txt_collector 1_2010.json
"""

import sys
import json


g_config = {
    "key": "围墙标准段正立面图",
    "layout": "布局1",
    "layer": "G-大样（标注）"  # none able
}


def is_text_in_viewport(text, vp):
    x = text["x"]
    y = text['y']
    dst_x_left = vp["x"] - vp["width"]/2
    dst_y_top = vp["y"] - vp['height']/2
    dst_x_right = vp["x"] + vp["width"]/2
    dst_y_bottom = vp["y"] + vp['height']/2
    return dst_x_left <= x <= dst_x_right and dst_y_top <= y <= dst_y_bottom


def get_texts_belong_viewports(texts, viewports):
    result = []
    for text in texts:
        for vp in viewports:
            if is_text_in_viewport(text, vp):
                result.append(vp)
    return result


def get_viewport_texts(viewports, texts):
    result = []
    for vp in viewports:
        items = []
        for text in texts:
            if is_text_in_viewport(text, vp):
                items.append(text)
        if items:
            result.append({"viewport": vp, "texts": items})
    return result


def find_texts_by_key(elements):
    """
    获取包含key的文本的viewports，及下面的文字
    :param elements: 文件里的元素列表
    :param key: 待查询的文本
    :return: [{ viewport: {}, texts: [{}] }]
    """
    text_es = list(filter(lambda e: e['type'] in ['TEXT', 'MTEXT'], elements))
    key_texts = list(filter(lambda e: g_config['key'] in e['text'], text_es))
    viewport_es = list(filter(lambda e: e['type'] == 'VIEWPORT', elements))
    viewport_es = list(filter(lambda e: e['layout'] == g_config["layout"], viewport_es))
    dst_viewports = get_texts_belong_viewports(key_texts, viewport_es)
    if g_config['layer']:
        text_es = list(filter(lambda e: e['layer'] == g_config['layer'], elements))
    return get_viewport_texts(dst_viewports, text_es)


def main():
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        # f.writelines([(t+'\n') for t in texts])
        # f.writelines([json.dumps(t) + '\n' for t in texts])
        # f.writelines([t['text'] + '\n' for t in texts])
        elements = json.load(f)
        result = find_texts_by_key(elements)
        print(result)


if __name__ == '__main__':
    main()