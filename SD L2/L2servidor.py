import Pyro4
import random
import threading
import time
import re


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class InsultServer:
    def __init__(self):
        self.lista_insultos = {"tonto", "payaso", "subnormal"}  # Uso set para evitar duplicados
        self.observers = []  # Suscriptores broadcasting

    def guardar_insulto(self, insulto):
        if insulto not in self.lista_insultos:
            self.lista_insultos.add(insulto)
            return f"Insulto '{insulto}' añadido a la lista."
        return f"El insulto '{insulto}' ya está en la lista."

    def mostrar_todos_insultos(self):
        return list(self.lista_insultos)

    def publicar_insulto_random(self):
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
            time.sleep(5)  # Enviar cada 5 segundos


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class InsultFilter:
    def __init__(self):
        self.textos_filtrados = []

    def filtrar_texto(self, texto, lista_insultos):
        patron = r'\b(' + '|'.join(re.escape(insulto) for insulto in lista_insultos) + r')\b'
        texto_filtrado = re.sub(patron, "CENSORED", texto, flags=re.IGNORECASE)
        self.textos_filtrados.append(texto_filtrado)
        return texto_filtrado

    def obtener_textos_filtrados(self):
        return self.textos_filtrados


def iniciar_servidor():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()

    insult_server = InsultServer()
    insult_filter = InsultFilter()
    
    insult_server_uri = daemon.register(insult_server)
    insult_filter_uri = daemon.register(insult_filter)
    
    ns.register("insult.server", insult_server_uri)
    ns.register("insult.filter", insult_filter_uri)

    # Iniciar el broadcast en un hilo separado
    broadcaster_thread = threading.Thread(target=insult_server.notificar_observadores, daemon=True)
    broadcaster_thread.start()

    print(f"Servidor de insultos activo. URI: {insult_server_uri}")
    print(f"Filter service activo. URI: {insult_filter_uri}")

    daemon.requestLoop()


if __name__ == "__main__":
    iniciar_servidor()
