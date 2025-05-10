import pika
import time
import subprocess

MAX_WORKERS = 10
MIN_WORKERS = 3
UMBRAL_SUBIDA = 2   # Si hay más de este número de mensajes -> añadir worker
UMBRAL_BAJADA = 0   # Si no hay mensajes -> bajar workers
INTERVALO_ESCALADO = 3       # Segundos entre chequeos
INTERVALO_MONITOREO = 1

workers = []

def contar_mensajes():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        queue = channel.queue_declare(queue='insult_queue', passive=True)
        return queue.method.message_count
    except Exception as e:
        print(f"Error al consultar la cola: {e}")
        return 0

def lanzar_worker():
    proceso = subprocess.Popen(["python3", "serverH_con_redis3.py"])
    workers.append(proceso)
    print(f"Worker lanzado (PID {proceso.pid})")

def terminar_worker():
    if workers:
        proceso = workers.pop()
        proceso.terminate()
        print(f"Worker terminado (PID {proceso.pid})")

def main():
    # Lanzar los workers iniciales
    for _ in range(MIN_WORKERS):
        lanzar_worker()

    segundos = 0

    try:
        while True:
            mensajes = contar_mensajes()
            print(f"Mensajes en cola: {mensajes} | Workers activos: {len(workers)}")

            if segundos % INTERVALO_ESCALADO == 0:
                if mensajes > UMBRAL_SUBIDA and len(workers) < MAX_WORKERS:
                    lanzar_worker()

                elif mensajes <= UMBRAL_BAJADA and len(workers) > MIN_WORKERS:
                    terminar_worker()

            time.sleep(INTERVALO_MONITOREO)
            segundos += INTERVALO_MONITOREO

    except KeyboardInterrupt:
        print("\nFinalizando todos los workers...")
        while workers:
            terminar_worker()

if __name__ == "__main__":
    main()
