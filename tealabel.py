#!/usr/bin/env python3
import urllib3
import xml.dom.minidom
from jinja2 import Environment, FileSystemLoader
import os.path
import io
import re
import pyqrcode
import qrcode
import base64


box_dimensions = [60, 75]
box_margins = [5, 5]

base_x = 10
base_y = 10
current_x = 0
current_y = 0

elements = [i for i in range(3)]
labels = []

b_use_proxy = True
b_use_file = True

if b_use_file:
    with open ("the_2.xml", "r") as f_data:
        data_source_xml = ' '.join(line.replace('\n', '') for line in f_data)
else:
    data_source_xml = ''
    if b_use_proxy:
        http = urllib3.ProxyManager('http://localhost:3128/')
    else:
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

        s_end_page = ""
        if (i_tea_count % 9) == 8:
            s_end_page = "</page><page>"
            
        qr2 = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=10,
            border=0,
        )
        qr2.add_data(s_url)
        qr2.make(fit=True)
        boutput2 = io.BytesIO()
        qr2.make_image().save(boutput2)

        s_src= 'data:image/png;base64,%s' % base64.b64encode(boutput2.getvalue()).decode().replace('\n', '')


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
            'qr_src' : s_src,
            'endpage' : s_end_page,
        })

        i_tea_count += 1
        # if i_tea_count > 9:
            # break

# TODO multiple files (SVG does not manage multi pages yet)
env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
template = env.get_template('template.svg.tpl')

with open('labels.svg', 'w', encoding='UTF-8') as f_output:
    f_output.write(template.render(
        labels=labels, 
        doc_height=(current_y + box_dimensions[1] + box_margins[1]))
    )
