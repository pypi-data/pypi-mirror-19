# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='ncp',
      version='1.9',
      packages=find_packages(),
      include_package_data=True,  # 启用清单文件MANIFEST.in
      exclude_package_data={'': ['.gitignore']},
      zip_safe=False,
      install_requires=['jinja2>=2.9'],
      entry_points='''
        [console_scripts]
        ncp=ncp.app:main
    ''')
