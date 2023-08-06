# -*- coding: utf-8 -*-
import configparser
import datetime
import os
import shutil
import urllib.request
from html.parser import HTMLParser

import click
from jinja2 import TemplateNotFound

import blogbook.constant
import blogbook.toolbox.file


class HtmlStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def error(self, message):
        pass

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def pre_process_dynamic(file_path, filename, output_dir, setting, markdown, base_path):
    relative_path = os.path.relpath(blogbook.toolbox.file.parentdir(file_path), base_path)
    base_url = blogbook.constant.URL_SEPARATOR
    if relative_path != os.path.curdir:
        base_url += urllib.request.pathname2url(relative_path) + blogbook.constant.URL_SEPARATOR

    # filename_pattern = blogbook.constant.FILENAME_REGEX.match(filename)
    # output_name = filename_pattern.group(5)
    name = filename.replace('.md', '')

    page = {
        'title': name.capitalize(),
        'url': base_url + name,
        'layout': setting['blog']['default_layout'],
        'content': {
            'path': file_path,
            'position': 0,
            'output_dir': output_dir,
            'output_path': os.path.join(output_dir, name)
        }
    }
    # if filename_pattern.group(2) and filename_pattern.group(3) and filename_pattern.group(4):
    #     year = int(filename_pattern.group(2))
    #     month = int(filename_pattern.group(3))
    #     day = int(filename_pattern.group(4))
    #     page['date'] = datetime.date(year, month, day)

    if os.path.isfile(file_path):

        with open(file_path, 'r') as stream:

            content_position = int(stream.tell())

            line = stream.readline()
            while line and not line.strip():
                content_position = int(stream.tell())
                line = stream.readline()

            if line.strip() == '---':

                meta = ''

                line = stream.readline()
                while line and not line.strip() == '---':
                    meta += line
                    line = stream.readline()
                    content_position = int(stream.tell())

                if not line.strip() == '---':
                    raise click.UsageError('Meta section open but never close on content file [{}]'.format(filename))

                configuration = configparser.ConfigParser()
                configuration.read_string(meta)
                if configuration.has_section('page'):
                    page.update(configuration['page'])

                line = stream.readline()
                while line and not line.strip():
                    content_position = int(stream.tell())
                    line = stream.readline()

            if 'excerpt' not in page:

                excerpt = line

                line = stream.readline()
                while line and not line == setting['excerpt']['separator']:
                    excerpt += line
                    line = stream.readline()

                if excerpt and excerpt.strip():

                    stripper = HtmlStripper()
                    stripper.feed(markdown(excerpt))
                    page['excerpt'] = stripper.get_data()

                    excerpt_words = page['excerpt'].split()
                    if len(excerpt_words) > setting['excerpt']['max_word']:
                        page['excerpt'] = ' '.join(excerpt_words[:setting['excerpt']['max_word']]) + '...'

        page['content']['position'] = content_position

    return page


def process_static(file_path, output_dir):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    shutil.copy(file_path, output_dir)


def pre_process(path, output_dir, context, markdown, base_content_path=None):
    """
    Scan source directory in order to :
        - Copy any file other than content file (*.md) into destination directory.
        - Parse content file to populate site dictionary context.
    """
    base_content_path = base_content_path if base_content_path else path

    for entry in os.scandir(path):

        if not any(
            content_exclude_pattern.match(entry.name) is not None
            for content_exclude_pattern in context['setting']['path']['content_exclude_patterns']
        ):

            if entry.is_dir():
                pre_process(
                    entry.path,
                    os.path.join(output_dir, entry.name),
                    context,
                    markdown,
                    base_content_path
                )

            elif entry.is_file():

                if entry.name.lower().endswith(blogbook.constant.MARKDOWN_EXT):

                    page = pre_process_dynamic(
                        entry.path, entry.name, output_dir, context['setting'], markdown, base_content_path
                    )

                    layout_group = page['layout'] + 's'
                    if layout_group in context['site']:
                        context['site'][layout_group].append(page)
                    else:
                        context['site'][layout_group] = [page]

                else:
                    process_static(entry.path, output_dir)


def post_process_dynamic(page, context, markdown, environment):
    """
    Scan site dictionary context in order to generate static html page
    base on site setting, template and page content.
    """

    output_dir = page['content']['output_dir']
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(page['content']['output_path'], 'w') as output_stream:

        context['page'] = page

        if 'path' in page['content']:
            with open(page['content']['path'], 'r') as source_stream:
                source_stream.seek(page['content']['position'])
                context['content'] = markdown(source_stream.read())

        try:
            output_stream.write(
                environment.get_template(page['layout'] + blogbook.constant.LAYOUT_EXT).render(context)
            )
        except TemplateNotFound as ex:
            raise click.UsageError('Missing required layout : {}'.format(ex.message))

        context.pop('content', None)
