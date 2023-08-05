netsu Network Supervisor
========================

.. image:: https://travis-ci.org/netsu-project/netsu.svg?branch=master
    :target: https://travis-ci.org/netsu-project/netsu

.. image:: https://coveralls.io/repos/github/netsu-project/netsu/badge.svg?branch=master
    :target: https://coveralls.io/github/netsu-project/netsu?branch=master


Get sources:

.. code:: shell

    git clone https://github.com/netsu-project/netsu
    cd netsu

Run checks and unit tests:

.. code:: shell

    pip3 install tox
    python3 -m tox

Install latest master release via pip:

.. code:: shell

    # install uwsgi and uwsgi-plugin-python3 via your favourite package manager
    pip3 install netsu

Install from sources:

.. code:: shell

    # install uwsgi and uwsgi-plugin-python3 via your favourite package manager
    python3 setup.py sdist
    cd dist
    pip3 install netsu*

Some usage examples:

.. code:: shell

    # start service
    systemctl start netsud

    # query for running config
    netsu-ctl get running-config

    # query for system config
    netsu-ctl get system-config

    # query for system state
    netsu-ctl get system-state

    # set empty running config
    netsu-ctl set running-config '{}'

    # configure nic-bond-vlan-bridge and rollback if lost connectivity
    # (requires netsu-plugin-networkmanager and netsu-plugin-connectivitycheck)
    netsu-ctl set running-config \
    '{
      "nm_bridge": {
        "br0": {
          "ipv4": {
            "method": "manual",
            "addresses": [
              {"address": "192.168.10.2", "prefix": 24}
            ],
            "gateway": "192.168.10.1"
          }
        }
      },
      "nm_vlan": {
        "vlan10": {
          "device": "bond1",
          "id": 10,
          "master": {"name": "br0", "type": "bridge"}
        }
      },
      "nm_bond": {
        "bond1": {
          "mode": "balance-rr"
        }
      },
      "nm_ethernet": {
        "ens3": {
          "master": {"name": "bond1", "type": "bond"}
        }
      }
    }' \
    '{"connectivitycheck_ping": {"address": "www.github.com"}}'

    # save running config into persistent
    netsu-ctl set persistent-config --copy-from-table running-config
