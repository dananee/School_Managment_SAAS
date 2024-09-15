-- MySQL dump 10.13  Distrib 8.4.2, for Linux (x86_64)
--
-- Host: localhost    Database: school_managment_db
-- ------------------------------------------------------
-- Server version	8.4.2

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
-- Table structure for table `Attendance`
--

DROP TABLE IF EXISTS `Attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Attendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` datetime(6) NOT NULL,
  `schedule_id` bigint DEFAULT NULL,
  `school_id` bigint NOT NULL,
  `teacher_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Attendance_schedule_id_2aa77b1e_fk_ClassSchedule_id` (`schedule_id`),
  KEY `Attendance_school_id_8e33f6a6_fk_school_data_tb_id` (`school_id`),
  KEY `Attendance_teacher_id_0d59a776_fk_Teacher_id` (`teacher_id`),
  CONSTRAINT `Attendance_schedule_id_2aa77b1e_fk_ClassSchedule_id` FOREIGN KEY (`schedule_id`) REFERENCES `ClassSchedule` (`id`),
  CONSTRAINT `Attendance_school_id_8e33f6a6_fk_school_data_tb_id` FOREIGN KEY (`school_id`) REFERENCES `school_data_tb` (`id`),
  CONSTRAINT `Attendance_teacher_id_0d59a776_fk_Teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `Teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Attendance`
--

LOCK TABLES `Attendance` WRITE;
/*!40000 ALTER TABLE `Attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `Attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Attendance_student`
--

DROP TABLE IF EXISTS `Attendance_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Attendance_student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `attendance_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Attendance_student_attendance_id_student_id_06a69a35_uniq` (`attendance_id`,`student_id`),
  KEY `Attendance_student_student_id_b92dae6d_fk_Student_id` (`student_id`),
  CONSTRAINT `Attendance_student_attendance_id_ef91304d_fk_Attendance_id` FOREIGN KEY (`attendance_id`) REFERENCES `Attendance` (`id`),
  CONSTRAINT `Attendance_student_student_id_b92dae6d_fk_Student_id` FOREIGN KEY (`student_id`) REFERENCES `Student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Attendance_student`
--

LOCK TABLES `Attendance_student` WRITE;
/*!40000 ALTER TABLE `Attendance_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `Attendance_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ClassRoom`
--

DROP TABLE IF EXISTS `ClassRoom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ClassRoom` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `room_name` varchar(255) NOT NULL,
  `capacity` int NOT NULL,
  `building` varchar(255) DEFAULT NULL,
  `is_virtual` tinyint(1) NOT NULL,
  `school_id` bigint DEFAULT NULL,
  `subjects_taught_id` bigint DEFAULT NULL,
  `assigned_teacher_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ClassRoom_subjects_taught_id_6c813ae7_fk_Subject_id` (`subjects_taught_id`),
  KEY `ClassRoom_assigned_teacher_id_e75d197a_fk_Teacher_id` (`assigned_teacher_id`),
  KEY `ClassRoom_school_id_7f9ece7d_fk_school_data_tb_id` (`school_id`),
  CONSTRAINT `ClassRoom_assigned_teacher_id_e75d197a_fk_Teacher_id` FOREIGN KEY (`assigned_teacher_id`) REFERENCES `Teacher` (`id`),
  CONSTRAINT `ClassRoom_school_id_7f9ece7d_fk_school_data_tb_id` FOREIGN KEY (`school_id`) REFERENCES `school_data_tb` (`id`),
  CONSTRAINT `ClassRoom_subjects_taught_id_6c813ae7_fk_Subject_id` FOREIGN KEY (`subjects_taught_id`) REFERENCES `Subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ClassRoom`
--

LOCK TABLES `ClassRoom` WRITE;
/*!40000 ALTER TABLE `ClassRoom` DISABLE KEYS */;
/*!40000 ALTER TABLE `ClassRoom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ClassRoom_classes_taught`
--

DROP TABLE IF EXISTS `ClassRoom_classes_taught`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ClassRoom_classes_taught` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `classroom_id` bigint NOT NULL,
  `classe_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ClassRoom_classes_taught_classroom_id_classe_id_5128b3b2_uniq` (`classroom_id`,`classe_id`),
  KEY `ClassRoom_classes_taught_classe_id_f6204551_fk_Classe_id` (`classe_id`),
  CONSTRAINT `ClassRoom_classes_taught_classe_id_f6204551_fk_Classe_id` FOREIGN KEY (`classe_id`) REFERENCES `Classe` (`id`),
  CONSTRAINT `ClassRoom_classes_taught_classroom_id_b80f5800_fk_ClassRoom_id` FOREIGN KEY (`classroom_id`) REFERENCES `ClassRoom` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ClassRoom_classes_taught`
--

LOCK TABLES `ClassRoom_classes_taught` WRITE;
/*!40000 ALTER TABLE `ClassRoom_classes_taught` DISABLE KEYS */;
/*!40000 ALTER TABLE `ClassRoom_classes_taught` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ClassSchedule`
--

DROP TABLE IF EXISTS `ClassSchedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ClassSchedule` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `day` varchar(10) NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `class_room_id` bigint NOT NULL,
  `school_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ClassSchedule_class_room_id_0f8cfc33_fk_ClassRoom_id` (`class_room_id`),
  KEY `ClassSchedule_school_id_9b30cc18_fk_school_data_tb_id` (`school_id`),
  CONSTRAINT `ClassSchedule_class_room_id_0f8cfc33_fk_ClassRoom_id` FOREIGN KEY (`class_room_id`) REFERENCES `ClassRoom` (`id`),
  CONSTRAINT `ClassSchedule_school_id_9b30cc18_fk_school_data_tb_id` FOREIGN KEY (`school_id`) REFERENCES `school_data_tb` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ClassSchedule`
--

LOCK TABLES `ClassSchedule` WRITE;
/*!40000 ALTER TABLE `ClassSchedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `ClassSchedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Classe`
--

DROP TABLE IF EXISTS `Classe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Classe` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `class_name` varchar(200) NOT NULL,
  `grade` varchar(200) NOT NULL,
  `school_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Classe_school_id_4b2212f5_fk_school_data_tb_id` (`school_id`),
  CONSTRAINT `Classe_school_id_4b2212f5_fk_school_data_tb_id` FOREIGN KEY (`school_id`) REFERENCES `school_data_tb` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Classe`
--

LOCK TABLES `Classe` WRITE;
/*!40000 ALTER TABLE `Classe` DISABLE KEYS */;
INSERT INTO `Classe` VALUES (1,'A1','Bac',1);
/*!40000 ALTER TABLE `Classe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Exam`
--

DROP TABLE IF EXISTS `Exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Exam` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `exam_name` varchar(200) NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `class_association_id` bigint DEFAULT NULL,
  `school_id` bigint DEFAULT NULL,
  `subject_association_id` bigint DEFAULT NULL,
  `teacher_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Exam_teacher_id_a24d60fd_fk_Teacher_id` (`teacher_id`),
  KEY `Exam_class_association_id_6d32f18a_fk_Classe_id` (`class_association_id`),
  KEY `Exam_school_id_37c6d464_fk_school_data_tb_id` (`school_id`),
  KEY `Exam_subject_association_id_474888a2_fk_Subject_id` (`subject_association_id`),
  CONSTRAINT `Exam_class_association_id_6d32f18a_fk_Classe_id` FOREIGN KEY (`class_association_id`) REFERENCES `Classe` (`id`),
  CONSTRAINT `Exam_school_id_37c6d464_fk_school_data_tb_id` FOREIGN KEY (`school_id`) REFERENCES `school_data_tb` (`id`),
  CONSTRAINT `Exam_subject_association_id_474888a2_fk_Subject_id` FOREIGN KEY (`subject_association_id`) REFERENCES `Subject` (`id`),
  CONSTRAINT `Exam_teacher_id_a24d60fd_fk_Teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `Teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Exam`
--

LOCK TABLES `Exam` WRITE;
/*!40000 ALTER TABLE `Exam` DISABLE KEYS */;
/*!40000 ALTER TABLE `Exam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Grade`
--

DROP TABLE IF EXISTS `Grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Grade` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `grade` varchar(255) NOT NULL,
  `student_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Grade_student_id_62618c56_fk_Student_id` (`student_id`),
  CONSTRAINT `Grade_student_id_62618c56_fk_Student_id` FOREIGN KEY (`student_id`) REFERENCES `Student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Grade`
--

LOCK TABLES `Grade` WRITE;
/*!40000 ALTER TABLE `Grade` DISABLE KEYS */;
/*!40000 ALTER TABLE `Grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Notification`
--

DROP TABLE IF EXISTS `Notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(2) NOT NULL,
  `message` varchar(255) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `author` varchar(100) NOT NULL,
  `status` varchar(2) NOT NULL,
  `read` tinyint(1) NOT NULL,
  `sender_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Notification_sender_id_8fa3ad21_fk_SchoolMembers_id` (`sender_id`),
  CONSTRAINT `Notification_sender_id_8fa3ad21_fk_SchoolMembers_id` FOREIGN KEY (`sender_id`) REFERENCES `SchoolMembers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Notification`
--

LOCK TABLES `Notification` WRITE;
/*!40000 ALTER TABLE `Notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `Notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Parent`
--

DROP TABLE IF EXISTS `Parent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Parent` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `Parent_user_id_a6af2263_fk_SchoolMembers_id` FOREIGN KEY (`user_id`) REFERENCES `SchoolMembers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Parent`
--

LOCK TABLES `Parent` WRITE;
/*!40000 ALTER TABLE `Parent` DISABLE KEYS */;
/*!40000 ALTER TABLE `Parent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Parent_student`
--

DROP TABLE IF EXISTS `Parent_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Parent_student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `parent_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Parent_student_parent_id_student_id_5bc1f97a_uniq` (`parent_id`,`student_id`),
  KEY `Parent_student_student_id_55b79700_fk_Student_id` (`student_id`),
  CONSTRAINT `Parent_student_parent_id_a7fd6bc8_fk_Parent_id` FOREIGN KEY (`parent_id`) REFERENCES `Parent` (`id`),
  CONSTRAINT `Parent_student_student_id_55b79700_fk_Student_id` FOREIGN KEY (`student_id`) REFERENCES `Student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Parent_student`
--

LOCK TABLES `Parent_student` WRITE;
/*!40000 ALTER TABLE `Parent_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `Parent_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Person`
--

DROP TABLE IF EXISTS `Person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Person` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `phone` varchar(128) DEFAULT NULL,
  `gender` varchar(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_owner` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `birth_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Person`
--

LOCK TABLES `Person` WRITE;
/*!40000 ALTER TABLE `Person` DISABLE KEYS */;
INSERT INTO `Person` VALUES (1,'pbkdf2_sha256$720000$NmhFEPonP2eiX7JOGmlWp8$1COvudojStf5oxq3++EZ50BRiTrT6XKByz8+jQWCFAE=','2024-09-13 15:44:05.016862','','',NULL,'M','admin@email.com',0,1,1,1,NULL),(2,'pbkdf2_sha256$720000$xuhQwa7PrE6gLXB5dbDv5L$MIyQeWQSjeD4At1Hv70xyMtwbTUJSDWk4VUTd36o8Mc=','2024-09-13 15:45:41.039707','Haitham','Dororo','0695-156156','M','haitham@email.com',1,1,1,0,'1980-06-12'),(3,'pbkdf2_sha256$720000$A3yqWNTDKYOQfhJqjRucfi$jlX1cURSuk9DrQxUiJ6O9nnELT/JEQjFDNzgQG7S01E=','2024-09-13 15:47:29.083901','Simon','brand','0651-515151','M','dasopi7435@konetas.com',0,1,0,0,'2000-05-20'),(4,'pbkdf2_sha256$720000$yX28Yt2SsIhVK5xDsh3a7w$JjsSAUn+Dy5hL/k1SMal3s2drf1EKVFbMfrxPnExrBo=','2024-09-14 14:01:52.799981','Kalma','Moukn','0651-561556','M','teboyol717@amxyy.com',0,1,0,0,'1997-08-12'),(5,'pbkdf2_sha256$720000$5mvtzRIt87O1ZTuN29BRDl$aGcsipHFUI8sQSF5MRfrwU6MhJ0JGEgud/NrR7NIoz4=','2024-09-14 14:27:07.457970','Mali','Joul','0651-561556','M','pegojoc781@sigmazon.com',0,1,0,0,'1997-08-12'),(6,'pbkdf2_sha256$720000$I97XYrYHN2PMeTHM70SoCW$zxR/mLXVBXn5HHkzNaf0Iid4UJJx6XWslttVVZ5Qbu0=','2024-09-14 15:34:10.656429','Kal','Poul','0651-561556','M','pegojo81@sigmazon.com',0,1,0,0,'1997-08-12'),(7,'pbkdf2_sha256$720000$RQObTdTjWMOm0UIvqMMDpJ$w6ur8LXS7OzpN/G97cSJlNxFfQFcGHfIuQOXSvHqWqQ=','2024-09-14 15:34:30.582654','Lal','Foul','0651-561556','M','pegojo811@sigmazon.com',0,1,0,0,'1997-08-12'),(8,'pbkdf2_sha256$720000$GtcZWnHmMDk6f1TvZ5IEMQ$5DEoaFw3xkQC7Vg5eeq82Gdj1XqLRaqNiXpPL2DEbyU=','2024-09-14 15:34:51.658615','Poad','Eoul','0651-561556','M','pegojo881@sigmazon.com',0,1,0,0,'1997-08-12'),(9,'pbkdf2_sha256$720000$pNOgAbfld4JUon4bOu7NFs$Kg/KXuxvVIlLiyRkFrm3JmMWDCDtf99lw+63c092jOg=','2024-09-14 15:35:17.026513','Ooad','Zoul','0651-561556','M','pegojo8e1@sigmazon.com',0,1,0,0,'1997-08-12'),(10,'pbkdf2_sha256$720000$KUznKNtsta0xPZ180l7XoH$Pi8S0S6T3EnQh3q8R53w+m9diY7PPZ4Zoh/9Q+0oq6w=','2024-09-14 15:37:28.043000','Zoad','Moul','0651-561556','M','po8e1@sigmazon.com',0,1,0,0,'1997-08-12'),(11,'pbkdf2_sha256$720000$H8mrgWxI5eILbp6RHOjpRr$nTaWFPiTCM1Pgs37dOtzXrqu65QK9g3+zLMigiLioRo=','2024-09-14 15:37:41.499502','Ioad','Moul','0651-561556','M','po5e1@sigmazon.com',0,1,0,0,'1997-08-12'),(12,'pbkdf2_sha256$720000$7DQHOQoKZqEIubS5zNMxvK$6jMaYYWnRjytboYJKNAW9wAaAwbvW0dlLX/3R152oMw=','2024-09-14 15:38:19.273063','Coad','Woul','0651-561556','M','po5e1@seigmazon.com',0,1,0,0,'1997-08-12'),(13,'pbkdf2_sha256$720000$ToUjpExPaIzV3t4ljxgN2b$lDaEnnONIjuaTSPq65CvUyRA+B6rFlJIjeyhXU0k9RE=','2024-09-14 15:38:29.329561','Coad','Woul','0651-561556','M','po5e1@senigmazon.com',0,1,0,0,'1997-08-12'),(14,'pbkdf2_sha256$720000$mQ6MHTnpI4zcHEm5g2GeQ0$QYk1sq8SB9PsM2FnImj7CmOb+5HL4jwIH9Mtmg+0/Q0=','2024-09-14 15:38:38.222026','Coad','Woul','0651-561556','M','po5e1@fnigmazon.com',0,1,0,0,'1997-08-12'),(15,'pbkdf2_sha256$720000$laBVthuu6ED0nFlHWt1im2$/7Aj1AW5QTlEbrBVthWlPE74qQdpXWNVogHXBKIGZGY=','2024-09-14 15:38:44.868803','Coad','Woul','0651-561556','M','po51e1@fnigmazon.com',0,1,0,0,'1997-08-12'),(16,'pbkdf2_sha256$720000$CQBdHX4ROcKRPMzF3oT9Hj$bxbae1IZJrnXKjXY+wC7qkvxQEWGhVAHr8s/yxIU4uI=','2024-09-14 15:38:51.895235','Coad','Woul','0651-561556','M','po512e1@fnigmazon.com',0,1,0,0,'1997-08-12'),(17,'pbkdf2_sha256$720000$mFJcGOaunZ0VaE3xOTSwHi$t0UpD/80gNqQQ+64+CM+3Woes3MCSqkDMK2su8KVW8s=','2024-09-14 15:38:57.982019','Coad','Woul','0651-561556','M','po5123e1@fnigmazon.com',0,1,0,0,'1997-08-12'),(18,'pbkdf2_sha256$720000$de5goz85dNfFImkdERmHi6$10ThSYTQyxf4XMbizQCHndsFwB4PkPtC5JUEgu0YRqM=','2024-09-14 15:39:05.414387','Coad','Woul','0651-561556','M','po51230e1@fnigmazon.com',0,1,0,0,'1997-08-12'),(19,'pbkdf2_sha256$720000$7sh248y5KLobtCANmgy7jI$HgBm+cFktkUMYsp7ce8cm27iszGAVg9rxkJnRcHEgXs=','2024-09-14 15:39:15.785690','Coad','Woul','0651-561556','M','po50e1@fnigmazon.com',0,1,0,0,'1997-08-12'),(20,'pbkdf2_sha256$720000$YNhBOqtpWdPW1Mt89HbhyE$gfDPxPbklXj4vTpzWfL4m0PmCO/qV8LwtkcLGwT3pPM=','2024-09-14 15:39:27.615106','Coad','Woul','0651-561556','M','po501e1@fnigmazon.com',0,1,0,0,'1997-08-12'),(21,'pbkdf2_sha256$720000$i1F48FUsfNHKEkD3lY6hmF$L09HSGHWjfOPi7VAoMpQckg2jcCi53SOF0l7Dp3TtvQ=','2024-09-14 15:39:36.502100','Coad','Woul','0651-561556','M','po502e1@fnigmazon.com',0,1,0,0,'1997-08-12'),(22,'pbkdf2_sha256$720000$MRRc9JrWWp22W9rNOS2XTj$xnLuWMAuB7tOU3st9lI5mHzMGM7T1uJlT7RzQJl4JXA=','2024-09-14 15:39:44.736323','Coad','Woul','0651-561556','M','po503e1@fnigmazon.com',0,1,0,0,'1997-08-12'),(23,'pbkdf2_sha256$720000$rAykWzu0Ty2dqdxTHTFRN4$JlDR7VK9rTYaD2iTCOWw8sykjg6+IEZZQzfEQjdU+Fg=','2024-09-14 15:39:52.850322','Coad','Woul','0651-561556','M','po504e1@fnigmazon.com',0,1,0,0,'1997-08-12'),(24,'pbkdf2_sha256$720000$sENmRC4j2hRhOEkb3ic2dK$SB8hA1akqVJbm6tybc9RbiPZQzsdSvdDl0MFqGSaWWI=','2024-09-14 15:40:00.293857','Coad','Woul','0651-561556','M','po505e1@fnigmazon.com',0,1,0,0,'1997-08-12'),(25,'pbkdf2_sha256$720000$0vajxXzyztJcPCuGUI8oZg$NHho80Y950Z0bboYdG1w738qwh5aSIibD6ft6sT5Ock=','2024-09-14 15:41:04.380523','Coad','Woul','0652-111556','M','po506e1@fnigmazon.com',0,1,0,0,'1997-08-12'),(26,'pbkdf2_sha256$720000$HgLq1HWm9HYXOg8TmNyL3K$Y1c+F01zR5oYj9ynKm4/YME6VjfCxGvE6ky3mXMPGJw=','2024-09-14 15:41:13.311298','Coad','Woul','0652-111556','M','po506e2@fnigmazon.com',0,1,0,0,'1997-08-12'),(27,'pbkdf2_sha256$720000$140tWWNuk08WMAGHS9tNLO$QNnYpMKy4CHljKOrLvjmHGXGSuMki7AAu8sM9ccLyrM=','2024-09-14 15:41:19.124934','Coad','Woul','0652-111556','M','po506e3@fnigmazon.com',0,1,0,0,'1997-08-12'),(28,'pbkdf2_sha256$720000$ZDp4K87FcK27G4AFnawnlZ$/2uKPdr966AmacdI55NPyL1AcBpGiaf/cZLfjYlKFq8=','2024-09-14 15:41:29.918162','Coad','Woul','0652-111556','M','po506e4@fnigmazon.com',0,1,0,0,'1997-08-12'),(29,'pbkdf2_sha256$720000$eLTOThrl61lUm32Fk6oB1G$dgCH0wdNy8RrxzJIQyu+fitrK1FcmpMitimBwjWpNp4=','2024-09-14 15:41:59.521408','Coad','Woul','0652-111556','M','po506ed4@fnigmazon.com',0,1,0,0,'1997-08-12'),(30,'pbkdf2_sha256$720000$6m22kfiptR3FMZXry9XEEk$mKxCQdN22w3q5ogNnbklkWiXTiVne05xJ4CvmFKc4ts=','2024-09-14 15:42:22.525309','Coad','Woul','0652-111556','M','po516ed4@fnigmazon.com',0,1,0,0,'1997-08-12');
/*!40000 ALTER TABLE `Person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Result`
--

DROP TABLE IF EXISTS `Result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Result` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `score` double NOT NULL,
  `exam_id` bigint DEFAULT NULL,
  `student_id` bigint DEFAULT NULL,
  `teacher_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Result_exam_id_ceadc2f7_fk_Exam_id` (`exam_id`),
  KEY `Result_student_id_b7ca3953_fk_Student_id` (`student_id`),
  KEY `Result_teacher_id_8998ec9d_fk_Teacher_id` (`teacher_id`),
  CONSTRAINT `Result_exam_id_ceadc2f7_fk_Exam_id` FOREIGN KEY (`exam_id`) REFERENCES `Exam` (`id`),
  CONSTRAINT `Result_student_id_b7ca3953_fk_Student_id` FOREIGN KEY (`student_id`) REFERENCES `Student` (`id`),
  CONSTRAINT `Result_teacher_id_8998ec9d_fk_Teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `Teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Result`
--

LOCK TABLES `Result` WRITE;
/*!40000 ALTER TABLE `Result` DISABLE KEYS */;
/*!40000 ALTER TABLE `Result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SchoolMembers`
--

DROP TABLE IF EXISTS `SchoolMembers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SchoolMembers` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `profile_image` varchar(100) DEFAULT NULL,
  `role` varchar(2) NOT NULL,
  `person_id` bigint NOT NULL,
  `school_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `person_id` (`person_id`),
  KEY `SchoolMembers_school_id_e380af46_fk_school_data_tb_id` (`school_id`),
  CONSTRAINT `SchoolMembers_person_id_eed6e98f_fk_Person_id` FOREIGN KEY (`person_id`) REFERENCES `Person` (`id`),
  CONSTRAINT `SchoolMembers_school_id_e380af46_fk_school_data_tb_id` FOREIGN KEY (`school_id`) REFERENCES `school_data_tb` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SchoolMembers`
--

LOCK TABLES `SchoolMembers` WRITE;
/*!40000 ALTER TABLE `SchoolMembers` DISABLE KEYS */;
INSERT INTO `SchoolMembers` VALUES (1,'images/7b938f3f-8b3.jpg','OW',2,1),(2,'images/2aa039e2-fb8.jpg','ST',3,1),(3,'images/b00f41eb-106.jpg','TE',4,1),(4,'images/3d47a56e-ca1.jpg','TE',5,1),(5,'images/28b7b0b3-eac.jpg','TE',6,1),(6,'images/87521836-d68.jpg','TE',7,1),(7,'images/f2e42a3f-77e.jpg','TE',8,1),(8,'images/1e33fb2f-41c.jpg','TE',9,1),(9,'images/77952923-06c.jpg','TE',10,1),(10,'images/2631ade7-735.jpg','TE',11,1),(11,'images/8621ae04-2a1.jpg','TE',12,1),(12,'images/798268c6-6a3.jpg','TE',13,1),(13,'images/049989d2-258.jpg','TE',14,1),(14,'images/7abf808a-13c.jpg','TE',15,1),(15,'images/2ca184f6-b4d.jpg','TE',16,1),(16,'images/2fb3b6c1-aaf.jpg','TE',17,1),(17,'images/56e836b9-34e.jpg','TE',18,1),(18,'images/e78b711a-931.jpg','TE',19,1),(19,'images/d9fc4d8d-183.jpg','TE',20,1),(20,'images/9c9ceb50-63b.jpg','TE',21,1),(21,'images/8b55a738-e22.jpg','TE',22,1),(22,'images/54e44749-939.jpg','TE',23,1),(23,'images/ddd1db7c-278.jpg','TE',24,1),(24,'images/935c423e-d92.jpg','TE',25,1),(25,'images/aa644672-6f2.jpg','TE',26,1),(26,'images/ca1a1c6a-b3d.jpg','TE',27,1),(27,'images/ab763d80-27a.jpg','TE',28,1),(28,'images/0809227f-bbf.jpg','TE',29,1),(29,'images/c4e59ed1-c35.jpg','TE',30,1);
/*!40000 ALTER TABLE `SchoolMembers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Staff`
--

DROP TABLE IF EXISTS `Staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Staff` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `position` varchar(255) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `Staff_user_id_e5c5c721_fk_SchoolMembers_id` FOREIGN KEY (`user_id`) REFERENCES `SchoolMembers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Staff`
--

LOCK TABLES `Staff` WRITE;
/*!40000 ALTER TABLE `Staff` DISABLE KEYS */;
/*!40000 ALTER TABLE `Staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Student`
--

DROP TABLE IF EXISTS `Student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `classe_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `Student_classe_id_4a6346ea_fk_Classe_id` (`classe_id`),
  CONSTRAINT `Student_classe_id_4a6346ea_fk_Classe_id` FOREIGN KEY (`classe_id`) REFERENCES `Classe` (`id`),
  CONSTRAINT `Student_user_id_a3b33364_fk_SchoolMembers_id` FOREIGN KEY (`user_id`) REFERENCES `SchoolMembers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Student`
--

LOCK TABLES `Student` WRITE;
/*!40000 ALTER TABLE `Student` DISABLE KEYS */;
INSERT INTO `Student` VALUES (1,1,2);
/*!40000 ALTER TABLE `Student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Subject`
--

DROP TABLE IF EXISTS `Subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Subject` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject_name` varchar(255) NOT NULL,
  `school_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Subject_school_id_8bd56269_fk_school_data_tb_id` (`school_id`),
  CONSTRAINT `Subject_school_id_8bd56269_fk_school_data_tb_id` FOREIGN KEY (`school_id`) REFERENCES `school_data_tb` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Subject`
--

LOCK TABLES `Subject` WRITE;
/*!40000 ALTER TABLE `Subject` DISABLE KEYS */;
/*!40000 ALTER TABLE `Subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Teacher`
--

DROP TABLE IF EXISTS `Teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Teacher` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `qualification` varchar(255) NOT NULL,
  `experience` int NOT NULL,
  `specialization` varchar(255) NOT NULL,
  `address` longtext NOT NULL,
  `joining_date` date NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `Teacher_user_id_cb44dc21_fk_SchoolMembers_id` FOREIGN KEY (`user_id`) REFERENCES `SchoolMembers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Teacher`
--

LOCK TABLES `Teacher` WRITE;
/*!40000 ALTER TABLE `Teacher` DISABLE KEYS */;
INSERT INTO `Teacher` VALUES (1,'Biology',3,'Biology','Mkenes','2024-09-14',3),(2,'Math',3,'Math','Mkenes','2024-09-14',4),(3,'Biology',3,'Biology','Mkenes','2024-09-14',5),(4,'Biology',3,'Biology','Mkenes','2024-09-14',6),(5,'Biology',3,'Biology','Mkenes','2024-09-14',7),(6,'Biology',3,'Biology','Mkenes','2024-09-14',8),(7,'Physics',3,'Physics','Mkenes','2024-09-14',9),(8,'Biology',3,'Biology','Mkenes','2024-09-14',10),(9,'Biology',3,'Biology','Mkenes','2024-09-14',11),(10,'Biology',3,'Biology','Mkenes','2024-09-14',12),(11,'Biology',3,'Biology','Mkenes','2024-09-14',13),(12,'Biology',3,'Biology','Mkenes','2024-09-14',14),(13,'Biology',3,'Biology','Mkenes','2024-09-14',15),(14,'Biology',3,'Biology','Mkenes','2024-09-14',16),(15,'Biology',3,'Biology','Mkenes','2024-09-14',17),(16,'Biology',3,'Biology','Mkenes','2024-09-14',18),(17,'Biology',3,'Biology','Mkenes','2024-09-14',19),(18,'Biology',3,'Biology','Mkenes','2024-09-14',20),(19,'Biology',3,'Biology','Mkenes','2024-09-14',21),(20,'Biology',3,'Biology','Mkenes','2024-09-14',22),(21,'Biology',3,'Biology','Mkenes','2024-09-14',23),(22,'Biology',3,'Biology','Mkenes','2024-09-14',24),(23,'Biology',3,'Biology','Mkenes','2024-09-14',25),(24,'Biology',3,'Biology','Mkenes','2024-09-14',26),(25,'Biology',3,'Biology','Mkenes','2024-09-14',27),(26,'Biology',3,'Biology','Mkenes','2024-09-14',28),(27,'Biology',3,'Biology','Mkenes','2024-09-14',29);
/*!40000 ALTER TABLE `Teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Teacher_teaching_classes`
--

DROP TABLE IF EXISTS `Teacher_teaching_classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Teacher_teaching_classes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `teacher_id` bigint NOT NULL,
  `classe_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Teacher_teaching_classes_teacher_id_classe_id_9f9ee780_uniq` (`teacher_id`,`classe_id`),
  KEY `Teacher_teaching_classes_classe_id_b5397085_fk_Classe_id` (`classe_id`),
  CONSTRAINT `Teacher_teaching_classes_classe_id_b5397085_fk_Classe_id` FOREIGN KEY (`classe_id`) REFERENCES `Classe` (`id`),
  CONSTRAINT `Teacher_teaching_classes_teacher_id_309db657_fk_Teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `Teacher` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Teacher_teaching_classes`
--

LOCK TABLES `Teacher_teaching_classes` WRITE;
/*!40000 ALTER TABLE `Teacher_teaching_classes` DISABLE KEYS */;
INSERT INTO `Teacher_teaching_classes` VALUES (1,1,1),(2,2,1),(3,3,1),(4,4,1),(5,5,1),(6,6,1),(7,7,1),(8,8,1),(9,9,1),(10,10,1),(11,11,1),(12,12,1),(13,13,1),(14,14,1),(15,15,1),(16,16,1),(17,17,1),(18,18,1),(19,19,1),(20,20,1),(21,21,1),(22,22,1),(23,23,1),(24,24,1),(25,25,1),(26,26,1),(27,27,1);
/*!40000 ALTER TABLE `Teacher_teaching_classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Person',6,'add_person'),(22,'Can change Person',6,'change_person'),(23,'Can delete Person',6,'delete_person'),(24,'Can view Person',6,'view_person'),(25,'Can add Classe',7,'add_classe'),(26,'Can change Classe',7,'change_classe'),(27,'Can delete Classe',7,'delete_classe'),(28,'Can view Classe',7,'view_classe'),(29,'Can add School Data',8,'add_schooldatamodel'),(30,'Can change School Data',8,'change_schooldatamodel'),(31,'Can delete School Data',8,'delete_schooldatamodel'),(32,'Can view School Data',8,'view_schooldatamodel'),(33,'Can add Classe Room',9,'add_classroom'),(34,'Can change Classe Room',9,'change_classroom'),(35,'Can delete Classe Room',9,'delete_classroom'),(36,'Can view Classe Room',9,'view_classroom'),(37,'Can add Classe Schedule',10,'add_classschedule'),(38,'Can change Classe Schedule',10,'change_classschedule'),(39,'Can delete Classe Schedule',10,'delete_classschedule'),(40,'Can view Classe Schedule',10,'view_classschedule'),(41,'Can add Event',11,'add_events'),(42,'Can change Event',11,'change_events'),(43,'Can delete Event',11,'delete_events'),(44,'Can view Event',11,'view_events'),(45,'Can add SchoolMember',12,'add_schoolmembers'),(46,'Can change SchoolMember',12,'change_schoolmembers'),(47,'Can delete SchoolMember',12,'delete_schoolmembers'),(48,'Can view SchoolMember',12,'view_schoolmembers'),(49,'Can add Notification',13,'add_notification'),(50,'Can change Notification',13,'change_notification'),(51,'Can delete Notification',13,'delete_notification'),(52,'Can view Notification',13,'view_notification'),(53,'Can add admin',14,'add_admin'),(54,'Can change admin',14,'change_admin'),(55,'Can delete admin',14,'delete_admin'),(56,'Can view admin',14,'view_admin'),(57,'Can add Staff',15,'add_staff'),(58,'Can change Staff',15,'change_staff'),(59,'Can delete Staff',15,'delete_staff'),(60,'Can view Staff',15,'view_staff'),(61,'Can add Student',16,'add_student'),(62,'Can change Student',16,'change_student'),(63,'Can delete Student',16,'delete_student'),(64,'Can view Student',16,'view_student'),(65,'Can add Parent',17,'add_parent'),(66,'Can change Parent',17,'change_parent'),(67,'Can delete Parent',17,'delete_parent'),(68,'Can view Parent',17,'view_parent'),(69,'Can add Grade',18,'add_grade'),(70,'Can change Grade',18,'change_grade'),(71,'Can delete Grade',18,'delete_grade'),(72,'Can view Grade',18,'view_grade'),(73,'Can add Subject',19,'add_subject'),(74,'Can change Subject',19,'change_subject'),(75,'Can delete Subject',19,'delete_subject'),(76,'Can view Subject',19,'view_subject'),(77,'Can add Exam',20,'add_exam'),(78,'Can change Exam',20,'change_exam'),(79,'Can delete Exam',20,'delete_exam'),(80,'Can view Exam',20,'view_exam'),(81,'Can add Teacher',21,'add_teacher'),(82,'Can change Teacher',21,'change_teacher'),(83,'Can delete Teacher',21,'delete_teacher'),(84,'Can view Teacher',21,'view_teacher'),(85,'Can add Result',22,'add_result'),(86,'Can change Result',22,'change_result'),(87,'Can delete Result',22,'delete_result'),(88,'Can view Result',22,'view_result'),(89,'Can add Attendance',23,'add_attendance'),(90,'Can change Attendance',23,'change_attendance'),(91,'Can delete Attendance',23,'delete_attendance'),(92,'Can view Attendance',23,'view_attendance'),(93,'Can add fcm device',24,'add_fcmdevice'),(94,'Can change fcm device',24,'change_fcmdevice'),(95,'Can delete fcm device',24,'delete_fcmdevice'),(96,'Can view fcm device',24,'view_fcmdevice'),(97,'Can add FCM device',25,'add_fcmdevice'),(98,'Can change FCM device',25,'change_fcmdevice'),(99,'Can delete FCM device',25,'delete_fcmdevice'),(100,'Can view FCM device',25,'view_fcmdevice');
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
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_Person_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_Person_id` FOREIGN KEY (`user_id`) REFERENCES `Person` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-09-13 15:44:41.234708','1','1 - El Mansour',1,'[{\"added\": {}}]',8,1);
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
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(25,'fcm_django','fcmdevice'),(14,'school_managment','admin'),(23,'school_managment','attendance'),(7,'school_managment','classe'),(9,'school_managment','classroom'),(10,'school_managment','classschedule'),(11,'school_managment','events'),(20,'school_managment','exam'),(24,'school_managment','fcmdevice'),(18,'school_managment','grade'),(13,'school_managment','notification'),(17,'school_managment','parent'),(6,'school_managment','person'),(22,'school_managment','result'),(8,'school_managment','schooldatamodel'),(12,'school_managment','schoolmembers'),(15,'school_managment','staff'),(16,'school_managment','student'),(19,'school_managment','subject'),(21,'school_managment','teacher'),(5,'sessions','session');
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
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'school_managment','0001_initial','2024-09-13 15:42:52.139086'),(2,'contenttypes','0001_initial','2024-09-13 15:42:52.180752'),(3,'admin','0001_initial','2024-09-13 15:42:52.351683'),(4,'admin','0002_logentry_remove_auto_add','2024-09-13 15:42:52.360388'),(5,'admin','0003_logentry_add_action_flag_choices','2024-09-13 15:42:52.371460'),(6,'contenttypes','0002_remove_content_type_name','2024-09-13 15:42:52.447620'),(7,'auth','0001_initial','2024-09-13 15:42:52.689905'),(8,'auth','0002_alter_permission_name_max_length','2024-09-13 15:42:52.754965'),(9,'auth','0003_alter_user_email_max_length','2024-09-13 15:42:52.763865'),(10,'auth','0004_alter_user_username_opts','2024-09-13 15:42:52.771626'),(11,'auth','0005_alter_user_last_login_null','2024-09-13 15:42:52.779623'),(12,'auth','0006_require_contenttypes_0002','2024-09-13 15:42:52.782168'),(13,'auth','0007_alter_validators_add_error_messages','2024-09-13 15:42:52.789724'),(14,'auth','0008_alter_user_username_max_length','2024-09-13 15:42:52.798030'),(15,'auth','0009_alter_user_last_name_max_length','2024-09-13 15:42:52.806703'),(16,'auth','0010_alter_group_name_max_length','2024-09-13 15:42:52.849177'),(17,'auth','0011_update_proxy_permissions','2024-09-13 15:42:52.876130'),(18,'auth','0012_alter_user_first_name_max_length','2024-09-13 15:42:52.883103'),(19,'fcm_django','0001_initial','2024-09-13 15:42:52.987226'),(20,'fcm_django','0002_auto_20160808_1645','2024-09-13 15:42:53.032361'),(21,'fcm_django','0003_auto_20170313_1314','2024-09-13 15:42:53.039225'),(22,'fcm_django','0004_auto_20181128_1642','2024-09-13 15:42:53.046003'),(23,'fcm_django','0005_auto_20170808_1145','2024-09-13 15:42:53.067376'),(24,'fcm_django','0006_auto_20210802_1140','2024-09-13 15:42:53.082791'),(25,'fcm_django','0007_auto_20211001_1440','2024-09-13 15:42:53.112415'),(26,'fcm_django','0008_auto_20211224_1205','2024-09-13 15:42:53.154229'),(27,'fcm_django','0009_alter_fcmdevice_user','2024-09-13 15:42:53.182481'),(28,'fcm_django','0010_unique_registration_id','2024-09-13 15:42:53.190738'),(29,'fcm_django','0011_fcmdevice_fcm_django_registration_id_user_id_idx','2024-09-13 15:42:53.197173'),(30,'school_managment','0002_fcmdevice','2024-09-13 15:42:53.256376'),(31,'school_managment','0003_alter_person_phone','2024-09-13 15:42:53.314040'),(32,'school_managment','0004_alter_person_phone','2024-09-13 15:42:53.368030'),(33,'school_managment','0005_alter_person_phone','2024-09-13 15:42:53.419597'),(34,'school_managment','0006_alter_classroom_assigned_teacher_and_more','2024-09-13 15:42:53.480828'),(35,'sessions','0001_initial','2024-09-13 15:42:53.521458');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('peib9eis0yz9p2d1gzahatca6vrthjbu','.eJxVjMsOwiAQRf-FtSEdkKG4dO83NDMDSNVA0sfK-O-2SRe6Pefc-1YDrUsZ1jlNwxjVRYE6_TImeaa6i_igem9aWl2mkfWe6MPO-tZiel2P9u-g0Fy2dUBrjKCBrg8ANkkg59Fbh9xtCIUzSU4ELMjn4D13GICdtZRdD059vrimNxQ:1sp8Sr:YCKaM_QE-29TToBecEzRRnCqc15R5A7znTrXRcUdYrk','2024-09-27 15:44:05.022188');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fcm_django_fcmdevice`
--

DROP TABLE IF EXISTS `fcm_django_fcmdevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fcm_django_fcmdevice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `date_created` datetime(6) DEFAULT NULL,
  `device_id` varchar(255) DEFAULT NULL,
  `registration_id` longtext NOT NULL,
  `type` varchar(10) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fcm_django_fcmdevice_user_id_6cdfc0a2_fk_Person_id` (`user_id`),
  KEY `fcm_django_fcmdevice_device_id_a9406c36` (`device_id`),
  CONSTRAINT `fcm_django_fcmdevice_user_id_6cdfc0a2_fk_Person_id` FOREIGN KEY (`user_id`) REFERENCES `Person` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fcm_django_fcmdevice`
--

LOCK TABLES `fcm_django_fcmdevice` WRITE;
/*!40000 ALTER TABLE `fcm_django_fcmdevice` DISABLE KEYS */;
/*!40000 ALTER TABLE `fcm_django_fcmdevice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_data_tb`
--

DROP TABLE IF EXISTS `school_data_tb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `school_data_tb` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `email` varchar(200) NOT NULL,
  `logo_image` varchar(100) DEFAULT NULL,
  `education_stage` varchar(12) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_data_tb`
--

LOCK TABLES `school_data_tb` WRITE;
/*!40000 ALTER TABLE `school_data_tb` DISABLE KEYS */;
INSERT INTO `school_data_tb` VALUES (1,'El Mansour','No 38 jamaa Zerka','mansour@gmail.com','images/logo_UyVfMSU.png','PR');
/*!40000 ALTER TABLE `school_data_tb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_managment_admin`
--

DROP TABLE IF EXISTS `school_managment_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `school_managment_admin` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `school_managment_admin_user_id_cc964581_fk_SchoolMembers_id` FOREIGN KEY (`user_id`) REFERENCES `SchoolMembers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_managment_admin`
--

LOCK TABLES `school_managment_admin` WRITE;
/*!40000 ALTER TABLE `school_managment_admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_managment_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_managment_events`
--

DROP TABLE IF EXISTS `school_managment_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `school_managment_events` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `event_name` varchar(200) NOT NULL,
  `desricption` longtext NOT NULL,
  `date_start` datetime(6) NOT NULL,
  `date_end` datetime(6) NOT NULL,
  `color` varchar(12) NOT NULL,
  `is_all_day` tinyint(1) NOT NULL,
  `school_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `school_managment_events_school_id_f5834163_fk_school_data_tb_id` (`school_id`),
  CONSTRAINT `school_managment_events_school_id_f5834163_fk_school_data_tb_id` FOREIGN KEY (`school_id`) REFERENCES `school_data_tb` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_managment_events`
--

LOCK TABLES `school_managment_events` WRITE;
/*!40000 ALTER TABLE `school_managment_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_managment_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_managment_fcmdevice`
--

DROP TABLE IF EXISTS `school_managment_fcmdevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `school_managment_fcmdevice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(255) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `school_managment_fcmdevice_user_id_f4592519_fk_SchoolMembers_id` (`user_id`),
  CONSTRAINT `school_managment_fcmdevice_user_id_f4592519_fk_SchoolMembers_id` FOREIGN KEY (`user_id`) REFERENCES `SchoolMembers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_managment_fcmdevice`
--

LOCK TABLES `school_managment_fcmdevice` WRITE;
/*!40000 ALTER TABLE `school_managment_fcmdevice` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_managment_fcmdevice` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-15  0:13:27
