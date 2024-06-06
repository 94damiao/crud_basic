
CREATE DATABASE IF NOT EXISTS `produtos`;
USE `produtos`;


CREATE TABLE IF NOT EXISTS `products` (
  `descricao` varchar(50) DEFAULT NULL,
  `preco` varchar(50) DEFAULT NULL,
  `codigo` bigint NOT NULL AUTO_INCREMENT,
  `datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted` int DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
