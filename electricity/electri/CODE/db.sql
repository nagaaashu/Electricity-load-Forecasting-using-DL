/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - electricity
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`electricity` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `electricity`;

/*Table structure for table `power` */

DROP TABLE IF EXISTS `power`;

CREATE TABLE `power` (
  `S.no` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`S.no`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;


/*Table structure for table `tablename1` */

DROP TABLE IF EXISTS `tablename1`;

CREATE TABLE `tablename1` (
  `sno` int(10) NOT NULL AUTO_INCREMENT,
  `index` int(50) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  `generation biomass` varchar(100) DEFAULT NULL,
  `generation fossil brown coal/lignite` varchar(100) DEFAULT NULL,
  `generation fossil coal-derived gas` varchar(100) DEFAULT NULL,
  `generation fossil gas` varchar(100) DEFAULT NULL,
  `generation fossil hard coal` varchar(100) DEFAULT NULL,
  `generation fossil oil` varchar(100) DEFAULT NULL,
  `generation fossil oil shale` varchar(100) DEFAULT NULL,
  `generation fossil peat` varchar(100) DEFAULT NULL,
  `generation geothermal` varchar(100) DEFAULT NULL,
  `generation hydro pumped storage aggregated` varchar(100) DEFAULT NULL,
  `generation hydro pumped storage consumption` varchar(100) DEFAULT NULL,
  `generation hydro run-of-river and poundage` varchar(100) DEFAULT NULL,
  `generation hydro water reservoir` varchar(100) DEFAULT NULL,
  `generation marine` varchar(100) DEFAULT NULL,
  `generation nuclear` varchar(100) DEFAULT NULL,
  `generation other` varchar(100) DEFAULT NULL,
  `generation other renewable` varchar(100) DEFAULT NULL,
  `generation solar` varchar(100) DEFAULT NULL,
  `generation waste` varchar(100) DEFAULT NULL,
  `generation wind offshore` varchar(100) DEFAULT NULL,
  `generation wind onshore` varchar(100) DEFAULT NULL,
  `forecast solar day ahead` varchar(100) DEFAULT NULL,
  `forecast wind offshore eday ahead` varchar(100) DEFAULT NULL,
  `forecast wind onshore day ahead` varchar(100) DEFAULT NULL,
  `total load forecast` varchar(100) DEFAULT NULL,
  `total load actual` varchar(100) DEFAULT NULL,
  `price day ahead` varchar(100) DEFAULT NULL,
  `price actual` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=35065 DEFAULT CHARSET=latin1;
