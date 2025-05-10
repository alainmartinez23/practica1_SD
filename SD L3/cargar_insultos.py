# cargar_insultos.py
import redis
import random
import time

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
WORK_QUEUE = "filter_queue_prueba"

NUM_INSULTOS = 1000

def cargar_insultos():
    client.delete(WORK_QUEUE)  # Limpiar cola
    start = time.time()
    for i in range(NUM_INSULTOS):
        texto = f"Texto con insulto_{random.randint(1, 1000)} incluido #{i}"
        client.rpush(WORK_QUEUE, texto)
    end = time.time()
    print(f"Hecho. Se han cargado {NUM_INSULTOS} en {round(end - start, 2)} segundos")


if __name__ == "__main__":
    cargar_insultos()
