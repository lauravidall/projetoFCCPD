# Projeto de Serviço de Envio e Recebimento de Mensagens

## Visão Geral
Este projeto é uma implementação de um sistema de envio e recebimento de mensagens utilizando RabbitMQ, composto por três principais componentes:
- *Produtor de Mensagens (Java)*: Envia mensagens relacionadas a reservas de livros.
- *Consumidor de Mensagens (Python)*: Recebe mensagens de acordo com o gênero de livro escolhido.
- *Backend de Auditoria (Python)*: Recebe todas as mensagens enviadas, independente do gênero.

O sistema visa demonstrar a utilização de filas e exchanges do RabbitMQ, utilizando o tipo de exchange topic para distribuir mensagens entre diferentes consumidores, de acordo com o gênero.

## Requisitos
1. RabbitMQ deve estar instalado e rodando.
2. O produtor deve ser executado em Java e o consumidor em Python.

### Instalação do RabbitMQ (Windows)
1. Baixe e instale o RabbitMQ e Erlang.
2. Adicione o diretório sbin do RabbitMQ às variáveis de ambiente do sistema.
3. Para iniciar o servidor RabbitMQ, execute rabbitmq-server.bat no terminal.
4. Acesse o painel do RabbitMQ em http://localhost:15672 (usuário: guest, senha: guest).

### Instalação do RabbitMQ (MacOS)
1. Utilize o Homebrew para instalar RabbitMQ: brew install rabbitmq
2. Inicie o servidor RabbitMQ: brew services start rabbitmq
3. Acesse o painel do RabbitMQ em http://localhost:15672 (usuário: guest, senha: guest).

## Como Rodar o Projeto
### 1. Menu
- Abra o terminal e execute o comando sh python3 menu.py
  Isso iniciará o menu, que lhe dará a opção de rodar o produtor, o consumidor, a auditoria ou sair.
  
- Caso queira rodar os componentes separadamente, use os passos (1.1), (1.2) e (1.3)
### 1.1. Backend de Auditoria
- Navegue até o diretório auditoriaEmPython e execute o comando:
  sh
  python3 auditoria.py
  
  Isso iniciará o backend de auditoria, que receberá todas as mensagens enviadas pelo produtor.

### 1.2. Consumidor de Mensagens
- Navegue até o diretório consumidorEmPython e execute:
  sh
  python3 consumidor.py
  
  Escolha o gênero do livro para escutar as mensagens específicas dessa fila.

### 1.3. Produtor de Mensagens
- Navegue até o diretório produtor e execute o comando Maven:
  sh
  mvn exec:java -Dexec.mainClass="com.reservalivros.Produtor" 
  
  Preencha as informações solicitadas (ID do usuário, nome do livro, gênero do livro).

## Estrutura do Código
### 1. Produtor (Java)
- *Envio de Mensagens Persistentes*: As mensagens enviadas são marcadas como persistentes para garantir que sejam consumidas mesmo se não houver consumidores disponíveis no momento do envio.
- *Exchange*: Utilizamos uma exchange do tipo topic para que cada mensagem seja roteada para filas específicas baseadas na chave de roteamento.

### 2. Consumidor (Python)
- *Filtragem por Gênero*: O consumidor permite escolher um gênero de livro e escutar apenas as mensagens dessa categoria.
- *Persistência*: A fila também é marcada como durável para garantir que as mensagens fiquem disponíveis até serem consumidas.

### 3. Backend de Auditoria (Python)
- *Recepção de Todas as Mensagens*: O backend de auditoria recebe todas as mensagens, independentemente do gênero, para fins de monitoramento.

## Justificativa para o Uso do topic Exchange
Utilizamos a exchange do tipo topic porque ela permite maior flexibilidade no roteamento das mensagens. Dessa forma, podemos definir diferentes padrões de chave de roteamento, garantindo que as mensagens cheguem apenas aos consumidores corretos. Isso facilita o processo de gerenciamento das filas por gêneros de livros.
