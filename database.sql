-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `categoryId` tinyint(4) DEFAULT NULL,
  `name` varchar(29) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Men'),(2,'Books'),(3,'Computers and Accessories'),(4,'Movies, Music and Video Games'),(5,'Jwelery, Watches and Eyewear'),(6,'Women');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kart`
--

DROP TABLE IF EXISTS `kart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kart` (
  `userId` varchar(0) DEFAULT NULL,
  `productId` varchar(0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kart`
--

LOCK TABLES `kart` WRITE;
/*!40000 ALTER TABLE `kart` DISABLE KEYS */;
/*!40000 ALTER TABLE `kart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `productId` tinyint(4) DEFAULT NULL,
  `name` varchar(11) DEFAULT NULL,
  `price` decimal(5,2) DEFAULT NULL,
  `description` varchar(22) DEFAULT NULL,
  `image` varchar(15) DEFAULT NULL,
  `stock` tinyint(4) DEFAULT NULL,
  `categoryId` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Paracetamol',25.00,'Fever Medicine','paracetamol.jpg',10,1),(2,'Advil',50.45,'Fever Medicine','Advil.jpg',5,1),(3,'Diclofenac',19.99,'Fever Medicine','diclofenac.jpg',10,1),(4,'Pedia Care',30.00,'Fever Medicine','pediacare.jpg',4,1),(5,'Panadol',29.99,'Fever Medicine','panadol.jpeg',7,1),(6,'Bactroban',145.00,'Skin Care Medicine','bactroban.jpg',8,2),(7,'Bee Magic',90.00,'Skin Care Medicine','beemagic.jpg',15,2),(8,'Brite',75.00,'Skin Care Medicine','brite.jpg',12,2),(9,'Retin-A',110.00,'Skin Care Medicine','retin-a.jpg',5,2),(10,'Piroxicam',45.00,'Skin Care Medicine','piroxicam.jpeg',15,2),(11,'Boiron',79.99,'Physical Care Medicine','boiron.jpg',20,3),(12,'Bonecare',120.00,'Physical Care Medicine','bonecare.jpg',10,3),(13,'Boniheal',99.00,'Physical Care Medicine','boniheal.jpg',12,3),(14,'calcihills',110.00,'Physical Care Medicine','calcihills.jpg',10,3),(15,'Orajel',65.00,'Dental Care Medicine','orajel.jpeg',5,4),(16,'Red Cross',70.00,'Dental Care Medicine','redcross.jpg',10,4),(17,'Desval',90.00,'Neuro Care Medicine','desval.jpeg',5,5),(18,'Levroxa',75.00,'Neuro Care Medicine','levroxa.jpg',10,5),(19,'Relgin',90.00,'Neuro Care Medicine','relgin.jpg',12,5);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `userId` tinyint(4) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `email` varchar(26) DEFAULT NULL,
  `firstName` varchar(6) DEFAULT NULL,
  `lastName` varchar(5) DEFAULT NULL,
  `address1` varchar(29) DEFAULT NULL,
  `address2` varchar(3) DEFAULT NULL,
  `zipcode` varchar(6) DEFAULT NULL,
  `city` varchar(6) DEFAULT NULL,
  `state` varchar(7) DEFAULT NULL,
  `country` varchar(5) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'0cc175b9c0f1b6a831c399e269772661','abcd@example.com','Harsh','Shah','scaa','asa','as','asc','dasd','dfas','dsa'),(2,'25f9e794323b453885f5181f1b624d0b','hemantahuja.1016@gmail.com','Hemant','Ahuja','H No. 717/14, GURU NANAK PURA','','124001','ROHTAK','Haryana','India','09138459808'),(3,'25f9e794323b453885f5181f1b624d0b','hemantahuja.1016@gmail.com','Hemant','Ahuja','H No. 717/14, GURU NANAK PURA','','124001','ROHTAK','Haryana','India','09138459808');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-08-22 15:20:25
