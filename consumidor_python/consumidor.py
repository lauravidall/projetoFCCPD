import pika
import sys
import time

def main():
    generos = ['ficcao', 'fantasia', 'misterio', 'romance', 'terror', 'biografia', 'ciencia', 'historia', 'poesia']

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
                genero = generos[indice_escolhido]
                queue_name = f"reserva_fila_{genero}"

                while True:
                    try:
                        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
                        channel = connection.channel()

                        print(f"\nAguardando reservas de livros do gênero: {genero}.")
                        print("Pressione 'ctrl+c' para voltar ao menu")

                        channel.queue_declare(queue=queue_name, durable=True)

                        def callback(ch, method, properties, body):
                            print(f"Reserva recebida! Detalhes: {body.decode()}")

                        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
                        channel.start_consuming()

                    except pika.exceptions.AMQPConnectionError:
                        print("Conexão perdida. Tentando reconectar em 3 segundos...")
                        time.sleep(3)
                    except KeyboardInterrupt:
                        print("\nParando o consumo de mensagens...")
                        break
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Escolha inválida. Digite um número.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma encerrado.")
