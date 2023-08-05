"""
Project Tasks that can be invoked using using the program "invoke" or "inv"
"""

import os
import glob
from invoke import task

# disable the check for unused-arguments to ignore unused ctx parameter in tasks
# pylint: disable=unused-argument

def get_files():
    """
    Get the files to run analysis on
    """
    files = [
        'dploy',
        'setup.py',
        'tasks.py',
    ]
    files.extend(glob.glob(os.path.join('tests', '*.py')))
    files_string = ' '.join(files)
    return files_string

@task
def setup(ctx):
    """
    Install python requirements
    """
    ctx.run('python3 -m pip install -r requirements.txt')

@task
def clean(ctx):
    """
    Clean repository using git
    """
    ctx.run('git clean --interactive', pty=True)

@task
def lint(ctx):
    """
    Run pylint on this module
    """
    cmd = 'python3 -m pylint --output-format=parseable {files}'
    ctx.run(cmd.format(files=get_files()))

@task
def metrics(ctx):
    """
    Run radon code metrics on this module
    """
    cmd = 'radon {metric} --min B {files}'
    metrics_to_run = ['cc', 'mi']
    for metric in metrics_to_run:
        ctx.run(cmd.format(metric=metric, files=get_files()))

@task
def test(ctx):
    """
    Test Task
    """
    cmd = 'py.test'
    ctx.run(cmd)

@task(test, lint, default=True)
def default(ctx):
    """
    Default Tasks
    """
    pass

@task(clean)
def build(ctx):
    """
    Task to build an executable using pyinstaller
    """
    cmd = 'pyinstaller -n dploy --onefile ' + os.path.join('dploy', '__main__.py')
    ctx.run(cmd)
