import redis
import time

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
WORK_QUEUE = "filter_queue_prueba"

def medir_tiempo_procesado():
    print("Procesando elementos de la cola...")
    start = time.time()
    count = 0

    while True:
        texto = client.lpop(WORK_QUEUE)
        if texto is None:
            break
        print(f"[{count}] {texto}")
        count += 1
        time.sleep(0.1)

    end = time.time()
    print(f"\nSe procesaron {count} textos en {round(end - start, 2)} segundos.")

if __name__ == "__main__":
    medir_tiempo_procesado()

