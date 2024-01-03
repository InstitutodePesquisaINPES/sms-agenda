create schema agenda;

use agenda;

CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `cpf` varchar(14),
  `sus` varchar(19),
  `senha` varchar(50) NOT NULL,
  `user_type` varchar(20),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci; 

CREATE TABLE `agendamentos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `data_agendada` date NOT NULL, 
  `horario_agendado` time NOT NULL,
  `nome_cliente` varchar(255) NOT NULL,
  `servico_agendado` varchar(255) NOT NULL,
  `data_agendamento` date NOT NULL,
  `senha` varchar(10) NOT NULL,
  `status` varchar(25) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_usuario` (`id_usuario`,`data_agendada`,`horario_agendado`),
  CONSTRAINT `agendamentos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `horarios_disponiveis` (
    `id` int NOT NULL AUTO_INCREMENT,
    `hora_inicio` time NOT NULL,
    `hora_pausa` time NOT NULL, 
    `tempo_pausa` time NOT NULL,
    `hora_retomada` time NOT NULL,
    `hora_final` time NOT NULL, 
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `servico` (     
  `id` int NOT NULL AUTO_INCREMENT,     
  `id_servico` int NOT NULL,     
  `tempo_atendimento` time NOT NULL,      
  PRIMARY KEY(`id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

insert into servico (id_servico, tempo_atendimento) values (1, "00:20:00");
insert into servico (id_servico, tempo_atendimento) values (2, "00:20:00");
insert into servico (id_servico, tempo_atendimento) values (3, "00:20:00");
insert into servico (id_servico, tempo_atendimento) values (4, "00:20:00");
insert into servico (id_servico, tempo_atendimento) values (5, "00:20:00");


CREATE TABLE `documentos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_agendamento` int NOT NULL,
  `caminho1` varchar(255) DEFAULT NULL,
  `caminho2` varchar(255) DEFAULT NULL,
  `caminho3` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`id_agendamento`) REFERENCES `agendamentos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


insert into horarios_disponiveis (hora_inicio, hora_pausa, tempo_pausa, hora_retomada, hora_final) values ("07:00:00", "11:00:00", "02:00:00", "13:00:00", "17:00:00");

insert into usuario (id, email, nome, cpf, sus, senha, user_type) values (1, "admin@gmail.com", "admin", "211.111.111-11", "211.111.111.1111-11", "12345678", "administrador");


