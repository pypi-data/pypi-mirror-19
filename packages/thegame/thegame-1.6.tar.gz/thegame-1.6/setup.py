import ast
import codecs
import os
from setuptools import find_packages, setup


# CONFIGURATION

package_name = 'thegame'
long_doc_file = 'README.rst'
classifiers = [
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]


# CONFIGURATION CODE - DO NOT TOUCH


class MetaDataFinder(ast.NodeVisitor):
    def __init__(self):
        self.data = {}

    def visit_Assign(self, node):
        if node.targets[0].id in (
                '__version__',
                '__author__',
                '__contact__',
                '__homepage__',
                '__license__',
        ):
            self.data[node.targets[0].id[2:-2]] = node.value.s


def read(*path_parts):
    filename = os.path.join(os.path.dirname(__file__), *path_parts)

    with codecs.open(filename) as fp:
        return fp.read()


def find_info(*path_parts):
    finder = MetaDataFinder()
    node = ast.parse(read(*path_parts))
    finder.visit(node)
    info = finder.data
    info['docstring'] = ast.get_docstring(node)
    return info


package_info = find_info(package_name, '__init__.py')


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name=package_name,
    version=package_info['version'],
    packages=find_packages(),
    include_package_data=True,
    description=package_info['docstring'],
    long_description=read(long_doc_file),
    url=package_info['homepage'],
    author=package_info['author'],
    author_email=package_info['contact'],
    license=package_info['license'],
    classifiers=classifiers,
)
