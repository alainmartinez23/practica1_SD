### server.py ###
import redis
import time
import random
from threading import Thread

# Conectar a Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
INSULTS_LIST = "insults"
BROADCAST_CHANNEL = "insult_broadcast"
FILTERED_TEXTS = "filtered_texts"
WORK_QUEUE = "filter_queue"

# Función para obtener todos los insultos
def get_insults():
    return list(client.smembers(INSULTS_LIST))

# Función para obtener un insulto aleatorio
def get_random_insult():
    insults = get_insults()
    if insults:
        return random.choice(insults)
    return "No hay insultos disponibles."

# Función para publicar un insulto cada 5 segundos
def insult_broadcaster():
    while True:
        insult = get_random_insult()
        if insult != "No hay insultos disponibles.":
            client.publish(BROADCAST_CHANNEL, insult)
        time.sleep(5)

# Función para filtrar un texto
def filter_text(text):
    insults = get_insults()
    for insult in insults:
        text = text.replace(insult, "CENSORED")
    client.rpush(FILTERED_TEXTS, text)
    return text

# Procesador de la cola de trabajo
def filter_worker():
    while True:
        text = client.lpop(WORK_QUEUE)
        if text:
            filter_text(text)
        time.sleep(1)

# Inicio el broadcast en un thread
thread_broadcast = Thread(target=insult_broadcaster, daemon=True)
thread_broadcast.start()

# Iniciar el worker en un hilo
thread_filter = Thread(target=filter_worker, daemon=True)
thread_filter.start()

print("InsultServer corriendo... Esperando peticiones.")
while True:
    time.sleep(1)  # Mantener el servidor en ejecución