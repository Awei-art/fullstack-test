-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: grape_shop
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$1200000$m7qVbdSSdAvrKITZphLNX7$95ZGT0rAzEhhieThkgT4tsKzoy5EofQjfm8u+5lwT7g=','2026-02-19 08:31:41.827485',1,'testuser','','','abc@gmail.com',1,1,'2026-02-06 01:24:54.858923','一般會員',NULL);
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add variety',7,'add_variety'),(26,'Can change variety',7,'change_variety'),(27,'Can delete variety',7,'delete_variety'),(28,'Can view variety',7,'view_variety'),(29,'Can add product',8,'add_product'),(30,'Can change product',8,'change_product'),(31,'Can delete product',8,'delete_product'),(32,'Can view product',8,'view_product'),(33,'Can add product image',9,'add_productimage'),(34,'Can change product image',9,'change_productimage'),(35,'Can delete product image',9,'delete_productimage'),(36,'Can view product image',9,'view_productimage'),(37,'Can add 商品規格/等級',10,'add_productgrade'),(38,'Can change 商品規格/等級',10,'change_productgrade'),(39,'Can delete 商品規格/等級',10,'delete_productgrade'),(40,'Can view 商品規格/等級',10,'view_productgrade');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-02-06 03:12:20.677312','1','巨峰葡萄',1,'[{\"added\": {}}]',7,1),(2,'2026-02-06 03:12:49.929215','2','麝香葡萄',1,'[{\"added\": {}}]',7,1),(3,'2026-02-06 03:13:50.684029','3','貓眼葡萄',1,'[{\"added\": {}}]',7,1),(4,'2026-02-06 03:14:58.096912','4','我的心葡萄',1,'[{\"added\": {}}]',7,1),(5,'2026-02-06 03:15:32.301292','5','天晴葡萄',1,'[{\"added\": {}}]',7,1),(6,'2026-02-06 03:16:26.477731','6','皇冠葡萄',1,'[{\"added\": {}}]',7,1),(7,'2026-02-06 03:17:19.061540','7','長野紫葡萄',1,'[{\"added\": {}}]',7,1),(8,'2026-02-06 03:20:20.684382','8','妮娜葡萄',1,'[{\"added\": {}}]',7,1),(9,'2026-02-06 03:22:42.504891','9','悟紅玉葡萄',1,'[{\"added\": {}}]',7,1),(10,'2026-02-06 03:23:27.199762','10','天山葡萄',1,'[{\"added\": {}}]',7,1),(11,'2026-02-06 04:14:58.183265','1','巨峰風葡萄禮盒',1,'[{\"added\": {}}]',8,1),(12,'2026-02-06 04:18:21.037904','2','麝香葡萄禮盒',1,'[{\"added\": {}}]',8,1),(13,'2026-02-06 04:24:42.503275','3','貓眼葡萄禮盒',1,'[{\"added\": {}}]',8,1),(14,'2026-02-06 04:31:19.748562','4','我的心葡萄禮盒',1,'[{\"added\": {}}]',8,1),(15,'2026-02-06 04:35:36.671066','5','天晴葡萄禮盒',1,'[{\"added\": {}}]',8,1),(16,'2026-02-06 04:43:09.191455','6','皇冠葡萄禮盒',1,'[{\"added\": {}}]',8,1),(17,'2026-02-06 04:49:28.813591','7','長野紫葡萄禮盒',1,'[{\"added\": {}}]',8,1),(18,'2026-02-06 04:55:41.809209','8','妮娜葡萄禮盒',1,'[{\"added\": {}}]',8,1),(19,'2026-02-06 05:02:09.075626','9','悟紅玉葡萄禮盒',1,'[{\"added\": {}}]',8,1),(20,'2026-02-06 05:06:43.727857','10','天山葡萄禮盒',1,'[{\"added\": {}}]',8,1),(21,'2026-02-06 05:10:08.281624','11','三色葡萄禮盒',1,'[{\"added\": {}}]',8,1),(22,'2026-02-06 05:15:32.931234','12','雙色葡萄禮盒',1,'[{\"added\": {}}]',8,1),(23,'2026-02-06 05:23:20.042303','12','雙色葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u70ba\\u6df7\\u5408\\u79ae\\u76d2\"]}}]',8,1),(24,'2026-02-06 05:23:24.376607','11','三色葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u70ba\\u6df7\\u5408\\u79ae\\u76d2\"]}}]',8,1),(25,'2026-02-06 05:59:00.065456','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(26,'2026-02-06 05:59:03.072789','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(27,'2026-02-06 05:59:06.077658','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(28,'2026-02-06 05:59:09.266712','9','悟紅玉葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(29,'2026-02-06 13:19:56.563477','1','巨峰葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5546\\u54c1\\u540d\\u7a31\"]}}]',8,1),(30,'2026-02-06 14:58:38.598747','1','巨峰葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5eab\\u5b58\\u6578\\u91cf\"]}}]',8,1),(31,'2026-02-07 13:27:52.697298','2','麝香葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5217\\u8868\\u7c21\\u8ff0\"]}}]',8,1),(32,'2026-02-07 13:28:28.182897','3','貓眼葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5217\\u8868\\u7c21\\u8ff0\"]}}]',8,1),(33,'2026-02-07 13:28:55.246528','4','我的心葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5217\\u8868\\u7c21\\u8ff0\"]}}]',8,1),(34,'2026-02-07 13:29:22.469042','5','天晴葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5217\\u8868\\u7c21\\u8ff0\"]}}]',8,1),(35,'2026-02-07 13:30:19.460411','6','皇冠葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5217\\u8868\\u7c21\\u8ff0\"]}}]',8,1),(36,'2026-02-07 13:30:40.960475','7','長野紫葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5217\\u8868\\u7c21\\u8ff0\"]}}]',8,1),(37,'2026-02-07 13:31:10.097002','8','妮娜葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5217\\u8868\\u7c21\\u8ff0\"]}}]',8,1),(38,'2026-02-07 13:31:26.446387','9','悟紅玉葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5217\\u8868\\u7c21\\u8ff0\"]}}]',8,1),(39,'2026-02-07 13:31:38.702952','10','天山葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5217\\u8868\\u7c21\\u8ff0\"]}}]',8,1),(40,'2026-02-07 13:33:26.427387','11','三色葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5217\\u8868\\u7c21\\u8ff0\"]}}]',8,1),(41,'2026-02-07 13:34:48.841140','12','雙色葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5217\\u8868\\u7c21\\u8ff0\"]}}]',8,1),(42,'2026-02-09 01:56:41.105591','1','巨峰葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(43,'2026-02-09 02:33:02.697766','12','雙色葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(44,'2026-02-09 02:41:16.641887','12','雙色葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(45,'2026-02-09 02:41:26.339467','11','三色葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(46,'2026-02-09 02:41:39.634439','10','天山葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(47,'2026-02-09 02:41:51.349625','9','悟紅玉葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(48,'2026-02-09 02:41:58.782632','8','妮娜葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(49,'2026-02-09 02:42:11.412227','7','長野紫葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(50,'2026-02-09 02:42:17.081365','7','長野紫葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(51,'2026-02-09 02:42:27.012311','6','皇冠葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(52,'2026-02-09 02:42:35.330270','5','天晴葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(53,'2026-02-09 02:42:42.513710','4','我的心葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(54,'2026-02-09 02:42:53.937525','3','貓眼葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(55,'2026-02-09 02:43:14.387782','2','麝香葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u8a08\\u91cf\\u55ae\\u4f4d\", \"\\u898f\\u683c\\u6578\\u503c\"]}}]',8,1),(56,'2026-02-09 02:43:29.299092','2','麝香葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u50f9\\u683c\", \"\\u8a08\\u91cf\\u55ae\\u4f4d\"]}}]',8,1),(57,'2026-02-09 02:43:37.472992','1','巨峰葡萄禮盒',2,'[]',8,1),(58,'2026-02-09 04:00:53.552478','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(59,'2026-02-09 04:01:11.538983','10','天山葡萄',2,'[]',7,1),(60,'2026-02-09 04:01:35.682611','10','天山葡萄禮盒',2,'[]',8,1),(61,'2026-02-09 04:01:55.862477','10','天山葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5eab\\u5b58\\u6578\\u91cf\"]}}]',8,1),(62,'2026-02-09 04:47:43.795119','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(63,'2026-02-10 02:39:03.616467','1','巨峰葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(64,'2026-02-10 02:40:06.418899','2','麝香葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(65,'2026-02-10 02:50:35.458740','1','巨峰葡萄',2,'[]',7,1),(66,'2026-02-10 02:52:25.012935','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(67,'2026-02-10 02:55:23.850751','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(68,'2026-02-10 02:59:08.302793','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(69,'2026-02-10 02:59:43.188409','1','巨峰葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(70,'2026-02-10 03:02:09.559106','2','麝香葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5eab\\u5b58\\u6578\\u91cf\"]}}]',8,1),(71,'2026-02-10 03:26:13.753023','12','雙色葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u6df7\\u5408\\u53e3\\u5473\\u4e0a\\u9650\"]}}]',8,1),(72,'2026-02-10 03:26:13.757146','11','三色葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u6df7\\u5408\\u53e3\\u5473\\u4e0a\\u9650\"]}}]',8,1),(73,'2026-02-10 04:00:57.923736','8','妮娜葡萄',2,'[]',7,1),(74,'2026-02-10 05:11:33.279283','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(75,'2026-02-10 05:17:05.039862','8','妮娜葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(76,'2026-02-10 05:17:05.042988','7','長野紫葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(77,'2026-02-10 05:17:05.044470','6','皇冠葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(78,'2026-02-10 05:17:05.046129','5','天晴葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(79,'2026-02-10 05:17:05.047767','4','我的心葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(80,'2026-02-10 05:37:17.261405','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(81,'2026-02-10 05:37:17.264562','9','悟紅玉葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(82,'2026-02-10 05:37:17.266670','8','妮娜葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(83,'2026-02-10 05:37:17.268873','7','長野紫葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(84,'2026-02-10 05:37:17.270376','6','皇冠葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(85,'2026-02-10 05:47:38.099068','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(86,'2026-02-10 05:47:38.103460','9','悟紅玉葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(87,'2026-02-10 05:47:38.105464','8','妮娜葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(88,'2026-02-10 05:47:38.107292','7','長野紫葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(89,'2026-02-10 05:54:09.914289','5','天晴葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(90,'2026-02-10 06:16:50.328442','1','巨峰葡萄禮盒',2,'[{\"added\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u5de8\\u5cf0\\u8461\\u8404\\u79ae\\u76d2 - S \\u7279\\u7d1a\\u679c\"}}, {\"added\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u5de8\\u5cf0\\u8461\\u8404\\u79ae\\u76d2 - A \\u512a\\u9078\\u679c\"}}]',8,1),(91,'2026-02-10 06:54:07.215134','1','巨峰葡萄禮盒',2,'[{\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u5de8\\u5cf0\\u8461\\u8404\\u79ae\\u76d2 - S \\u7279\\u7d1a\\u679c\", \"fields\": [\"\\u5eab\\u5b58\"]}}]',8,1),(92,'2026-02-10 07:04:56.014607','1','巨峰葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5eab\\u5b58\\u6578\\u91cf\"]}}]',8,1),(93,'2026-02-11 04:59:07.193718','1','巨峰葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u6df7\\u5408\\u53e3\\u5473\\u4e0a\\u9650\"]}}]',8,1),(94,'2026-02-11 05:02:15.354689','1','巨峰葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(95,'2026-02-11 06:48:46.404386','1','巨峰葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(96,'2026-02-11 06:48:52.602186','1','巨峰葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(97,'2026-02-11 06:57:22.833612','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(98,'2026-02-11 06:57:22.835927','8','妮娜葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(99,'2026-02-11 06:57:22.837935','7','長野紫葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(100,'2026-02-11 06:58:04.072667','10','天山葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(101,'2026-02-11 06:58:04.074935','8','妮娜葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(102,'2026-02-11 06:58:04.076973','7','長野紫葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(103,'2026-02-11 06:58:04.078631','6','皇冠葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(104,'2026-02-12 00:41:30.414366','1','巨峰葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(105,'2026-02-12 00:42:55.767439','1','巨峰葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(106,'2026-02-12 00:48:15.122869','1','巨峰葡萄禮盒',2,'[{\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u5de8\\u5cf0\\u8461\\u8404\\u79ae\\u76d2 - A \\u512a\\u9078\\u679c\", \"fields\": [\"\\u5eab\\u5b58\"]}}, {\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u5de8\\u5cf0\\u8461\\u8404\\u79ae\\u76d2 - S \\u7279\\u7d1a\\u679c\", \"fields\": [\"\\u5eab\\u5b58\"]}}]',8,1),(107,'2026-02-12 00:49:42.813007','1','巨峰葡萄禮盒',2,'[]',8,1),(108,'2026-02-12 00:53:37.887684','1','巨峰葡萄禮盒',2,'[{\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u5de8\\u5cf0\\u8461\\u8404\\u79ae\\u76d2 - A \\u512a\\u9078\\u679c\", \"fields\": [\"\\u5eab\\u5b58\"]}}, {\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u5de8\\u5cf0\\u8461\\u8404\\u79ae\\u76d2 - S \\u7279\\u7d1a\\u679c\", \"fields\": [\"\\u5eab\\u5b58\"]}}]',8,1),(109,'2026-02-12 00:55:26.539411','1','巨峰葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5eab\\u5b58\\u6578\\u91cf\"]}}]',8,1),(110,'2026-02-12 00:56:34.702375','1','巨峰葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5eab\\u5b58\\u6578\\u91cf\"]}}, {\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u5de8\\u5cf0\\u8461\\u8404\\u79ae\\u76d2 - A \\u512a\\u9078\\u679c\", \"fields\": [\"\\u5eab\\u5b58\"]}}, {\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u5de8\\u5cf0\\u8461\\u8404\\u79ae\\u76d2 - S \\u7279\\u7d1a\\u679c\", \"fields\": [\"\\u5eab\\u5b58\"]}}]',8,1),(111,'2026-02-12 01:00:40.071137','1','巨峰葡萄禮盒',2,'[{\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u5de8\\u5cf0\\u8461\\u8404\\u79ae\\u76d2 - S \\u7279\\u7d1a\\u679c\", \"fields\": [\"\\u7b49\\u7d1a\\u540d\\u7a31\", \"\\u50f9\\u683c\"]}}, {\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u5de8\\u5cf0\\u8461\\u8404\\u79ae\\u76d2 - A \\u512a\\u9078\\u679c\", \"fields\": [\"\\u7b49\\u7d1a\\u540d\\u7a31\", \"\\u50f9\\u683c\"]}}]',8,1),(112,'2026-02-12 01:00:58.357623','1','巨峰葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(113,'2026-02-12 01:01:33.625805','1','巨峰葡萄禮盒',2,'[{\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u5de8\\u5cf0\\u8461\\u8404\\u79ae\\u76d2 - S \\u7279\\u7d1a\\u679c\", \"fields\": [\"\\u5eab\\u5b58\"]}}]',8,1),(114,'2026-02-12 01:58:37.064710','11','三色葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5eab\\u5b58\\u6578\\u91cf\"]}}]',8,1),(115,'2026-02-12 02:00:48.243719','11','三色葡萄禮盒',2,'[{\"added\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u4e09\\u8272\\u8461\\u8404\\u79ae\\u76d2 - S \\u7279\\u7d1a\\u679c\"}}, {\"added\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u4e09\\u8272\\u8461\\u8404\\u79ae\\u76d2 - A \\u512a\\u9078\\u679c\"}}]',8,1),(116,'2026-02-12 02:03:45.586124','11','三色葡萄禮盒',2,'[{\"added\": {\"name\": \"\\u5546\\u54c1\\u66f4\\u591a\\u5716\\u7247\", \"object\": \"\\u4e09\\u8272\\u8461\\u8404\\u79ae\\u76d2 \\u7684\\u5716\\u7247\"}}]',8,1),(117,'2026-02-12 02:07:21.532849','11','三色葡萄禮盒',2,'[{\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u4e09\\u8272\\u8461\\u8404\\u79ae\\u76d2 - A \\u512a\\u9078\\u679c\", \"fields\": [\"\\u5eab\\u5b58\"]}}]',8,1),(118,'2026-02-12 03:32:10.880856','11','三色葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5eab\\u5b58\\u6578\\u91cf\"]}}]',8,1),(119,'2026-02-12 03:33:15.775494','11','三色葡萄禮盒',2,'[{\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u4e09\\u8272\\u8461\\u8404\\u79ae\\u76d2 - S \\u7279\\u7d1a\\u679c\", \"fields\": [\"\\u5eab\\u5b58\"]}}]',8,1),(120,'2026-02-12 03:34:04.469956','11','三色葡萄禮盒',2,'[{\"changed\": {\"fields\": [\"\\u5eab\\u5b58\\u6578\\u91cf\"]}}]',8,1),(121,'2026-02-12 03:38:00.165059','2','麝香葡萄禮盒',2,'[{\"added\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u9e9d\\u9999\\u8461\\u8404\\u79ae\\u76d2 - S \\u7279\\u7d1a\\u679c\"}}, {\"added\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u9e9d\\u9999\\u8461\\u8404\\u79ae\\u76d2 - A \\u512a\\u9078\\u679c\"}}]',8,1),(122,'2026-02-12 03:38:42.820919','2','麝香葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(123,'2026-02-12 03:55:14.394869','2','麝香葡萄禮盒',2,'[{\"changed\": {\"name\": \"\\u5546\\u54c1\\u898f\\u683c/\\u7b49\\u7d1a\", \"object\": \"\\u9e9d\\u9999\\u8461\\u8404\\u79ae\\u76d2 - S \\u7279\\u7d1a\\u679c\", \"fields\": [\"\\u5eab\\u5b58\"]}}]',8,1),(124,'2026-02-12 03:55:46.650591','2','麝香葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(125,'2026-02-12 05:01:21.671281','2','麝香葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1),(126,'2026-02-12 05:04:17.945085','2','麝香葡萄',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u6709\\u8ca8\"]}}]',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (6,'accounts','user'),(1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session'),(8,'store','product'),(10,'store','productgrade'),(9,'store','productimage'),(7,'store','variety');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-02-06 01:20:36.925501'),(2,'contenttypes','0002_remove_content_type_name','2026-02-06 01:20:37.089738'),(3,'auth','0001_initial','2026-02-06 01:20:37.714131'),(4,'auth','0002_alter_permission_name_max_length','2026-02-06 01:20:37.860734'),(5,'auth','0003_alter_user_email_max_length','2026-02-06 01:20:37.870607'),(6,'auth','0004_alter_user_username_opts','2026-02-06 01:20:37.879127'),(7,'auth','0005_alter_user_last_login_null','2026-02-06 01:20:37.890546'),(8,'auth','0006_require_contenttypes_0002','2026-02-06 01:20:37.896514'),(9,'auth','0007_alter_validators_add_error_messages','2026-02-06 01:20:37.909585'),(10,'auth','0008_alter_user_username_max_length','2026-02-06 01:20:37.920794'),(11,'auth','0009_alter_user_last_name_max_length','2026-02-06 01:20:37.932718'),(12,'auth','0010_alter_group_name_max_length','2026-02-06 01:20:37.967435'),(13,'auth','0011_update_proxy_permissions','2026-02-06 01:20:37.979116'),(14,'auth','0012_alter_user_first_name_max_length','2026-02-06 01:20:37.988402'),(15,'accounts','0001_initial','2026-02-06 01:20:38.782486'),(16,'admin','0001_initial','2026-02-06 01:20:39.122069'),(17,'admin','0002_logentry_remove_auto_add','2026-02-06 01:20:39.138554'),(18,'admin','0003_logentry_add_action_flag_choices','2026-02-06 01:20:39.153746'),(19,'sessions','0001_initial','2026-02-06 01:20:39.269394'),(20,'store','0001_initial','2026-02-06 02:57:04.261016'),(21,'store','0002_product','2026-02-06 03:44:13.734101'),(22,'store','0003_variety_is_active','2026-02-06 05:58:07.110251'),(23,'store','0004_product_short_description','2026-02-07 13:21:21.755571'),(24,'store','0005_product_badge_product_unit_type_product_unit_value','2026-02-09 01:55:24.591063'),(25,'store','0006_alter_product_unit_type','2026-02-09 02:20:37.314537'),(26,'store','0007_productimage','2026-02-09 13:10:59.746514'),(27,'store','0008_alter_productimage_options_productimage_order_and_more','2026-02-09 13:19:24.542228'),(28,'store','0009_product_mix_limit','2026-02-10 03:19:12.354186'),(29,'store','0010_productgrade','2026-02-10 06:08:22.743828'),(30,'store','0011_alter_productgrade_options','2026-02-12 01:09:07.547055');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('lm83jihe3061zakadi343y2hnm1jiexq','.eJxVjEEOwiAQRe_C2pC2MEBduvcMZJgZpGpoUtqV8e7apAvd_vfef6mI21ri1mSJE6uz6tXpd0tID6k74DvW26xprusyJb0r-qBNX2eW5-Vw_w4KtvKtkYw4b60lDzAKB0rsJIuh0QBbIWLuHcBgkgMO1nfe5ewBu5RN4EG9PwCXOHo:1voAbE:YpEetJuHYbveES10v7_WBrwBHup4CfvbBdeY4vMpXnI','2026-02-20 01:25:32.729711'),('w59xnxct242tsd5owpqh69yvbl4obliq','.eJxVjEEOwiAQRe_C2pC2MEBduvcMZJgZpGpoUtqV8e7apAvd_vfef6mI21ri1mSJE6uz6tXpd0tID6k74DvW26xprusyJb0r-qBNX2eW5-Vw_w4KtvKtkYw4b60lDzAKB0rsJIuh0QBbIWLuHcBgkgMO1nfe5ewBu5RN4EG9PwCXOHo:1vszRl:ZtLJqdXxIBji17_fs6iyiSTcDWuvshTKpo6TcUKSNFE','2026-03-05 08:31:41.858004');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_product`
--

DROP TABLE IF EXISTS `store_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` int unsigned NOT NULL,
  `stock` int unsigned NOT NULL,
  `is_mixed` tinyint(1) NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `short_description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `badge` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `unit_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `unit_value` decimal(5,1) NOT NULL,
  `mix_limit` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `store_product_chk_1` CHECK ((`price` >= 0)),
  CONSTRAINT `store_product_chk_2` CHECK ((`stock` >= 0)),
  CONSTRAINT `store_product_chk_3` CHECK ((`mix_limit` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_product`
--

LOCK TABLES `store_product` WRITE;
/*!40000 ALTER TABLE `store_product` DISABLE KEYS */;
INSERT INTO `store_product` VALUES (1,'巨峰葡萄禮盒',700,50,0,'【紫黑色的寶石，記憶中的經典美味——巨峰葡萄】\r\n🍇 來自日本的「葡萄之王」 巨峰 (Kyoho) 源自日本，是由「石原早生」與「森田尼」交配選育而成的經典品種。因為果粒碩大、色澤如墨玉般深邃，故有「葡萄之王」的美譽。自引進台灣數十年來，經過在地農民的精湛改良，台灣巨峰的品質已達世界頂尖水準。\r\n\r\n🍇 為什麼它是台灣人的最愛？ 在新品種層出不窮的今天，巨峰依然穩坐台灣人心中的冠軍寶座，原因就在於它無可取代的**「黃金風味」**：\r\n\r\n完美的糖酸比：巨峰不只有單純的甜，而是濃郁果香中帶有一絲絲微酸的尾韻，層次豐富，久吃不膩。\r\n\r\n獨特的口感：果肉緊實Q彈，果汁豐沛，且果皮容易剝離（脫皮性佳），吃起來優雅又滿足。\r\n\r\n懷舊的香氣：那股特有的濃郁葡萄香（Foxy flavor），正是台灣人記憶中「最好吃的葡萄」該有的味道。\r\n\r\n這盒巨峰葡萄，承載著成熟的種植工藝與飽滿的心意，圓潤大氣，是您送禮時最體面、也最能傳遞溫度的選擇。','product_images/grape03.png','','','catty',4.0,0),(2,'麝香葡萄禮盒',1500,50,0,'【如翡翠般閃耀的香氛奇蹟——頂級麝香葡萄】\r\n🍇 日本育種工藝的巔峰 麝香葡萄（Shine Muscat）是日本耗費多年心血，以「安藝津21號」與「白南」交配選育出的夢幻品種。它自帶一股獨特的高雅花香，彷彿荔枝與玫瑰的混合香氣，因此在日本被譽為「可以吃的香水」。\r\n\r\n🍇 風靡全日本的理由 在日本，麝香葡萄是送禮市場的絕對王者。它顛覆了吃葡萄的體驗：\r\n\r\n皮薄爽脆，整顆連皮吃：完全不乾澀的薄皮，咬下時會有清脆的「啵」一聲，口感極佳。\r\n\r\n極致高甜，無籽多汁：糖度常達 18 度以上，卻因獨特的香氣而清爽不膩。\r\n\r\n視覺饗宴：如翡翠寶石般的外觀，擺在盤中就是藝術品。\r\n\r\n🍇 不用飛日本，「田原溫室」為您零時差呈獻 許多人認為頂級麝香葡萄只能仰賴日本空運，但「田原溫室」證明了台灣職人的實力。我們採用與日本同步的溫室栽培技術，嚴格控管日照、水分與疏果工序。','product_images/grape04.png','人氣 No.1！自帶荔枝花香，皮薄無籽，口感清脆香甜，大眾接受度最高。','','bunch',3.0,1),(3,'貓眼葡萄禮盒',1000,1,0,'【黑夜中的紫鑽，行家的隱藏版清單——貓眼葡萄】\r\n🍇 巨峰與麝香的完美混血 貓眼葡萄（Pione / ピオーネ）是日本葡萄發展史上的傑作，它結合了「巨峰」的濃郁甜味與「麝香葡萄」的清爽香氣與大果粒特性。因為果實碩大、色澤深紫近黑，在光線下宛如貓眼般神秘深邃，故有此美名。\r\n\r\n🍇 日本人眼中的「黑葡萄之王」 在日本，貓眼葡萄的地位與巨峰不相上下，甚至在高端禮品市場更受青睞。日本人喜愛它的理由很直接：\r\n\r\n壓倒性的存在感：果粒通常比巨峰更大、更飽滿，視覺衝擊力極強。\r\n\r\n進化的口感：它保留了巨峰那種如紅酒般的醇厚風味，但果肉更紮實緊緻，酸甜層次分明，被形容為「成熟大人的風味」。\r\n\r\n🍇 台灣市面難尋的珍稀滋味 在台灣，巨峰隨處可見，但正宗的貓眼葡萄卻極為稀少。通常您只能在百貨公司的頂級進口超市（如 CitySuper、Mia C\'bon）的冷藏櫃中，看到標著昂貴價格的日本空運盒裝。這是因為貓眼葡萄的著色與栽培難度極高，對環境極為挑剔。\r\n\r\n🍇 獻給懂吃的您，「田原溫室」限量採收 現在，您不需要特地去精品超市掃貨。「田原溫室」挑戰栽培極限，成功在台灣種出了這款夢幻逸品。我們保留了最新鮮的果粉與滋味，讓您以最純粹的方式，品嚐這款市面上罕見、風味濃郁深邃的黑色寶石。','product_images/grape_variety08.png','被譽為「黑色寶石」，果粒碩大，擁有濃郁酒香與絕佳酸甜比，行家最愛。','','bunch',3.0,1),(4,'我的心葡萄禮盒',2000,1,0,'【以愛為名，渾然天成——My Heart 寶石紅愛心葡萄】\r\n❤️ 是真的！大自然親手雕琢的愛心 第一眼看見它，許多人會忍不住驚呼：「這是有用模具塑形的嗎？」 請相信您的眼睛，這絕對不是人工模具壓製，而是源自日本的奇蹟品種。它天生就是如此浪漫的愛心形狀！每一顆心型果實，都是大自然基因與極致栽培工藝的完美結合。\r\n\r\n❤️ 葡萄界的夢幻稀有種 「My Heart」結合了麝香葡萄的爽脆口感。它在台灣極為罕見，因為栽培難度極高——要種出形狀完美對稱、色澤如紅寶石般透亮的愛心，需要極為嚴苛的溫室環境與職人技術。這不是隨處可見的水果，而是僅有少數人能擁有的夢幻逸品。\r\n\r\n❤️ 始於顏值，忠於口感 千萬別以為它只是「長得好看」。My Heart 繼承了麝香葡萄的優點：\r\n\r\n皮薄無籽：洗淨後直接連皮大口咬下。\r\n\r\n極致脆甜：果肉紮實硬脆，糖度經常飆破 20 度，甜美多汁且帶有清新的花果香。\r\n\r\n❤️ 最頂級的告白神器 它的名字就叫**「My Heart」（我的心）**。 還有什麼比這更適合送給摯愛？不需要過多的言語，送上這一盒，就是將滿滿的真心捧到對方面前。無論是情人節、紀念日，或是想要傳遞心意的時刻，「田原溫室」為您獻上這份最獨特、最深情的甜蜜驚喜。','product_images/grape_variety01.png','天然夢幻的心型外觀，紅寶石色澤，口感清脆高甜，送禮告白神器。','','bunch',3.0,1),(5,'天晴葡萄禮盒',1600,1,0,'【超越麝香的極致顛峰——天晴葡萄】\r\n🍇 傳說中的「幻之品種」 如果說麝香葡萄是綠色葡萄的女王，那麼「天晴」就是當之無愧的帝王。 這是由著名的日本培育出的稀世珍品。它的存在本身就是一種挑戰——在麝香葡萄已經如此受歡迎的當下，天晴硬是將「美味的上限」再往上推升了一個層次。\r\n\r\n🍇 視覺與味覺的雙重震撼 天晴最讓人一眼難忘的，是它那驚人的尺寸。\r\n\r\n碩大無朋：它的果粒比一般的麝香葡萄更為巨大、圓潤，拿在手中沉甸甸的份量感，展現出壓倒性的氣勢。\r\n\r\n口感進化：它繼承了麝香葡萄的優雅花香與無籽爽脆，但甜度更為濃縮深邃，果汁爆發力更強。這是一種更為成熟、厚實的頂級風味。\r\n\r\n🍇 日本人也難以一親芳澤 「天晴」之所以珍貴，是因為它即便在日本，也是屬於**「產地限定」**的夢幻逸品。由於栽培難度極高、產量稀少，除了高級水果專賣店或親自造訪產地，一般日本超市幾乎見不到它的蹤影。\r\n\r\n🍇 獻給追求極致的您 不用買機票飛往日本產地尋寶，「田原溫室」將這份傳說帶到了您面前。 我們以職人精神細心呵護每一串天晴，只為將這款**「比稀有更稀有」**的綠色寶石，獻給真正懂得品味的您。這不只是一盒葡萄，更是水果界金字塔頂端的體驗。','product_images/grape_variety04.png','麝香葡萄的「巨大進化版」，果實更圓潤碩大，產量稀少，極致奢華。','','bunch',3.0,1),(6,'皇冠葡萄禮盒',1300,1,0,'【巨峰的進化完全體——皇冠】\r\n👑 應對氣候變遷的新世代傑作 在地球暖化、氣候異常的挑戰下，傳統巨峰葡萄常面臨著色不佳的困境。為了延續黑色葡萄的美味傳奇，「皇冠」應運而生。它是為了新時代而育成的強勢品種，即使在高溫環境下，依然能呈現出完美深邃的墨黑光澤，展現出強韌的生命力與頂級的賣相。\r\n\r\n👑 視覺與口感的雙重升級 如果說巨峰是經典，那皇冠就是「升級後的震撼」。\r\n\r\n壓倒性的巨大：它的果粒比一般巨峰明顯大上一號，視覺上的飽滿度令人驚艷。\r\n\r\n紮實彈牙的肉質：不同於巨峰偏軟多汁的口感，大皇冠的果肉更為硬實Q彈，咬下去有實在的阻力感，咀嚼起來更具滿足度。\r\n\r\n👑 傳承經典香氣，風味更濃郁 它保留了台灣人最愛的獨特狐香（Foxy flavor）——那股濃郁醉人的葡萄芬芳，但在口感上卻更為俐落。深厚的紫黑色果皮下，包裹著高糖度且酸甜適中的果汁，每一口都是記憶中熟悉的美味，卻擁有前所未有的爽快食感。\r\n\r\n👑 獻給懂趨勢的品味家 這不只是一串葡萄，更是農業技術戰勝氣候變遷的美味證明。「田原溫室」為您引進這款市面上少見的潛力新星，讓您在送禮時，不僅送出美味，更送出了一份與時俱進的獨特話題。','product_images/grape_variety06.png','巨峰的升級版，色澤墨黑，果粒比巨峰更大，肉質更紮實Q彈，風味濃厚。','','bunch',3.0,1),(7,'長野紫葡萄禮盒',1500,1,0,'黑色的奇蹟，連皮享用的極致奢華——長野紫葡萄】\r\n🍇 日本葡萄界的革命性品種 如其名長野紫是日本長野縣耗時多年所培育的新星品種。在日本超市，它與麝香葡萄並列為兩大頂級明星，是無數愛好者心中「一生必嚐」的夢幻逸品。\r\n\r\n🍇 顛覆常識！唯一的「全食」黑葡萄 一般人對黑色葡萄的印象都是「皮厚、要吐皮」。但長野紫打破了這個規則！ 它繼承了歐亞種葡萄的優點，皮薄如紙，完全無澀味。洗淨後，您可以像吃麝香葡萄一樣，整顆直接放入嘴裡。那種咬破清脆果皮、瞬間迸發濃郁果汁的快感，是傳統巨峰無法比擬的全新體驗。\r\n\r\n🍇 橢圓寶石，難以量產的珍稀美味 不同於圓潤的巨峰，長野紫呈現優雅的長橢圓形。 這款葡萄極為嬌貴，栽培過程中容易裂果，對環境要求近乎苛求，因此即使在日本，產量也相當稀少，難以大規模量產。\r\n\r\n🍇 比巨峰更清爽的「大人味」 它的風味既保留了巨峰的濃郁香甜，又多了一份屬於「列扎馬特」的清爽高雅。甜度雖高，卻因連皮食用的清脆口感而絲毫不膩，被譽為黑葡萄風味的完全體。\r\n\r\n🍇 「田原溫室」限量呈獻 物以稀為貴，這款連日本人都視為珍寶的葡萄，現在由我們為您呈現。無需剝皮、無需吐籽，請盡情享受這款能一口品嚐到黑色葡萄濃郁靈魂的稀有傑作。','product_images/grape_variety02.png','少數「能連皮吃」的黑葡萄，無籽不澀，風味優雅細緻，日本夢幻逸品。','','bunch',3.0,1),(8,'妮娜葡萄禮盒',1500,1,0,'【紅色葡萄的最高傑作——妮娜皇后】\r\n👑 繼巨峰之後，日本最新的紅色傳奇 如果不滿足於傳統的紫黑巨峰，那麼「妮娜皇后」絕對能震撼您的味蕾。 這是日本近年來最受矚目的紅色葡萄新品種，被視為紅葡萄界的巔峰之作。在日本，它以絕美的鮮紅色澤與驚人的美味，迅速擄獲了無數饕客的心，地位正急速攀升，直逼麝香葡萄。\r\n\r\n👑 台灣難得一見的「隱藏版」美味 在台灣，妮娜皇后之所以鮮為人知，是因為它的種植難度極高。紅葡萄要「著色完美」極度考驗氣候與技術，稍有不慎就會顏色不均。因此，市面上極少有農園願意挑戰，它是真正**「有錢也未必買得到」**的稀有珍品。但在「田原溫室」，我們克服了重重困難，成功將這位嬌貴的皇后留在了台灣。\r\n\r\n👑 超越巨峰的奢華享受 它的魅力，一入口就懂：\r\n\r\n比巨峰更巨大的霸氣：果粒碩大圓潤，視覺尺寸往往比巨峰更具份量感。\r\n\r\n令人著迷的「紅酒香」：不同於一般的果香，妮娜皇后帶有一股獨特而濃郁的草莓與紅酒混合香氣，風味高雅且富有層次。\r\n\r\n極致高甜：糖度極高，酸味極低，皮薄多汁，每一口都是濃縮的甜蜜炸彈。\r\n\r\n👑 送禮的最高品味 送膩了常見的水果嗎？送上一盒妮娜皇后，送的是一份「懂行」的驚喜。那如紅寶石般璀璨的色澤，象徵著富貴與熱情，絕對是讓收禮者眼睛一亮、難以忘懷的頂級好禮。','product_images/grape_variety03.png','紅葡萄女王，帶有獨特草莓與紅酒香氣，糖度極高，色澤豔麗迷人。','','bunch',3.0,1),(9,'悟紅玉葡萄禮盒',1500,0,0,'如乒乓球般的震撼視覺！巨大的紅寶石——悟紅玉】\r\n\r\n🔴 挑戰葡萄界的尺寸天花板 打開禮盒的瞬間，準備好迎接一聲驚嘆：「這真的是葡萄嗎？」 悟紅玉（Gorby）以其驚人的巨大果粒聞名，發育良好的果實甚至能長得像乒乓球一樣壯觀！它是葡萄界名副其實的巨無霸，拿在手中那沈甸甸的份量感，絕對能帶來前所未有的視覺震撼。\r\n\r\n🔴 職人技術打造的「鮮紅寶石」 「悟紅玉」之名，寓意著如紅玉（紅寶石）般珍貴的色澤。 在溫暖的台灣，要讓紅色葡萄完美轉色是極高難度的挑戰（容易著色不均或過深變黑）。但「田原溫室」運用特殊的調節技術與精準的肥培管理，成功克服氣候限制，讓每一顆巨果都披上鮮豔誘人的寶石紅外衣，晶瑩剔透，名符其實。\r\n\r\n🔴 色香味俱全的奢華滋味 它不只大，還很好吃！ 悟紅玉擁有一股獨特的淡雅清香，果肉屬於硬脆紮實的口感，咬下時能感受到果肉的彈性，隨後是高甜度的果汁在口中迸發。\r\n\r\n🔴 送出「重量級」的心意 這是一份極具份量的禮物。無論是那如紅寶石般喜氣的色澤，還是如乒乓球般霸氣的尺寸，悟紅玉都是送禮時展現大氣、尊榮感的最佳選擇。','product_images/grape_variety05.png','視覺震撼！果粒可達乒乓球大小，鮮紅如紅寶石，口感硬脆多汁。','','bunch',3.0,1),(10,'天山葡萄禮盒',1200,1,0,'【這不是葡萄，這是綠色的寶石炸彈——天山葡萄】\r\n🍇 挑戰「一口吃不下」的巨大極限 第一次見到「天山」，每個人都會懷疑自己的眼睛：「這真的是葡萄嗎？」 它的體型大到顛覆常識！單顆就能長到像乒乓球、甚至小雞蛋那麼大（約 30~40 克）。拿在手裡沉甸甸的，一顆就幾乎塞滿手掌。這不是普通的水果，它是葡萄界的巨人，光是擺在盤子裡，氣場就足以鎮壓全場。\r\n\r\n🍇 咬下去是「瀑布」般的果汁感 別被它粗獷的巨大外表騙了，它的口感其實比誰都細緻。 因為果皮極薄（薄到幾乎無法剝皮），天山葡萄最棒的吃法就是整顆連皮大口咬下。 那一瞬間，您會感受到什麼叫「爆漿」——清爽高雅的甜味伴隨著驚人的果汁量，在口中像瀑布一樣湧出。它不像麝香葡萄那麼甜膩，而是充滿水分的清甜，吃完一顆，就像喝了一杯現榨果汁般解渴又過癮。\r\n\r\n🍇 農夫最頭痛的「嬌氣千金」 為什麼市面上這麼少見？因為它真的太難伺候了！ 天山葡萄又有個綽號叫**「裂果天山」。正因為它的皮太薄、肉太脆，只要空氣稍微潮濕一點，果實就會裂開，種植風險極高。能成功從樹上採摘下來的每一顆，都是農夫與老天爺搶時間的「奇蹟生還者」**。\r\n\r\n🍇 送一份「絕對會被記住」的驚喜 在日本，這可是連媒體都爭相報導、一串動輒破萬日幣的超高級品。 如果您想找一份禮物，能讓收禮的人第一眼就驚呼、第一口就感動，那「田原溫室」的天山葡萄絕對是唯一解。這不只是一盒葡萄，更是一個會讓大家熱烈討論的美味話題。','product_images/grape_variety04_p4ZWrCm.png','體型巨大的「奇蹟葡萄」，皮極薄、果汁如瀑布般豐沛，市面極罕見。','','bunch',3.0,1),(11,'三色葡萄禮盒',1800,10,1,'【田原嚴選】一盒收盡季節的奢華——頂級三色葡萄珠寶盒\r\n✨ 為什麼要選擇？小孩子才做選擇，懂享受的您全都要！ 打開禮盒的瞬間，彷彿打開了一個璀璨的珠寶盒。 深邃的黑曜石、透亮的翡翠綠、嬌豔的紅寶石——我們將葡萄界最迷人的三種色澤，完美匯聚於一盒之中。這不僅是味蕾的盛宴，更是一場華麗的視覺饗宴。\r\n\r\n🍇 園主親選．今日的「旬」之味 (Omakase) 為了讓您品嚐到真正的「完熟」滋味，我們的三色禮盒沒有固定名單。 葡萄的熟成是大自然的節奏，無法催促。每天清晨，「田原溫室」的職人會巡視果園，親自挑選當下糖度最高、香氣最足、口感最棒的三種品種進行搭配。\r\n\r\n您收到的，絕對是**「當天果園裡的冠軍」**。每一次開箱，都是一場與季節相遇的驚喜！\r\n\r\n🌈 您的禮盒可能包含以下夢幻陣容：\r\n\r\n🖤 黑色的濃郁靈魂： 可能是經典的巨峰，或是帶有酒香的貓眼，甚至是巨大的大皇冠。象徵著葡萄最醇厚、傳統的王者風味。\r\n\r\n💚 綠色的清香優雅： 或許是自帶花香的麝香葡萄，或者是巨大稀有的天山、天晴。清脆爽口，如同將森林的氣息一口咬下。\r\n\r\n❤️ 紅色的稀有驚艷： 幸運的話，您將遇見帶有草莓香的妮娜皇后，或是巨大的紅寶石悟紅玉，甚至是心型的My Heart。這是市面上最難尋覓的甜美滋味。\r\n\r\n🎁 送禮的最高境界 這一盒，滿足了所有挑剔的味蕾。 喜歡濃郁的長輩、喜愛清脆的小孩、追求稀有的行家，都能在其中找到自己的最愛。送上一盒「三色珠寶盒」，代表著您面面俱到的貼心，與不凡的品味。','product_images/S__41623565_0.jpg','如珠寶盒般的夢幻逸品！一次集結紅、綠、黑三種色澤，每日精選當下最完熟品種，送禮氣派首選。','','bunch',3.0,3),(12,'雙色葡萄禮盒',1200,1,1,'【自選．雙重奏】田原頂級雙色葡萄禮盒\r\n✨ 您的禮盒，由您親自定義 不想被固定組合束縛？想要一次品嚐兩種截然不同的頂級滋味？ 「田原溫室」特別推出自選雙色禮盒，把選擇權交回您的手中。我們每日更新架上最新鮮的採收名單，讓您依照個人喜好或送禮對象的口味，自由搭配出最完美的「美味二重奏」。\r\n\r\n🍇 創造專屬於您的風味對比 葡萄的世界如此精彩，為什麼要只選一種？透過雙色搭配，您可以體驗味蕾的層次跳躍：\r\n\r\n經典互補（黑＋綠）： 選擇濃郁醇厚的巨峰/貓眼，搭配清脆爽口的麝香葡萄。一濃一清，一軟一脆，是永遠吃不膩的黃金組合。\r\n\r\n視覺饗宴（紅＋綠）： 將帶有獨特花香的妮娜皇后或My Heart，與如翡翠般的天晴/天山搭配。紅綠相映的聖誕配色，是送禮最吸睛的選擇。\r\n\r\n奢華攻頂（稀有＋稀有）： 趁著庫存釋出，將兩款市面上罕見的「幻之品種」強強聯手，打造一盒有錢也難買到的夢幻逸品。\r\n\r\n📦 產地直送，庫存即時連線 我們的選單與溫室庫存同步。只要您在選單上點得到的，就是我們現在樹上正新鮮、準備為您採摘的。 不再盲選，不再將就。現在就點開選單，組合出一盒充滿您個人風格的頂級葡萄禮盒吧！','product_images/S__41623565_0_W383nDO.jpg','嚴選當季雙色組合！一次品嚐兩種截然不同的頂級風味，無論是濃郁或清爽，讓您好事成雙，美味加倍。','','bunch',2.0,2);
/*!40000 ALTER TABLE `store_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_product_varieties`
--

DROP TABLE IF EXISTS `store_product_varieties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_product_varieties` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` bigint NOT NULL,
  `variety_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `store_product_varieties_product_id_variety_id_cda4e5a7_uniq` (`product_id`,`variety_id`),
  KEY `store_product_varieties_variety_id_0ae16f05_fk_store_variety_id` (`variety_id`),
  CONSTRAINT `store_product_varieties_product_id_b7080061_fk_store_product_id` FOREIGN KEY (`product_id`) REFERENCES `store_product` (`id`),
  CONSTRAINT `store_product_varieties_variety_id_0ae16f05_fk_store_variety_id` FOREIGN KEY (`variety_id`) REFERENCES `store_variety` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_product_varieties`
--

LOCK TABLES `store_product_varieties` WRITE;
/*!40000 ALTER TABLE `store_product_varieties` DISABLE KEYS */;
INSERT INTO `store_product_varieties` VALUES (1,1,1),(2,2,2),(3,3,3),(4,4,4),(5,5,5),(6,6,6),(7,7,7),(8,8,8),(9,9,9),(10,10,10),(11,11,1),(12,11,2),(13,11,3),(14,11,4),(15,11,5),(16,11,6),(17,11,7),(18,11,8),(19,11,9),(20,11,10),(21,12,1),(22,12,2),(23,12,3),(24,12,4),(25,12,5),(26,12,6),(27,12,7),(28,12,8),(29,12,9),(30,12,10);
/*!40000 ALTER TABLE `store_product_varieties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_productgrade`
--

DROP TABLE IF EXISTS `store_productgrade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_productgrade` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` int NOT NULL,
  `stock` int NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_productgrade_product_id_c462b42c_fk_store_product_id` (`product_id`),
  CONSTRAINT `store_productgrade_product_id_c462b42c_fk_store_product_id` FOREIGN KEY (`product_id`) REFERENCES `store_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_productgrade`
--

LOCK TABLES `store_productgrade` WRITE;
/*!40000 ALTER TABLE `store_productgrade` DISABLE KEYS */;
INSERT INTO `store_productgrade` VALUES (1,'A 優選果',550,0,1),(2,'S 特級果',700,20,1),(3,'S 特級果',1800,0,11),(4,'A 優選果',1500,0,11),(5,'S 特級果',1500,0,2),(6,'A 優選果',1200,10,2);
/*!40000 ALTER TABLE `store_productgrade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_productimage`
--

DROP TABLE IF EXISTS `store_productimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_productimage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` bigint NOT NULL,
  `order` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_productimage_product_id_e50e4046_fk_store_product_id` (`product_id`),
  CONSTRAINT `store_productimage_product_id_e50e4046_fk_store_product_id` FOREIGN KEY (`product_id`) REFERENCES `store_product` (`id`),
  CONSTRAINT `store_productimage_chk_1` CHECK ((`order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_productimage`
--

LOCK TABLES `store_productimage` WRITE;
/*!40000 ALTER TABLE `store_productimage` DISABLE KEYS */;
INSERT INTO `store_productimage` VALUES (1,'product_gallery/Gemini_Generated_Image_q7w4o6q7w4o6q7w4.png',11,0);
/*!40000 ALTER TABLE `store_productimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_variety`
--

DROP TABLE IF EXISTS `store_variety`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_variety` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_variety`
--

LOCK TABLES `store_variety` WRITE;
/*!40000 ALTER TABLE `store_variety` DISABLE KEYS */;
INSERT INTO `store_variety` VALUES (1,'巨峰葡萄','紫黑色','葡萄之王，果肉緊實多汁，糖度高且帶有濃郁的傳統葡萄香氣，是台灣人最熟悉的頂級風味。',1),(2,'麝香葡萄','綠色','日本最具代表性的品種，果皮極薄可連皮食用，果肉脆彈，帶有獨特的高雅花香與荔枝香氣。',0),(3,'貓眼葡萄','紫黑色','巨峰葡萄的進階品種，果實碩大如貓眼般深邃，無籽多汁，酸甜比例完美，口感爽脆。',1),(4,'我的心葡萄','紅色','極為稀有的心形葡萄，果粒呈現浪漫的愛心形狀，皮薄多汁，帶有清甜的蜂蜜香氣，送禮首選，栽培難度非常困難。',0),(5,'天晴葡萄','綠色','麝香葡萄的高階品種，果實更為緊實脆口，糖度極高，帶有淡淡的清爽果香，口感層次豐富。',1),(6,'皇冠葡萄','紫黑色','果粒巨大，外型霸氣如皇冠，口感清脆香甜，水分極多，是近年最新因應氣候發展出的品種。',0),(7,'長野紫葡萄','紫黑色','巨峰與歐洲葡萄的混種，果形橢圓，兼具巨峰的濃郁甜味和歐洲葡萄皮薄特性，可連皮食用，口感絕佳。',0),(8,'妮娜葡萄','紅色','又稱妮娜皇后，帶有獨特的紅酒與草莓香氣，糖度極高，色澤如紅寶石般璀璨，極具人氣。',0),(9,'悟紅玉葡萄','紅色','果皮呈現美麗的透亮紅色，據說能長到跟高爾夫球一樣的大，甜度高且帶有優雅的香氣，因著色困難栽培難度高。',0),(10,'天山葡萄','綠色','世界最大級的葡萄品種之一，果粒極大，皮薄肉脆，清甜不膩，視覺效果極為震撼。',0);
/*!40000 ALTER TABLE `store_variety` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-23 14:30:49
