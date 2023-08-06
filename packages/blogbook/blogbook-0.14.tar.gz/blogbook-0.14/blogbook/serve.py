# -*- coding: utf-8 -*-
import configparser
import http.server
import json
import os
import posixpath
import urllib.parse
from http import HTTPStatus

import click
import sys

import io

import mistune
import re
from jinja2 import Environment, FileSystemLoader
from PIL import Image

import blogbook.constant
import blogbook.toolbox.collection


class LogbookHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    http.server.SimpleHTTPRequestHandler.extensions_map.update({'': 'text/html'})

    def do_POST(self):

        if list(urllib.parse.urlparse(self.path))[2] == '/images':

            """Serve a POST request."""
            r, info = self.deal_post_data()
            print((r, info, "by: ", self.client_address))
            f = io.BytesIO()
            f.write(info.encode())
            length = f.tell()
            f.seek(0)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(length))
            self.end_headers()
            if f:
                self.copyfile(f, self.wfile)
                f.close()
        else:

            url_parts = list(urllib.parse.urlparse(self.path))

            # abandon query parameters
            path = url_parts[2]
            try:
                path = urllib.parse.unquote(path, errors='surrogatepass')
            except UnicodeDecodeError:
                path = urllib.parse.unquote(path)
            path = posixpath.normpath(path)
            words = path.split('/')
            words = filter(None, words)
            path = self.home
            for word in words:
                if os.path.dirname(word) or word in (os.curdir, os.pardir):
                    # Ignore components that are not a simple file/directory name
                    continue
                path = os.path.join(path, word)

            filename = os.path.basename(path) + '.md'
            parent_path = blogbook.toolbox.file.parentdir(path)
            for file in os.listdir(parent_path):
                file_path = os.path.join(parent_path, file)
                if os.path.isfile(file_path) and file.endswith(filename):
                    path = file_path
                    break

            context = {'page': blogbook.build.process.pre_process_dynamic(
                path, os.path.basename(path), self.base_path, self.setting, self.markdown, self.home
            )}

            # Doesn't do anything with posted data
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = json.loads(str(self.rfile.read(content_length), 'utf-8'))  # <--- Gets the data itself

            configuration = configparser.ConfigParser()

            if os.path.isfile(path):

                with open(context['page']['content']['path'], 'r') as source_stream:

                    line = source_stream.readline()
                    while line and not line.strip():
                        line = source_stream.readline()

                    if line.strip() == '---':

                        meta = ''

                        line = source_stream.readline()
                        while line and not line.strip() == '---':
                            meta += line
                            line = source_stream.readline()

                        configuration.read_string(meta)

                        # line = source_stream.readline()
                        # while line and not line.strip():
                        #     line = source_stream.readline()

            page_diff = blogbook.toolbox.collection.DictDiffer(post_data['page'], context['page'])

            if not configuration.has_section('page'):
                configuration.add_section('page')
            for added in page_diff.added():
                configuration.set('page', added, post_data['page'][added])
            for removed in page_diff.removed():
                configuration.remove_option('page', removed)
            for changed in page_diff.changed():
                configuration.set('page', changed, post_data['page'][changed])

            with open(path, 'w') as stream:
                if configuration['page']:
                    stream.write('---\n')
                    configuration.write(stream)
                    stream.write('---\n')
                stream.write(post_data['content'])

            f = io.BytesIO()
            f.write('Update'.encode())
            length = f.tell()
            f.seek(0)
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(length))
            self.end_headers()
            if f:
                self.copyfile(f, self.wfile)
                f.close()

    def deal_post_data(self):

        content_type = self.headers['content-type']
        if not content_type:
            return False, "Content-Type header doesn't contain boundary"
        boundary = content_type.split("=")[1].encode()
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return False, "Content NOT begin with boundary"
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())
        if not fn:
            return False, "Can't find out file name..."

        url_parts = list(urllib.parse.urlparse(self.path))
        path = url_parts[2]
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = self.home
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)
        fn = os.path.join(path, fn[0])

        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)

        bio = io.BytesIO()

        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith(b'\r'):
                    preline = preline[0:-1]

                bio.write(preline)

                im = Image.open(bio)
                im.thumbnail((1440, 900), Image.ANTIALIAS)
                try:
                    im.save(fn, optimize=True, quality=75)
                except IOError:
                    return False, "Can't create file to write, do you have permission to write?"

                bio.close()
                im.close()

                return True, "File '%s' upload success!" % fn
            else:
                bio.write(preline)
                preline = line
        return False, "Unexpect Ends of data."

    def send_head(self):

        url_parts = list(urllib.parse.urlparse(self.path))
        query = dict(urllib.parse.parse_qsl(url_parts[4]))

        if url_parts[2] == '/images':

            r = self.environment.get_template('image.html').render({})

            enc = sys.getfilesystemencoding()
            encoded = r.encode(enc, 'surrogateescape')

            f = io.BytesIO()
            f.write(encoded)
            f.seek(0)

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html; charset=%s" % enc)
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()

            return f

        elif query.get('edit', False) and '.' not in url_parts[2]:

            # abandon query parameters
            path = url_parts[2]
            try:
                path = urllib.parse.unquote(path, errors='surrogatepass')
            except UnicodeDecodeError:
                path = urllib.parse.unquote(path)
            path = posixpath.normpath(path)
            words = path.split('/')
            words = filter(None, words)
            path = self.home
            for word in words:
                if os.path.dirname(word) or word in (os.curdir, os.pardir):
                    # Ignore components that are not a simple file/directory name
                    continue
                path = os.path.join(path, word)

            filename = os.path.basename(path) + '.md'
            parent_path = blogbook.toolbox.file.parentdir(path)
            for file in os.listdir(parent_path):
                file_path = os.path.join(parent_path, file)
                if os.path.isfile(file_path) and file.endswith(filename):
                    path = file_path
                    break

            context = {'page': blogbook.build.process.pre_process_dynamic(
                path, os.path.basename(path), self.base_path, self.setting, self.markdown, self.home
            )}

            if os.path.isfile(path):
                with open(context['page']['content']['path'], 'r') as source_stream:
                    source_stream.seek(context['page']['content']['position'])
                    context['content'] = source_stream.read()

            r = self.environment.get_template('page.html').render(context)

            enc = sys.getfilesystemencoding()
            encoded = r.encode(enc, 'surrogateescape')

            f = io.BytesIO()
            f.write(encoded)
            f.seek(0)

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html; charset=%s" % enc)
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()

            return f

        else:
            return http.server.SimpleHTTPRequestHandler.send_head(self)

    def translate_path(self, path):

        # abandon query parameters
        path = list(urllib.parse.urlparse(self.path))[2]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = self.base_path
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'

        if os.path.isdir(path):
            for ext in '', '.html', '.htm':
                index = '{}/index{}'.format(path, ext)
                if os.path.isfile(index):
                    return index
            self.send_error(404)

        return path


class LogbookHTTPServer(http.server.HTTPServer):
    def __init__(self, home, base_path, host_name, port, setting, *args, **kwargs):
        http.server.HTTPServer.__init__(self, (host_name, port), LogbookHTTPRequestHandler, *args, **kwargs)
        self.RequestHandlerClass.base_path = base_path
        self.RequestHandlerClass.home = home
        self.RequestHandlerClass.setting = setting
        self.RequestHandlerClass.markdown = mistune.Markdown()
        self.RequestHandlerClass.environment = Environment(loader=FileSystemLoader(blogbook.constant.DEV_EDITOR_PATH))


def run_server(home, root, port, setting):
    httpd = LogbookHTTPServer(home, root, 'localhost', port, setting)

    click.echo('Serving path : "{}" at [http://localhost:{}]'.format(root, port))
    click.echo('Press <Ctrl-C> to exit.'.format(root, port))
    httpd.serve_forever()
