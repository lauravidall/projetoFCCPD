import os
import subprocess

def start_produtor():
    # Comando para iniciar o produtor em Java
    print("Iniciando o produtor...")
    subprocess.run(["java", "-cp", "produtor_java/target/produtor_java-1.0-SNAPSHOT.jar", "com.consultamedica.Produtor"])

def start_consumidor():
    # Comando para iniciar o consumidor em Python
    print("Iniciando o consumidor...")
    subprocess.run(["python3", "consumidor_python/consumidor.py"])

def start_auditoria():
    # Comando para iniciar o backend de auditoria em Python
    print("Iniciando o backend de auditoria...")
    subprocess.run(["python3", "backend_auditoria/backend_auditoria.py"])

def menu():
    while True:
        print("\n=== Sistema de Mensagens ===")
        print("1. Iniciar Produtor")
        print("2. Iniciar Consumidor")
        print("3. Iniciar Backend de Auditoria")
        print("4. Sair")

        escolha = input("Escolha uma opção (1-4): ")

        if escolha == "1":
            start_produtor()
        elif escolha == "2":
            start_consumidor()
        elif escolha == "3":
            start_auditoria()
        elif escolha == "4":
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
