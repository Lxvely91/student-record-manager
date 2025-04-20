-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 16, 2025 at 12:42 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `accountant_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `accountants`
--

CREATE TABLE `accountants` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `number` varchar(255) DEFAULT NULL,
  `type` varchar(118) DEFAULT NULL,
  `file_path` varchar(255) NOT NULL,
  `department` varchar(255) DEFAULT NULL,
  `religion` varchar(11) DEFAULT NULL,
  `religion_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accountants`
--

INSERT INTO `accountants` (`id`, `name`, `number`, `type`, `file_path`, `department`, `religion`, `religion_id`) VALUES
(1, 'soumi', '12ssdd', '0', '', NULL, '0', NULL),
(2, 'soumi', '12ssdd', '0', '', NULL, '0', NULL),
(3, 'soumi', '12ssdd', '0', '', NULL, '0', NULL),
(4, 'soumi', '12ssdd', '0', '', NULL, '0', NULL),
(5, 'soumi', '12ssdd', '0', '', NULL, '0', NULL),
(6, 'soumi', '12ssdd', 'Personal', '', NULL, '0', NULL),
(7, 'aaa', '12345', 'Personal', '', NULL, '0', NULL),
(8, 'koushik pal', 'abc32', 'Business', '', NULL, '0', NULL),
(9, 'dipankar biswas', 'dipu123', 'Personal', '', NULL, '0', NULL),
(12, 'demo', 'number bola baron', 'Business', '????\0JFIF\0\0\0\0\0\0??\0?\0\n\n\n\"\"$$6*&&*6>424>LDDL_Z_||?\n\n\n\"\"$$6*&&*6>424>LDDL_Z_||???\0?\"\0??\03\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0??\0\0\0\0?g??j??ˠͲ?\r?', NULL, '0', NULL),
(13, 'aa', 'aa2', 'Business', 'uploads\\WhatsApp Image 2024-12-10 at 1.36.40 PM (1).jpeg', NULL, '0', NULL),
(14, 'puchi', 'nei', 'Personal', 'uploads\\2ecc1143-ab64-440b-901f-bdbaee1845b4.jpeg', NULL, '0', NULL),
(15, 'pucha', 'nei', 'Business', 'uploads\\1699535255_pg-3-12.jpg', NULL, 'hindu', NULL),
(16, 'aaaa', 'a1', 'Business', 'uploads\\WhatsApp Image 2025-02-20 at 12.53.35 PM.jpeg', NULL, 'muslim', NULL),
(17, 'demo test', '123456', 'Business', 'uploads\\1280px-Maniktala_Crossing_-_Kolkata_7342.JPG', NULL, 'hindu', NULL),
(18, 'raju roy', '43weerrr', 'Business', 'uploads\\1280px-Maniktala_Crossing_-_Kolkata_7342.JPG', NULL, 'muslim', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `imported_data`
--

CREATE TABLE `imported_data` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `designation` varchar(255) DEFAULT NULL,
  `salary` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `imported_data`
--

INSERT INTO `imported_data` (`id`, `name`, `designation`, `salary`, `address`) VALUES
(1, '', '', '', ''),
(2, 'soumi', 'junior project manager ', '20000.0', 'maniktala');

-- --------------------------------------------------------

--
-- Table structure for table `religion`
--

CREATE TABLE `religion` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `religion`
--

INSERT INTO `religion` (`id`, `name`) VALUES
(1, 'hindu'),
(2, 'muslim');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accountants`
--
ALTER TABLE `accountants`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `imported_data`
--
ALTER TABLE `imported_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `religion`
--
ALTER TABLE `religion`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accountants`
--
ALTER TABLE `accountants`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `imported_data`
--
ALTER TABLE `imported_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `religion`
--
ALTER TABLE `religion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
