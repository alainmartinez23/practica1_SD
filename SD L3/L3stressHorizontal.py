import redis
import time
import random
import string

# Configuración
NUM_PETICIONES = 1000 
WORK_QUEUE = "filter_queue2"
FILTERED_TEXTS = "filtered_texts2"

# Conexión a Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Limpiar colas anteriores
client.delete(WORK_QUEUE)
client.delete(FILTERED_TEXTS)

# Generador de textos aleatorios (con algunos insultos)
def generar_texto(insultos):
    insulto = random.choice(list(insultos))
    texto = f"Eres un {insulto}"
    return texto

# Obtener insultos ya existentes en Redis
insultos_actuales = client.smembers("insults2")
if not insultos_actuales:
    client.sadd("insults2", "tonto", "payaso", "subnormal")
    insultos_actuales = client.smembers("insults2")

# Enviar textos a la cola
print("Enviando textos a la cola...")
for _ in range(NUM_PETICIONES):
    texto = generar_texto(insultos_actuales)
    client.rpush(WORK_QUEUE, texto)

# Esperar a que todos los textos sean procesados
print("Esperando que los workers procesen todo...")
start_time = time.time()
errores = 0

while True:
    restantes = client.llen(WORK_QUEUE)
    procesados = client.llen(FILTERED_TEXTS)

    if procesados >= NUM_PETICIONES:
        break

    if restantes == 0 and procesados < NUM_PETICIONES:
        errores += NUM_PETICIONES - procesados
        break

    time.sleep(0.5)

end_time = time.time()

# Resultados
print("----Stress test completado----")
print(f"Total de peticiones: {NUM_PETICIONES}")
print(f"Tiempo total: {round(end_time - start_time, 2)} segundos")
print(f"Textos por segundo: {round(NUM_PETICIONES / (end_time - start_time), 2)}")
print(f"Errores detectados: {errores}")
