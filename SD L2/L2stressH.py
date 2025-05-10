import Pyro4
import random
import time
from multiprocessing import Pool

# Nodos disponibles
nodos = [
    "PYRONAME:insult.server.1", 
    "PYRONAME:insult.server.2",
    "PYRONAME:insult.server.3",
    "PYRONAME:insult.server.4",
    #"PYRONAME:insult.server.5",
    #"PYRONAME:insult.server.6",
    #"PYRONAME:insult.server.7",
    #"PYRONAME:insult.server.8",
    #"PYRONAME:insult.server.9",
    #"PYRONAME:insult.server.10"
]

# Función que se ejecutará en paralelo
def realizar_peticion(i):
    nodo_uri = nodos[i % len(nodos)]
    try:
        servidor = Pyro4.Proxy(nodo_uri)
        insulto = servidor.publicar_insulto_random()
        return insulto
    except Pyro4.errors.CommunicationError as e:
        return f"Error en la conexión con {nodo_uri}: {str(e)}"

# Stress test
NUM_PETICIONES = 1000
PROCESOS = 200

if __name__ == "__main__":
    start_time = time.time()
    errores = 0

    with Pool(processes=PROCESOS) as pool:
        resultados = pool.map(realizar_peticion, range(NUM_PETICIONES))

    for r in resultados:
        if "Error" in r:
            errores += 1

    end_time = time.time()

    # Resultados
    print("----Stress test multiprocessing completado----")
    print(f"Total de peticiones: {NUM_PETICIONES * PROCESOS}")
    print(f"Tiempo total: {round(end_time - start_time, 2)} segundos")
    print(f"Errores detectados: {errores}")
