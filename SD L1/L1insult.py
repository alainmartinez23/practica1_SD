# Este código solo contiene el InsultServer, y es una versión reducida
# que la he utilizado para hacerle el stress test

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import random

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    class InsultServer:
        def __init__(self):
            self.lista_insultos = set()  # Pongo un set para no tener duplicados

        def guardar_insulto(self, insulto):
            if insulto not in self.lista_insultos:
                self.lista_insultos.add(insulto)
                return f"Insulto '{insulto}' añadido correctamente."
            else:
                return f"Insulto '{insulto}' ya estaba en la lista."

        def mostrar_todos_insultos(self):
            return list(self.lista_insultos)

        def publicar_insulto_random(self):
            if self.lista_insultos:
                return random.choice(list(self.lista_insultos))
            return "No hay insultos disponibles."

    servidor = InsultServer()
    server.register_instance(servidor)

    print("InsultServer activo en http://localhost:8000")
    server.serve_forever()
