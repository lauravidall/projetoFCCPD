package com.reservalivros;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import java.util.Scanner;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Produtor {

    private static final String EXCHANGE_NAME = "reserva_livros";
    
    private static final String[] GENEROS = {
        "ficcao", "fantasia", "misterio", "romance", "terror", 
        "biografia", "ciencia", "historia", "poesia"
    };

    private static ConnectionFactory configurarFactory() {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        return factory;
    }

    private static void enviarMensagem(Channel channel, String usuarioId, String tituloLivro, String generoLivro) throws Exception {
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy - HH:mm"));
        String mensagem = String.format("[%s] Usuário %s reservou '%s' (Gênero: %s)", timestamp, usuarioId, tituloLivro, generoLivro);
        
        String routingKey = "reserva." + generoLivro; 
        
        AMQP.BasicProperties props = new AMQP.BasicProperties.Builder()
                .deliveryMode(2)
                .build();
        
        channel.basicPublish(EXCHANGE_NAME, routingKey, props, mensagem.getBytes("UTF-8"));
        System.out.println("Reserva enviada: " + mensagem);
    }
    

    private static String escolherGenero(Scanner scanner) {
        System.out.println("Escolha o gênero do livro:");
        for (int i = 0; i < GENEROS.length; i++) {
            System.out.println((i + 1) + ". " + GENEROS[i]);
        }
        
        System.out.print("Digite o número do gênero da sua escolha: ");
        int escolha = scanner.nextInt();
        scanner.nextLine(); 
        
        if (escolha >= 1 && escolha <= GENEROS.length) {
            return GENEROS[escolha - 1];
        } else {
            System.out.println("Gênero inválido. Tente novamente.");
            return null;
        }
    }

    public static void main(String[] argv) {
        System.out.println("Tentando conectar ao RabbitMQ...");
try (Connection connection = configurarFactory().newConnection();
     Channel channel = connection.createChannel();
     Scanner scanner = new Scanner(System.in)) {

    System.out.println("Conectado com sucesso!");

            channel.exchangeDeclare(EXCHANGE_NAME, "topic", true);
            System.out.println("***** Sistema de Reserva de Livros *****");
            
            while (true) {
                System.out.print("Informe o ID do usuário (ou digite 'sair' para encerrar): ");
                String usuarioId = scanner.nextLine();
                if (usuarioId.equalsIgnoreCase("sair")) {
                    break;
                }
                
                System.out.print("Título do livro: ");
                String tituloLivro = scanner.nextLine();
                
                String generoLivro;
                do {
                    generoLivro = escolherGenero(scanner);
                } while (generoLivro == null);
                
                enviarMensagem(channel, usuarioId, tituloLivro, generoLivro);
            }
            
        } catch (Exception e) {
            System.err.println("Erro ao enviar a mensagem: " + e.getMessage());
        }
    }
}