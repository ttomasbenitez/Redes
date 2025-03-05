# TP1-Redes
Primer TP de la Materia Redes de la Facultad de Ingeniera de la UBA


## Ejecución

#### Mininet

Crear la topología con cuatro host: un servidor y tres clientes.

```
sudo mn --topo single,4 --link tc,loss=10
```

En caso de tener un archivo python que lo customize entonces usar:

```
sudo mn --custom topo.py --topo mytopo
```

Abrir cada uno de los hosts. Ejemplo para el host h1:

```
xterm h1
```

#### Servidor

Abrir el servidor en el host h1 (mininet le asigna la ip 10.0.0.1), que escuche en el puerto 12000 y con ubicación en `/home/user1/Escritorio/`

```
python3 start-server.py -H 10.0.0.1 -p 12000 -s /home/user1/Escritorio/
```

#### Cliente

##### Upload

Subir un archivo. En este caso se envía un archivo llamado *mi_archivo.txt* a la IP y puerto del server, y se guardará como *mi_archivo_subido.txt*.

```
python3 upload.py -H 10.0.0.1 -p 12000 -s /home/user1/Escritorio/mi_archivo.txt --pro sw -n mi_archivo_subido.txt
```

##### Download

Descargar un archivo. En este caso se descarga un archivo llamado *mi_archivo.txt* del server, y se guardará como *mi_archivo_descargado.txt*.

```
python3 download.py -H 10.0.0.1 -p 12000 -n mi_archivo.txt --pro sw -d mi_archivo_descargado.txt
```
### Verificación de Integridad
Usar el comando:
```
md5sum archivo1 archivo2 | awk '{print $1}' | sort | uniq -c

```
Si los hashes son iguales sube el contador.

### Conectividad
__WARNING: Esto debe ser dentro de la shell de mininet no en  xterm__
Usar el comando:
```
pingall

```
