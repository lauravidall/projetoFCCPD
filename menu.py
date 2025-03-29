import subprocess
import platform

processos = []

def start_produtor():
    # Comando para iniciar o produtor em Java
    print("Iniciando o produtor...")
    subprocess.run(["java", "-cp", "produtor/target/produtor-1.0-SNAPSHOT.jar", "com.reservalivros.Produtor"])

def start_consumidor():
    # Comando para iniciar o consumidor em Python
    print("Iniciando o consumidor...")
    subprocess.run(["python3", "consumidorEmPython/consumidor.py"])

def start_auditoria():
    # Comando para iniciar auditoria em Python
    print("Iniciando auditoria...")
    subprocess.run(["python3", "auditoriaEmPython/auditoria.py"])

def stop_processos():
    for processo in processos:
        processo.terminate()
    processos.clear()

def menu():
    try:
        while True:
            print("\n***** Sistema de Mensagens *****")
            print("1. Iniciar Produtor")
            print("2. Iniciar Consumidor")
            print("3. Iniciar Auditoria")
            print("4. Sair")

            numero = input("Escolha um número de 1 a 4: ")

            if numero == "1":
                start_produtor()
            elif numero == "2":
                start_consumidor()
            elif numero == "3":
                start_auditoria()
            elif numero == "4":
                print("Encerrando o sistema...")
                stop_processos()
                break
            else:
                print("Opção inválida. Tente novamente.")
    except KeyboardInterrupt:
        print("\nEncerrando o sistema...")
        stop_processos()

if __name__ == "__main__":
    menu()
