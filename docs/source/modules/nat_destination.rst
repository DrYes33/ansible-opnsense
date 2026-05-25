.. _modules_nat_destination:

.. include:: ../_include/head.rst

===============
NAT Destination
===============

**STATE**: stable

**TESTS**: `Playbook <https://github.com/oxlorg/collection_opnsense/blob/latest/tests/nat_destination.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `Destination NAT / Port Forwarding <https://docs.opnsense.org/manual/nat.html#destination-nat-port-forward>`_

Contribution
************

Thanks to `@Rath <https://github.com/superstes>`_ for developing this module!

----

Limitations
***********

This plugin has some limitations you need to know of:

* ports don't support aliases
* each of these parameters only takes ONE value per rule:

  * port
  * protocol (*or 'any'*)
  * ip-protocol (*IPv4/IPv6*)

* interfaces must be provided as used in the network config (*p.e. 'opt1' instead of 'DMZ'*)

  * per example see menu: 'Interface - Assignments - Interface ID (in brackets)'
  * this brings problems if the interface-names are not the same on both nodes when using HA-setups

----

Info
****

Savepoint
=========

You can prevent lockout-situations using the savepoint systems:

- :ref:`oxlorg.opnsense.savepoint <modules_savepoint>`

Web-UI
======

Menu: 'Firewall → NAT → Destination NAT'

Definition
**********

Module alias: oxlorg.opnsense.dnat

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "match_fields","list","true","\-","\-","Fields that are used to match configured rules with the running config - if any of those fields are changed, the module will think it's a new rule. At least one of: 'sequence', 'interface', 'target', 'target_port', 'ip_protocol', 'protocol', 'source_invert', 'source_net', 'source_port', 'destination_invert', 'destination_net', 'destination_port', 'description', 'uuid'"
    "sequence","int","false","1","seq","Sequence for rule processing, Integer between 1 and 999999"
    "interface","string","false for deletion, else true","\-","i, int","The interface to match this rule on"
    "ip_protocol","string","false","'inet'","ip, ip_proto","IP protocol to match. One of: 'inet', 'inet6', 'inet46' (*IPv4 = 'inet', IPv6 = 'inet6', Both = 'inet46'*)"
    "protocol","string","false","'any'","p, proto","Protocol like 'TCP', 'UDP', 'ICMP', 'TCP/UDP' and so on. For options see the WEB-UI."
    "source_invert","boolean","false","false","si, src_inv, src_not","Inverted matching of the source"
    "source_net","string","false","'any'","s, src, source","Host, network, alias or 'any'"
    "source_port","string","false","\-","sp, src_port","Leave empty to allow all, valid port-number, name, alias or range"
    "destination_invert","boolean","false","false","di, dest_inv, dest_not","Inverted matching of the destination"
    "destination_net","string","false","'any'","d, dest, destination","Host, network, alias or 'any'"
    "destination_port","string","false","\-","dp, dest_port","Leave empty to allow all, valid port-number, name, alias or range"
    "target","string","false for deletion, else true","\-","tgt, t","NAT translation target - Packets matching this rule will be mapped to the IP address given here. Host, network or alias"
    "target_port","int","false","\-","np, nat_port","Redirect target port on the NAT translation target"
    "log","boolean","false","true","l","If rule matches should be shown in the firewall logs"
    "description","string","false","\-","name, desc","Description for the rule"
    "state","string","false","'present'","st","State of the rule. One of: 'present', 'absent'"
    "enabled","boolean","false","true","en","If the rule should be en- or disabled"
    "uuid","string","false","\-","\-","Optionally you can supply the uuid of an existing rule"
    "reload","boolean","false","true","apply", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

----

Usage
*****

First you will have to know about **rule-matching**.

The module somehow needs to link the configured and existing rules to manage them.

You need to set how this matching is done by setting the 'match_fields' parameter!

It is **recommended** to use/set **unique identifiers** like 'description' to make sure rules can be matched without overlapping.

You could also use the UUID of existing rules as ID - but you would have to pull (*list*) and configure those 'manually'.

----

Examples
********

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.nat_destination:
          match_fields: ['description']

        oxlorg.opnsense.list:
          target: 'nat_destination'

      tasks:
        - name: Example
          oxlorg.opnsense.nat_destination:
            description: 'example'
            match_fields: ['description']
            target: '192.168.0.10'
            target_port: 443
            interface: 'wan'
            protocol: 'TCP'
            destination_net: 'wanip'
            destination_port: '443'
            # sequence: 1
            # ip_protocol: 'inet'
            # source_invert: false
            # source_net: 'any'
            # source_port: 'any'
            # destination_invert: false
            # log: true
            # enabled: true
            # debug: false
            # state: 'present'
            # reload: true

        - name: Adding rule
          oxlorg.opnsense.nat_destination:
            description: 'test1'
            source: 'any'
            destination: 'wanip'
            destination_port: '443'
            target: '192.168.0.10'
            target_port: 443
            interface: 'wan'
            protocol: 'TCP'
            # match_fields: ['description']

        - name: Disabling rule
          oxlorg.opnsense.nat_destination:
            description: 'test1'
            source: 'any'
            destination: 'wanip'
            destination_port: '443'
            target: '192.168.0.10'
            target_port: 443
            interface: 'wan'
            protocol: 'TCP'
            enabled: false
            # match_fields: ['description']

        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'nat_destination'
          register: existing_entries

        - name: Printing peers
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Removing rule
          oxlorg.opnsense.nat_destination:
            description: 'test1'
            state: 'absent'
            # match_fields: ['description']
