import os
import subprocess
import unittest
import json
from argparse import ArgumentParser
from enum import Enum
from unittest.suite import TestSuite

from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner


def check(config, root_dir, fix_subs):
    print('Check: started')
    for sub in config.subs:
        if isinstance(sub, GitSub):
            _, output, _ = get_cmd_result('git', '--git-dir', os.path.join(root_dir, 'subs', sub.name, '.git'),
                                          '--work-tree', os.path.join(root_dir, 'subs', sub.name),
                                          'rev-parse', 'HEAD')
            if output[:-1] != sub.commit:
                if fix_subs:
                    cmd('git', '--git-dir', os.path.join(root_dir, 'subs', sub.name, '.git'),
                        '--work-tree', os.path.join(root_dir, 'subs', sub.name),
                        'checkout', output[:-1])
                else:
                    print('Sub ' + sub.name + ' has wrong revision.\n  Referenced: ' + sub.commit + '\n  Actual: ' +
                          output[:-1])

            if git_has_uncommited_changes(root_dir, sub):
                print('Sub ' + sub.name + ' is not commited.')
    print('Check: finished')


def git_has_uncommited_changes(root_dir, sub):
    _, output, _ = get_cmd_result('git', '--git-dir', os.path.join(root_dir, 'subs', sub.name, '.git'),
                                  '--work-tree', os.path.join(root_dir, 'subs', sub.name),
                                  'status', '--short')
    return bool(output)


def clean():
    print('Clean: started')
    print('Clean: finished')


def build_binaries(config):
    print('Build binaries: started')
    if config.project_type == ProjectType.dot_net:
        cmd('C:\\Program Files (x86)\\MSBuild\\14.0\\Bin\\MSBuild.exe', 'src/AccountingTools.sln',
            '/property:Configuration=Release', '/property:Platform=Any CPU', '/fileloggerparameters:Encoding=UTF-8')
    print('Build binaries: finished')


def cmd(*args, cwd=None):
    print('cmd: ' + ' '.join(args))
    rc = subprocess.call(args, timeout=20*60, shell=True, cwd=cwd)
    assert rc == 0, 'Command returned code ' + str(rc)


def get_cmd_result(*args, encoding='utf-8'):
    pid = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pid.communicate(timeout=10)
    return pid.returncode, out.decode(encoding), err.decode(encoding)


def build_artifacts_and_test(config, project_root_dir):
    print('Build artifacts and test: started')
    if config.project_type == ProjectType.python:
        python_test(project_root_dir)
    print('Build artifacts and test: finished')


def python_test(project_root_dir):
    suite = TestSuite()
    for all_test_suite in unittest.defaultTestLoader.discover('test/src', pattern='test_*.py'):
        for test_suite in all_test_suite:
            suite.addTests(test_suite)
    if is_running_under_teamcity():
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    saved_curdir = os.curdir
    try:
        os.chdir(os.path.join(project_root_dir, 'test/src'))
        runner.run(suite)
    finally:
        os.chdir(saved_curdir)


def commit(config, root_dir, new_feature):
    for sub in config.subs:
        if isinstance(sub, GitSub) and git_has_uncommited_changes(root_dir, sub):
            cmd('git', '--git-dir', os.path.join(root_dir, 'subs', sub.name, '.git'),
                '--work-tree', os.path.join(root_dir, 'subs', sub.name),
                'branch', 'feature/' + new_feature)
            cmd('git', '--git-dir', os.path.join(root_dir, 'subs', sub.name, '.git'),
                '--work-tree', os.path.join(root_dir, 'subs', sub.name),
                'checkout', 'feature/' + new_feature)
            cmd('\Program Files (x86)\GitExtensions\gitex.cmd', 'commit',
                cwd=os.path.join(root_dir, 'subs/build-tools'))


def process(config, root_dir, *args):
    print('Project ' + config.project_name)
    print('Project root dir: ' + root_dir)
    parser = ArgumentParser(prog='bt.py')
    parser.add_argument('command', nargs='?', choices=['check', 'clean', 'bin-only', 'all', 'commit'], default='all')
    parser.add_argument('--update-subs', nargs='?', type=bool, const=True, default=False)
    parser.add_argument('--new-feature')
    parsed_args = parser.parse_args(args)

    with open(os.path.join(root_dir, 'btgen.json'), 'r') as f:
        generated_config = json.load(f)

    config.load_generated_config(generated_config)

    if parsed_args.command == 'commit':
        if not parsed_args.new_feature:
            print('--new-feature argument is not specified.')
            return
        commit(config, root_dir, parsed_args.new_feature)
        return

    check(config, root_dir, is_running_under_teamcity() or parsed_args.update_subs)
    if parsed_args.command == 'check':
        return

    clean()
    if parsed_args.command == 'clean':
        return

    build_binaries(config)
    if parsed_args.command == 'bin-only':
        return

    build_artifacts_and_test(config, root_dir)


class Config(object):
    def __init__(self):
        self.version_major = 0
        self.version_minor = 1
        self.project_name = 'unnamed'
        self.project_type = ProjectType.none
        self.subs = []

    def load_generated_config(self, generated_config):
        for sub in self.subs:
            sub.load_generated_config(generated_config)


class ProjectType(Enum):
    none = 0
    python = 1
    dot_net = 2


class GitSub(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def load_generated_config(self, generated_config):
        self.commit = generated_config['subs'][self.name]
