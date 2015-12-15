#!/usr/bin/env python3
import urllib3
import xml.dom.minidom
from jinja2 import Environment, FileSystemLoader
import os.path
import io
import re
import pyqrcode

box_dimensions = [60, 75]
box_margins = [5, 5]

base_x = 10
base_y = 10
current_x = 0
current_y = 0

elements = [i for i in range(3)]
labels = []

http = urllib3.PoolManager()
data_source_request = http.request('GET', "http://mikael.hautin.fr/fileadmin/media/the/the_2.xml")
if data_source_request.status != 200:
    print(data_source_request.status)
    os._exit(1)

data_source_xml = data_source_request.data.decode('utf-8')

with xml.dom.minidom.parseString(data_source_xml) as data_source_dom:
    i_tea_count = 0
    for o_current_tea in data_source_dom.getElementsByTagName("tea"):
        s_name = o_current_tea.getAttribute('name')

        dom_shop = o_current_tea.getElementsByTagName('shop')[0]
        s_origin = dom_shop.getAttribute('name')
        s_url = dom_shop.getAttribute('url')

        dom_kind = o_current_tea.getElementsByTagName('kind')[0]
        s_kind = dom_kind.getAttribute('code')
        s_type = dom_kind.getAttribute('name')

        # positioning
        if (i_tea_count % 3) == 0:
            current_x = base_x

            if current_y > 0:
                current_y += box_dimensions[1] + box_margins[1]
            else:
                current_y = base_y
        else:
            current_x += box_dimensions[0] + box_margins[0]

        url = pyqrcode.create(s_url, error='Q')
        buffer = io.BytesIO()
        url.svg(buffer, xmldecl=False, svgns=False, scale=2.55)
        s_qr = buffer.getvalue().decode('UTF-8')
        print(s_qr)
        s_qr = s_qr.replace('<svg', '<svg x="18.5mm" y="45mm"')
        s_qr = re.sub('(width|height)="[^"]+"', '\g<1>="35mm"', s_qr)
        print(s_qr)

        # img2 = qrcode.make('Some data here')

        # <tea name="Racconto di Natale">
        # 	<kind name="thé noir indien" />
        # 	<shop name="La Via del Tè" location="Firenze" url="http://www.laviadelte.com" />
        # 	<ingredientlist>
        # 		<ingredient name="pomme" />
        # 		<ingredient name="cannelle" />
        # 		<ingredient name="clous de girofle" />
        # 		<ingredient name="coriandre" />
        # 		<ingredient name="fraise en morceaux" />
        # 		<ingredient name="souci des jardins" />
        # 	</ingredientlist>
        # 	<locationlist>
        # 		<location name="bureau" />
        # 	</locationlist>
        # </tea>
        labels.append({
            'x': current_x,
            'y': current_y,
            'name': s_name,
            'type': s_type,
            'kind': s_kind,
            'origin': s_origin,
            'qr': s_qr,
        })

        i_tea_count += 1
        break

env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
template = env.get_template('template.svg.tpl')

with open('labels.svg', 'w', encoding='UTF-8') as f_output:
    f_output.write(template.render(labels=labels))
