#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pypl',
        version = '11.2',
        description = '''''',
        long_description = '''''',
        author = "Ingo Fruend",
        author_email = "pypl@ingofruend.net",
        license = 'MIT',
        url = '',
        scripts = [],
        packages = ['pypl'],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = ['svgwrite'],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
