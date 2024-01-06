-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Dec 06, 2023 at 06:45 AM
-- Server version: 5.7.39
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `autogro`
--
CREATE DATABASE IF NOT EXISTS `autogro` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `autogro`;

-- --------------------------------------------------------

--
-- Table structure for table `gro_component_types`
--

CREATE TABLE `gro_component_types` (
  `componentTypeID` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `defaultSettings` text COMMENT 'key-value pair:              ''defaultSettings'' : {\r\n                ''status'' : ''0''\r\n            }'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `gro_instances`
--

CREATE TABLE `gro_instances` (
  `instanceID` int(11) NOT NULL,
  `ownerID` int(11) NOT NULL,
  `serialNumber` varchar(255) NOT NULL,
  `deviceModelID` int(11) DEFAULT NULL,
  `components` mediumtext,
  `accessPolicy` text COMMENT '{\r\n ownerID: int, \r\n access: [\r\n   { userID: int, \r\n     access: string \r\n   }\r\n ]\r\n\r\n}',
  `modelID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `gro_models`
--

CREATE TABLE `gro_models` (
  `modelID` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '0',
  `name` varchar(255) NOT NULL,
  `modelNumber` varchar(60) NOT NULL,
  `modelVersion` varchar(20) NOT NULL,
  `modelCodeName` varchar(60) DEFAULT NULL,
  `modelFamilyName` varchar(60) DEFAULT NULL,
  `modelReleaseDate` datetime DEFAULT NULL COMMENT '2023-01-01 12:30:00',
  `components` text COMMENT '{\r\n    ''version'': ''1'',\r\n    ''releaseDate'': ''20231101'',\r\n    ''items'': [\r\n        {\r\n            ''componentTypeID'': ''2001'',\r\n            ''name'': ''Camera'',\r\n            ''defaultSettings'' : {\r\n                ''status'' : ''0''\r\n            }\r\n        },'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
  `userID` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '0',
  `FirstName` varchar(100) DEFAULT NULL,
  `LastName` varchar(100) DEFAULT NULL,
  `EmailAddress` varchar(120) DEFAULT NULL,
  `devicesInActive` text,
  `devicesActive` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userID`, `active`, `FirstName`, `LastName`, `EmailAddress`, `devicesInActive`, `devicesActive`) VALUES
(1, 0, 'T111est', 'Use111rsnf', 'te11st.user@autogroai.com', NULL, NULL),
(6, 0, 'Test', 'User', 'test.user@autogroai.com', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_api_keys`
--

CREATE TABLE `user_api_keys` (
  `userID` int(11) DEFAULT NULL,
  `api_key` varchar(255) DEFAULT NULL,
  `api_secret` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
  MODIFY `componentTypeID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gro_instances`
--
ALTER TABLE `gro_instances`
  MODIFY `instanceID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `gro_models`
--
ALTER TABLE `gro_models`
  MODIFY `modelID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

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

CREATE USER 'agapi'@'%' IDENTIFIED WITH mysql_native_password BY 'HUf1ZT$cDYFcO8nYu!FH'; GRANT SELECT, INSERT, UPDATE, DELETE ON autogro.* TO 'agapi'@'%'; REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 20000 MAX_CONNECTIONS_PER_HOUR 100 MAX_UPDATES_PER_HOUR 10000 MAX_USER_CONNECTIONS 100;

