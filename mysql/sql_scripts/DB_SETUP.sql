-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Jan 20, 2024 at 01:58 AM
-- Server version: 8.2.0
-- PHP Version: 8.2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `autogro`
--
CREATE DATABASE IF NOT EXISTS `autogro` DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci;
USE `autogro`;

-- --------------------------------------------------------

--
-- Table structure for table `gro_component_types`
--

CREATE TABLE `gro_component_types` (
  `componentTypeID` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `measurementTypes` json NOT NULL COMMENT '{ id,\r\n  title,\r\n  dataType\r\n}',
  `defaultSettings` json DEFAULT NULL COMMENT '{ param1,\r\n  param2\r\n}',
  `active` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `gro_component_types`
--

INSERT INTO `gro_component_types` (`componentTypeID`, `name`, `measurementTypes`, `defaultSettings`, `active`) VALUES
(2, 'flowMeter', '[{\"id\": \"1\", \"title\": \"rotations\", \"dataType\": \"int\"}]', '[{\"name\": \"serialNumber\", \"value\": \"0001\"}]', 1),
(3, 'phSensor', '[{\"id\": \"1\", \"title\": \"level\", \"dataType\": \"decimal\"}]', '[{\"name\": \"serialNumber\", \"value\": \"0001\"}]', 1),
(4, 'soilSensor', '[{\"id\": \"1\", \"title\": \"level\", \"dataType\": \"decimal\"}]', '[{\"name\": \"serialNumber\", \"value\": \"0001\"}]', 1),
(5, 'valve', '[{\"id\": \"1\", \"title\": \"status\", \"dataType\": \"int\"}]', '[{\"name\": \"serialNumber\", \"value\": \"0001\"}]', 1),
(6, 'waterPump', '[{\"id\": \"1\", \"title\": \"status\", \"dataType\": \"int\"}]', '[{\"name\": \"serialNumber\", \"value\": \"0001\"}]', 1),
(7, 'TDS', '[{\"id\": \"1\", \"title\": \"ppm\", \"dataType\": \"int\"}]', '[{\"name\": \"serialNumber\", \"value\": \"0001\"}]', 1);

-- --------------------------------------------------------

--
-- Table structure for table `gro_data_1`
--

CREATE TABLE `gro_data_1` (
  `id` bigint UNSIGNED NOT NULL,
  `deviceID` int NOT NULL,
  `componentID` int NOT NULL,
  `componentTypeID` int NOT NULL,
  `measurementType` tinyint UNSIGNED NOT NULL COMMENT 'enum relative to component-type',
  `data` varchar(20) NOT NULL COMMENT 'parsable number 88888888.8888888888 ',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tag` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `gro_data_1`
--

INSERT INTO `gro_data_1` (`id`, `deviceID`, `componentID`, `componentTypeID`, `measurementType`, `data`, `timestamp`, `tag`) VALUES
(133, 1, 5001, 5, 1, '0', '2024-01-19 19:37:39', 'using api v1'),
(134, 1, 5002, 5, 1, '0', '2024-01-19 19:37:39', 'using api v1'),
(135, 1, 5003, 5, 1, '0', '2024-01-19 19:37:39', 'using api v1'),
(136, 1, 5004, 5, 1, '0', '2024-01-19 19:37:39', 'using api v1'),
(137, 1, 5005, 5, 1, '0', '2024-01-19 19:37:39', 'using api v1'),
(138, 1, 2001, 2, 1, '0', '2024-01-19 19:37:39', 'using api v1'),
(139, 1, 6001, 4, 1, '1', '2024-01-19 19:37:39', 'using api v1'),
(140, 1, 5001, 5, 1, '0', '2024-01-19 19:38:56', 'using api v1'),
(141, 1, 5002, 5, 1, '0', '2024-01-19 19:38:56', 'using api v1'),
(142, 1, 5003, 5, 1, '0', '2024-01-19 19:38:56', 'using api v1'),
(143, 1, 5004, 5, 1, '0', '2024-01-19 19:38:56', 'using api v1'),
(144, 1, 5005, 5, 1, '0', '2024-01-19 19:38:56', 'using api v1'),
(145, 1, 2001, 2, 1, '0', '2024-01-19 19:38:56', 'using api v1'),
(146, 1, 6001, 6, 1, '1', '2024-01-19 19:38:56', 'using api v1'),
(147, 1, 5001, 5, 1, '0', '2024-01-19 19:39:20', 'using api v1'),
(148, 1, 5002, 5, 1, '0', '2024-01-19 19:39:20', 'using api v1'),
(149, 1, 5003, 5, 1, '1', '2024-01-19 19:39:20', 'using api v1'),
(150, 1, 5004, 5, 1, '0', '2024-01-19 19:39:20', 'using api v1'),
(151, 1, 5005, 5, 1, '0', '2024-01-19 19:39:20', 'using api v1'),
(152, 1, 2001, 2, 1, '2000', '2024-01-19 19:39:20', 'using api v1'),
(153, 1, 6001, 6, 1, '1', '2024-01-19 19:39:20', 'using api v1'),
(154, 1, 5001, 5, 1, '0', '2024-01-19 19:40:05', 'using api v1'),
(155, 1, 5002, 5, 1, '0', '2024-01-19 19:40:05', 'using api v1'),
(156, 1, 5003, 5, 1, '1', '2024-01-19 19:40:05', 'using api v1'),
(157, 1, 5004, 5, 1, '0', '2024-01-19 19:40:05', 'using api v1'),
(158, 1, 5005, 5, 1, '0', '2024-01-19 19:40:05', 'using api v1'),
(159, 1, 2001, 2, 1, '300', '2024-01-19 19:40:05', 'using api v1'),
(160, 1, 6001, 6, 1, '1', '2024-01-19 19:40:05', 'using api v1'),
(161, 1, 5001, 5, 1, '0', '2024-01-19 19:40:10', 'using api v1'),
(162, 1, 5002, 5, 1, '0', '2024-01-19 19:40:10', 'using api v1'),
(163, 1, 5003, 5, 1, '1', '2024-01-19 19:40:10', 'using api v1'),
(164, 1, 5004, 5, 1, '0', '2024-01-19 19:40:10', 'using api v1'),
(165, 1, 5005, 5, 1, '0', '2024-01-19 19:40:10', 'using api v1'),
(166, 1, 2001, 2, 1, '44', '2024-01-19 19:40:10', 'using api v1'),
(167, 1, 6001, 6, 1, '1', '2024-01-19 19:40:10', 'using api v1'),
(168, 1, 3000, 3, 1, '2.4', '2024-01-19 19:40:36', 'using api v1'),
(169, 1, 7001, 7, 1, '2.4', '2024-01-19 19:40:36', 'using api v1'),
(170, 1, 4001, 4, 1, '88', '2024-01-19 19:40:36', 'using api v1'),
(171, 1, 4002, 4, 1, '88', '2024-01-19 19:40:36', 'using api v1'),
(172, 1, 4003, 4, 1, '88', '2024-01-19 19:40:36', 'using api v1'),
(173, 1, 4004, 4, 1, '44', '2024-01-19 19:40:36', 'using api v1'),
(174, 1, 4005, 4, 1, '44', '2024-01-19 19:40:36', 'using api v1'),
(175, 1, 3000, 3, 1, '1.2', '2024-01-19 19:41:10', 'using api v1'),
(176, 1, 7001, 7, 1, '356', '2024-01-19 19:41:10', 'using api v1'),
(177, 1, 4001, 4, 1, '77', '2024-01-19 19:41:10', 'using api v1'),
(178, 1, 4002, 4, 1, '88', '2024-01-19 19:41:10', 'using api v1'),
(179, 1, 4003, 4, 1, '88', '2024-01-19 19:41:10', 'using api v1'),
(180, 1, 4004, 4, 1, '44', '2024-01-19 19:41:10', 'using api v1'),
(181, 1, 4005, 4, 1, '44', '2024-01-19 19:41:10', 'using api v1'),
(182, 1, 3000, 3, 1, '1.2', '2024-01-19 19:41:30', 'using api v1'),
(183, 1, 7001, 7, 1, '356', '2024-01-19 19:41:30', 'using api v1'),
(184, 1, 4001, 4, 1, '77', '2024-01-19 19:41:30', 'using api v1'),
(185, 1, 4002, 4, 1, '88', '2024-01-19 19:41:30', 'using api v1'),
(186, 1, 4003, 4, 1, '88', '2024-01-19 19:41:30', 'using api v1'),
(187, 1, 4004, 4, 1, '44', '2024-01-19 19:41:30', 'using api v1'),
(188, 1, 4005, 4, 1, '44', '2024-01-19 19:41:30', 'using api v1'),
(189, 1, 3000, 3, 1, '2222', '2024-01-19 19:41:59', 'using api v1'),
(190, 1, 7001, 7, 1, '11111', '2024-01-19 19:41:59', 'using api v1'),
(191, 1, 4001, 4, 1, '77', '2024-01-19 19:41:59', 'using api v1'),
(192, 1, 4002, 4, 1, '88', '2024-01-19 19:41:59', 'using api v1'),
(193, 1, 4003, 4, 1, '88', '2024-01-19 19:41:59', 'using api v1'),
(194, 1, 4004, 4, 1, '44', '2024-01-19 19:41:59', 'using api v1'),
(195, 1, 4005, 4, 1, '44', '2024-01-19 19:41:59', 'using api v1'),
(196, 1, 3000, 3, 1, '2222', '2024-01-19 19:42:21', 'using api v1'),
(197, 1, 7001, 7, 1, '345353534', '2024-01-19 19:42:21', 'using api v1'),
(198, 1, 4001, 4, 1, '77', '2024-01-19 19:42:21', 'using api v1'),
(199, 1, 4002, 4, 1, '88', '2024-01-19 19:42:21', 'using api v1'),
(200, 1, 4003, 4, 1, '88', '2024-01-19 19:42:21', 'using api v1'),
(201, 1, 4004, 4, 1, '44', '2024-01-19 19:42:21', 'using api v1'),
(202, 1, 4005, 4, 1, '44', '2024-01-19 19:42:21', 'using api v1'),
(203, 1, 5001, 5, 1, '0', '2024-01-19 19:44:49', 'using api v1'),
(204, 1, 5002, 5, 1, '0', '2024-01-19 19:44:49', 'using api v1'),
(205, 1, 5003, 5, 1, '1', '2024-01-19 19:44:49', 'using api v1'),
(206, 1, 5004, 5, 1, '0', '2024-01-19 19:44:49', 'using api v1'),
(207, 1, 5005, 5, 1, '0', '2024-01-19 19:44:49', 'using api v1'),
(208, 1, 2001, 2, 1, '44', '2024-01-19 19:44:49', 'using api v1'),
(209, 1, 6001, 6, 1, '1', '2024-01-19 19:44:49', 'using api v1'),
(210, 1, 5001, 5, 1, '0', '2024-01-19 19:44:50', 'using api v1'),
(211, 1, 5002, 5, 1, '0', '2024-01-19 19:44:50', 'using api v1'),
(212, 1, 5003, 5, 1, '1', '2024-01-19 19:44:50', 'using api v1'),
(213, 1, 5004, 5, 1, '0', '2024-01-19 19:44:50', 'using api v1'),
(214, 1, 5005, 5, 1, '0', '2024-01-19 19:44:50', 'using api v1'),
(215, 1, 2001, 2, 1, '44', '2024-01-19 19:44:50', 'using api v1'),
(216, 1, 6001, 6, 1, '1', '2024-01-19 19:44:50', 'using api v1'),
(217, 1, 3000, 3, 1, '2222', '2024-01-20 01:45:05', 'using api v1'),
(218, 1, 7001, 7, 1, '345353534', '2024-01-20 01:45:05', 'using api v1'),
(219, 1, 4001, 4, 1, '77', '2024-01-20 01:45:05', 'using api v1'),
(220, 1, 4002, 4, 1, '88', '2024-01-20 01:45:05', 'using api v1'),
(221, 1, 4003, 4, 1, '88', '2024-01-20 01:45:05', 'using api v1'),
(222, 1, 4004, 4, 1, '44', '2024-01-20 01:45:05', 'using api v1'),
(223, 1, 4005, 4, 1, '44', '2024-01-20 01:45:05', 'using api v1'),
(224, 1, 3000, 3, 1, '2222', '2024-01-20 01:45:37', 'using api v1'),
(225, 1, 7001, 7, 1, '345353534', '2024-01-20 01:45:37', 'using api v1'),
(226, 1, 4001, 4, 1, '77', '2024-01-20 01:45:37', 'using api v1'),
(227, 1, 4002, 4, 1, '66', '2024-01-20 01:45:37', 'using api v1'),
(228, 1, 4003, 4, 1, '44', '2024-01-20 01:45:37', 'using api v1'),
(229, 1, 4004, 4, 1, '44', '2024-01-20 01:45:37', 'using api v1'),
(230, 1, 4005, 4, 1, '44', '2024-01-20 01:45:37', 'using api v1'),
(231, 1, 3000, 3, 1, '2222', '2024-01-20 01:52:30', 'using api v1'),
(232, 1, 7001, 7, 1, '345353534', '2024-01-20 01:52:30', 'using api v1'),
(233, 1, 4001, 4, 1, '77', '2024-01-20 01:52:30', 'using api v1'),
(234, 1, 4002, 4, 1, '66', '2024-01-20 01:52:30', 'using api v1'),
(235, 1, 4003, 4, 1, '44', '2024-01-20 01:52:30', 'using api v1'),
(236, 1, 4004, 4, 1, '44', '2024-01-20 01:52:30', 'using api v1'),
(237, 1, 4005, 4, 1, '44', '2024-01-20 01:52:30', 'using api v1');

-- --------------------------------------------------------

--
-- Table structure for table `gro_instances`
--

CREATE TABLE `gro_instances` (
  `instanceID` int NOT NULL,
  `ownerID` int NOT NULL,
  `name` varchar(30) NOT NULL,
  `serialNumber` varchar(255) NOT NULL,
  `components` json DEFAULT NULL,
  `accessPolicy` json DEFAULT NULL COMMENT '{\r\n ownerID: int, \r\n access: [\r\n   { userID: int, \r\n     access: string \r\n   }\r\n ]\r\n\r\n}',
  `modelID` int DEFAULT NULL,
  `lastUpdate` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `gro_instances`
--

INSERT INTO `gro_instances` (`instanceID`, `ownerID`, `name`, `serialNumber`, `components`, `accessPolicy`, `modelID`, `lastUpdate`) VALUES
(1, 1, 'h2', 'Sunrise', '[{\"componentTypeID\": \"1\"}, {\"componentTypeID\": \"2\"}]', '[{\"aa1\": \"1\"}, {\"bb2\": \"2\"}]', 1, '2024-01-18 03:20:29');

-- --------------------------------------------------------

--
-- Table structure for table `gro_models`
--

CREATE TABLE `gro_models` (
  `modelID` int NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '0',
  `name` varchar(255) NOT NULL,
  `modelNumber` varchar(60) NOT NULL,
  `modelVersion` varchar(20) NOT NULL,
  `modelCodeName` varchar(60) DEFAULT NULL,
  `modelFamilyName` varchar(60) DEFAULT NULL,
  `modelReleaseDate` datetime DEFAULT NULL COMMENT '2023-01-01 12:30:00',
  `components` text COMMENT '{\r\n    ''version'': ''1'',\r\n    ''releaseDate'': ''20231101'',\r\n    ''items'': [\r\n        {\r\n            ''componentTypeID'': ''2001'',\r\n            ''name'': ''Camera'',\r\n            ''defaultSettings'' : {\r\n                ''status'' : ''0''\r\n            }\r\n        },'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `gro_models`
--

INSERT INTO `gro_models` (`modelID`, `active`, `name`, `modelNumber`, `modelVersion`, `modelCodeName`, `modelFamilyName`, `modelReleaseDate`, `components`) VALUES
(1, 0, 'Conway', '2', '0.1', 'Sunrise', 'Genesis', '2023-12-05 19:00:00', '[{\"componentTypeID\": \"sensorTemp99999\"}, {\"componentTypeID\": \"sensorSoil0300\"}, {\"componentTypeID\": \"sensorPh4000\"}, {\"componentTypeID\": \"sensorSoil9900\"}, {\"componentTypeID\": \"sensorHum0008\"}]'),
(2, 0, 'Harrison', '1', '0.1', 'Sunrise', 'Genesis', '2023-12-05 19:00:00', '[{\"componentTypeID\": \"sensorTemp9001\"}, {\"componentTypeID\": \"sensorSoil0300\"}, {\"componentTypeID\": \"sensorPh4000\"}, {\"componentTypeID\": \"sensorSoil9900\"}, {\"componentTypeID\": \"sensorHum8000\"}]');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userID` int NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '0',
  `FirstName` varchar(100) DEFAULT NULL,
  `LastName` varchar(100) DEFAULT NULL,
  `EmailAddress` varchar(120) DEFAULT NULL,
  `devicesInActive` text,
  `devicesActive` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userID`, `active`, `FirstName`, `LastName`, `EmailAddress`, `devicesInActive`, `devicesActive`) VALUES
(1, 0, 'Sam', 'Winstead', 'support@autogroai.com', NULL, NULL),
(6, 0, 'Steve', 'Switty', 'steve@autogroai.com', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_api_keys`
--

CREATE TABLE `user_api_keys` (
  `userID` int DEFAULT NULL,
  `api_key` varchar(255) DEFAULT NULL,
  `api_secret` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `user_api_keys`
--

INSERT INTO `user_api_keys` (`userID`, `api_key`, `api_secret`) VALUES
(1, 'abcd1234dd', 'secretdd');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `gro_component_types`
--
ALTER TABLE `gro_component_types`
  ADD PRIMARY KEY (`componentTypeID`);

--
-- Indexes for table `gro_data_1`
--
ALTER TABLE `gro_data_1`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `gro_instances`
--
ALTER TABLE `gro_instances`
  ADD PRIMARY KEY (`instanceID`),
  ADD KEY `modelID` (`modelID`),
  ADD KEY `ownerID` (`ownerID`);

--
-- Indexes for table `gro_models`
--
ALTER TABLE `gro_models`
  ADD PRIMARY KEY (`modelID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userID`);

--
-- Indexes for table `user_api_keys`
--
ALTER TABLE `user_api_keys`
  ADD KEY `userID` (`userID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `gro_component_types`
--
ALTER TABLE `gro_component_types`
  MODIFY `componentTypeID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `gro_data_1`
--
ALTER TABLE `gro_data_1`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=238;

--
-- AUTO_INCREMENT for table `gro_instances`
--
ALTER TABLE `gro_instances`
  MODIFY `instanceID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `gro_models`
--
ALTER TABLE `gro_models`
  MODIFY `modelID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `gro_instances`
--
ALTER TABLE `gro_instances`
  ADD CONSTRAINT `gro_instances_ibfk_1` FOREIGN KEY (`modelID`) REFERENCES `gro_models` (`modelID`);

--
-- Constraints for table `user_api_keys`
--
ALTER TABLE `user_api_keys`
  ADD CONSTRAINT `user_api_keys_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`);
COMMIT;

CREATE USER 'agapi'@'%' IDENTIFIED BY 'password1234!agapi'; GRANT SELECT, INSERT, UPDATE, DELETE ON autogro.* TO 'agapi'@'%'; REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 20000 MAX_CONNECTIONS_PER_HOUR 100 MAX_UPDATES_PER_HOUR 10000 MAX_USER_CONNECTIONS 100;
