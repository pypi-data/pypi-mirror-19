'''
@author:   Nick Handy
@date:     12/28/16
@summary:  Distribution setup module using nh_embedded_list_printer.py
'''

from distutils.core import setup

setup( 
    name            = 'nh_embedded_list_printer',
    version         = '1.0.0',
    py_modules      = ['nh_embedded_list_printer'],
    author          = 'nhandy',
    author_email    = 'nichandy@gmail.com',
    url             = 'https://www.youtube.com/channel/UCNfouAHV2SXSI9G2sGNCv8A',
    description     = 'A simple printer of nested lists',
    )