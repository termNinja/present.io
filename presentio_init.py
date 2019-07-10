#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import stat
from typing import Dict

def get_user_input() -> Dict[str, str]:
    # Title of the presentation
    title = input('Title of your presentation: ')

    # Author of the presentation
    author = input('Author of your presentation: ')

    # Name of the files
    file_name = input('Name of the file (for example "slides" or "phd" - empty string for default): ')
    if not file_name:
        file_name = 'slides'

    # The directory in which the presentation is being kept
    # We assume the user is there already and is calling this
    # script to initialize the directory for work.
    dir = os.getcwd()

    return {
        'title': title,
        'author': author,
        'file_name': file_name,
        'dir': dir,
    }

def generate_md_template(data: Dict[str, str]) -> str:
    author = data['author']
    title = data['title']
    return f"""---
title: '{title}'
aspectratio: 169
author: {author}
urlcolor: cyan
colorlinks: true
---

# {title}
    """

def generate_files(data: Dict[str, str], content: str):
    target_file = data['file_name'] + '.md'
    try:
        with open(target_file, 'w') as fid:
            fid.write(content)
            os.mkdir('images')
    except IOError:
        sys.exit("Failed creating file {target_file}")

def generate_compile_file(data: Dict[str, str]) -> str:
    file_name: str = data['file_name']
    compile_content: str = f"""#! /usr/bin/env bash
#pandoc -t beamer {file_name}.md  --pdf-engine=xelatex -V theme:metropolis -o {file_name}.pdf
pandoc -t beamer {file_name}.md  -V theme:metropolis -o {file_name}.pdf
"""
    try:
        with open('compile.sh', 'w') as fid:
            fid.write(compile_content)
        st = os.stat('compile.sh')
        os.chmod('compile.sh', st.st_mode | stat.S_IEXEC)
    except IOError as e:
        print(e)
        sys.exit('Failed creating compile.sh')


def main():
    data: Dict[str, str] = get_user_input()
    md_template: str = generate_md_template(data)
    generate_files(data, md_template)
    generate_compile_file(data)

if __name__ == "__main__":
    main()
