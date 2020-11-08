# HuaweiSMSender
Python script to send SMS using Huawei new[er] USB dongles via the HTTP interface

# Howto
1. Install prerequisites
2. Use the script (detailed instructions will come soon, but the whole cocept is quite simple)

# Compatible devices - tested
Huawei E3372

# Compatible devices - should work
Huawei E3131
Huawei E3131

# Prerequisites

## Mandatory
python-requests

## Recommended
python-bs4

# Resources used:
https://stackoverflow.com/questions/38016641/sending-and-receiving-sms-by-command-line-with-huawei-e3131-and-hilink-on-a-debi
http://www.sunspot.co.uk/Projects/raspberrypi_LAN_master/SMS/SMS-textmessages.html


# Notes on NetworkManager
sudo nmcli
sudo nmcli dev set eth1 managed yes
sudo vim /etc/network/interfaces (just auto lo stuff)
sudo vim /etc/NetworkManager/NetworkManager.conf (ifupdown managed false)
sudo vim /usr/lib/NetworkManager/conf.d/10-globally-managed-devices.conf (unmanaged-devices=*,except:type:wifi,except:type:ethernet)
sudo service network-manager restart

# Notes on setup up interfaces (eth1 on ubuntu raspi)
Manage multiple NetworkManager connections autoconnect and start up priority in Linux.

Configure which NetworkManager connection should be active after system reboot or which connection should be activated when current active connection will be deactivated.

First of all you have to ensure that connection is set to connect automatically.
Every connection is set to connect automatically by default.

You can double-check that connection is set to connect automatically with command:
nmcli c s <con_name> | grep autoconnect

If connection.autoconnect setting is set to “no” you can set it to “yes” with below command:
nmcli c mod <con_name> connection.autoconnect yes

To set autoconnect priority use command:
nmcli c mod <con_name> connection.autoconnect-priority <X>
where X represents priority number.

To review connection priority run command:
nmcli c s <con_name> | grep priority

Higher priority number means higher autoconnect priority so connection with highest priority number will be activated if connection.autoconnect is set to “yes” as well.

To list all NetworkManager connections configured on the server run:
nmcli c s

To list active NetworkManager connection run:
nmcli c s --active

NOTE: Only one NetworkManager connection can be active per one network interface. If you have multiple network interfaces more connections can be active but only one connection per one Network interface.

Review connection’s IP addresses with nmcli connection show command:
nmcli c s con1 | grep -i address
nmcli c s con2 | grep -i address
nmcli c s con3 | grep -i address

Set autoconnect-priority for configured NetworkManager connections:
nmcli c mod con1 connection.autoconnect-priority 1
nmcli c mod con2 connection.autoconnect-priority 2
nmcli c mod con3 connection.autoconnect-priority 3

Review value of autoconnect-priority and also verify that autoconnect is set to “yes”:
nmcli c s con1 | grep autoconnect
nmcli c s con2 | grep autoconnect
nmcli c s con3 | grep autoconnect

Reboot server:
shutdown -r now

After reboot – connection with highest priority will be active (con3 in our case).
nmcli c s --active
ip a

Deactivate NetworkManager connection with highest priority which is con3:
nmcli con down con3

NetworkManager connection with second highest priority will become active.
Review active NetworkManager connection:
nmcli c s --active
ip a

Deactivate NetworkManager connection with second highest priority which is con2:
nmcli con down con2

NetworkManager connection with lower priority will become active.
Review active NetworkManager connection:
nmcli c s --active
ip a

Add fourth NetworkManager connection:
nmcli con add con-name con4 type ethernet ifname eth0

This connection was set-up as “auto” – Automatic (Dynamic – DHCP) connection by default.
nmcli c s con4 | grep method

NetworkManager priority of newly added connection is automatically set to “0” by default and autoconnect is set to “yes” by default.
nmcli c s con4 | grep autoconnect

Activate new NetworkManager connection:
nmcli con up con4

Confirm that con4 NetworkManager connection is now active:
nmcli c s --active
ip a

Reboot server
shutdown -r now

Review active NetworkManager connection which is con3 because it has highest autoconnect-priority:
nmcli c s
nmcli c s --active
ip a
