import Pyro4
import threading

@Pyro4.expose
class Cliente:
    def update(self, insulto):
        print(f"\nInsulto recibido: {insulto}\n> ", end="", flush=True)

def opciones():
    print(""" 
1. Añadir un insulto.
2. Ver toda la lista de insultos disponibles.
3. Obtener un insulto aleatorio.
4. Filtrar un texto.
5. Ver textos filtrados.
6. Suscribirse al broadcast de insultos.
7. Salir.
""")

def iniciar_cliente():
    daemon = Pyro4.Daemon()
    cliente = Cliente()
    uri = daemon.register(cliente)
    threading.Thread(target=daemon.requestLoop, daemon=True).start()  # Hilo para escuchar los insultos del broadcast
    return uri

def main():
    ns = Pyro4.locateNS()
    insult_server = Pyro4.Proxy(ns.lookup("insult.server"))  # Obtener URI del servidor de insultos
    filter_service = Pyro4.Proxy(ns.lookup("insult.filter"))  # Obtener URI del servicio de filtrado
    
    client_uri = iniciar_cliente()  # Obtener URI del cliente

    while True:
        opciones()
        opcion = input("Elige: ")

        if opcion == "1":
            insulto = input("Añade el insulto: ").strip().lower()
            print(insult_server.guardar_insulto(insulto))

        elif opcion == "2":
            print("Lista de insultos:")
            print("\n".join(insult_server.mostrar_todos_insultos()))

        elif opcion == "3":
            print("Insulto aleatorio:", insult_server.publicar_insulto_random())

        elif opcion == "4":
            texto = input("Introduce un texto para filtrar: ")
            lista_insultos = insult_server.mostrar_todos_insultos()
            print("Texto filtrado:", filter_service.filtrar_texto(texto, lista_insultos))

        elif opcion == "5":
            print("Textos filtrados:")
            print("\n".join(filter_service.obtener_textos_filtrados()))

        elif opcion == "6":
            print(insult_server.suscribirse(client_uri))
            print("Te has suscrito al broadcast de insultos.")

        elif opcion == "7":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
