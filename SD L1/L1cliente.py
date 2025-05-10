#cliente
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import threading


s = xmlrpc.client.ServerProxy('http://localhost:8000')

def recibir_insulto(insulto):
    # Función para recibir insultos aleatorios del servidor
    print(f"\nInsulto recibido: {insulto}")

def iniciar_servidor_cliente():
    # Servidor interno del cliente para recibir insultos
    with SimpleXMLRPCServer(("localhost", 9000), allow_none=True, logRequests=False) as server:
        server.register_function(recibir_insulto, "recibir_insulto")
        print("Servidor cliente escuchando en puerto 9000 para insultos...")
        server.serve_forever()

# Uso un thread para el broadcast de insultos
cliente_thread = threading.Thread(target=iniciar_servidor_cliente, daemon=True)
cliente_thread.start()

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

while True:
    opciones()
    opcion = input("Elige: ")

    if opcion == "1":
        insulto = input("Añade el insulto: ")
        print(s.guardar_insulto(insulto.lower()))

    elif opcion == "2":
        print("Lista de insultos:")
        print("\n".join(s.mostrar_todos_insultos()))

    elif opcion == "3":
        print("Insulto aleatorio:", s.publicar_insulto_random())

    elif opcion == "4":
        texto = input("Introduce un texto para filtrar: ")
        print("Texto filtrado:", s.filtrar_texto(texto))

    elif opcion == "5":
        print("Textos filtrados:")
        print("\n".join(s.obtener_textos_filtrados()))

    elif opcion == "6":
        print("Suscribiéndose al broadcast de insultos...")
        print(s.suscribirse("http://localhost:9000"))

    elif opcion == "7":
        print("Hasta luego")
        break

    else:
        print("Opción no válida.")


    