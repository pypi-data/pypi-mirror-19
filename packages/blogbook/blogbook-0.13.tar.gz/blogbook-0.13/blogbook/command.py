# -*- coding: utf-8 -*-
import configparser
import getpass
import os
import posixpath
import re
import shutil
import sys
import zipfile

import click
import dulwich.client
import mistune
import paramiko
from PIL import Image
from dulwich import porcelain
from jinja2 import Environment, FileSystemLoader

import blogbook.build.process
import blogbook.build.watch
import blogbook.constant
import blogbook.repo.push
import blogbook.serve
import blogbook.toolbox.file
from blogbook.push.repo import CustomRepo


class Blogbook(object):
    def __init__(self, work_dir, blogbook_dir):

        self.work_dir = os.path.abspath(work_dir)
        if blogbook_dir:
            self.blogbook_dir = os.path.abspath(blogbook_dir)
        else:
            self.blogbook_dir = os.path.join(self.work_dir, blogbook.constant.LOGBOOK_DIRECTORY)

        self.layouts_dir = os.path.join(self.work_dir, blogbook.constant.LAYOUTS_DIRECTORY)

        self.remotes = {}
        self.remotes_config_path = os.path.join(self.blogbook_dir, 'remotes')
        if os.path.isfile(self.remotes_config_path):
            configuration = configparser.ConfigParser()
            configuration.read(self.remotes_config_path)
            self.remotes = configuration._sections

        self.output_config_path = os.path.join(self.blogbook_dir, 'output')
        if os.path.isfile(self.output_config_path):
            with open(self.output_config_path, 'r') as stream:
                self.output_dir = stream.read()
        else:
            self.output_dir = os.path.join(self.work_dir, blogbook.constant.DEFAULT_OUTPUT)

        self.verbose = False
        self.setting = {
            'blog': {
                'default_layout': 'post',
                'language': 'en',
                'name': os.path.basename(self.work_dir).capitalize(),
            },
            'author': {
                'name': getpass.getuser()
            },
            'content': {
                'exclude_patterns': ['_*', '.*']
            },
            'excerpt': {
                'separator': '\n',
                'max_word': 20
            }
        }

        self.setting_path = os.path.join(self.layouts_dir, 'config')
        if os.path.isfile(self.setting_path):
            configuration = configparser.ConfigParser()
            configuration.read(self.setting_path)
            self.setting.update(configuration._sections)

        self.setting['content']['exclude_patterns'] = [
            re.compile(content_exclude_pattern.replace('.', '\.').replace('*', '.*'))
            for content_exclude_pattern in self.setting['content']['exclude_patterns']
        ]

    def set_config(self, key, value):
        self.setting[key] = value
        if self.verbose:
            click.echo('  config[%s] = %s'.format(key, value), file=sys.stderr)

    def __repr__(self):
        return '<Blogbook {}>'.format(self.work_dir)


pass_blog = click.make_pass_decorator(Blogbook)


@click.group()
@click.option(
    '--work_dir',
    default=os.getcwd()
)
@click.option(
    '--blogbook_dir',
    default=None
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Enables verbose mode.'
)
@click.version_option()
@click.pass_context
def main(context, work_dir, blogbook_dir, verbose):
    """Repo is a command line tool that showcases how to build complex
    command line interfaces with Click.
    This tool is supposed to look like a distributed version control
    system to show how something like this can be structured.
    """
    context.obj = Blogbook(work_dir, blogbook_dir)
    context.obj.verbose = verbose


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
@click.option(
    '--bare',
    is_flag=True,
    help='Force override existing directory'
)
@click.argument(
    'directory',
    default=os.getcwd()
)
@pass_blog
def new(blog, force, layout, bare, directory):
    """
    Create a new blogbook.
    """

    if os.path.isdir(directory) and not blogbook.toolbox.file.is_empty(directory) and not force:
        click.echo(
            blog.work_dir + ' already exist and is not an empty directory, '
            + 'either user an other directory or use the --force flag.'
        )
        return

    if not os.path.isdir(layout) and not zipfile.is_zipfile(layout):
        raise click.BadParameter('You must provide either an existing layout directory or zip file')

    click.echo('Create new blogbook into [{}]'.format(directory))
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)

    if not bare:

        blogbook.toolbox.file.force_mkdir(blog.blogbook_dir)

        git_dir = os.path.join(blog.blogbook_dir, '.git')
        if os.path.isdir(git_dir):
            shutil.rmtree(git_dir)
        with CustomRepo.init(directory, git_dir) as repo:

            with open(os.path.join(git_dir, 'info', 'exclude'), 'w') as stream:
                stream.write(os.path.basename(blog.blogbook_dir))

            click.echo('with layouts [{}]'.format(os.path.basename(layout)))
            layouts_path = blog.layouts_dir
            if os.path.isdir(layouts_path):
                shutil.rmtree(layouts_path)

            if os.path.isdir(layout):
                shutil.copytree(layout, layouts_path)
            elif zipfile.is_zipfile(layout):
                with zipfile.ZipFile(layout) as zf:
                    zf.extractall(layouts_path)

            porcelain.add(repo)
            porcelain.commit(repo, b'Initial Commit', committer=b'Blog New <blog@new>')

    else:

        git_dir = os.path.join(directory, 'bare.git')
        if os.path.isdir(git_dir):
            shutil.rmtree(git_dir)
        CustomRepo.init_bare(git_dir)

        work_dir = os.path.join(
            directory, 'build', os.path.basename(directory).replace(blogbook.constant.LOGBOOK_DIRECTORY, '')
        )
        with CustomRepo(work_dir, git_dir) as repo:

            click.echo('with layouts [{}]'.format(os.path.basename(layout)))
            layouts_path = os.path.join(work_dir, blogbook.constant.LAYOUTS_DIRECTORY)
            if os.path.isdir(layouts_path):
                shutil.rmtree(layouts_path)

            if os.path.isdir(layout):
                shutil.copytree(layout, layouts_path)
            elif zipfile.is_zipfile(layout):
                with zipfile.ZipFile(layout) as zf:
                    zf.extractall(layouts_path)

            porcelain.add(repo)
            porcelain.commit(repo, b'Initial Commit', committer=b'Blog New <blog@new>')

        shutil.rmtree(work_dir)


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

    if not os.path.isdir(blog.blogbook_dir):
        raise click.UsageError('Not a blogbook directory : {}'.format(blog.work_dir))

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
@click.argument('directory')
@pass_blog
def output(blog, directory):
    """
    Configure a new blogbook.
    """

    if not os.path.isdir(blog.blogbook_dir):
        raise click.UsageError('Not a blogbook directory : {}'.format(blog.work_dir))

    with open(blog.output_config_path, 'w') as stream:
        stream.write(directory)


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
def remote(blog, set, unset):
    """
    Configure a new blogbook.
    """

    if not os.path.isdir(blog.blogbook_dir):
        raise click.UsageError('Not a blogbook directory : {}'.format(blog.work_dir))

    configuration = configparser.ConfigParser()
    if os.path.isfile(blog.remotes_config_path):
        configuration.read(blog.remotes_config_path)

    if set:
        section, option = set[0].split('.', 1)
        if not configuration.has_section(section):
            configuration.add_section(section)
        configuration.set(section, option, set[1])
        with open(blog.remotes_config_path, 'w') as stream:
            configuration.write(stream)
    if unset:
        section, option = unset.split('.', 1)
        if configuration.has_section(section):
            configuration.remove_option(section, option)
            if not configuration[section]:
                configuration.remove_section(section)
        with open(blog.remotes_config_path, 'w') as stream:
            configuration.write(stream)


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

    output = blog.output_dir
    layouts = blog.layouts_dir

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

    blogbook.build.process.pre_process(blog.work_dir, output, context, markdown)

    def get_key(site_page):
        return site_page.get('date') or '0001-01-01', site_page['title']

    for group, pages in context['site'].items():
        context['site'][group] = sorted(pages, reverse=True, key=get_key)

    environment = Environment(loader=FileSystemLoader(layouts))
    for pages in context['site'].values():
        for page in pages:
            blogbook.build.process.post_process_dynamic(page, context, markdown, environment)

    if watch:
        watcher = blogbook.build.watch.LogbookContentWatcher(blog.work_dir, output, context, markdown, environment)
        try:
            blogbook.serve.run_server(blog.work_dir, output, 1234, blog.setting)
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
    blogbook.serve.run_server(blog.work_dir, blog.output_dir, port, blog.setting)


@main.command()
@click.argument(
    'name',
    default=None
)
@pass_blog
def push(blog, name):
    """
    Serve a blogbook generated content for test purpose only.
    """

    if name is None:
        remote_config = blog.remotes.get(name, {})
    else:
        remote_config = next(iter(blog.remotes.values()), {})

    if 'host' not in remote_config:
        raise click.UsageError('Missing remote host setting')

    client = paramiko.SSHClient()
    client.load_host_keys(blogbook.constant.SSH_HOST_KEYS)
    client.set_missing_host_key_policy(blogbook.repo.push.ConfirmAddPolicy())

    client.connect(remote_config['host'])

    if 'path' in remote_config:
        remote_path = '/var/blog/' + os.path.basename(blog.work_dir) + blogbook.constant.LOGBOOK_DIRECTORY
    else:
        remote_path = remote_config['path']
    # client.exec_command('rm -rf {}'.format(remote_path))
    client.exec_command('blogbook new --bare {}'.format(remote_path))
    if 'output' in remote_config:
        client.exec_command('blogbook --blogbook_dir={} output {}'.format(remote_path, remote_config['output']))

    # sftp = client.open_sftp()
    # with sftp.open(remote_path + '/config', mode='w') as s:
    #     if 'output' in blog.setting['remote']:
    #         configuration = configparser.ConfigParser()
    #         configuration.add_section('path')
    #         configuration.set('path', 'output', value=blog.setting['remote']['output'])
    #         configuration.write(s)
    #
    # for local_root, dir_names, file_names in os.walk(blog.work_dir):
    #
    #     current_remote_root = remote_path
    #     relative_path = os.path.relpath(local_root, blog.work_dir)
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

    client.close()

    with CustomRepo(blog.work_dir, os.path.join(blog.blogbook_dir, '.git')) as r:

        porcelain.add(r)

        s = porcelain.status(r)
        if any(c for c in s.staged.values()):
            porcelain.commit(r, b'Commit/Push blog', committer=b'Blog Pusher <blog@pusher>')

        porcelain.push(r, 'ssh://{}{}'.format(remote_config['host'], posixpath.normpath(remote_path)), refspecs='+master')


# @main.command()
# @click.argument('source')
# @click.argument('destination')
# @pass_blog
# def add(blog, source, destination):
#     if os.path.isfile(source) and source.lower().endswith('.jpg'):
#         im = Image.open(source)
#         im.thumbnail((800, 1200), Image.ANTIALIAS)
#         im.save(os.path.join(blog.work_dir, destination), optimize=True, quality=75)


if __name__ == "__main__":
    main()
