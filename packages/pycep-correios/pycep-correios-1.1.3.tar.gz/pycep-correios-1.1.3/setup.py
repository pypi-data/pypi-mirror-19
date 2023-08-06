# -*- coding: utf-8 -*-
# #############################################################################
# The MIT License (MIT)
#
# Copyright (c) 2016 Michell Stuttgart
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# #############################################################################

from setuptools import setup, find_packages

setup(
    name='pycep-correios',
    version='1.1.3',
    keywords='correios development cep',
    packages=find_packages(exclude=['*test*']),
    zip_safe=False,
    url='https://github.com/mstuttgart/pycep-correios',
    license='MIT',
    author='Michell Stuttgart',
    author_email='michellstut@gmail.com',
    description=u'Método para busca de dados de CEP no webservice dos '
                'Correios',
    long_description=open('README.md', 'r').read(),
    package_data={
            'pycep-correios': ['templates/*xml']
    },
    install_requires=[
        'requests >= 2.10.0',
        'Jinja2 >= 2.8',
    ],
    test_suite='test',
    tests_require=[
        'coverage',
        'coveralls',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.4',
        
    ],
)
