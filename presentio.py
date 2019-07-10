#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import stat
import argparse
from inspect import cleandoc
from typing import Dict
from pretty_print import regular_msg, warn_msg, fail_msg, success_msg
from document_data import DocumentData


def file_exists(file_name: str) -> bool:
    return True if os.path.exists(file_name) else False


def ensure_user_is_not_a_moron(detected_file_name: str) -> bool:
    """
    If file collision is detected, we must ask the user if he/she really wants
    to purge old files.
    """

    msg = f"Duplicate file {detected_file_name} found, do you want to PURGE it and create a new one? [y/n]"

    warn_msg(msg)

    answer: str = input().lower().strip()

    # Make sure user responded
    while answer not in ['y', 'n']:
        warn_msg(msg)
        answer: str = input().lower().strip()

    if answer == 'y':
        return True
    elif answer == 'n':
        return False
    else:
        fail_msg("Failed to answer")
        sys.exit()
        return False


def get_document_info(args) -> DocumentData:
    """
    Reads the input of the user from standard input
    and creates a required object.
    """

    author: str = args.author if args.author else input(
        'Author of your presentation: ')
    title: str = args.title if args.title else input(
        'Title of your presentation: ')
    bibliography: bool = True if args.bibliography else False

    # If use didn't give us a file name,
    # we create the file name out of the title.
    if not args.filename:
        file_name = title.strip().lower().replace(' ', '_')
    else:
        file_name = args.filename

    # The directory in which the presentation is being kept
    # We assume the user is there already and is calling this
    # script to initialize the directory for work.
    directory = os.getcwd()

    return DocumentData(
        author,
        title,
        file_name,
        directory,
        bibliography,
    )

def check_if_user_aborts_to_overwrite_the_file(target_file: str) -> None:
    if file_exists(target_file) and not ensure_user_is_not_a_moron(target_file):
        fail_msg("Aborted by the will of the user.")
        sys.exit()

def generate_md_template(data: DocumentData) -> None:
    """
    Returns the content of the md file template.
    """

    target_file: str = data.file_name + '.md'
    check_if_user_aborts_to_overwrite_the_file(target_file)

    header_includes: str = r'''headerincludes: |
        \newcommand{\theimage}[1]{\includegraphics[width=1\textwidth,height=0.9\textheight,keepaspectratio]{#1}}'''

    literature_payload = """
    ## Citing a resource
    - The answer is 42! [@the42]

    ## References
    """ if data.bibliography else ''

    md_template: str = cleandoc(
    f"""---
    title: '{data.title}'
    aspectratio: 169
    author: {data.author}
    urlcolor: cyan
    colorlinks: true
    {header_includes}
    ---

    # {data.title}

    ## My First Slide
    - Hello from {data.author}
    - Thank you for using `presentio`! <3
    {literature_payload}""")

    try:
        with open(target_file, 'w') as fid:
            fid.write(md_template)
            regular_msg(f"Created {target_file}.")
            if not os.path.exists('images'):
                os.mkdir('images')
            regular_msg(f"Created images directory.")
    except IOError as exception:
        fail_msg(exception)
        fail_msg(f"Failed creating file {target_file}")
        sys.exit()


def generate_compile_file(data: DocumentData) -> str:
    """
    Generates a compile file named `compile.sh` to be later use to compile the document.
    It's recommended to bind your editor to some shortcut to execute this script when needed.
    """
    file_name: str = data.file_name
    target_file: str = 'compile.sh'

    check_if_user_aborts_to_overwrite_the_file(target_file)

    bib_payload: str = f""" \\
            --filter pandoc-citeproc \\
            --bibliography=literature.bib
    """ if data.bibliography else ''

    compile_content: str = cleandoc(
        f"""#! /usr/bin/env bash
        # pandoc -t beamer {data.file_name}.md  --pdf-engine=xelatex -V theme:metropolis -o {data.file_name}.pdf
        pandoc \\
            -t beamer {data.file_name}.md \\
            -V theme:metropolis \\
            -o {file_name}.pdf {bib_payload}
        """)

    try:
        with open(target_file, 'w') as fid:
            fid.write(compile_content)
        regular_msg(f"Created {target_file}.")

        # Make it executable
        st = os.stat(target_file)
        os.chmod(target_file, st.st_mode | stat.S_IEXEC)
        regular_msg(f"Edited {target_file} to be executable.")
    except IOError as e:
        fail_msg(e)
        fail_msg('Failed creating compile.sh')
        sys.exit()


def generate_bibliography_file() -> None:
    target_file: str = 'literature.bib'
    check_if_user_aborts_to_overwrite_the_file(target_file)

    payload: str = cleandoc("""
    @article{the42,
        added-at = {2012-01-27T14:41:50.000+0100},
        author = {Adams, Douglas},
        biburl = {https://www.bibsonomy.org/bibtex/2e170eb13993a56f57e814c7537caa316/nosebrain},
        interhash = {2689edbe3de2f39388b4d16880b7fbe9},
        intrahash = {e170eb13993a56f57e814c7537caa316},
        keywords = {galaxy guide hitchhiker scifi},
        timestamp = {2013-06-25T18:26:30.000+0200},
        title = {The Hitchhiker's Guide to the Galaxy},
        year = 1995
    }
    """)

    try:
        with open(target_file, 'w') as fid:
            fid.write(payload)
        regular_msg(f"Created {target_file}.")

    except IOError as exc:
        fail_msg(exc)
        fail_msg(f'Failed creating {target_file}')
        sys.exit()


def main():
    parser = argparse.ArgumentParser()
    parser.prog = 'presentio'
    parser.add_argument('-a', '--author', help='Author of the presentation')
    parser.add_argument('-t', '--title', help='Title of the presentation')
    parser.add_argument('-b', '--bibliography',
                        help='Add the bibliography support', action='store_true')
    parser.add_argument('-f', '--filename',
                        help='Name of the file to be created')
    args = parser.parse_args()

    data: DocumentData = get_document_info(args)
    generate_md_template(data)
    if data.bibliography:
        generate_bibliography_file()
    generate_compile_file(data)
    success_msg(f"Your document {data.title} is ready! Enjoy!")


if __name__ == "__main__":
    main()
