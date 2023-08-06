#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup script for jupyter_contrib_nbextensions."""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from __future__ import print_function

import os
from glob import glob

from setuptools import find_packages, setup


# -----------------------------------------------------------------------------
# main setup call
# -----------------------------------------------------------------------------


def main():

    setup(
        name='helloWorld_nb_extension',
        description="Simple hello world extension for jupyter notebook.",
        version='0.2',
        author='Belal Amin',
        author_email='belalmostafa30@gmail.com',
        keywords=['IPython', 'Jupyter', 'notebook'],
        platforms=['Any'],
        packages=find_packages('src'),
        package_dir={'': 'src'},
        include_package_data=True,
        py_modules=[
            os.path.splitext(os.path.basename(path))[0]
            for path in glob('src/*.py')
        ],
        install_requires=[
            'ipython_genutils',
            'jupyter_core',
            'jupyter_nbextensions_configurator',
            'nbconvert',
            'notebook >=4.0',
            'psutil >=2.2.1',
            'pyyaml',
            'tornado',
            'traitlets',
        ],
        extras_require={
            'test': [
                'nbformat',
                'nose',
                'pip',
                'requests',
            ],
            'test:python_version == "2.7"': [
                'mock',
            ],
        },
        # we can't be zip safe as we require templates etc to be accessible to
        # jupyter server
        zip_safe=False,
        entry_points={
            'console_scripts': [
                'jupyter-contrib-nbextension = jupyter_contrib_nbextensions.application:main',  # noqa: E501
            ],
            'jupyter_contrib_core.app.subcommands': [
                'nbextension = jupyter_contrib_nbextensions.application:jupyter_contrib_core_app_subcommands',  # noqa: E501
            ],
            'nbconvert.exporters': [
                'html_toc = jupyter_contrib_nbextensions.nbconvert_support.toc2:TocExporter',  # noqa: E501
                'html_embed = jupyter_contrib_nbextensions.nbconvert_support.embedhtml:EmbedHTMLExporter',  # noqa: E501
            ],
        },
        scripts=[os.path.join('scripts', p) for p in [
            'jupyter-contrib-nbextension',
        ]],
        classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: JavaScript',
            'Programming Language :: Python',
            'Topic :: Utilities',
        ],
    )


if __name__ == '__main__':
    main()
