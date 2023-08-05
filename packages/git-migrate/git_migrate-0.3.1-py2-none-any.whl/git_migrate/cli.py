# -*- coding: utf-8 -*-

import tempfile
import hashlib
import subprocess
import glob
import os
import pipes
import re
from ConfigParser import RawConfigParser
import sys
import colorama
from colorama import Fore, Back, Style

def main():
    colorama.init()
    config = parse_config()
    scripts = find_scripts(config['command_files_path'])

    if not scripts:
        return

    clone_detached_branch(config['detached_branch_name'])
    for script in scripts:
        run_script(script, config['detached_branch_name'])

def parse_config():
    config = RawConfigParser()
    config.add_section('core')
    config.read([
        os.path.join(os.path.dirname(__file__), '.gitmigrate.dist'),
        '.gitmigrate'
    ])
    branch = config.get('core', 'detached_branch_name')
    path = config.get('core', 'command_files_path')
    path = filter(None, [line.strip() for line in path.splitlines()])
    return {
        'detached_branch_name': branch,
        'command_files_path': path
    }

def find_scripts(pathes):
    all = []
    for path in pathes:
        all += glob.glob(path)
    filtered = filter(os.path.isfile, all)
    return filtered

def clone_detached_branch(detached_branch_name):
    current_path  = os.getcwd()
    detached_path = get_detached_path(current_path)

    has_branch = has_detached_branch(detached_branch_name)

    subprocess.check_output(['rm', '-rf', detached_path])
    subprocess.check_output(['mkdir', detached_path])
    os.chdir(detached_path)

    if has_branch:
        subprocess.check_output(['git', 'clone', '-b', detached_branch_name, '--single-branch', current_path, '.'], stderr=subprocess.STDOUT)
    else:
        subprocess.check_output(['git', 'clone', '--no-checkout', current_path, '.'], stderr=subprocess.STDOUT)
        subprocess.check_output(['git', 'checkout', '--orphan', detached_branch_name], stderr=subprocess.STDOUT)
        subprocess.check_output(['git', 'rm', '-rf', '.'], stderr=subprocess.STDOUT)
        subprocess.check_output(['git', 'commit', '--allow-empty', '-m', 'Root'], stderr=subprocess.STDOUT)
        subprocess.check_output(['git', 'push', 'origin', detached_branch_name], stderr=subprocess.STDOUT)

    os.chdir(current_path)

def get_detached_path(current_path):
    return '{}/gitmigrate_{}_{}'.format(
        tempfile.gettempdir(),
        os.path.basename(current_path),
        hashlib.md5(current_path).hexdigest()
    )

def has_detached_branch(detached_branch_name):
    return is_process_succeed(subprocess.call(['git', 'show-ref', '--verify', '--quiet', 'refs/heads/' + detached_branch_name]))

def is_process_succeed(code):
    return 0 == code

def is_process_failed(code):
    return not is_process_succeed(code)

def run_script(script, detached_branch_name):
    print '{}Running{} {}{}{}{}'.format(Style.DIM, Style.RESET_ALL, Style.BRIGHT, Fore.GREEN, script, Style.RESET_ALL)

    head, steps = parse_diff(script, detached_branch_name)
    if not steps:
        return

    for step in steps:
        print '{}…{} {}{}{}{}'.format(Style.DIM, Style.RESET_ALL, Style.NORMAL, Fore.YELLOW, step, Style.RESET_ALL)
        code = execute_step('\n'.join(head + [step]))
        if is_process_failed(code):
            raise RuntimeError('Step "{}" failed'.format(step))
        save_script_step(script, step, detached_branch_name)

def parse_script(script):
    with open(script) as f:
        lines = f.read().splitlines()

    return split_head_steps(lines)

def split_head_steps(lines):
    if '' not in lines:
        return ([], [])

    index = lines.index('') + 1
    return lines[:index], lines[index:]

def parse_diff(script, detached_branch_name):
    diff = subprocess.check_output(['git', 'diff', '--no-ext-diff', '--unified=0', '--no-color', detached_branch_name, 'HEAD', '--', script])
    lines = [line[1:] for line in diff.splitlines() if is_line_added(line, script)]
    return split_head_steps(lines)

def is_line_added(line, script):
    return re.match('^\+', line) and not re.match('^\+\+\+.+' + re.escape(script) + '$', line)

def execute_step(source):
    with tempfile.NamedTemporaryFile(bufsize=0) as f:
        f.write(source)
        os.chmod(f.name, 0700)
        f.file.close()
        return subprocess.call([f.name])

def save_script_step(script, step, detached_branch_name):
    current_path  = os.getcwd()
    detached_path = get_detached_path(current_path)
    os.chdir(detached_path)
    with open(script, 'ab') as f:
        f.write(step + '\n')
    subprocess.check_output(['git', 'add', script], stderr=subprocess.STDOUT)
    subprocess.check_output(['git', 'commit', '-m', pipes.quote('Step "{}" from script "{}"'.format(step, script))], stderr=subprocess.STDOUT)
    subprocess.check_output(['git', 'push', 'origin', detached_branch_name], stderr=subprocess.STDOUT)
    os.chdir(current_path)

if __name__ == '__main__':
    main()
