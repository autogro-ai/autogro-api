-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Dec 03, 2023 at 02:59 PM
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
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `gro_instances`
--

CREATE TABLE `gro_instances` (
  `instanceID` int(11) NOT NULL,
  `serialNumber` varchar(255) NOT NULL,
  `deviceModelID` int(11) DEFAULT NULL,
  `components` mediumtext,
  `accessPolicy` text,
  `modelID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `gro_models`
--

CREATE TABLE `gro_models` (
  `modelID` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `components` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
  ADD KEY `modelID` (`modelID`);

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
  MODIFY `modelID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userID` int(11) NOT NULL AUTO_INCREMENT;

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
