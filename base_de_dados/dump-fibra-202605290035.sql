/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.7.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: fibra
-- ------------------------------------------------------
-- Server version	12.2.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `simulacoes`
--

DROP TABLE IF EXISTS `simulacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `simulacoes` (
  `fibra` varchar(80) NOT NULL,
  `nome` varchar(120) NOT NULL,
  `distancia_km` double NOT NULL,
  `potencia_mw` double NOT NULL,
  `potencia_dbm` varchar(100) NOT NULL DEFAULT '0.0',
  `perda_pct` double NOT NULL DEFAULT 0,
  `perda_db` double NOT NULL DEFAULT 0,
  `qualidade` varchar(20) NOT NULL,
  `racio` double NOT NULL DEFAULT 1,
  `criado_em` datetime NOT NULL DEFAULT current_timestamp(),
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='simulações';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `simulacoes`
--

LOCK TABLES `simulacoes` WRITE;
/*!40000 ALTER TABLE `simulacoes` DISABLE KEYS */;
INSERT INTO `simulacoes` VALUES
('Multimodo Simplex','Multimodo Simplex – 4 km',4,0.631,'0.0',36.9,0,'BOM',1,'2026-05-28 11:30:04',2),
('Multimodo Duplex','Multimodo Duplex – 42 km',42,0.008,'0.0',99.2,0,'FRACO',1,'2026-05-28 12:16:19',3);
/*!40000 ALTER TABLE `simulacoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'fibra'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-05-29  0:35:36
