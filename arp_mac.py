# -*- coding: utf-8 -*-

import os
import sys
from scapy.all import srp,Ether,ARP,conf


ipscan = '192.168.0.1/24'
try:
    ans,unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ipscan),timeout=60,verbose=False)
except Exception,e:
    print str(e)
else:
    for snd,rcv in ans:
        list_mac = rcv.sprintf("%Ether.src% - %ARP.psrc%")
        print list_mac
