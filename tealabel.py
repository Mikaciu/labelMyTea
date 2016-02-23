#!/usr/bin/env python3
import base64
import io
import os.path
import xml.dom.minidom

import qrcode
import urllib3
from jinja2 import Environment, FileSystemLoader

elements = [i for i in range(3)]
labels = []


class TeaLabel:
    base_x = 10
    base_y = 10
    box_dimensions = [60, 75]
    box_margins = [5, 5]

    def __init__(self):
        self.current_x = 0
        self.current_y = 0
        self.env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
        self.template = self.env.get_template('template_v2.svg')

    def write_to_page(self, i_page_number, l_labels):
        with open('labels{}.svg'.format(i_page_number), 'w', encoding='UTF-8') as f_output:
            f_output.write(self.template.render(
                    labels=l_labels,
                    doc_height=(self.current_y + TeaLabel.box_dimensions[1] + TeaLabel.box_margins[1]))
            )

    def load_data(self, b_use_proxy=False, b_use_file=False):
        if b_use_file:
            with open("the_2.xml", "r") as f_data:
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
        return data_source_xml

    def process(self):
        with xml.dom.minidom.parseString(self.load_data(b_use_proxy=False, b_use_file=False)) as data_source_dom:
            labels = []
            i_tea_count = 0
            i_page_number = 1
            for o_current_tea in data_source_dom.getElementsByTagName("tea"):
                # flush page
                if (i_tea_count % 9) == 0 and i_tea_count > 0:
                    self.write_to_page(i_page_number, labels)
                    labels = []
                    i_page_number += 1
                    # reset y coordinate
                    self.current_y = 0

                s_temp = s_duration = ''

                s_name = o_current_tea.getAttribute('name')

                dom_shop = o_current_tea.getElementsByTagName('shop')[0]
                s_origin = dom_shop.getAttribute('name')
                s_url = dom_shop.getAttribute('url')

                dom_kind = o_current_tea.getElementsByTagName('kind')[0]
                s_kind = dom_kind.getAttribute('code')
                s_type = dom_kind.getAttribute('name')

                dom_temp = o_current_tea.getElementsByTagName('temp')
                if len(dom_temp) > 0:
                    s_temp = dom_temp[0].getAttribute('value')
                if s_temp != '':
                    s_temp = '{}°'.format(s_temp)

                dom_duration = o_current_tea.getElementsByTagName('duration')
                if len(dom_duration) > 0:
                    s_duration = dom_duration[0].getAttribute('value')
                if s_duration != '':
                    s_duration = '{}\''.format(s_duration)

                # positioning
                if (i_tea_count % 3) == 0:
                    self.current_x = TeaLabel.base_x

                    if self.current_y > 0:
                        self.current_y += TeaLabel.box_dimensions[1] + TeaLabel.box_margins[1]
                    else:
                        self.current_y = TeaLabel.base_y
                else:
                    self.current_x += TeaLabel.box_dimensions[0] + TeaLabel.box_margins[0]

                s_src = ''
                if s_url != '':
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

                    s_src = 'data:image/png;base64,%s' % base64.b64encode(boutput2.getvalue()).decode().replace('\n',
                                                                                                                '')

                l_ingredients = []
                dom_ingredientlist = o_current_tea.getElementsByTagName("ingredientlist")
                if len(dom_ingredientlist) > 0:
                    l_ingredients = [i.getAttribute('name') for i in
                                     dom_ingredientlist[0].getElementsByTagName(
                                             'ingredient')]

                s_ingredients = ', '.join(l_ingredients)

                labels.append({
                    'x': self.current_x,
                    'y': self.current_y,
                    'name': s_name,
                    'type': s_type,
                    'kind': s_kind,
                    'origin': s_origin,
                    'qr_src': s_src,
                    'ingredients': s_ingredients,
                    'temp': s_temp,
                    'duration': s_duration,
                })

                i_tea_count += 1

        # last page
        self.write_to_page(i_page_number, labels)


o_tea_label_maker = TeaLabel()
o_tea_label_maker.process()
