import pika
import uuid
import json

class InsultClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, action, data=None):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='insult_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id),
            body=json.dumps({"action": action, "data": data}))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

if __name__ == "__main__":
    client = InsultClient()

    while True:
        print("\nOpciones:")
        print("1. Añadir insulto")
        print("2. Obtener insulto aleatorio")
        print("3. Ver lista de insultos")
        print("4. Enviar texto para censurar")
        print("5. Ver textos censurados")
        print("6. Salir")
        opcion = input("Selecciona opción: ")

        if opcion == "1":
            insulto = input("Introduce insulto: ")
            res = client.call("add", insulto)
        elif opcion == "2":
            res = client.call("get")
        elif opcion == "3":
            res = client.call("list")
        elif opcion == "4":
            texto = input("Introduce texto: ")
            res = client.call("filter_text", texto)
        elif opcion == "5":
            res = client.call("get_filtered_texts")
        elif opcion == "6":
            break
        else:
            res = {"status": "error", "message": "Opción inválida"}

        print("→", res)
