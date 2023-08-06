# -*- coding: utf-8 -*-
import configparser
import getpass
import os
import re
import shutil
import sys
import zipfile

import click
import mistune
import paramiko
from PIL import Image
from jinja2 import Environment, FileSystemLoader
from dulwich import porcelain
from dulwich.repo import Repo

import blogbook.build.process
import blogbook.build.watch
import blogbook.constant
import blogbook.repo.push
import blogbook.serve
import blogbook.toolbox.file


class Blogbook(object):
    def __init__(self, home):
        self.home = home
        self.verbose = False
        self.setting = {
            'path': {
                'content_exclude_patterns': ['_*', '.*'],
                'layouts': os.path.join(home, blogbook.constant.LAYOUTS_DIRECTORY),
                'output': os.path.join(home, blogbook.constant.DEFAULT_OUTPUT)
            },
            'blog': {
                'default_layout': 'post',
                'language': 'en',
                'name': os.path.basename(home).capitalize(),
            },
            'excerpt': {
                'separator': '\n',
                'max_word': 20
            },
            'author': {
                'name': getpass.getuser()
            }
        }

        self.setting_path = os.path.join(home, blogbook.constant.LOGBOOK_DIRECTORY, 'config')
        if os.path.isfile(self.setting_path):
            configuration = configparser.ConfigParser()
            configuration.read(self.setting_path)
            self.setting.update(configuration._sections)

        self.setting['path']['content_exclude_patterns'] = [
            re.compile(content_exclude_pattern.replace('.', '\.').replace('*', '.*'))
            for content_exclude_pattern in self.setting['path']['content_exclude_patterns']
        ]

    def set_config(self, key, value):
        self.setting[key] = value
        if self.verbose:
            click.echo('  config[%s] = %s'.format(key, value), file=sys.stderr)

    def __repr__(self):
        return '<Blogbook {}>'.format(self.home)


pass_blog = click.make_pass_decorator(Blogbook)


@click.group()
@click.option(
    '--home',
    '-h',
    default=os.getcwd()
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Enables verbose mode.'
)
@click.version_option()
@click.pass_context
def main(context, home, verbose):
    """Repo is a command line tool that showcases how to build complex
    command line interfaces with Click.
    This tool is supposed to look like a distributed version control
    system to show how something like this can be structured.
    """
    context.obj = Blogbook(os.path.abspath(home))
    context.obj.verbose = verbose


@main.command()
@click.option(
    '--set',
    nargs=2,
    metavar='KEY VALUE',
    help='Overwrite a config key/value pair.'
)
@click.option(
    '--unset',
    metavar='KEY',
    help='Remove a config key and is value.'
)
@pass_blog
def config(blog, set, unset):
    """
    Configure a new blogbook.
    """

    if not os.path.isdir(os.path.join(blog.home, blogbook.constant.LOGBOOK_DIRECTORY)):
        raise click.UsageError('Not a blogbook directory : {}'.format(blog.home))

    configuration = configparser.ConfigParser()
    if os.path.isfile(blog.setting_path):
        configuration.read(blog.setting_path)

    if set:
        section, option = set[0].split('.', 1)
        if not configuration.has_section(section):
            configuration.add_section(section)
        configuration.set(section, option, set[1])
        with open(blog.setting_path, 'w') as stream:
            configuration.write(stream)
    if unset:
        section, option = unset.split('.', 1)
        if configuration.has_section(section):
            configuration.remove_option(section, option)
            if not configuration[section]:
                configuration.remove_section(section)
        with open(blog.setting_path, 'w') as stream:
            configuration.write(stream)


@main.command()
@click.option(
    '-f', '--force',
    is_flag=True,
    help='Force override existing directory'
)
@click.option(
    '-l', '--layout',
    default=os.path.join(blogbook.constant.BUILTIN_LAYOUT_PATH, 'default'),
    metavar='PATH',
    help='The blogbook template path.'
)
@pass_blog
def new(blog, force, layout):
    """
    Create a new blogbook.
    """

    if os.path.isdir(blog.home) and not blogbook.toolbox.file.is_empty(blog.home) and not force:
        raise click.UsageError(
            blog.home + ' already exist and is not an empty directory, '
            + 'either user an other directory or use the --force flag.'
        )

    if not os.path.isdir(layout) and not zipfile.is_zipfile(layout):
        raise click.BadParameter('You must provide either an existing layout directory or zip file')

    click.echo('Create new blogbook into [{}]'.format(blog.home))
    if not os.path.isdir(blog.home):
        os.makedirs(blog.home, exist_ok=True)

    logbook_work_path = os.path.join(blog.home, blogbook.constant.LOGBOOK_DIRECTORY)
    blogbook.toolbox.file.force_mkdir(logbook_work_path)
    with open(os.path.join(logbook_work_path, 'version'), 'w') as stream_logbook:
        stream_logbook.write('0')

    git_dir = os.path.join(blog.home, '.git')
    if os.path.isdir(git_dir):
        shutil.rmtree(git_dir)
    porcelain.init(blog.home)

    click.echo('with layouts [{}]'.format(os.path.basename(layout)))
    layouts_path = blog.setting['path']['layouts']
    if os.path.isdir(layouts_path):
        shutil.rmtree(layouts_path)

    if os.path.isdir(layout):
        shutil.copytree(layout, layouts_path)
    elif zipfile.is_zipfile(layout):
        with zipfile.ZipFile(layout) as zf:
            zf.extractall(layouts_path)


@main.command()
@click.option(
    '-w', '--watch',
    is_flag=True,
    help='Build on change and run server.'
)
@pass_blog
def build(blog, watch):
    """
    Build a blogbook from his template.
    """

    output = blog.setting['path']['output']
    layouts = blog.setting['path']['layouts']

    if not os.path.isdir(layouts) or blogbook.toolbox.file.is_empty(layouts):
        raise click.UsageError('Missing layout into ' + layouts)

    blogbook.toolbox.file.force_mkdir(output)

    assets_path = os.path.join(layouts, blogbook.constant.ASSETS_DIRECTORY)
    if os.path.isdir(assets_path) and not blogbook.toolbox.file.is_empty(assets_path):
        shutil.copytree(assets_path, os.path.join(output, blogbook.constant.ASSETS_DIRECTORY))

    context = {
        'setting': blog.setting,
        'site': {}
    }
    markdown = mistune.Markdown()

    blogbook.build.process.pre_process(blog.home, output, context, markdown)

    def get_key(site_page):
        return site_page.get('date') or '0001-01-01', site_page['title']

    for group, pages in context['site'].items():
        context['site'][group] = sorted(pages, reverse=True, key=get_key)

    environment = Environment(loader=FileSystemLoader(layouts))
    for pages in context['site'].values():
        for page in pages:
            blogbook.build.process.post_process_dynamic(page, context, markdown, environment)

    if watch:
        watcher = blogbook.build.watch.LogbookContentWatcher(blog.home, output, context, markdown, environment)
        try:
            blogbook.serve.run_server(blog.home, output, 1234, blog.setting)
        except KeyboardInterrupt:
            watcher.stop()


@main.command()
@click.option(
    '-p', '--port',
    default=1234,
    metavar='PORT',
    help='Port on which binding the server.'
)
@pass_blog
def serve(blog, port):
    """
    Serve a blogbook generated content for test purpose only.
    """
    blogbook.serve.run_server(blog.home, blog.setting['path']['output'], port, blog.setting)


@main.command()
@pass_blog
def push(blog):
    """
    Serve a blogbook generated content for test purpose only.
    """

    # if 'remote' not in blog.setting or 'host' not in blog.setting['remote']:
    #     raise click.UsageError('Missing remote host setting')

    r = Repo(blog.home)
    porcelain.add(r)

    s = porcelain.status(r)
    if any(c for c in s.staged.values()):

        porcelain.commit(r, b'Commit/Push blog', committer=b'Tui <tui@tui.ca>')
        # porcelain.pus

    # client = paramiko.SSHClient()
    # client.load_host_keys(blogbook.constant.SSH_HOST_KEYS)
    # client.set_missing_host_key_policy(blogbook.repo.push.ConfirmAddPolicy())
    #
    # client.connect(blog.setting['remote']['host'])
    #
    # remote_root = '/var/www/blogbook/' + os.path.basename(blog.home)
    # client.exec_command('rm -rf {}'.format(remote_root))
    # client.exec_command('mkdir -p {}'.format(remote_root))
    #
    # sftp = client.open_sftp()
    # for local_root, dir_names, file_names in os.walk(blog.home):
    #
    #     current_remote_root = remote_root
    #     relative_path = os.path.relpath(local_root, blog.home)
    #     if relative_path != os.curdir:
    #         current_remote_root += '/' + relative_path.replace('\\', '/')
    #
    #     for file_name in file_names:
    #         local_file_path = os.path.join(local_root, file_name)
    #         remote_file_path = current_remote_root + '/' + file_name
    #         click.echo('{} --> {}'.format(local_file_path, remote_file_path))
    #         sftp.put(local_file_path, remote_file_path)
    #     for dir_name in dir_names:
    #         remote_dir_path = current_remote_root + '/' + dir_name
    #         click.echo('{} --> {}'.format(os.path.join(local_root, dir_name), remote_dir_path))
    #         sftp.mkdir(remote_dir_path)
    #
    # client.close()


@main.command()
@click.argument('source')
@click.argument('destination')
@pass_blog
def add(blog, source, destination):
    if os.path.isfile(source) and source.lower().endswith('.jpg'):
        im = Image.open(source)
        im.thumbnail((800, 1200), Image.ANTIALIAS)
        im.save(os.path.join(blog.home, destination), optimize=True, quality=75)


if __name__ == "__main__":
    main()
