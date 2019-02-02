#!/usr/bin/env python3
import base64
import io
import re
import os.path
import xml.dom.minidom

import argparse
import certifi
import qrcode
import urllib3
from jinja2 import Environment, FileSystemLoader


class TeaLabel:
    base_x = 3
    base_y = 3
    box_dimensions = [60, 60]
    box_margins = [5, 5]
    i_labels_per_line = 3
    i_labels_per_page = 12

    def __init__(self):
        self.current_x = 0
        self.current_y = 0

        self.parameters = {}
        self.handle_arguments()
        # Init Jinja2 template
        self.env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
        self.template = self.env.get_template(self.parameters['template_file'])

    def handle_arguments(self):
        arg_parser = argparse.ArgumentParser(description='Generates tea labels in svg format')

        local_or_download_group = arg_parser.add_mutually_exclusive_group(required=True)
        local_or_download_group.add_argument('--source-file', help='The path to the XML file to use as source')
        local_or_download_group.add_argument('--download-url', help='The url from which to download the XML file')

        arg_parser.add_argument('--proxy', required=False, default='')
        arg_parser.add_argument('--template-file', required=False, default='template_v2.svg')
        arg_parser.add_argument('--generated-file-name', required=False, default='labels.svg')

        self.parameters = vars(arg_parser.parse_args())

    def write_to_page(self, i_page_number, l_labels):
        with open('labels{}.svg'.format(i_page_number), 'w', encoding='UTF-8') as f_output:
            f_output.write(self.template.render(
                labels=l_labels,
                doc_height=(self.current_y + TeaLabel.box_dimensions[1] + TeaLabel.box_margins[1]))
            )

    def load_data(self):
        if 'source_file' in self.parameters and self.parameters['source_file'] is not None:
            with open(self.parameters['source_file'], "r") as f_data:
                data_source_xml = ' '.join(line.replace('\n', '') for line in f_data)
        else:
            if self.parameters['proxy'] != '':
                http = urllib3.ProxyManager(self.parameters['proxy'])
            else:
                http = urllib3.PoolManager(
                    cert_reqs='CERT_REQUIRED',
                    ca_certs=certifi.where()
                )

            data_source_request = http.request('GET', self.parameters['download_url'])
            if data_source_request.status != 200:
                print(data_source_request.status)
                sys.exit(1)

            data_source_xml = data_source_request.data.decode('utf-8')
        return data_source_xml

    def process(self):
        with xml.dom.minidom.parseString(self.load_data()) as data_source_dom:
            labels = []
            i_tea_count = 0
            i_page_number = 1
            for o_current_tea in data_source_dom.getElementsByTagName("tea"):
                # flush page
                if (i_tea_count % TeaLabel.i_labels_per_page) == 0 and i_tea_count > 0:
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
                if (i_tea_count % TeaLabel.i_labels_per_line) == 0:
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


if __name__ == '__main__':
    o_tea_label_maker = TeaLabel()
    o_tea_label_maker.process()
