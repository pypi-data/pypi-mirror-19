'''
Created on 2017年1月5日

@author: koyaku
'''
from distutils.core import setup
from test.regrtest import DESCRIPTION

setup(
      name          ='movie_list_kuyt',
      version       ='1.0.0',
      py_modules    =['movie_list'],
      author        ='huyue',
      author_email  ='cwkoyaku@163.com',
      url           ='http://www.koy.com',
      description   ='A simple printer of movie_list',
      )