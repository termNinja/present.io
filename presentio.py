#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import stat
import argparse
from inspect import cleandoc
from typing import Dict


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def regular_msg(msg: str) -> None:
    """Prints out a blue colored message to standard output."""
    print(f"{bcolors.OKBLUE} {msg} {bcolors.ENDC}")


def success_msg(msg: str) -> None:
    """Prints out a green colored message to standard output."""
    print(f"{bcolors.OKGREEN} {msg} {bcolors.ENDC}")


def fail_msg(msg: str) -> None:
    """Prints out a red colored message to standard output."""
    print(f"{bcolors.FAIL} {msg} {bcolors.ENDC}")


def warn_msg(msg: str) -> None:
    """Prints out a yellowish colored message to standard output."""
    print(f"{bcolors.WARNING} {msg} {bcolors.ENDC}")


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


class DocumentData:
    """
    Represents a data object that is used to fill in the template.
    """

    def __init__(self, author, title, file_name, directory):
        self.author = author
        self.title = title
        self.file_name = file_name
        self.directory = directory

    def __repr__(self):
        return f"[document] author={self.author} title={self.title} file_name={self.file_name} directory={self.directory}"

    def __str__(self):
        return self.__repr__()


def get_document_info() -> DocumentData:
    """
    Reads the input of the user from standard input
    and creates a required object.
    """

    parser = argparse.ArgumentParser()
    parser.prog = 'presentio'
    parser.add_argument('-a', '--author', help='Author of the presentation')
    parser.add_argument('-t', '--title', help='Title of the presentation')
    parser.add_argument('-f', '--filename',
                        help='Name of the file to be created')
    args = parser.parse_args()

    author: str = args.author if args.author else input(
        'Author of your presentation: ')
    title: str = args.title if args.title else input(
        'Title of your presentation: ')

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
        title,
        author,
        file_name,
        directory
    )


def generate_md_template(data: DocumentData) -> None:
    """
    Returns the content of the md file template.
    """

    target_file: str = data.file_name + '.md'

    if file_exists(target_file) and not ensure_user_is_not_a_moron(target_file):
        # We abort
        fail_msg("Aborted by the will of the user.")
        sys.exit()

    md_template: str = cleandoc(
        f"""---
        title: '{data.title}'
        aspectratio: 169
        author: {data.author}
        urlcolor: cyan
        colorlinks: true
        ---

        # {data.title}""")

    try:
        with open(target_file, 'w') as fid:
            fid.write(md_template)
            regular_msg(f"Created {target_file}.")
            if not os.path.exists('images'):
                os.mkdir('images')
            regular_msg(f"Created images directory.")
    except IOError as e:
        fail_msg(e)
        fail_msg(f"Failed creating file {target_file}")
        sys.exit()


def generate_compile_file(data: DocumentData) -> str:
    """
    Generates a compile file named `compile.sh` to be later use to compile the document.
    It's recommended to bind your editor to some shortcut to execute this script when needed.
    """
    file_name: str = data.file_name
    target_file: str = 'compile.sh'

    if file_exists(target_file) and not ensure_user_is_not_a_moron(target_file):
        # We abort
        fail_msg("Aborted by the will of the user.")
        sys.exit()

    compile_content: str = cleandoc(
        f"""#! /usr/bin/env bash
        #pandoc -t beamer {data.file_name}.md  --pdf-engine=xelatex -V theme:metropolis -o {data.file_name}.pdf
        pandoc -t beamer {data.file_name}.md  -V theme:metropolis -o {file_name}.pdf
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


def main():
    data: DocumentData = get_document_info()
    generate_md_template(data)
    generate_compile_file(data)
    success_msg(f"Your document {data.title} is ready! Enjoy!")


if __name__ == "__main__":
    main()
