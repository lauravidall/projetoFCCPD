import pika
import time

generos = ['ficcao', 'fantasia', 'misterio', 'romance', 'terror', 'biografia', 'ciencia', 'historia', 'poesia']

def conectar_fila(queue_name):
    while True:
        try:
            conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            canal = conexao.channel()
            canal.queue_declare(queue=queue_name, durable=True)
            return conexao, canal
        except pika.exceptions.AMQPConnectionError:
            print("Conexão perdida. Tentando reconectar em 3 segundos...")
            time.sleep(3)

def consumir_mensagens(genero):
    queue_name = f"reserva_fila_{genero}"
    conexao, canal = conectar_fila(queue_name)
    
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
