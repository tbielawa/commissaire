Getting Involved
================

Development Location
--------------------
The code for commissaire lives on GitHub. The main repo can be found at
https://github.com/projectatomic/commissaire.

Development Setup
-----------------
See `DEVEL.rst <https://github.com/projectatomic/commissaire/blob/master/DEVEL.rst>`_

Vagrant
-------

A ``Vagrantfile`` is provided which will give you a full local development setup.

To run the vagrant development environment make sure you have a supported
virtualization system, vagrant and vagrant-sshfs installed, and have all
commissaire projects checked out in the parent folder as the commissaire
vagrant box will attempt to mount them over SSH.

.. code-block:: shell

   $ ls ../ | grep 'commissaire'
   commissaire
   commissaire-http
   commissaire-service
   $


To run the vagrant development environment make sure you have a support
virtualization system as well as vagrant installed and execute ``./tools/vagrantup``.

.. warning::

   If you want to use the ``vagrant`` command directly note that you will have to follow the same start up process used in ``./tools/vagrantup``

.. note::

   If you decide to use the ``vagrant`` command directly, the ``fedora-atomic`` host will
   require a manual work-around to mount the shared folder at ``/home/vagrant/sync``.
   After the box is up the first time, run ``vagrant ssh fedora-atomic`` to log into the
   virtual machine, then run ``sudo rpm-ostree install fuse-sshfs``.  Exit back out to
   the host machine and restart the virtual machine with ``vagrant reload fedora-atomic``.

.. note::

    You will need to add an ssh pub key to ``/root/.ssh/authorized_keys`` on nodes if you will not be using ``cloud-init`` for bootstrapping.

==================== =============== ================ =========
Server               IP              OS               AutoStart
==================== =============== ================ =========
Servers (etcd/redis) 192.168.152.101 Fedora Cloud 25  Yes
Fedora Node          192.168.152.110 Fedora Cloud 25  Yes
Fedora Atomic Node   192.168.152.111 Fedora Atomic 25 Yes
Commissaire          192.168.152.100 Fedora Cloud 25  No
Kubernetes           192.168.152.102 Fedora Cloud 25  No
==================== =============== ================ =========

For more information see the `Vagrant site <https://www.vagrantup.com>`_.

Getting Up To Speed
-------------------

As you can see commissaire uses a number of libraries.

.. literalinclude:: ../requirements.txt

Of these, the most important to be up to speed on are:

- ansible: https://www.ansible.com/

Standards
---------

Conventions
~~~~~~~~~~~

Code
````
Like most projects commissaire expects specific coding standards to be followed.
`pep8 <https://www.python.org/dev/peps/pep-0008/>`_ is followed strictly with
the exception of E402: module level import not at top of file.

Commissaire Proposal Document
`````````````````````````````
A Commissaire Proposal Document (CPD) must be submitted and approved before
significantly changing the current implementation. This applies to
changes which  break backward compatibility, replace a subsystem, change the
user experience, etc.. For information on the CPD process see
`CPD-1: CPD Process <https://github.com/projectatomic/commissaire/wiki/cpd-1>`_ and the `CPD Template <https://github.com/projectatomic/commissaire/wiki/cpd_template>`_.

Ansible Templates
`````````````````

Variables are used with jinja2 templates and should always prefix
**commissaire_**. Here is a current list variables in use as examples:

============================================= ======================================================
Name                                          Description
============================================= ======================================================
commissaire_targets                           Host(s) to target
commissaire_install_libselinux_python         Command to install libselinux-python
commissaire_install_flannel                   Command to install flannel
commissaire_flanneld_config_local             Local flannel config file to template to the target(s)
commissaire_flanneld_config                   Remote path to the flannel config
commissaire_flannel_service                   Name of the flannel service
commissaire_install_docker                    Command to install docker
commissaire_docker_config_local               Local docker config file to template to the target(s)
commissaire_docker_config                     Remote path to the docker config
commissaire_docker_service                    Name of the docker service
commissaire_install_kube                      Command to install kubernetes minion packages
commissaire_kubernetes_config_local           Local kubernetes config file to template to the target(s)
commissaire_kubernetes_config                 Remote path to the kubernetes config
commissaire_kubeconfig_config_local           Local kubeconfig file to template to the target(s)
commissaire_kubeconfig_config                 Remote path to the kubeconfig
commissaire_kubelet_service                   Name of the kubelet service
commissaire_kubeproxy_service                 Name of the kubernetes proxy service
commissaire_restart_command                   Host restart command
commissaire_upgrade_command                   Host upgrade command
commissaire_bootstrap_ip                      The IP address of the host
commissaire_kubernetes_api_server_url         The kubernetes api server (scheme://host:port)
commissaire_kubernetes_client_cert_path       Path to the kubernetes client certificate
commissaire_kubernetes_client_key_path        Path to the kubernetes client key
commissaire_kubernetes_client_cert_path_local Path to the local kubernetes client certificate
commissaire_kubernetes_client_key_path_local  Path to the local kubernetes client key
commissaire_kubernetes_bearer_token           The bearer token used to contact kubernetes
commissaire_docker_registry_host              The docker registry host
commissaire_docker_registry_port              The docker registry port
commissaire_etcd_server_url                   The etcd server (scheme://host:port)
commissaire_etcd_ca_path                      Path to the etcd certificate authority
commissaire_etcd_client_cert_path             Path to the etcd client certificate
commissaire_etcd_client_key_path              Path to the etcd client key
commissaire_etcd_ca_path_local                Path to the local etcd certificate authority
commissaire_etcd_client_cert_path_local       Path to the local etcd client certificate
commissaire_etcd_client_key_path_local        Path to the local etcd client key
commissaire_flannel_key                       The flannel configuration key
============================================= ======================================================

Testing
~~~~~~~

Unit Testing
````````````
commissaire uses TravisCI to verify that all unit tests are passing.
**All unit tests must pass and coverage must be above 80% before code
will be accepted. No exceptions.**.

To run unit tests locally and see where your code stands:

.. include:: examples/run_unittest_example.rst


End-to-End/BDD Testing
``````````````````````

commissaire uses `Behave <http://pythonhosted.org/behave/>`_ to execute
end to end/BDD tests. You will need to have the following in your parent
directory to properly be able to execute tests locally.

.. code-block:: shell

   $ ls ../ | grep 'comm'
   commctl
   commissaire
   commissaire-http
   commissaire-service
   $


To run e2e/bdd tests locally and see where your code stands:

.. include:: examples/run_e2e_bdd_example.rst

There are a number of tags within the tests. Using these tags can target
specific parts of the codebase without running the full suite. Use ``-t`` to
specify tags. ``-k`` is also helpful as it will suppress showing the tests
that did not run. Using a ``~`` before the tag will disable all test with that tag.
See behave ``--tags-help`` for more details

============= =====================================================
Tag           Description
============= =====================================================
anonymous     Tests without authentication
clientcert    Tests that use a client certificate
cluster       Tests that are specific to cluster functionality
clusterexec   Tests that use the clusterexec code
create        Tests that create a resource
delete        Tests that delete a resource
deploy        Tests which use the deploy functionality
hosts         Tests that are specific to the hosts functionality
list          Tests that list a resource
recreate      Tests that recreate a resource
restart       Tests which use the restart functionality
retrieve      Tests the get a resource
slow          Tests that are known to run slow
ssh           Tests which use the ssh related functionality
status        Tests that are specific to the status functionality
upgrade       Tests which use the upgrade functionality
============= =====================================================

.. include:: examples/run_e2e_bdd_with_tags_example.rst
