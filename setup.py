from setuptools import setup, find_packages
import re


setup(
    name="due_deligence",
    version='1.42',
    description='EDINETから有価証券報告書を取得して企業の割安度を判定します。',
    author='Kobori Akira',
    author_email='private.beats@gmail.com',
    url='https://github.com/koboriakira/due_deligence',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    license='MIT',
    entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      duedeli = due_deligence.cli:main
    """
)
