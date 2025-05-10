import xmlrpc.client
import multiprocessing
import time
import random

# CONFIGURACIÓN
NUM_PROCESOS = 100
NUM_PETICIONES_POR_PROCESO = 50
SERVIDORES = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    #"http://localhost:8003",
    #"http://localhost:8004",
    #"http://localhost:8005",
    #"http://localhost:8006",
    #"http://localhost:8007",
    #"http://localhost:8008",
    #"http://localhost:8009"
] 

# Reparto round-robin
def get_server_proxy(index):
    url = SERVIDORES[index % len(SERVIDORES)]
    return xmlrpc.client.ServerProxy(url, allow_none=True)

def cliente_simulado(proc_index):
    errores = 0
    for i in range(NUM_PETICIONES_POR_PROCESO):
        try:
            proxy = get_server_proxy(proc_index + i)
            proxy.guardar_insulto(f"insulto_{proc_index}_{i}_{random.randint(0, 10000)}")
            proxy.publicar_insulto_random()
        except Exception as e:
            errores += 1
    return errores

def ejecutar_test():
    print(f"Lanzando stress test con {len(SERVIDORES)} nodo(s)...")
    start = time.time()

    with multiprocessing.Pool(processes=NUM_PROCESOS) as pool:
        errores_por_proceso = pool.map(cliente_simulado, range(NUM_PROCESOS))

    end = time.time()

    errores = sum(errores_por_proceso)
    print("----Stress test completado----")
    print(f"Total de procesos: {NUM_PROCESOS}")
    print(f"Peticiones por proceso: {NUM_PETICIONES_POR_PROCESO}")
    print(f"Peticiones totales: {NUM_PROCESOS * NUM_PETICIONES_POR_PROCESO}")
    print(f"Tiempo total: {round(end - start, 2)} segundos")
    print(f"Errores detectados: {errores}")

if __name__ == "__main__":
    ejecutar_test()
