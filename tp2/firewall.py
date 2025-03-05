# Coursera :
# - Software Defined Networking ( SDN ) course
# -- Programming Assignment : Layer -2 Firewall Application Professor : Nick Feamster
# Teaching Assistant : Arpit Gupta
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr, IPAddr
from collections import namedtuple
from lector import leer_json
import os
import json
import pox.lib.packet as pkt
# Add your imports here ...
log = core.getLogger()
# Add your global variables here ...
class Firewall ( EventMixin ) :
    PROTOCOLOS_TP = {
        "tcp": pkt.ipv4.TCP_PROTOCOL,
        "udp": pkt.ipv4.UDP_PROTOCOL,
        "icmp": pkt.ipv4.ICMP_PROTOCOL
    }

    PROTOCOLOS_NW = {
        "ipv4": pkt.ethernet.IP_TYPE,
        "ipv6": pkt.ethernet.IPV6_TYPE
    }

    def __init__ ( self ) :
        self.listenTo(core.openflow )
        self.firewalls = leer_json("firewalls_rules.json")

        log.debug ( " Enabling ␣ Firewall ␣ Module " )
    def _handle_ConnectionUp ( self , event ) :
        # return
        for firewall in self.firewalls:
            if event.dpid == firewall["id_switch"]:
                for regla in firewall["reglas"]:
                    self.agregar_regla(event, regla["politica"])
                    log.debug("Regla: %s , en el switch %s ",regla["definicion"],dpidToStr(event.dpid))
        # Add your logic here ...
        
    def agregar_regla(self, event, regla):
        coincidencias = of.ofp_match()
        #log.debug(regla)

        if "transporte" in  regla:
            self.agregar_reglas_transporte(regla["transporte"], coincidencias)
            #log.debug("transporte")
        if "red" in regla:
            self.agregar_regla_red(regla["red"], coincidencias)
        if "enlace_de_datos" in regla:
            self.agregar_regla_enlace_de_datos(regla["enlace_de_datos"], coincidencias)
               
        mensaje = of.ofp_flow_mod()
        mensaje.match = coincidencias
        #log.debug(coincidencias.tp_dst)
        event.connection.send(mensaje)

    def agregar_reglas_transporte(self, regla_transporte, coincidencias):
        if "puerto_destino" in regla_transporte:
            coincidencias.tp_dst = regla_transporte["puerto_destino"]
            #log.debug("en el destino %d",regla_transporte["puerto_destino"])
        if "puerto_origen" in regla_transporte:
            coincidencias.tp_src = regla_transporte["puerto_origen"]


    def agregar_regla_red(self, regla_red, coincidencias):
        if "protocolo" in regla_red and regla_red["protocolo"] in self.PROTOCOLOS_TP:
            #log.debug(self.PROTOCOLOS_TP[regla_red["protocolo"]])
            coincidencias.nw_proto = self.PROTOCOLOS_TP[regla_red["protocolo"]]

        if "ip_origen" in regla_red:
            coincidencias.nw_src = IPAddr(regla_red["ip_origen"])
        
        if "ip_destino" in regla_red:
            coincidencias.nw_dst = IPAddr(regla_red["ip_destino"])
    
    def agregar_regla_enlace_de_datos(self, regla_enlace, coincidencias):
        if "tipo_ip" in regla_enlace and regla_enlace["tipo_ip"] in self.PROTOCOLOS_NW:
            #log.debug(self.PROTOCOLOS_NW[regla_enlace["tipo_ip"]])
            coincidencias.dl_type = self.PROTOCOLOS_NW[regla_enlace["tipo_ip"]]
        
        if "mac_origen" in regla_enlace:
            coincidencias.dl_src = EthAddr(regla_enlace["mac_origen"])
        
        if "mac_destino" in regla_enlace:
            coincidencias.dl_dst = EthAddr(regla_enlace["mac_destino"])

def launch () :
    # Starting the Firewall module
    core.registerNew(Firewall)