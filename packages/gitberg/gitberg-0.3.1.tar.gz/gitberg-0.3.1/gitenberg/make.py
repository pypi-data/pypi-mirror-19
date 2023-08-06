#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Makes an organized git repo of a book folder
"""

from __future__ import print_function
import codecs
from os.path import abspath, dirname

import jinja2
import sh

class NewFilesHandler():
    """ NewFilesHandler - templates and copies additional files to book repos

    """
    README_FILENAME = 'README.rst'

    def __init__(self, book):
        self.book = book

        package_loader = jinja2.PackageLoader('gitenberg', 'templates')
        self.env = jinja2.Environment(loader=package_loader)

    def add_new_files(self):
        self.template_readme()
        self.copy_files()

    def template_readme(self):
        template = self.env.get_template('README.rst.j2')
        readme_text = template.render(
            title=self.book.meta.title,
            author=self.book.meta.author,
            book_id=self.book.book_id
        )

        readme_path = "{0}/{1}".format(
            self.book.local_path,
            self.README_FILENAME
        )
        with codecs.open(readme_path, 'w', 'utf-8') as readme_file:
            readme_file.write(readme_text)

    def copy_files(self):
        """ Copy the LICENSE and CONTRIBUTING files to each folder repo """
        files = [u'LICENSE', u'CONTRIBUTING.rst']
        this_dir = dirname(abspath(__file__))
        for _file in files:
            sh.cp(
                '{0}/templates/{1}'.format(this_dir, _file),
                '{0}/'.format(self.book.local_path)
            )

        # copy metadata rdf file
        sh.cp(
            self.book.meta.rdf_path,
            '{0}/'.format(self.book.local_path)
        )
        self.book.meta.dump_file('{0}/metadata.yaml'.format(self.book.local_path))
