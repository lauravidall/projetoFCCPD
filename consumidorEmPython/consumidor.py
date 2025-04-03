import pika
import time
import uuid  # Para criar um identificador único para cada consumidor

EXCHANGE_NAME = "reserva_livros"
generos = ['Ficcao', 'Fantasia', 'Misterio', 'Romance', 'Terror', 'Biografia', 'Ciencia', 'Historia', 'Poesia']

def conectar_fila(routing_key):
    while True:
        try:
            conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            canal = conexao.channel()

            # Garante que a exchange existe
            canal.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)

            # Cria uma fila EXCLUSIVA e TEMPORÁRIA para cada cliente
            result = canal.queue_declare(queue='', exclusive=True)  
            queue_name = result.method.queue  

            # Faz o bind da fila exclusiva para a exchange com a routing key do gênero
            canal.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=routing_key)

            print(f"Consumidor conectado na fila {queue_name} com routing key {routing_key}")

            return conexao, canal, queue_name
        except pika.exceptions.AMQPConnectionError:
            print("Conexão perdida. Tentando reconectar em 3 segundos...")
            time.sleep(3)

def consumir_mensagens(genero):
    routing_key = f"reserva.{genero}"

    conexao, canal, queue_name = conectar_fila(routing_key)

    print(f"\nAguardando reservas de livros do gênero: {genero}.")
    print("Pressione 'CTRL+C' para sair")

    def callback(ch, method, properties, body):
        print(f"Reserva recebida! Detalhes: {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    try:
        canal.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
        canal.start_consuming()
    except KeyboardInterrupt:
        print("\nParando o consumo de mensagens...")
    finally:
        conexao.close()

def main():
    while True:
        print("\nEscolha um gênero para filtrar as reservas de livros:")
        for i, genero in enumerate(generos, start=1):
            print(f"{i}. {genero}")
        print("0. Sair")

        escolha = input("Digite o número do gênero desejado: ")
        
        if escolha == '0':
            print("Saindo...")
            break
        
        try:
            indice_escolhido = int(escolha) - 1
            if 0 <= indice_escolhido < len(generos):
                consumir_mensagens(generos[indice_escolhido])
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Escolha inválida. Digite um número.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma encerrado.")
