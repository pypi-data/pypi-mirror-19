"""
The MIT License (MIT)

Copyright (c) 2016 WavyCloud

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import logging
import os
import sys
import re
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup

logging.getLogger().setLevel(logging.INFO)


def get_param_description(params_soup):
    result = ''.join(params_soup.findAll(text=True)).replace('\n\n', '\n')
    i = result.find(' --')
    if i < 0:
        return ''
    else:
        return result[i + 4:].replace('  ', ' ')


def get_params_soup(method_soup):
    fields_block = method_soup.find('dl', class_='docutils field-list')
    if not fields_block or not fields_block.find(string='Parameters'):
        return

    return fields_block.find('dd', class_='field-body')

def get_request_syntax(method_soup):
    highlights = method_soup.findAll("div", {"class":"highlight-python"})
    if highlights:
        return highlights[0].text
    else:
        return ''

def get_description(method_soup):
    description = ""
    for desc in method_soup.contents[3].findAll('p', recursive=False):
        description += desc.text + os.linesep
    description = re.sub('Request Syntax', '', description, re.IGNORECASE)
    description = re.sub('Usage', '', description, re.IGNORECASE)
    return description

def get_return_type(method_soup):
    match = re.search('Return type(.*)', method_soup.text, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return ""

def get_response_syntax(method_soup):
    highlights = method_soup.findAll("div", {"class": "highlight-python"})
    if len(highlights) > 1:
        return highlights[1].text
    else:
        return ''


def get_response_structure(method_soup):
    highlights = method_soup.findAll("ul", {"class": "simple"})
    if len(highlights) > 1:
        return highlights[1].text
    else:
        return ''

def iter_params(method_soup):
    params_soup = get_params_soup(method_soup)
    if not params_soup:
        return
    if params_soup.find('strong', recursive=False):
        description = get_param_description(params_soup)
        yield params_soup.strong.text, params_soup.em.text, description
    else:
        for li in params_soup.find('ul').find_all('li', recursive=False):
            description = get_param_description(li)
            yield li.strong.text, li.em.text, description


def iter_methods(soup):
    methods_set = set()
    for method_html in soup.find_all('dl', class_='method'):
        method_name = method_html.find('tt', class_='descname').text
        if method_name in methods_set:
            continue
        methods_set.add(method_name)
        yield method_name, method_html


def iter_method_params(soup):
    for method, method_soup in iter_methods(soup.find(id='client')):
        param_dict = OrderedDict((param, (type, description)) for param, type, description in iter_params(method_soup))
        request_syntax = get_request_syntax(method_soup)
        description = get_description(method_soup)
        return_type = get_return_type(method_soup)
        response_syntax = get_response_syntax(method_soup)
        response_structure = get_response_structure(method_soup)
        yield method, \
              param_dict, \
              re.sub(r'[^\x00-\x7F]+', '', description), \
              re.sub(r'[^\x00-\x7F]+', '', request_syntax), \
              re.sub(r'[^\x00-\x7F]+', '', return_type), \
              re.sub(r'[^\x00-\x7F]+', '', response_syntax), \
              re.sub(r'[^\x00-\x7F]+', '', response_structure)


def iter_method_params_description(soup):
    for method, method_soup in iter_methods(soup.find(id='client')):
        param_dict = OrderedDict((param, type) for param, type, description in iter_params(method_soup))
        yield method, param_dict


def to_python_type(param_type):
    return param_type


def iter_all_services(services_url='https://boto3.readthedocs.io/en/latest/reference/services/'):
    soup = BeautifulSoup(requests.get(services_url)._content, 'html.parser')
    for x in soup.find_all(class_='toctree-wrapper compound'):
        for li in x.find_all('li', class_='toctree-l1'):
            yield li.a.text, '{}{}'.format(services_url, li.a.attrs['href'])


def generate_service_code(url, dist_filepath):
    soup = BeautifulSoup(requests.get(url)._content, 'html.parser')
    import codecs
    with codecs.open(dist_filepath, 'w+', encoding='utf-8') as f:
        for line in iter_code_lines(soup):
            f.write('{}\n'.format(re.sub(r'[^\x00-\x7F]+', ' ', line)))

    return get_class_name(soup)


def get_init_path():
    return os.path.join(os.path.dirname(__file__), '__init__.py')


def append_class_to_init(service_name, class_name):
    with open(get_init_path(), 'a') as f:
        line = 'from pyboto3.{} import {}\n'.format(service_name, class_name)
        f.write(line)


def get_filename(service_name):
    filename = service_name.lower()
    if filename == 'lambda':
        filename = 'lambda_'
    return filename


def generate_all_services_code(dir_path):
    open(get_init_path(), 'w+').close()
    for service_name, url in iter_all_services():
        filename = get_filename(service_name)
        dist_filepath = os.path.join(dir_path, '{}.py'.format(filename))
        logging.info("Generating code for service {} to {}".format(service_name, dist_filepath))
        generate_service_code(url, dist_filepath)
        logging.info("Code for service {} generated successfully to {}".format(service_name, dist_filepath))


def get_method_description(method_soup):
    return method_soup.dd.p.text


def clean_param_description(param_description, indent=3):
    result = param_description.encode('utf-8')
    result = result.replace('"', "'")
    result = result.replace('\n\n', '\n')
    # indent params
    result = result.replace('\n', '\n' + ' ' * 4 * indent)
    return result


def clean_class_name(name):
    return re.sub('[^a-zA-Z0-9]', '', name).capitalize()


def get_class_name(service_soup):
    """
    :
    :param service_soup:
    :return:
    :returns
    """
    return clean_class_name(service_soup.find(class_='highlight').find(class_='s1').text.strip("'"))


def iter_code_lines(soup):
    '''

    :param soup:
    :return:
    '''
    yield "'''"
    yield globals()['__doc__']
    yield "'''"
    yield ""
    for method_name, params, description, request_syntax, return_type, response_syntax, response_structure in iter_method_params(soup):
        yield 'def {}({}{}):'.format(method_name, '=None, '.join(params.keys()),
                                               '=None' if params else '')
        yield '    """'
        yield '    {}'.format(description.encode('utf-8').replace('\n', '\n    '))
        if request_syntax:
            yield '    :example: {}'.format(request_syntax.replace('\n', '\n    '))
        for param, (param_type, param_description) in params.iteritems():
            param_description = clean_param_description(param_description)
            yield '    :type {}: {}'.format(param, to_python_type(param_type))
            yield '    :param {}: {}'.format(param, param_description)
            yield ''
        if return_type:
            yield '    :rtype: {}'.format(to_python_type(return_type))
        if response_syntax:
            yield '    :return: {}'.format(response_syntax.replace('\n', '\n    '))
        if response_structure:
            yield '    :returns: {}'.format(response_structure.replace('\n', '\n    '))
        yield '    """'
        yield "    pass"
        yield ""

if __name__ == '__main__':
    generate_all_services_code(os.path.dirname(__file__))