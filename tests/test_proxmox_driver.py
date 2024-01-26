#
# Proxmox driver tests.
#

import contextlib
import os
import pathlib
import subprocess
import pytest


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


def check_env(name):
    """Verify test environment is set."""
    value = os.environ.get(name)
    assert value != None, f'{name} is not set'
    assert value != '', f'{name} is empty'


def test_molecule_init_scenario(tmpdir):
    print('')
    with chdir(tmpdir):
        molecule('init', 'scenario', '--driver-name', 'molecule-proxmox')
        assert pathlib.Path('molecule/default/converge.yml').exists()
        assert pathlib.Path('molecule/default/create.yml').exists()
        assert pathlib.Path('molecule/default/destroy.yml').exists()
        assert pathlib.Path('molecule/default/molecule.yml').exists()


@pytest.mark.parametrize('scenario', [
                           'default', 'by-name', 'by-vmid', 'cloud-init'])
def test_molecule_test(scenario):
    print('')
    check_env('PROXMOX_HOST')
    check_env('PROXMOX_NODE')
    check_env('PROXMOX_PASSWORD')
    check_env('PROXMOX_SSH_IDENTITY_FILE')
    check_env('PROXMOX_SSH_USER')
    check_env('PROXMOX_TEMPLATE_NAME')
    check_env('PROXMOX_TEMPLATE_VMID')
    check_env('PROXMOX_TOKEN_ID')
    check_env('PROXMOX_TOKEN_SECRET')
    check_env('PROXMOX_USER')
    testdir = pathlib.Path(__file__).resolve().parent
    projectdir = testdir / 'proxmox_driver'
    with chdir(projectdir):
        molecule('reset', '--scenario-name', scenario)
        molecule('test', '--scenario-name', scenario)
