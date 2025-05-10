### client.py ###
import redis
import random
from threading import Thread

def listen_broadcast():
    BROADCAST_CHANNEL = "insult_broadcast"
    client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    pubsub = client.pubsub()
    pubsub.subscribe(BROADCAST_CHANNEL)
    print("Escuchando broadcast de insultos...")
    for message in pubsub.listen():
        if message["type"] == "message":
            print("\n[Broadcast]", message["data"])

def menu():
    client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    INSULTS_LIST = "insults"
    FILTERED_TEXTS = "filtered_texts"
    WORK_QUEUE = "filter_queue"
    
    listening = False
    while True:
        print("""
1. Añadir un insulto.
2. Ver toda la lista de insultos disponibles.
3. Obtener un insulto aleatorio.
4. Filtrar un texto.
5. Ver textos filtrados.
6. Suscribirse al broadcast de insultos.
7. Salir.
""")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            insult = input("Ingrese un insulto: ")
            client.sadd(INSULTS_LIST, insult)
            print(f"Insulto '{insult}' agregado.")
        elif opcion == "2":
            print("Lista de insultos:", list(client.smembers(INSULTS_LIST)))
        elif opcion == "3":
            insults = list(client.smembers(INSULTS_LIST))
            if insults:
                print("Insulto aleatorio:", random.choice(insults))
            else:
                print("No hay insultos disponibles.")
        elif opcion == "4":
            text = input("Ingrese un texto: ")
            client.rpush(WORK_QUEUE, text)
            print("Texto enviado para filtrado.")
        elif opcion == "5":
            print("Textos filtrados:", list(client.lrange(FILTERED_TEXTS, 0, -1)))
        elif opcion == "6":
            if not listening:
                Thread(target=listen_broadcast, daemon=True).start()
                listening = True
                print("Suscripción al broadcast activada.")
            else:
                print("Ya estás suscrito al broadcast.")
        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

print("Cliente iniciado...")
menu()
