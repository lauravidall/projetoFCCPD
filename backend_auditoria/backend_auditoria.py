import pika

EXCHANGE_NAME = 'agendamento_consultas'

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)

    queue_name = 'auditoria_fila'
    channel.queue_declare(queue=queue_name, durable=True)

    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key='#')

    print(" [*] Aguardando mensagens de todos os tipos. Para sair, pressione CTRL+C")

    def callback(ch, method, properties, body):
        print(f" [x] Recebeu: {body.decode()}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    main()
