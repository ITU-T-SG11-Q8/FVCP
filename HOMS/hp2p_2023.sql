CREATE DATABASE  IF NOT EXISTS `hp2p_2023` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `hp2p_2023`;
-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: hp2p_2023
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `hp2p_auth_peer`
--

DROP TABLE IF EXISTS `hp2p_auth_peer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hp2p_auth_peer` (
  `overlay_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `peer_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`overlay_id`,`peer_id`),
  CONSTRAINT `fk_auth_overlay_id` FOREIGN KEY (`overlay_id`) REFERENCES `hp2p_overlay` (`overlay_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hp2p_auth_peer`
--

LOCK TABLES `hp2p_auth_peer` WRITE;
/*!40000 ALTER TABLE `hp2p_auth_peer` DISABLE KEYS */;
/*!40000 ALTER TABLE `hp2p_auth_peer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hp2p_channel`
--

DROP TABLE IF EXISTS `hp2p_channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hp2p_channel` (
  `channel_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `service_id` int NOT NULL,
  `channel_type` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`channel_id`,`service_id`),
  KEY `fk_channel_service_id` (`service_id`),
  CONSTRAINT `fk_channel_service_id` FOREIGN KEY (`service_id`) REFERENCES `hp2p_service` (`service_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hp2p_channel`
--

LOCK TABLES `hp2p_channel` WRITE;
/*!40000 ALTER TABLE `hp2p_channel` DISABLE KEYS */;
/*!40000 ALTER TABLE `hp2p_channel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hp2p_channel_attribute`
--

DROP TABLE IF EXISTS `hp2p_channel_attribute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hp2p_channel_attribute` (
  `channel_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `service_id` int NOT NULL,
  `keyword` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`channel_id`,`service_id`,`keyword`),
  KEY `fk_attribute_service_id_idx` (`service_id`),
  CONSTRAINT `fk_attribute_service_id` FOREIGN KEY (`service_id`) REFERENCES `hp2p_service` (`service_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hp2p_channel_attribute`
--

LOCK TABLES `hp2p_channel_attribute` WRITE;
/*!40000 ALTER TABLE `hp2p_channel_attribute` DISABLE KEYS */;
/*!40000 ALTER TABLE `hp2p_channel_attribute` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hp2p_channel_source`
--

DROP TABLE IF EXISTS `hp2p_channel_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hp2p_channel_source` (
  `channel_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `service_id` int NOT NULL,
  `peer_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`channel_id`,`service_id`,`peer_id`),
  KEY `fk_channel_source_service_id_idx` (`service_id`),
  CONSTRAINT `fk_channel_source_service_id` FOREIGN KEY (`service_id`) REFERENCES `hp2p_service` (`service_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hp2p_channel_source`
--

LOCK TABLES `hp2p_channel_source` WRITE;
/*!40000 ALTER TABLE `hp2p_channel_source` DISABLE KEYS */;
/*!40000 ALTER TABLE `hp2p_channel_source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hp2p_overlay`
--

DROP TABLE IF EXISTS `hp2p_overlay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hp2p_overlay` (
  `overlay_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `overlay_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sub_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `owner_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `overlay_status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heartbeat_interval` int NOT NULL DEFAULT '0',
  `heartbeat_timeout` int NOT NULL DEFAULT '0',
  `auth_keyword` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `auth_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `auth_admin_key` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `auth_access_key` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mn_cache` int DEFAULT NULL,
  `md_cache` int DEFAULT NULL,
  `recovery_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`overlay_id`),
  UNIQUE KEY `overlay_id_UNIQUE` (`overlay_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hp2p_overlay`
--

LOCK TABLES `hp2p_overlay` WRITE;
/*!40000 ALTER TABLE `hp2p_overlay` DISABLE KEYS */;
/*!40000 ALTER TABLE `hp2p_overlay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hp2p_peer`
--

DROP TABLE IF EXISTS `hp2p_peer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hp2p_peer` (
  `peer_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `overlay_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `display_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ticket_id` int DEFAULT NULL,
  `overlay_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sub_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `expires` int DEFAULT NULL,
  `address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `auth_password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `auth_public_key` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `num_primary` int NOT NULL DEFAULT '0',
  `num_out_candidate` int NOT NULL DEFAULT '0',
  `num_in_candidate` int NOT NULL DEFAULT '0',
  `costmap` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `report_time` datetime DEFAULT NULL,
  PRIMARY KEY (`peer_id`,`overlay_id`),
  KEY `fk_overlay_id_idx` (`overlay_id`),
  CONSTRAINT `fk_overlay_id` FOREIGN KEY (`overlay_id`) REFERENCES `hp2p_overlay` (`overlay_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hp2p_peer`
--

LOCK TABLES `hp2p_peer` WRITE;
/*!40000 ALTER TABLE `hp2p_peer` DISABLE KEYS */;
/*!40000 ALTER TABLE `hp2p_peer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hp2p_service`
--

DROP TABLE IF EXISTS `hp2p_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hp2p_service` (
  `service_id` int NOT NULL AUTO_INCREMENT,
  `overlay_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_datetime` datetime DEFAULT NULL,
  `end_datetime` datetime DEFAULT NULL,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`service_id`),
  UNIQUE KEY `service_id_UNIQUE` (`service_id`),
  UNIQUE KEY `overlay_id_UNIQUE` (`overlay_id`),
  KEY `fk_service_overlay_id_idx` (`overlay_id`),
  CONSTRAINT `fk_service_overlay_id` FOREIGN KEY (`overlay_id`) REFERENCES `hp2p_overlay` (`overlay_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hp2p_service`
--

LOCK TABLES `hp2p_service` WRITE;
/*!40000 ALTER TABLE `hp2p_service` DISABLE KEYS */;
/*!40000 ALTER TABLE `hp2p_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hp2p_service_block`
--

DROP TABLE IF EXISTS `hp2p_service_block`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hp2p_service_block` (
  `service_id` int NOT NULL,
  `peer_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`service_id`,`peer_id`),
  CONSTRAINT `fk_source_service_id0` FOREIGN KEY (`service_id`) REFERENCES `hp2p_service` (`service_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hp2p_service_block`
--

LOCK TABLES `hp2p_service_block` WRITE;
/*!40000 ALTER TABLE `hp2p_service_block` DISABLE KEYS */;
/*!40000 ALTER TABLE `hp2p_service_block` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hp2p_service_source`
--

DROP TABLE IF EXISTS `hp2p_service_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hp2p_service_source` (
  `service_id` int NOT NULL,
  `peer_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`service_id`,`peer_id`),
  CONSTRAINT `fk_source_service_id` FOREIGN KEY (`service_id`) REFERENCES `hp2p_service` (`service_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hp2p_service_source`
--

LOCK TABLES `hp2p_service_source` WRITE;
/*!40000 ALTER TABLE `hp2p_service_source` DISABLE KEYS */;
/*!40000 ALTER TABLE `hp2p_service_source` ENABLE KEYS */;
UNLOCK TABLES;


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-20 20:32:09
