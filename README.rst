***********************
Molecule Proxmox Plugin
***********************

This is an Ansible Molecule Driver plugin to manage instances on a
`Proxmox VE`_ hypervisor cluster.  Only virtual machines are supported at this
time.

Requirements
============

* Access to a `Proxmox VE`_ cluster
* One or more virtual machine templates with required setup
* Python package `proxmoxer`_
* Ansible module `community.general.proxmox_kvm`_

The required Python packages are automatically installed when
``molecule-proxmox`` is installed with ``pip``.

The ``proxmox_kvm`` module is included with the Community.General collection
and is automatically installed when Ansible is installed with ``pip``.


Virtual machine template requirements
-------------------------------------

The molecule instances are created by cloning Proxmox virtual machine
templates.  You will need to create one or more templates.

Templates have the following requirements.

* A cloud-init drive, if any cloud-init settings are used
* networking configured
* qemu-guest-agent installed and enabled in Proxmox
* Python installed for Ansible
* ssh server installed and enabled
* a user account (or created by cloud-init) for ssh access
* An ssh public in the ``authorized_keys`` of the user (or created by cloud-init)
  The corresponding private key must be located on the machine running
  molecule.
* You may need to add the user to the suoders file, depending on if any
  elevated privileges are required in your ``converge`` playbooks or if
  you enable the ``sethostname`` molecule-proxmox driver option.

Installation
============

The ``molecule-proxmox`` plugin may be installed with Python ``pip``. A virtualenv
is recommended.  The following commands install Ansible, Molecule, and the
Molecule Proxmox plugin in a virtualenv called ``.venv``.

.. code-block:: bash

    $ python3 -m venv .venv
    $ source .venv/bin/activate
    (.venv) $ pip install -U pip
    (.venv) $ pip install ansible molecule molecule-proxmox


Driver options
==============

``api_host``
  The Proxmox VE server hostname to connect to issue API commands.

``api_user``
  Proxmox user to manage the instances. The api_user must be in the
  form ``<username>@<realm>``.

``api_password``
  The ``api_user`` password. Specify either a password or a token.

``api_token_id``
  The ``api_user`` token id.

``api_token_secret``
  The ``api_user`` token value.

``proxmox_secrets``
  The fully qualified path to a yaml file containing connection options.
  This allows you to avoid putting your Proxmox passwords/tokens in the
  molecule configuration. The file may be encrypted with ``ansible-vault``.

``node``
  Proxmox node name to create the virtual machines.

``ssh_user``
  The user account for ssh access to the created virtual machines.

``ssh_identity_file``
  The path to the local ssh private key file for ssh access to the created
  virtual machines.

``sethostname``
  When ``yes``, set the hostname of the created virtual machine to the molecule
  instance name and add the hostname and non-loopback address to the
  ``/etc/hosts`` file.  The ``ssh_user`` must be in the sudoers list in the
  template image in order to use this option.

Platform instance configuration
===============================

The Proxmox template to be cloned can be specifed by name or numeric id.

``template_name``
  The name of the Proxmox virtual machine template to be cloned.

``template_vmid``
  The numeric id of the Proxmox virtual machine template to be cloned.

Cloud-init
==========

Cloud-init is supported with Proxmox templates setup with cloud-init support.

Cloud-init options my be added to the instance options in the ``platforms``
list.  See `community.general.proxmox_kvm`_ for available cloud-init options.

Examples
========

Connect with a Proxmox user and password.

.. code-block:: yaml

   # molecule.yml
   ---
   driver:
     name: molecule-proxmox
     options:
        api_host: pve01.example.com
        api_user: root@pam
        api_password: ********
        node: pve01
        ssh_user: molecule
        ssh_identity_file: /path/to/id_rsa
        sethostname: yes

   platforms:
     - name: test01
       template_name: debian12

Connect with a Proxmox API token.

.. code-block:: yaml

   # molecule.yml
   ---
   driver:
     name: molecule-proxmox
     options:
        # Connection settings with token.
        api_host: pve01.example.com
        api_user: root@pam
        api_token_id: ********
        api_token_secret: *******************************
        node: pve01
        ssh_user: tester
        ssh_identity_file: /path/to/id_rsa

   platforms:
     - name: test01
       template_name: debian11

Store the Proxmox user and password in a separate file.

.. code-block:: yaml

   # molecule.yml
   ---
   driver:
     name: molecule-proxmox
     options:
        # Sensitive settings may be located in a separate file.
        proxmox_secrets: /path/to/proxmox_secrets.yml
        node: pve01
        ssh_user: tester
        ssh_identity_file: /path/to/id_rsa
        template_name: debian11

   platforms:
     - name: test01
     - name: test02

.. code-block:: yaml

   # proxmox_secrets.yml
   ---
   api_host: pve01.example.com
   api_user: root@pam
   api_password: ************

Cloud-init options are supported on cloud-init enabled templates.
These options can be used to configure instances on first boot.

.. code-block:: yaml

   # molecule.yml
   ---
   driver:
     name: molecule-proxmox
     options:
        # Connection settings
        api_host: pve01.example.com
        api_user: root@pam
        api_password: ********
        node: pve01
        ssh_user: some_user
        ssh_identity_file: /path/to/id_rsa

   platforms:
     - name: test01
       template_name: debian12
       # Using cloud-init to setup the instance.
       ciuser: some_user
       cipassword: some_password
       ipconfig:
         ipconfig0: 'ip=192.168.0.2/24,gw=192.168.0.1'
       nameservers:
         - 192.169.0.245

Development
===========

To checkout the source code:

.. code-block:: bash

    $ git clone https://github.com/meffie/molecule-proxmox
    $ cd molecule-proxmox

A `Makefile` is provided to facilitate development and testing. A Python
virtualenv environment may be created with the `init` target.

.. code-block:: bash

    $ make init
    $ source .venv/bin/activate

Export the following shell environment variables to run the unit tests.

.. code-block:: bash

    # Connection info:
    export PROXMOX_HOST=<proxmox hostname>
    export PROXMOX_USER=<username@realm>
    export PROXMOX_PASSWORD=<password>
    export PROXMOX_TOKEN_ID=<id>
    export PROXMOX_TOKEN_SECRET=<secret>
    export PROXMOX_NODE=<proxmox node name>
    export PROXMOX_SSH_USER=<username>
    export PROXMOX_SSH_IDENTITY_FILE=<ssh key file for username>

    # Template id and names for unit tests:
    export PROXMOX_TEMPLATE_VMID=<template vmid to be cloned in by-vmid scenario>
    export PROXMOX_TEMPLATE_NAME=<template name to be cloned in by-name scenario>

To run the unit tests in verbose mode:

.. code-block:: bash

    $ make test

To run the unit tests in quiet mode:

.. code-block:: bash

    $ make check


Authors
=======

Molecule Proxmox Plugin was created by Michael Meffie based on code from
Molecule.

License
=======

The `MIT`_ License.


.. _`Proxmox VE`: https://www.proxmox.com/en/proxmox-ve
.. _`proxmoxer`: https://pypi.org/project/proxmoxer/
.. _`community.general.proxmox_kvm`: https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_kvm_module.html
.. _`MIT`: https://github.com/meffie/molecule-proxmox/blob/master/LICENSE
