import redis
import time
import random
from threading import Thread

# Conectar a Redis (único Redis, puerto 6379)
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

INSULTS_LIST = "insults"
FILTERED_TEXTS = "filtered_texts2"
WORK_QUEUE = "filter_queue2"

# Obtener insultos
def get_insults():
    return list(client.smembers(INSULTS_LIST))

# Insulto aleatorio
def get_random_insult():
    insults = get_insults()
    if insults:
        return random.choice(insults)
    return "No hay insultos disponibles."

# Worker que filtra textos en cola
def filter_worker(worker_id):
    print(f"[Worker {worker_id}] Iniciado")
    while True:
        text = client.lpop(WORK_QUEUE)
        if text:
            insults = get_insults()
            for insult in insults:
                text = text.replace(insult, "CENSORED")
            client.rpush(FILTERED_TEXTS, text)
            print(f"[Worker {worker_id}] Texto filtrado: {text}")
        else:
            print(f"[Worker {worker_id}] Sin textos en cola. Esperando...")
        time.sleep(0.1)

if __name__ == "__main__":

    # Identificador del worker
    worker_id = random.randint(1000, 9999)

    print(f"[Servidor Worker {worker_id}] Corriendo...")
    filter_worker(worker_id)
    

