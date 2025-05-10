# PRÁCTICA 1


## Aclaración inicial

Aquí simplemente se explica cómo ejecutar las pruebas, no el funcionamiento, para ello está el PDF.
Todas los tests están pensados para que funcione en Linux, no se ha comprobado si funciona en otros
sistemas operativos (podrían variar IPs por ejemplo)



# XMLRPC

Implementación básica. Ejecutar por terminal:
python3 L1servidor.py

python3 L1cliente.py


Para ejecutar el stress test:
python3 L1insult.py

python3 L1stress.py



Para ejecutar el escalado horizontal:

python3 L1server2horizontal.py 8000

python3 L1server2horizontal.py 8001

python3 L1server2horizontal.py 8002  // (si solo se quieren dos workers, esta línea se omite)

python3 L1stressHorizontal.py



# PYRO4

Yo tengo Pyro4 en un entorno virtual:

source pryo_env/bin/activate



Primero hay que iniciar el NameServer:

python3 -m Pyro4.naming



Para la implementación básica:

python3 L2servidor.py

python3 L2cliente.py



Para ver el stress test:

python3 L2insult.py

python3 L2stress.py



Para ejecutar el escalado horizontal y su respectivo stress test:

python3 L2server2horizontal2.py 1

python3 L2server2horizontal2.py 2

python3 L2server2horizontal2.py 3  // (Omitir esta línea si se quieren 2 servidores)

python3 L2stressH.py



# REDIS

Implementación básica. Ejecutar por terminal:

sudo systemctl start redis

python3 L3servidor.py

python3 L3cliente.py



Stress test y escalado horizontal. Primero cargo los insultos, luego lanzo el server o los servers.
Para ejecutar el escalado horizontal (mismo script, sin parámetros, en varias terminales): 

python3 cargar_insultos.py

python3 servidor_py_test.py

python3 servidor_py_test.py

python3 servidor_py_test.py



# RABBITMQ


Implementación básica. Ejecutar por terminal (con rabbitmq iniciado):

python3 L4servidor.py

python3 L4cliente.py



Stress test y escalado horizontal:

python3 servidorH_con_redis3.py (lanzar este script tantas veces como servers se desee)

python3 nuevo_stressH.py



Para el escalado dinámico:

python3 escalador.py

python3 nuevo_stressH.py