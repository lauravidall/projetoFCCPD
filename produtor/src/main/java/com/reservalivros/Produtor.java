package com.reservalivros;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import java.util.Scanner;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Produtor {

    private final static String EXCHANGE_NAME = "reserva_livros";

    public static void main(String[] argv) {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");

        try (Connection connection = factory.newConnection(); Channel channel = connection.createChannel()) {
            channel.exchangeDeclare(EXCHANGE_NAME, "topic", true);

            Scanner scanner = new Scanner(System.in);
            System.out.println("***** Sistema de Reserva de Livros *****");

            // Lista de gêneros possíveis
            String[] generos = {
                "ficcao", "fantasia", "misterio", "romance", "terror", 
                "biografia", "ciencia", "historia", "poesia"
            };

            while (true) {
                System.out.print("Informe o ID do usuário (ou digite 'sair' para encerrar): ");
                String usuarioId = scanner.nextLine();
                if (usuarioId.equalsIgnoreCase("sair")) {
                    break;
                }

                System.out.print("Título do livro: ");
                String tituloLivro = scanner.nextLine();

                System.out.println("Escolha o gênero do livro:");
                for (int i = 0; i < generos.length; i++) {
                    System.out.println((i + 1) + ". " + generos[i]);
                }

                System.out.print("Digite o número do gênero da sua escolha: ");
                int escolhaGenero = scanner.nextInt();
                scanner.nextLine(); 

                String generoLivro = "";

                if (escolhaGenero >= 1 && escolhaGenero <= generos.length) {
                    generoLivro = generos[escolhaGenero - 1];
                } else {
                    System.out.println("Gênero inválido. Tente novamente.");
                    continue;
                }

                String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy - HH:mm"));
                String mensagem = String.format("[%s] Usuário %s reservou '%s' (Gênero: %s)", timestamp, usuarioId, tituloLivro, generoLivro);
                
                String routingKey = "reserva." + generoLivro;
                
                AMQP.BasicProperties props = new AMQP.BasicProperties.Builder()
                        .deliveryMode(2)
                        .build();

                channel.basicPublish(EXCHANGE_NAME, routingKey, props, mensagem.getBytes("UTF-8"));
                System.out.println("Reserva enviada: " + mensagem);
            }

        } catch (Exception e) {
            System.err.println("Erro ao enviar a mensagem: " + e.getMessage());
        }
    }
}
