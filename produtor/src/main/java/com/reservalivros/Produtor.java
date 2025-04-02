package com.reservalivros;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import java.util.HashSet;
import java.util.Scanner;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Produtor {

    private static final String EXCHANGE_NAME = "reserva_livros";
    
    private static final String[] GENEROS = {
        "Ficção", "Fantasia", "Mistério", "Romance", "Terror", 
        "Biografia", "Ciência", "História", "Poesia"
    };

    private static final HashSet<String> GENEROS_SET = new HashSet<>();
    private static final HashSet<String> LIVROS_RESERVADOS = new HashSet<>();
    
    static {
        for (String genero : GENEROS) {
            GENEROS_SET.add(genero.toLowerCase());
        }
    }

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
        System.out.println("\n======================================");
        System.out.println("Reserva enviada com sucesso!");
        System.out.println("======================================\n");
    }
    
    private static String escolherGenero(Scanner scanner) {
        while (true) {
            System.out.println("\n======= Escolha o Gênero do Livro =======");
            for (int i = 0; i < GENEROS.length; i++) {
                System.out.printf("%d - %s\n", i + 1, GENEROS[i]);
            }
            System.out.println("=========================================");
            
            System.out.print("Digite o número ou o nome do gênero: ");
            String entrada = scanner.nextLine().trim().toLowerCase();
            
            try {
                int escolha = Integer.parseInt(entrada);
                if (escolha >= 1 && escolha <= GENEROS.length) {
                    return GENEROS[escolha - 1];
                }
            } catch (NumberFormatException e) {
                if (GENEROS_SET.contains(entrada)) {
                    return entrada.substring(0, 1).toUpperCase() + entrada.substring(1);
                }
            }
            
            System.out.println("Erro: Gênero inválido. Tente novamente.");
        }
    }

    private static String normalizarTitulo(String titulo) {
        titulo = titulo.trim().toLowerCase();
        String[] palavras = titulo.split(" ");
        StringBuilder sb = new StringBuilder();
        
        for (String palavra : palavras) {
            if (!palavra.isEmpty()) {
                sb.append(Character.toUpperCase(palavra.charAt(0))).append(palavra.substring(1)).append(" ");
            }
        }
        
        return sb.toString().trim();
    }

    public static void main(String[] argv) {
        System.out.println("Tentando conectar ao RabbitMQ...");
        try (Connection connection = configurarFactory().newConnection();
             Channel channel = connection.createChannel();
             Scanner scanner = new Scanner(System.in)) {
            
            System.out.println("Conectado com sucesso!");
            channel.exchangeDeclare(EXCHANGE_NAME, "topic", true);
            System.out.println("\n========================================");
            System.out.println("***** Sistema de Reserva de Livros *****");
            System.out.println("========================================\n");
            
            while (true) {
                System.out.print("Informe o ID do usuário (ou digite 'sair' para encerrar): ");
                String usuarioId = scanner.nextLine().trim();
                if (usuarioId.equalsIgnoreCase("sair")) {
                    break;
                }
                
                System.out.print("Título do livro: ");
                String tituloLivro = normalizarTitulo(scanner.nextLine());
                
                if (LIVROS_RESERVADOS.contains(tituloLivro)) {
                    System.out.println("\n========================================");
                    System.out.println("LIVRO JÁ RESERVADO: " + tituloLivro);
                    System.out.println("========================================\n");
                    continue;
                }
                
                String generoLivro = escolherGenero(scanner);
                
                LIVROS_RESERVADOS.add(tituloLivro);
                enviarMensagem(channel, usuarioId, tituloLivro, generoLivro);
            }
            
        } catch (Exception e) {
            System.err.println("Erro ao enviar a mensagem: " + e.getMessage());
        }
    }
}
