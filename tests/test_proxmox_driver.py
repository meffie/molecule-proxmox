#
# Proxmox driver tests.
#

import contextlib
import os
import pathlib
import subprocess


@contextlib.contextmanager
def chdir(path):
    prev = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)


def molecule(command, *args):
    args = ['molecule', command] + list(args)
    proc = subprocess.Popen(args)
    rc = proc.wait()
    assert rc == 0


def test_molecule_init_role(tmpdir):
    print('')
    with chdir(tmpdir):
        molecule('init', 'role', 'myrole', '--driver-name', 'proxmox')
        os.system('tree')
        assert pathlib.Path('myrole/molecule/default/INSTALL.rst').exists()


def test_molecule_init_scenario(tmpdir):
    print('')
    with chdir(tmpdir):
        molecule('init', 'scenario', '--driver-name', 'proxmox')
        os.system('tree')
        assert pathlib.Path('molecule/default/INSTALL.rst').exists()


def test_molecule_test():
    print('')
    project_directory = pathlib.Path(__file__).resolve().parent
    with chdir(project_directory):
        molecule('test')