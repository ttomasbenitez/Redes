# tp2-redes
Ejecutar el firewall:
````
python3.8 pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning firewall
````

Ejecutar la topologia (?: representa cualquier numero, menos los negativos):
````
sudo mn --custom topo.py --topo mytopo,agregar_switches=? --mac --arp --switch ovsk   --controller remote
````
