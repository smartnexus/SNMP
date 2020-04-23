# SNMP
Proyecto final Gestión de Redes. Enlace libreria de python: http://snmplabs.com/pysnmp/
<p align="center">
  <img src="https://i.imgur.com/0h2rcH2.png">
</p>

### HOST-RESOURCES-MIB
 Variable | OID | Descripción | Uso
| :---: | --- | --- | :---: |
| hrSystemDate | 1.3.6.1.2.1.25.1.2.0 | Hora exacta del sistema. | DATOS
| hrSystemNumUsers | 1.3.6.1.2.1.25.1.5.0 | Número de sesiones en el dispositivo. | DESCARTE
| hrSystemProcesses | 1.3.6.1.2.1.25.1.6.0 | Número de procesos activos en el dispositivo. | DESCARTE
| hrStorageSize | 1.3.6.1.2.1.25.2.2 | Memoria instalada en el sistem. | DATOS
| hrProcessorTable | 1.3.6.1.2.1.25.3.3.1.2 | Porcentaje de CPU en uso por cada procesador. | DATOS
| hrSWRunTable | 1.3.6.1.2.1.25.4.2 | Procesos que corre el sistema operativo sin contar aplicaciones de usuario. | DESCARTE
| hrSWRunPerfTable | 1.3.6.1.2.1.25.5.1 | Rendimiento de uso de CPU y memoria RAM de cada proceso del sistema operativo. | DESCARTE
| hrSWInstalledTable | 1.3.6.1.2.1.25.6.3 | Aplicaciones instaladas en el dispositivo. | DESCARTE
### LanMgr-MIB  
 Variable | OID | Descripción | Uso
| :---: | --- | --- | :---: |
| domPrimaryDomain | 1.3.6.1.4.1.77.1.4.1.0 | Dominio al que el dispositivo pertenece. | DESCARTE
### RFC1213-MIB  
 Variable | OID | Descripción | Uso
| :---: | --- | --- | :---: |
| sysDescr | 1.3.6.1.2.1.1.1.0 | Tipo de hardware, versión de sistema operativo. | DATOS
| sysUpTime | 1.3.6.1.2.1.1.3.0 | Tiempo de uso del dispositivo. | DATOS
| sysContact | 1.3.6.1.2.1.1.4.0 | Persona de contacto para este nodo en la red. | DATOS
| ipInReceives | 1.3.6.1.2.1.4.3.0 | Número de paquetes recibidos por las distintas interfaces. | DESCARTE
| ipInHdrErrors | 1.3.6.1.2.1.4.4.0 | Número de paquetes descartados por error en las cabeceras ip. | DESCARTE
| ipInAddrErrors | 1.3.6.1.2.1.4.5.0 | Número de paquetes descartados por error en el campo de dirección destino. | DESCARTE
