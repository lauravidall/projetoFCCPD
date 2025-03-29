# Projeto de Serviço de Envio e Recebimento de Mensagens

## Visão Geral
Este projeto é uma implementação de um sistema de envio e recebimento de mensagens utilizando RabbitMQ, composto por três principais componentes:
- *Produtor de Mensagens (Java)*: Envia mensagens relacionadas a agendamentos de consultas médicas.
- *Consumidor de Mensagens (Python)*: Recebe mensagens de acordo com a especialidade médica escolhida.
- *Backend de Auditoria (Python)*: Recebe todas as mensagens enviadas, independente da especialidade.

O sistema visa demonstrar a utilização de filas e exchanges do RabbitMQ, utilizando o tipo de exchange topic para distribuir mensagens entre diferentes consumidores, de acordo com a especialidade médica.

## Requisitos
1. RabbitMQ deve estar instalado e rodando.
2. O produtor deve ser executado em Java e o consumidor em Python.

### Instalação do RabbitMQ (Windows)
1. Baixe e instale o RabbitMQ e Erlang.
2. Adicione o diretório sbin do RabbitMQ às variáveis de ambiente do sistema.
3. Para iniciar o servidor RabbitMQ, execute rabbitmq-server.bat no terminal.
4. Acesse o painel do RabbitMQ em http://localhost:15672 (usuário: guest, senha: guest).

### Instalação do RabbitMQ (MacOS)
1. Utilize o Homebrew para instalar RabbitMQ: brew install rabbitmq.
2. Inicie o servidor RabbitMQ: brew services start rabbitmq.
3. Acesse o painel do RabbitMQ em http://localhost:15672 (usuário: guest, senha: guest).

## Como Rodar o Projeto
### 1. Backend de Auditoria
- Navegue até o diretório backend_auditoria e execute o comando:
  sh
  python3 backend_auditoria.py
  
  Isso iniciará o backend de auditoria, que receberá todas as mensagens enviadas pelo produtor.

### 2. Consumidor de Mensagens
- Navegue até o diretório consumidor_python e execute:
  sh
  python3 consumidor.py
  
  Escolha a especialidade médica para escutar as mensagens específicas dessa fila.

### 3. Produtor de Mensagens
- Navegue até o diretório produtor_java e execute o comando Maven:
  sh
  mvn exec:java -Dexec.mainClass="com.consultamedica.Produtor"
  
  Preencha as informações solicitadas (ID do paciente, tipo de solicitação, data e hora da consulta, especialidade médica e detalhes adicionais).

## Estrutura do Código
### 1. Produtor (Java)
- *Envio de Mensagens Persistentes*: As mensagens enviadas são marcadas como persistentes para garantir que sejam consumidas mesmo se não houver consumidores disponíveis no momento do envio.
- *Exchange*: Utilizamos uma exchange do tipo topic para que cada mensagem seja roteada para filas específicas baseadas na chave de roteamento.

### 2. Consumidor (Python)
- *Filtragem por Especialidade*: O consumidor permite escolher uma especialidade médica e escutar apenas as mensagens dessa categoria.
- *Persistência*: A fila também é marcada como durável para garantir que as mensagens fiquem disponíveis até serem consumidas.

### 3. Backend de Auditoria (Python)
- *Recepção de Todas as Mensagens*: O backend de auditoria recebe todas as mensagens, independentemente da especialidade, para fins de monitoramento.

## Justificativa para o Uso do topic Exchange
Utilizamos a exchange do tipo topic porque ela permite maior flexibilidade no roteamento das mensagens. Dessa forma, podemos definir diferentes padrões de chave de roteamento, garantindo que as mensagens cheguem apenas aos consumidores corretos. Isso facilita o processo de gerenciamento das filas por especialidade médica e permite adicionar novas especialidades no futuro sem alterar a lógica principal do produtor ou dos consumidores.
