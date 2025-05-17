-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 17, 2025 at 04:03 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `qismet_cafe`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`category_id`, `name`) VALUES
(3, 'Coffee'),
(2, 'Non-Coffee'),
(1, 'Pastries');

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `menu_id` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `price` smallint(6) NOT NULL,
  `size` enum('SMALL','MEDIUM','LARGE') DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `vat_percent` decimal(5,2) DEFAULT 12.00,
  `flavors` text DEFAULT NULL,
  `is_hidden` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`menu_id`, `category_id`, `name`, `price`, `size`, `image`, `vat_percent`, `flavors`, `is_hidden`) VALUES
(7, 3, 'Cappuccino', 100, 'SMALL', 'capuccino.jpg', 12.00, NULL, 0),
(8, 3, 'Cappuccino', 120, 'MEDIUM', 'capuccino.jpg', 12.00, NULL, 0),
(9, 3, 'Cappuccino', 140, 'LARGE', 'capuccino.jpg', 12.00, NULL, 0),
(10, 3, 'Macchiato', 100, 'SMALL', 'macchiato.jpg', 12.00, NULL, 0),
(11, 3, 'Macchiato', 120, 'MEDIUM', 'macchiato.jpg', 12.00, NULL, 0),
(12, 3, 'Macchiato', 140, 'LARGE', 'macchiato.jpg', 12.00, NULL, 0),
(13, 3, 'Caramel Dolce Latte', 110, 'SMALL', 'caramel dolce latte.jpg', 12.00, NULL, 0),
(14, 3, 'Caramel Dolce Latte', 130, 'MEDIUM', 'caramel dolce latte.jpg', 12.00, NULL, 0),
(15, 3, 'Caramel Dolce Latte', 150, 'LARGE', 'caramel dolce latte.jpg', 12.00, NULL, 0),
(16, 3, 'Mocha', 110, 'SMALL', 'mocha.jpg', 12.00, NULL, 0),
(17, 3, 'Mocha', 130, 'MEDIUM', 'mocha.jpg', 12.00, NULL, 0),
(18, 3, 'Mocha', 150, 'LARGE', 'mocha.jpg', 12.00, NULL, 0),
(19, 2, 'Oreo Milkshake', 90, 'SMALL', 'oreo_milkshake.jpg', 12.00, NULL, 0),
(20, 2, 'Oreo Milkshake', 110, 'MEDIUM', 'oreo_milkshake.jpg', 12.00, NULL, 0),
(21, 2, 'Oreo Milkshake', 130, 'LARGE', 'oreo_milkshake.jpg', 12.00, NULL, 0),
(22, 2, 'Matcha Latte', 100, 'SMALL', 'matcha_latte.jpg', 12.00, NULL, 0),
(23, 2, 'Matcha Latte', 120, 'MEDIUM', 'matcha_latte.jpg', 12.00, NULL, 0),
(24, 2, 'Matcha Latte', 140, 'LARGE', 'matcha_latte.jpg', 12.00, NULL, 0),
(25, 2, 'Chai Latte', 95, 'SMALL', 'chai.jpg', 12.00, NULL, 0),
(26, 2, 'Chai Latte', 115, 'MEDIUM', 'chai.jpg', 12.00, NULL, 0),
(27, 2, 'Chai Latte', 135, 'LARGE', 'chai.jpg', 12.00, NULL, 0),
(28, 2, 'Banana Milkshake', 95, 'SMALL', 'banana.jpg', 12.00, NULL, 0),
(29, 2, 'Banana Milkshake', 115, 'MEDIUM', 'banana.jpg', 12.00, NULL, 0),
(30, 2, 'Banana Milkshake', 135, 'LARGE', 'banana.jpg', 12.00, NULL, 0),
(31, 2, 'Strawberry Shake', 90, 'SMALL', 'strawberry.jpg', 12.00, NULL, 0),
(32, 2, 'Strawberry Shake', 110, 'MEDIUM', 'strawberry.jpg', 12.00, NULL, 0),
(33, 2, 'Strawberry Shake', 130, 'LARGE', 'strawberry.jpg', 12.00, NULL, 0),
(34, 2, 'Iced Lemon Tea', 100, 'SMALL', 'lemon.jpg', 12.00, NULL, 0),
(35, 2, 'Iced Lemon Tea', 120, 'MEDIUM', 'lemon.jpg', 12.00, NULL, 0),
(36, 2, 'Iced Lemon Tea', 140, 'LARGE', 'lemon.jpg', 12.00, NULL, 0),
(37, 1, 'Cookies', 60, NULL, 'cookies.jpg', 12.00, 'Chocolate Chip,Oatmeal Raisin,Double Chocolate', 0),
(38, 1, 'Muffins', 70, NULL, 'muffins.jpg', 12.00, 'Blueberry,Banana Nut,Chocolate', 0),
(39, 1, 'Croissant', 75, NULL, 'croissant.jpg', 12.00, 'Plain,Chocolate,Almond', 0),
(40, 1, 'Donut', 50, NULL, 'donut.jpg', 12.00, 'Glazed,Chocolate,Strawberry', 0),
(41, 1, 'Brownie', 65, NULL, 'brownie.jpg', 12.00, 'Classic,Walnut,Caramel', 0),
(42, 1, 'Cheesecake', 85, NULL, 'cheesecake.jpg', 12.00, 'New York,Blueberry,Mango', 0),
(46, 3, 'Espresso', 80, 'SMALL', 'espresso.jpg', 12.00, NULL, 0),
(47, 3, 'Espresso', 100, 'MEDIUM', 'espresso.jpg', 12.00, NULL, 0),
(48, 3, 'Espresso', 120, 'LARGE', 'espresso.jpg', 12.00, NULL, 0),
(54, 3, 'Americano', 90, 'SMALL', 'americano.jpg', 12.00, NULL, 0),
(55, 3, 'Americano', 110, 'MEDIUM', 'americano.jpg', 12.00, NULL, 0),
(56, 3, 'Americano', 130, 'LARGE', 'americano.jpg', 12.00, NULL, 0),
(57, 1, 'Cake', 100, NULL, 'images.jpg', 12.00, 'Chocolate', 0);

-- --------------------------------------------------------

--
-- Table structure for table `orderitems`
--

CREATE TABLE `orderitems` (
  `order_item_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `menu_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orderitems`
--

INSERT INTO `orderitems` (`order_item_id`, `order_id`, `menu_id`, `quantity`) VALUES
(361, 1, 46, 2),
(362, 1, 37, 1),
(364, 2, 38, 2),
(365, 3, 9, 1),
(366, 3, 40, 1),
(367, 4, 10, 2),
(368, 4, 39, 1),
(369, 5, 14, 1),
(370, 5, 41, 2),
(371, 6, 19, 1),
(372, 6, 42, 1),
(373, 7, 23, 2),
(374, 7, 37, 1),
(375, 8, 27, 1),
(376, 8, 38, 2),
(377, 9, 28, 1),
(378, 9, 40, 1),
(379, 10, 32, 2),
(380, 10, 39, 1),
(381, 11, 36, 1),
(382, 11, 41, 2),
(383, 12, 46, 1),
(384, 12, 42, 1),
(386, 13, 37, 1),
(387, 14, 9, 1),
(388, 14, 38, 2),
(389, 15, 10, 1),
(390, 15, 40, 1),
(391, 16, 14, 2),
(392, 16, 39, 1),
(393, 17, 19, 1),
(394, 17, 41, 2),
(395, 18, 23, 1),
(396, 18, 42, 1),
(397, 19, 27, 2),
(398, 19, 37, 1),
(399, 20, 28, 1),
(400, 20, 38, 2),
(401, 21, 32, 1),
(402, 21, 40, 1),
(403, 22, 36, 2),
(404, 22, 39, 1),
(405, 23, 46, 1),
(406, 23, 41, 2),
(408, 24, 42, 1),
(409, 25, 9, 2),
(410, 25, 37, 1),
(411, 26, 10, 1),
(412, 26, 38, 2),
(413, 27, 14, 1),
(414, 27, 40, 1),
(415, 28, 19, 2),
(416, 28, 39, 1),
(417, 29, 23, 1),
(418, 29, 41, 2),
(419, 30, 27, 1),
(420, 30, 42, 1),
(421, 51, 46, 3),
(422, 51, 37, 2),
(424, 52, 38, 4),
(425, 53, 9, 2),
(426, 53, 40, 3),
(427, 54, 10, 4),
(428, 54, 39, 2),
(429, 55, 14, 2),
(430, 55, 41, 4),
(431, 56, 19, 2),
(432, 56, 42, 3),
(433, 57, 23, 4),
(434, 57, 37, 2),
(435, 58, 27, 2),
(436, 58, 38, 4),
(437, 59, 28, 2),
(438, 59, 40, 3),
(439, 60, 32, 4),
(440, 60, 39, 2),
(441, 61, 36, 2),
(442, 61, 41, 4),
(443, 62, 46, 2),
(444, 62, 42, 3),
(446, 63, 37, 2),
(447, 64, 9, 2),
(448, 64, 38, 4),
(449, 65, 10, 2),
(450, 65, 40, 3),
(451, 66, 14, 4),
(452, 66, 39, 2),
(453, 67, 19, 2),
(454, 67, 41, 4),
(455, 68, 23, 2),
(456, 68, 42, 3),
(457, 69, 27, 4),
(458, 69, 37, 2),
(459, 70, 28, 2),
(460, 70, 38, 4),
(461, 71, 32, 2),
(462, 71, 40, 3),
(463, 72, 36, 4),
(464, 72, 39, 2),
(465, 73, 46, 2),
(466, 73, 41, 4),
(468, 74, 42, 3),
(469, 75, 9, 4),
(470, 75, 37, 2),
(471, 76, 10, 2),
(472, 76, 38, 4),
(473, 77, 14, 2),
(474, 77, 40, 3),
(475, 78, 19, 4),
(476, 78, 39, 2),
(477, 79, 23, 2),
(478, 79, 41, 4),
(479, 80, 27, 2),
(480, 80, 42, 3),
(481, 51, 21, 1),
(482, 51, 37, 1),
(483, 51, 37, 4),
(484, 52, 41, 1),
(485, 52, 21, 1),
(486, 52, 32, 1),
(487, 53, 15, 1),
(488, 53, 47, 1),
(489, 54, 8, 1),
(490, 55, 38, 1),
(491, 56, 11, 1),
(492, 56, 17, 1),
(493, 57, 17, 1),
(494, 57, 23, 1),
(495, 58, 8, 2),
(496, 58, 37, 1),
(497, 59, 12, 2),
(498, 59, 38, 2),
(499, 60, 18, 1),
(500, 60, 24, 1),
(501, 61, 7, 3),
(502, 61, 37, 2);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `order_date` datetime DEFAULT current_timestamp(),
  `order_type` enum('Dine In','Take Out') NOT NULL,
  `status` enum('Pending','Preparing','Ready','Completed') DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `user_id`, `order_date`, `order_type`, `status`) VALUES
(1, 2, '2025-05-11 08:15:00', 'Dine In', 'Completed'),
(2, 2, '2025-05-11 09:30:00', 'Take Out', 'Completed'),
(3, 2, '2025-05-11 10:45:00', 'Dine In', 'Completed'),
(4, 2, '2025-05-11 12:00:00', 'Take Out', 'Completed'),
(5, 2, '2025-05-11 14:20:00', 'Dine In', 'Completed'),
(6, 2, '2025-05-12 07:50:00', 'Take Out', 'Completed'),
(7, 2, '2025-05-12 09:10:00', 'Dine In', 'Completed'),
(8, 2, '2025-05-12 11:25:00', 'Take Out', 'Completed'),
(9, 2, '2025-05-12 13:40:00', 'Dine In', 'Completed'),
(10, 2, '2025-05-12 15:55:00', 'Take Out', 'Completed'),
(11, 2, '2025-05-13 08:30:00', 'Dine In', 'Completed'),
(12, 2, '2025-05-13 10:00:00', 'Take Out', 'Completed'),
(13, 2, '2025-05-13 12:15:00', 'Dine In', 'Completed'),
(14, 2, '2025-05-13 14:30:00', 'Take Out', 'Completed'),
(15, 2, '2025-05-13 16:45:00', 'Dine In', 'Completed'),
(16, 2, '2025-05-14 09:00:00', 'Take Out', 'Completed'),
(17, 2, '2025-05-14 11:20:00', 'Dine In', 'Completed'),
(18, 2, '2025-05-14 13:35:00', 'Take Out', 'Completed'),
(19, 2, '2025-05-14 15:50:00', 'Dine In', 'Completed'),
(20, 2, '2025-05-14 18:05:00', 'Take Out', 'Completed'),
(21, 2, '2025-05-15 08:10:00', 'Dine In', 'Completed'),
(22, 2, '2025-05-15 10:25:00', 'Take Out', 'Completed'),
(23, 2, '2025-05-15 12:40:00', 'Dine In', 'Completed'),
(24, 2, '2025-05-15 14:55:00', 'Take Out', 'Completed'),
(25, 2, '2025-05-15 17:10:00', 'Dine In', 'Completed'),
(26, 2, '2025-05-16 07:45:00', 'Take Out', 'Completed'),
(27, 2, '2025-05-16 09:15:00', 'Dine In', 'Completed'),
(28, 2, '2025-05-16 11:30:00', 'Take Out', 'Completed'),
(29, 2, '2025-05-16 13:45:00', 'Dine In', 'Completed'),
(30, 2, '2025-05-16 16:00:00', 'Take Out', 'Completed'),
(31, 2, '2025-05-17 08:20:00', 'Dine In', 'Completed'),
(32, 2, '2025-05-17 10:35:00', 'Take Out', 'Completed'),
(33, 2, '2025-05-17 12:50:00', 'Dine In', 'Completed'),
(34, 2, '2025-05-17 15:05:00', 'Take Out', 'Completed'),
(35, 2, '2025-05-17 17:20:00', 'Dine In', 'Completed'),
(36, 2, '2025-05-18 09:25:00', 'Take Out', 'Completed'),
(37, 2, '2025-05-18 11:40:00', 'Dine In', 'Completed'),
(38, 2, '2025-05-18 13:55:00', 'Take Out', 'Completed'),
(39, 2, '2025-05-18 16:10:00', 'Dine In', 'Completed'),
(40, 2, '2025-05-18 18:25:00', 'Take Out', 'Completed'),
(41, 2, '2025-05-19 08:00:00', 'Dine In', 'Completed'),
(42, 2, '2025-05-19 10:15:00', 'Take Out', 'Completed'),
(43, 2, '2025-05-19 12:30:00', 'Dine In', 'Completed'),
(44, 2, '2025-05-19 14:45:00', 'Take Out', 'Completed'),
(45, 2, '2025-05-19 17:00:00', 'Dine In', 'Completed'),
(46, 2, '2025-05-20 09:05:00', 'Take Out', 'Completed'),
(47, 2, '2025-05-20 11:20:00', 'Dine In', 'Completed'),
(48, 2, '2025-05-20 13:35:00', 'Take Out', 'Completed'),
(49, 2, '2025-05-20 15:50:00', 'Dine In', 'Completed'),
(50, 2, '2025-05-20 18:05:00', 'Take Out', 'Completed'),
(51, 2, '2025-05-16 13:40:54', 'Dine In', 'Completed'),
(52, 2, '2025-05-16 17:19:36', 'Take Out', 'Completed'),
(53, 2, '2025-05-16 17:21:03', 'Take Out', 'Completed'),
(54, 2, '2025-05-16 17:27:19', 'Dine In', 'Completed'),
(55, 2, '2025-05-17 20:39:38', 'Dine In', 'Completed'),
(56, 2, '2025-05-17 20:49:15', 'Dine In', 'Preparing'),
(57, 2, '2025-05-17 20:50:06', 'Dine In', 'Preparing'),
(58, 2, '2025-05-17 20:51:05', 'Dine In', 'Preparing'),
(59, 2, '2025-05-17 21:52:40', 'Dine In', 'Preparing'),
(60, 2, '2025-05-17 21:53:29', 'Take Out', 'Preparing'),
(61, 2, '2025-05-17 21:54:18', 'Take Out', 'Completed');

-- --------------------------------------------------------

--
-- Table structure for table `orderstatuslog`
--

CREATE TABLE `orderstatuslog` (
  `log_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `new_status` enum('Preparing','Ready','Completed') DEFAULT NULL,
  `updated_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orderstatuslog`
--

INSERT INTO `orderstatuslog` (`log_id`, `order_id`, `updated_by`, `new_status`, `updated_at`) VALUES
(1, 1, 3, 'Preparing', '2025-05-01 08:20:00'),
(2, 1, 3, 'Ready', '2025-05-01 08:30:00'),
(3, 1, 3, 'Completed', '2025-05-01 08:40:00'),
(4, 2, 3, 'Preparing', '2025-05-01 09:35:00'),
(5, 2, 3, 'Ready', '2025-05-01 09:45:00'),
(6, 2, 3, 'Completed', '2025-05-01 09:55:00'),
(7, 3, 3, 'Preparing', '2025-05-01 10:50:00'),
(8, 3, 3, 'Ready', '2025-05-01 11:00:00'),
(9, 3, 3, 'Completed', '2025-05-01 11:10:00'),
(10, 4, 3, 'Preparing', '2025-05-01 12:05:00'),
(11, 4, 3, 'Ready', '2025-05-01 12:15:00'),
(12, 4, 3, 'Completed', '2025-05-01 12:25:00'),
(13, 5, 3, 'Preparing', '2025-05-01 14:25:00'),
(14, 5, 3, 'Ready', '2025-05-01 14:35:00'),
(15, 5, 3, 'Completed', '2025-05-01 14:45:00'),
(16, 6, 3, 'Preparing', '2025-05-02 07:55:00'),
(17, 6, 3, 'Ready', '2025-05-02 08:05:00'),
(18, 6, 3, 'Completed', '2025-05-02 08:15:00'),
(19, 7, 3, 'Preparing', '2025-05-02 09:15:00'),
(20, 7, 3, 'Ready', '2025-05-02 09:25:00'),
(21, 7, 3, 'Completed', '2025-05-02 09:35:00'),
(22, 8, 3, 'Preparing', '2025-05-02 11:30:00'),
(23, 8, 3, 'Ready', '2025-05-02 11:40:00'),
(24, 8, 3, 'Completed', '2025-05-02 11:50:00'),
(25, 9, 3, 'Preparing', '2025-05-02 13:45:00'),
(26, 9, 3, 'Ready', '2025-05-02 13:55:00'),
(27, 9, 3, 'Completed', '2025-05-02 14:05:00'),
(28, 10, 3, 'Preparing', '2025-05-02 16:00:00'),
(29, 10, 3, 'Ready', '2025-05-02 16:10:00'),
(30, 10, 3, 'Completed', '2025-05-02 16:20:00'),
(61, 51, 3, 'Preparing', '2025-05-11 08:20:00'),
(62, 51, 3, 'Ready', '2025-05-11 08:30:00'),
(63, 51, 3, 'Completed', '2025-05-11 08:40:00'),
(64, 52, 3, 'Preparing', '2025-05-11 09:35:00'),
(65, 52, 3, 'Ready', '2025-05-11 09:45:00'),
(66, 52, 3, 'Completed', '2025-05-11 09:55:00'),
(67, 53, 3, 'Preparing', '2025-05-11 10:50:00'),
(68, 53, 3, 'Ready', '2025-05-11 11:00:00'),
(69, 53, 3, 'Completed', '2025-05-11 11:10:00'),
(70, 54, 3, 'Preparing', '2025-05-11 12:05:00'),
(71, 54, 3, 'Ready', '2025-05-11 12:15:00'),
(72, 54, 3, 'Completed', '2025-05-11 12:25:00'),
(73, 55, 3, 'Preparing', '2025-05-11 14:25:00'),
(74, 55, 3, 'Ready', '2025-05-11 14:35:00'),
(75, 55, 3, 'Completed', '2025-05-11 14:45:00'),
(76, 56, 3, 'Preparing', '2025-05-12 07:55:00'),
(77, 56, 3, 'Ready', '2025-05-12 08:05:00'),
(78, 56, 3, 'Completed', '2025-05-12 08:15:00'),
(79, 57, 3, 'Preparing', '2025-05-12 09:15:00'),
(80, 57, 3, 'Ready', '2025-05-12 09:25:00'),
(81, 57, 3, 'Completed', '2025-05-12 09:35:00'),
(82, 58, 3, 'Preparing', '2025-05-12 11:30:00'),
(83, 58, 3, 'Ready', '2025-05-12 11:40:00'),
(84, 58, 3, 'Completed', '2025-05-12 11:50:00'),
(85, 59, 3, 'Preparing', '2025-05-12 13:45:00'),
(86, 59, 3, 'Ready', '2025-05-12 13:55:00'),
(87, 59, 3, 'Completed', '2025-05-12 14:05:00'),
(88, 60, 3, 'Preparing', '2025-05-12 16:00:00'),
(89, 60, 3, 'Ready', '2025-05-12 16:10:00'),
(90, 60, 3, 'Completed', '2025-05-12 16:20:00'),
(91, 51, 3, 'Ready', '2025-05-16 13:41:13'),
(92, 51, 3, 'Completed', '2025-05-16 13:41:14'),
(93, 54, 3, 'Ready', '2025-05-17 19:11:16'),
(94, 54, 3, 'Completed', '2025-05-17 19:11:19'),
(95, 53, 3, 'Ready', '2025-05-17 19:11:57'),
(96, 53, 3, 'Completed', '2025-05-17 19:12:27'),
(97, 52, 3, 'Ready', '2025-05-17 19:12:33'),
(98, 52, 3, 'Completed', '2025-05-17 19:12:34'),
(99, 55, 3, 'Ready', '2025-05-17 20:40:20'),
(100, 55, 3, 'Completed', '2025-05-17 20:40:22'),
(101, 61, 3, 'Ready', '2025-05-17 21:58:50'),
(102, 61, 3, 'Completed', '2025-05-17 21:58:54');

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `method` enum('Cash','E-Wallet') NOT NULL,
  `vat_total` decimal(10,2) DEFAULT 0.00,
  `paid_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`payment_id`, `order_id`, `method`, `vat_total`, `paid_at`) VALUES
(1, 1, 'Cash', 26.40, '2025-05-01 08:40:00'),
(2, 2, 'E-Wallet', 30.00, '2025-05-01 09:55:00'),
(3, 3, 'Cash', 22.80, '2025-05-01 11:10:00'),
(4, 4, 'E-Wallet', 33.00, '2025-05-01 12:25:00'),
(5, 5, 'Cash', 31.20, '2025-05-01 14:45:00'),
(6, 6, 'E-Wallet', 21.00, '2025-05-02 08:15:00'),
(7, 7, 'Cash', 36.00, '2025-05-02 09:35:00'),
(8, 8, 'E-Wallet', 33.00, '2025-05-02 11:50:00'),
(9, 9, 'Cash', 17.40, '2025-05-02 14:05:00'),
(10, 10, 'E-Wallet', 35.40, '2025-05-02 16:20:00'),
(11, 11, 'Cash', 32.40, '2025-05-03 08:55:00'),
(12, 12, 'E-Wallet', 19.80, '2025-05-03 10:15:00'),
(13, 13, 'Cash', 33.60, '2025-05-03 12:25:00'),
(14, 14, 'E-Wallet', 33.60, '2025-05-03 14:40:00'),
(15, 15, 'Cash', 18.00, '2025-05-03 16:55:00'),
(31, 51, 'Cash', 43.20, '2025-05-11 08:40:00'),
(32, 52, 'E-Wallet', 49.20, '2025-05-11 09:55:00'),
(33, 53, 'Cash', 39.60, '2025-05-11 11:10:00'),
(34, 54, 'E-Wallet', 54.00, '2025-05-11 12:25:00'),
(35, 55, 'Cash', 51.60, '2025-05-11 14:45:00'),
(36, 56, 'E-Wallet', 41.40, '2025-05-12 08:15:00'),
(37, 57, 'Cash', 60.00, '2025-05-12 09:35:00'),
(38, 58, 'E-Wallet', 54.00, '2025-05-12 11:50:00'),
(39, 59, 'Cash', 31.80, '2025-05-12 14:05:00'),
(40, 60, 'E-Wallet', 58.80, '2025-05-12 16:20:00'),
(41, 61, 'Cash', 52.80, '2025-05-13 08:55:00'),
(42, 62, 'E-Wallet', 41.40, '2025-05-13 10:15:00'),
(43, 63, 'Cash', 56.40, '2025-05-13 12:25:00'),
(44, 64, 'E-Wallet', 55.20, '2025-05-13 14:40:00'),
(45, 65, 'Cash', 33.00, '2025-05-13 16:55:00'),
(46, 51, 'E-Wallet', 51.60, '2025-05-16 13:40:54'),
(47, 52, 'E-Wallet', 36.60, '2025-05-16 17:19:36'),
(48, 53, 'Cash', 30.00, '2025-05-16 17:21:03'),
(49, 54, 'E-Wallet', 14.40, '2025-05-16 17:27:19'),
(50, 55, 'Cash', 8.40, '2025-05-17 20:39:38'),
(51, 56, 'Cash', 30.00, '2025-05-17 20:49:15'),
(52, 57, 'E-Wallet', 30.00, '2025-05-17 20:50:06'),
(53, 58, 'Cash', 36.00, '2025-05-17 20:51:05'),
(54, 59, 'Cash', 50.40, '2025-05-17 21:52:40'),
(55, 60, 'E-Wallet', 34.80, '2025-05-17 21:53:29'),
(56, 61, 'Cash', 50.40, '2025-05-17 21:54:18');

-- --------------------------------------------------------

--
-- Table structure for table `salesreport`
--

CREATE TABLE `salesreport` (
  `report_id` int(11) NOT NULL,
  `order_date` date DEFAULT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `total_orders` int(11) DEFAULT NULL,
  `total_qty` int(11) DEFAULT NULL,
  `total_vat` decimal(10,2) DEFAULT 0.00,
  `total_sales` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `salesreport`
--

INSERT INTO `salesreport` (`report_id`, `order_date`, `item_name`, `total_orders`, `total_qty`, `total_vat`, `total_sales`) VALUES
(1, '2025-05-01', 'Espresso', 3, 4, 38.40, 320.00),
(2, '2025-05-02', 'Matcha Latte', 4, 5, 72.00, 600.00),
(3, '2025-05-03', 'Cookies', 6, 7, 50.40, 420.00),
(4, '2025-05-04', 'Brownie', 5, 10, 78.00, 650.00),
(5, '2025-05-05', 'Americano', 3, 4, 52.80, 440.00),
(6, '2025-05-11', 'Espresso', 3, 7, 67.20, 560.00),
(7, '2025-05-12', 'Matcha Latte', 4, 10, 144.00, 1200.00),
(8, '2025-05-13', 'Cookies', 6, 12, 86.40, 720.00),
(9, '2025-05-14', 'Brownie', 5, 20, 156.00, 1300.00),
(10, '2025-05-15', 'Americano', 3, 8, 105.60, 880.00),
(11, '2025-05-16', 'Oreo Milkshake', 2, 2, 31.20, 291.20),
(12, '2025-05-16', 'Cookies', 2, 5, 36.00, 336.00),
(13, '2025-05-16', 'Brownie', 1, 1, 7.80, 72.80),
(14, '2025-05-16', 'Strawberry Shake', 1, 1, 13.20, 123.20),
(15, '2025-05-16', 'Caramel Dolce Latte', 1, 1, 18.00, 168.00),
(16, '2025-05-16', 'Espresso', 1, 1, 12.00, 112.00),
(17, '2025-05-16', 'Cappuccino', 1, 1, 14.40, 134.40),
(18, '2025-05-17', 'Muffins', 2, 3, 25.20, 235.20),
(19, '2025-05-17', 'Macchiato', 2, 3, 48.00, 448.00),
(20, '2025-05-17', 'Mocha', 3, 3, 49.20, 459.20),
(21, '2025-05-17', 'Matcha Latte', 2, 2, 31.20, 291.20),
(22, '2025-05-17', 'Cappuccino', 2, 5, 64.80, 604.80),
(23, '2025-05-17', 'Cookies', 2, 3, 21.60, 201.60);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `role` enum('Customer','Admin','Barista') NOT NULL,
  `pin` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `role`, `pin`) VALUES
(1, 'Admin', '1234'),
(2, 'Customer', '2345'),
(3, 'Barista', '3456');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`menu_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `orderitems`
--
ALTER TABLE `orderitems`
  ADD PRIMARY KEY (`order_item_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `orderitems_ibfk_2` (`menu_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `orderstatuslog`
--
ALTER TABLE `orderstatuslog`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `order_id` (`order_id`);

--
-- Indexes for table `salesreport`
--
ALTER TABLE `salesreport`
  ADD PRIMARY KEY (`report_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `menu_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `orderitems`
--
ALTER TABLE `orderitems`
  MODIFY `order_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=503;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- AUTO_INCREMENT for table `orderstatuslog`
--
ALTER TABLE `orderstatuslog`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=103;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `salesreport`
--
ALTER TABLE `salesreport`
  MODIFY `report_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `menu`
--
ALTER TABLE `menu`
  ADD CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`);

--
-- Constraints for table `orderitems`
--
ALTER TABLE `orderitems`
  ADD CONSTRAINT `orderitems_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  ADD CONSTRAINT `orderitems_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`menu_id`) ON DELETE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `orderstatuslog`
--
ALTER TABLE `orderstatuslog`
  ADD CONSTRAINT `orderstatuslog_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  ADD CONSTRAINT `orderstatuslog_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
