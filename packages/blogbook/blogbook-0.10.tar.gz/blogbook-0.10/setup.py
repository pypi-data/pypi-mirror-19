from setuptools import setup, find_packages

setup(
    name='blogbook',
    version='0.10',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'jinja2',
        'mistune',
        'pyyaml',
        'watchdog',
        'paramiko',
        'Pillow',
        'dulwich'
    ],
    entry_points={
        'console_scripts': ['blogbook=blogbook.command:main']
    },
    url='https://github.com/pieceofstone/blogbook',
    author='noogg',
    author_email='tkclem@yahoo.fr',
)
