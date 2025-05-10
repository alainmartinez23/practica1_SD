import Pyro4
import random
import time
from multiprocessing import Pool

# Parámetros configurables
NUM_PROCESOS = 100
NUM_PETICIONES_POR_PROCESO = 50

# Lista de insultos de prueba
INSULTOS_PRUEBA = [
    "subnormal", "inútil", "tonto", "retrasado", "hdp",
    "anormal", "pelele", "payaso", "bobo"
]

def cliente_simulado(_):
    errores = 0
    try:
        insult_server = Pyro4.Proxy("PYRONAME:insult.server")

        for _ in range(NUM_PETICIONES_POR_PROCESO):
            accion = random.choice(["añadir", "lista", "recibir"])
            if accion == "añadir":
                insulto = random.choice(INSULTOS_PRUEBA)
                insult_server.guardar_insulto(insulto)
            elif accion == "lista":
                insult_server.mostrar_todos_insultos()
            elif accion == "recibir":
                insult_server.publicar_insulto_random()
    except Exception:
        errores += 1
    return errores

def ejecutar_test():
    start = time.time()
    with Pool(processes=NUM_PROCESOS) as pool:
        resultados = pool.map(cliente_simulado, range(NUM_PROCESOS))
    end = time.time()

    errores = sum(resultados)
    print("----Stress test completado----")
    print(f"Total de procesos: {NUM_PROCESOS}")
    print(f"Peticiones por proceso: {NUM_PETICIONES_POR_PROCESO}")
    print(f"Peticiones totales: {NUM_PROCESOS * NUM_PETICIONES_POR_PROCESO}")
    print(f"Tiempo total: {round(end - start, 2)} segundos")
    print(f"Errores detectados: {errores}")
    

if __name__ == "__main__":
    ejecutar_test()

