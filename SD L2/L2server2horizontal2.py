import Pyro4
import random
import threading
import time
import re
import sys

@Pyro4.expose
@Pyro4.behavior(instance_mode="percall")
class InsultServer:
    def __init__(self):
        self.lista_insultos = {"tonto", "payaso", "subnormal"}
        self.observers = []

    def guardar_insulto(self, insulto):
        time.sleep(0.2)
        if insulto not in self.lista_insultos:
            self.lista_insultos.add(insulto)
            return f"Insulto '{insulto}' añadido a la lista."
        return f"El insulto '{insulto}' ya está en la lista."

    def mostrar_todos_insultos(self):
        time.sleep(0.2)
        return list(self.lista_insultos)

    def publicar_insulto_random(self):
        time.sleep(0.2)
        if self.lista_insultos:
            return random.choice(list(self.lista_insultos))
        return "No hay insultos disponibles."

    def suscribirse(self, observer_uri):
        if observer_uri not in self.observers:
            self.observers.append(observer_uri)
            return f"Suscripción exitosa del cliente {observer_uri}."
        return f"El cliente {observer_uri} ya está suscrito."

    def notificar_observadores(self):
        while True:
            if self.lista_insultos and self.observers:
                insulto_random = self.publicar_insulto_random()
                for observer_uri in self.observers:
                    try:
                        observer = Pyro4.Proxy(observer_uri)
                        observer.update(insulto_random)
                    except Pyro4.errors.CommunicationError:
                        print(f"Error notificando a {observer_uri}. Eliminando...")
                        self.observers.remove(observer_uri)
            time.sleep(5)

def iniciar_servidor(nodo_id):
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()

    insult_server = InsultServer()

    insult_server_uri = daemon.register(insult_server)
    ns.register(f"insult.server.{nodo_id}", insult_server_uri)

    print(f"Servidor {nodo_id} activo en URI: {insult_server_uri}")

    # Lanzar el hilo de notificaciones
    threading.Thread(target=insult_server.notificar_observadores, daemon=True).start()

    daemon.requestLoop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Debes pasar el ID del nodo como argumento. Ejemplo:")
        print("   python3 insult_server.py 1")
        sys.exit(1)

    nodo_id = sys.argv[1]
    iniciar_servidor(nodo_id)
