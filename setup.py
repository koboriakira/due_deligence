from setuptools import setup, find_packages
import re


def get_requirements():
    for requirement in open('./requirements.txt').read().splitlines():
        removed_version = re.sub(r'==.*', '', requirement)
        yield removed_version.replace('-', '')


setup(
    name="due_deligence",
    version='1.0',
    description='EDINETから有価証券報告書を取得して企業の割安度を判定します。',
    author='Kobori Akira',
    # maintainer='',
    # maintainer_email='',
    author_email='private.beats@gmail.com',
    url='https://github.com/koboriakira/due_deligence',
    packages=find_packages(),
    requires=get_requirements(),
    # requires=open('./requirements.txt').read().splitlines(),
    license='MIT',
    entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      duedeli = due_deligence.cli:main
    """
)
