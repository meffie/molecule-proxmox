***********************
Molecule Proxmox Plugin
***********************

This is an experimental Molecule Driver pluging to manage instances on a
`Proxmox VE`_ hypervisor cluster.  Only virtual machines are supported at this
time.  Proxmox containers will be supported in a future release.

Requirements
============

* Access to a `Proxmox VE`_ cluster
* One or more ``cloud-init`` enabled virtual machine templates on the Proxmox VE cluster
* Python package `proxmoxer`_
* Ansible module `proxmox_kvm`_

The required Python packages are automatically installed when this package is
installed with ``pip``.  The ``proxmox_kvm`` module is included with the
Community.General Collection and is automatically installed when Ansible is
installed with ``pip``.


Example
=======

.. code-block:: yaml

   driver:
     name: proxmox
     options:


   platforms:
     - name: instance
       template: generic/centos8
       memory: 512
       cpus: 1


Authors
=======

Molecule Proxmox Plugin was created by Michael Meffie based on code from
Molecule.

License
=======

The `MIT`_ License.


.. _`Proxmox VE`: https://www.proxmox.com/en/proxmox-ve
.. _`proxmoxer`: https://pypi.org/project/proxmoxer/
.. _`proxmox_kvm`: https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_kvm_module.html
.. _`MIT`: https://github.com/meffie/molecule-proxmox/blob/master/LICENSE
