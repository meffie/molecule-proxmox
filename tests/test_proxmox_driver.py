#
# Proxmox driver tests.
#

import contextlib
import os
import pathlib
import subprocess
import pytest


PROJECT_DIR = pathlib.Path(__file__).resolve().parent / 'proxmox_driver'


@contextlib.contextmanager
def chdir(path):
    prev = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)


def molecule(command, *args, expected_rc=0):
    args = ['molecule', command] + list(args)
    proc = subprocess.Popen(args)
    rc = proc.wait()
    assert rc == expected_rc


def check_env(name):
    """Verify test environment is set."""
    value = os.environ.get(name)
    assert value is not None, f'{name} is not set'
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
    with chdir(PROJECT_DIR):
        molecule('reset', '--scenario-name', scenario)
        molecule('test', '--scenario-name', scenario)


def opener(path, flags):
    """ Create the file with mode bits set to 600. """
    return os.open(path, flags, 0o600)


@pytest.fixture
def secrets():
    check_env('PROXMOX_HOST')
    check_env('PROXMOX_USER')
    check_env('PROXMOX_PASSWORD')
    proxmox_host = os.environ['PROXMOX_HOST']
    proxmox_user = os.environ['PROXMOX_USER']
    proxmox_password = os.environ['PROXMOX_PASSWORD']
    path = pathlib.Path('.secrets.yaml').absolute()
    with open(path, 'w', opener=opener) as f:
        f.write('---\n')
        f.write(f'api_host: {proxmox_host}\n')
        f.write(f'api_user: {proxmox_user}\n')
        f.write(f'api_password: {proxmox_password}\n')
    os.environ['PROXMOX_SECRETS'] = path.as_posix()
    yield path
    os.unlink(path)


def test_secrets_file_present(secrets):
    print("")
    check_env('PROXMOX_NODE')
    check_env('PROXMOX_SSH_IDENTITY_FILE')
    check_env('PROXMOX_SSH_USER')
    check_env('PROXMOX_TEMPLATE_NAME')
    with chdir(PROJECT_DIR):
        molecule('reset', '--scenario-name', 'secrets')
        molecule('test', '--scenario-name', 'secrets')


def test_secrets_file_missing():
    print("")
    check_env('PROXMOX_NODE')
    check_env('PROXMOX_SSH_IDENTITY_FILE')
    check_env('PROXMOX_SSH_USER')
    check_env('PROXMOX_TEMPLATE_NAME')
    with chdir(PROJECT_DIR):
        molecule('reset', '--scenario-name', 'secrets')
        molecule('create', '--scenario-name', 'secrets', expected_rc=2)
