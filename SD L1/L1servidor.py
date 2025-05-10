# servidor
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import random
import re
import time
import threading

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()


    class Insultos:
        def __init__(self):
            # lo hago como set para que no haya insultos repetidos
            self.lista_insultos = {"inutil", "torpe", "tonto", "retrasado", "payaso"}
            self.textos_filtrados = []
            self.suscriptores = []

        def guardar_insulto( self, insult):
            # desde la parte del cliente mandaré el insulto en minúsculas para que no haya duplicados
            self.lista_insultos.add(insult)
            return f"Insulto '{insult}' añadido"
        
        def mostrar_todos_insultos(self):
            return list(self.lista_insultos)
        
        def publicar_insulto_random(self):
            if self.lista_insultos:
                return random.choice(list(self.lista_insultos))
            return "De momento no hay insultos."
        
        def filtrar_texto(self, texto):
            if not self.lista_insultos:
                return "No hay insultos para filtrar"
            
            patron = r'\b(' + '|'.join(re.escape(insulto) for insulto in self.lista_insultos) + r')\b'
            texto_filtrado = re.sub(patron, "CENSORED", texto, flags=re.IGNORECASE)

            self.textos_filtrados.append(texto_filtrado)
            return texto_filtrado
        
        def obtener_textos_filtrados(self):
            return self.textos_filtrados
        
        # Patrón observer
        def suscribirse(self, client_url):
            # Permite a un cliente suscribirse al broadcasting.
            if client_url not in self.suscriptores:
                self.suscriptores.append(client_url)
                return f"Cliente {client_url} suscrito correctamente."
            return f"Cliente {client_url} ya estaba suscrito."
        
        def desuscribirse(self, client_url):
            # Permite a un cliente dejar de recibir insultos
            if client_url in self.suscriptores:
                self.suscriptores.remove(client_url)
                return f"Cliente {client_url} eliminado de la lista de suscriptores."
            return f"Cliente {client_url} no estaba suscrito."
        
        def notificar_observadores(self):
            # Notifica a todos los observadores con un insulto random cada 5 segundos
            while True:
                if self.lista_insultos and self.suscriptores:
                    insulto_random = self.publicar_insulto_random()
                    for subscriber_url in self.suscriptores:
                        try:
                            cliente = xmlrpc.client.ServerProxy(subscriber_url)
                            cliente.recibir_insulto(insulto_random)
                        except Exception as e:
                            print(f"Error enviando a {subscriber_url}: {e}")
                            self.suscriptores.remove(subscriber_url)  # Eliminar cliente no disponible
                time.sleep(5)
        

    servidor_insultos = Insultos()
    server.register_instance(servidor_insultos)

    observer_thread = threading.Thread(target=servidor_insultos.notificar_observadores, daemon=True)
    observer_thread.start()

    print("Servidor activo!!")
    server.serve_forever()