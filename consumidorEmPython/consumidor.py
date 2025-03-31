import pika
import time

EXCHANGE_NAME = "reserva_livros"
generos = ['ficcao', 'fantasia', 'misterio', 'romance', 'terror', 'biografia', 'ciencia', 'historia', 'poesia']

def conectar_fila(queue_name, routing_key):
    while True:
        try:
            conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            canal = conexao.channel()
            
            # Declara a exchange (caso ainda não tenha sido criada)
            canal.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)
            
            # Declara a fila
            canal.queue_declare(queue=queue_name, durable=True)
            
            # Faz o binding da fila ao exchange com a routing key correta
            canal.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=routing_key)

            return conexao, canal
        except pika.exceptions.AMQPConnectionError:
            print("Conexão perdida. Tentando reconectar em 3 segundos...")
            time.sleep(3)

def consumir_mensagens(genero):
    queue_name = f"reserva_fila_{genero}"
    routing_key = f"reserva.{genero}"  # Routing key precisa bater com o que o produtor usa

    conexao, canal = conectar_fila(queue_name, routing_key)
    
    print(f"\nAguardando reservas de livros do gênero: {genero}.")
    print("Pressione 'CTRL+C' para voltar ao menu")
    
    def callback(ch, method, properties, body):
        print(f"Reserva recebida! Detalhes: {body.decode()}")
    
    try:
        canal.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
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
