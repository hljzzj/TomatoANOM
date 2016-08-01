环境:
scapy
sudo gedit /usr/local/lib/python2.7/dist-packages/scapy/all.py
注释掉下面3个内容
#if conf.ipv6_enabled:
# from utils6 import *
# from route6 import *
MySQLdb
srp
ARP
Ether
conf