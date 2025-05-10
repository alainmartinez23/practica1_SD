import xmlrpc.client
import random
import time
import multiprocessing

SERVER_URL = "http://localhost:8000"
NUM_PROCESOS = 100  # Número de clientes simulados
NUM_PETICIONES_POR_PROCESO = 10 # Peticiones que hace cada proceso

INSULTOS_PRUEBA = [
    "subnormal", "inútil", "tonto", "retrasado", "hdp",
    "anormal", "pelele", "payaso", "bobo"
]

def cliente_simulado(num_peticiones=10):
    cliente = xmlrpc.client.ServerProxy(SERVER_URL)
    resultados = []

    for _ in range(num_peticiones):
        accion = random.choice(["añadir", "recibir", "lista"])

        try:
            if accion == "añadir":
                insulto = random.choice(INSULTOS_PRUEBA) + "_" + str(random.randint(0, 100000))
                resultado = cliente.guardar_insulto(insulto)
            elif accion == "recibir":
                resultado = cliente.publicar_insulto_random()
            elif accion == "lista":
                resultado = cliente.mostrar_todos_insultos()
            resultados.append(resultado)
        except Exception as e:
            resultados.append(f"###Error: {e}")

    return resultados

def ejecutar_stress_test():
    print(f"Lanzando stress test con {NUM_PROCESOS} procesos...")
    start = time.time()

    with multiprocessing.Pool(processes=NUM_PROCESOS) as pool:
        resultados = pool.starmap(cliente_simulado, [(NUM_PETICIONES_POR_PROCESO,)] * NUM_PROCESOS)

    end = time.time()

    errores = sum(1 for proceso in resultados for r in proceso if isinstance(r, str) and r.startswith("###"))

    print("----Stress test completado----")
    print(f"Total de procesos: {NUM_PROCESOS}")
    print(f"Peticiones por proceso: {NUM_PETICIONES_POR_PROCESO}")
    print(f"Peticiones totales: {NUM_PROCESOS * NUM_PETICIONES_POR_PROCESO}")
    print(f"Tiempo total: {round(end - start, 2)} segundos")
    print(f"Errores detectados: {errores}")

if __name__ == "__main__":
    ejecutar_stress_test()
