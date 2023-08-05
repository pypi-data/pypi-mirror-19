# Copyright 2017 Josh Fischer

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

setup(
    name='GBRestructure',
    version='0.3.1',
    description='A CLI tool to help with multi-team Git branching strategies',
    author='Josh Fischer',
    author_email='josh@joshfischer.io',
    license='Apache',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Version Control',
      ],
    packages=find_packages(),
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=[
        'nose'
    ],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        gb=restructure.gb:cli
    ''',
)
