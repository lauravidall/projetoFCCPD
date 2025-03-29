import pika

EXCHANGE_NAME = 'reservas_livros'

def auditoria():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)

    queue_name = 'auditoria_fila'
    channel.queue_declare(queue=queue_name, durable=True)

    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key='#')

    print(" [*] Aguardando reservas de livros. Para sair, pressione CTRL+C")

    def callback(ch, method, properties, body):
        print(f" [x] Reserva auditada: {body.decode()}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    auditoria()