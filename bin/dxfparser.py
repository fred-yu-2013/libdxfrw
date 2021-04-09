# -*- coding: utf-8 -*-

"""
This dxf parser is for parsing dxf to get the entities data which will be used later.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import generators
from __future__ import division

import re
import sys
import ezdxf
import json


if len(sys.argv) != 3:
    print("Usage: ./dxfparser.py hello.dxf hello.txt")
    exit(1)


def get_texts(doc, result: list):
    es = doc.modelspace().query('TEXT')
    for e in es:
        """
        e.get_pos()[1].x，e.get_pos()[1].y: model space的文字下中坐标
        e.dxf.text: TEXT的文本
        """
        result.append({"type": "TEXT", "x": e.get_pos()[1].x, "y": e.get_pos()[1].y, "text": e.dxf.text})

    es = doc.modelspace().query('MTEXT')
    for e in es:
        t = re.sub(r'\{\\f[^;]+;([^}]+)\}', r'\1', e.plain_text()).replace('\\P', '\n')
        result.append({"type": "MTEXT", "x": e.dxf.insert.x, "y": e.dxf.insert.y, "text": t})


def get_viewports(doc, result: list):
    lo = doc.layout('布局1')
    es = lo.query('VIEWPORT')
    for e in es:
        """
        e.dxf.center.x, e.dxf.center.y: paper space的坐标，和model space坐标对不上
        e.dxf.width，e.dxf.height：paper space的坐标，和model space坐标对不上
        e.dxf.view_height: model space的高度
            自定义比例（aspect ratio）公式为：e.dxf.height / e.dxf.view_height
        e.view_target_point：viewport原点的坐标
        e.view_center_point: viewport model space相对于paper space的坐标。model space中心点坐标公式：
            x = e.dxf.view_target_point.x + e.dxf.view_center_point.x
            y = e.dxf.view_target_point.y + e.dxf.view_center_point.y
        """
        x = e.dxf.view_target_point.x + e.dxf.view_center_point.x
        y = e.dxf.view_target_point.y + e.dxf.view_center_point.y
        aspect_ratio = e.dxf.height / e.dxf.view_height
        width = e.dxf.width / aspect_ratio
        height = e.dxf.view_height
        result.append({"type": "VIEWPORT", "id": e.dxf.id, "x": x, "y": y,
                      "width": width, "height": height, "aspect_ratio": aspect_ratio})


def main():
    doc = ezdxf.readfile(sys.argv[1], encoding='utf-8')

    print(doc.dxfversion)
    old_enc_versions = ['AC1009', 'AC1015', 'AC1018']
    if doc.dxfversion in old_enc_versions:
        doc = ezdxf.readfile(sys.argv[1], encoding='cp932')
    print(doc.layout_names())

    result = []
    get_texts(doc, result)
    get_viewports(doc, result)

    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        # f.writelines([(t+'\n') for t in texts])
        # f.writelines([json.dumps(t) + '\n' for t in texts])
        # f.writelines([t['text'] + '\n' for t in texts])
        json.dump(result, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
