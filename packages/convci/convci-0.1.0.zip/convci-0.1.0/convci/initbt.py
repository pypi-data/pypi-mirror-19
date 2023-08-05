from argparse import ArgumentParser
import os
import shutil
import sys


def main(*args):
    parser = ArgumentParser(prog='initbt.py')
    parser.add_argument('project_dir')
    parsed_args = parser.parse_args(args)

    bt_src_dir = os.path.dirname(__file__)
    init_scripts_dir = os.path.join(bt_src_dir, 'initscripts')
    shutil.copy(os.path.join(init_scripts_dir, 'btconfig.py'), parsed_args.project_dir)
    dir_to_build_tools = os.path.relpath(bt_src_dir, parsed_args.project_dir).replace('\\', '/')
    with open(os.path.join(init_scripts_dir, 'bt.py'), 'r') as source_file:
        with open(os.path.join(parsed_args.project_dir, 'bt.py'), 'w') as dest_file:
            dest_file.write(source_file.read().format(dir_to_build_tools=dir_to_build_tools))

if __name__ == '__main__':
    main(*sys.argv[1:])
