import pika

EXCHANGE_NAME = 'reservas_livros'
QUEUE_NAME = 'auditoria_fila'
ROUTING_KEY = '#'

def configurar_conexao():
    conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conexao.channel()
    canal.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)
    canal.queue_declare(queue=QUEUE_NAME, durable=True)
    canal.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)
    return conexao, canal

def consumir_mensagens(canal):
    print(" [*] Aguardando reservas de livros. Para sair, pressione CTRL+C")
    canal.basic_consume(queue=QUEUE_NAME, on_message_callback=lambda ch, method, properties, body: print(f" [x] Reserva auditada: {body.decode()}"), auto_ack=True)
    canal.start_consuming()

def auditoria():
    conexao, canal = configurar_conexao()
    try:
        consumir_mensagens(canal)
    except KeyboardInterrupt:
        print("\n [!] Interrompido pelo usuário.")
    finally:
        conexao.close()

if __name__ == '__main__':
    auditoria()
