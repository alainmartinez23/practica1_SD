# Esté código es únicamente un InsultFilter en el cual aplicaré el stress test

import Pyro4
import random

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class InsultServer:
    def __init__(self):
        self.lista_insultos = {"tonto", "payaso", "subnormal"}

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

def iniciar_servidor():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()

    insult_server = InsultServer()
    insult_server_uri = daemon.register(insult_server)
    ns.register("insult.server", insult_server_uri)

    print(f"Servidor de insultos activo. URI: {insult_server_uri}")
    daemon.requestLoop()

if __name__ == "__main__":
    iniciar_servidor()
