-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 31, 2026 at 07:59 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `goviya_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `agriculture_officers`
--

CREATE TABLE `agriculture_officers` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `district` varchar(50) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `agriculture_officers`
--

INSERT INTO `agriculture_officers` (`id`, `name`, `district`, `phone`, `email`) VALUES
(1, 'Mr. Perera', 'Colombo', '071-1234567', 'perera@gov.lk'),
(2, 'Ms. Silva', 'Gampaha', '077-9876543', 'silva@gov.lk'),
(3, 'Mr. Bandara', 'Kandy', '070-5555555', 'bandara@gov.lk');

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `id` int(11) NOT NULL,
  `post_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`id`, `post_id`, `user_id`, `content`, `created_at`) VALUES
(1, 4, 2, 'it ok bro', '2026-01-31 04:52:47'),
(2, 4, 2, 'it ok bro', '2026-01-31 04:53:05');

-- --------------------------------------------------------

--
-- Table structure for table `diseases`
--

CREATE TABLE `diseases` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `crop_type` enum('paddy','plant') NOT NULL,
  `chemical_treatment` text DEFAULT NULL,
  `organic_treatment` text DEFAULT NULL,
  `general_advice` text DEFAULT NULL,
  `prevention` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `diseases`
--

INSERT INTO `diseases` (`id`, `name`, `crop_type`, `chemical_treatment`, `organic_treatment`, `general_advice`, `prevention`) VALUES
(1, 'bacterial_leaf_blight', 'paddy', 'Spray <b>Copper Oxychloride</b> (e.g., Lankem Copper). Mix 20g per 10L tank.', 'Apply fresh <b>Cow Dung slurry</b> mixed with water to strengthen plant immunity.', 'Monitor field water levels.', 'Use resistant varieties like Bg 352. Avoid excessive Nitrogen fertilizer (Urea).'),
(2, 'blast', 'paddy', 'Spray <b>Tricyclazole 75 WP</b> (e.g., Beam) or <b>Isoprothiolane 40 EC</b> (e.g., Fujione).', 'Spray <b>Silica-rich herbal extracts</b> (burned paddy husk ash mixed with water).', 'Keep the bunds clean.', 'Burn infected straw immediately. Do not keep water stagnant.'),
(3, 'brown_spot', 'paddy', 'Spray <b>Mancozeb 80 WP</b> or <b>Propiconazole</b> (e.g., Tilt).', 'Improve soil quality by adding <b>Potash (MOP)</b> and organic compost.', 'Check soil nutrition.', 'Use clean, certified seeds. Treat seeds with hot water (52°C) before sowing.'),
(4, 'Tomato___Late_blight', 'plant', 'Spray <b>Mancozeb</b> (e.g., Dithane M45) or <b>Chlorothalonil</b> (e.g., Bravo). Mix 30g per 16L tank.', 'Remove infected leaves immediately. Spray <b>Neem Oil (Kohomba Thel)</b> mixed with soap water.', 'Severe fungal infection.', 'Avoid overhead watering. Stake plants to improve air flow.'),
(5, 'Tomato___Early_blight', 'plant', 'Use <b>Antracol (Propineb)</b> or <b>Ridomil Gold</b>.', 'Mulch the soil with dried straw to prevent soil spores splashing onto leaves.', 'Common in wet weather.', 'Rotate crops with beans or corn (non-solanaceous crops).');

-- --------------------------------------------------------

--
-- Table structure for table `farmers`
--

CREATE TABLE `farmers` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `district` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `farmers`
--

INSERT INTO `farmers` (`id`, `name`, `email`, `password_hash`, `district`, `created_at`) VALUES
(1, 'pramitha sahan preethimal', 'pramithapreethimal@gmail.com', 'pbkdf2:sha256:1000000$cvAUqQ3NkooN0VRo$9c8f3a21f87c12b73bb0d93aeae43642d742dde9833d734c893ae062c13fe26f', 'Colombo', '2026-01-29 18:35:26'),
(2, 'nadeesha', 'nadeesha@gmail.com', 'pbkdf2:sha256:1000000$AQpQVbJgD46u5UVP$9bde792b900aaf8b2f97b5990f13c9b0dd2f2e29f9d234b6b696904c18808016', 'Kurunegala', '2026-01-31 04:44:18');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`id`, `user_id`, `title`, `content`, `image_path`, `created_at`) VALUES
(1, 1, 'Advice needed for blast', 'The AI suggested this treatment: <p>Spray Tricyclazole 75 WP or Isoprothiolane 40 EC.</p>. Has anyone tried this effectively?', NULL, '2026-01-31 04:04:37'),
(2, 1, 'Advice needed for Tomato___Late_blight', 'The AI suggested this treatment: <p>Apply fungicides containing Mandipropamid or Chlorothalonil immediately. Remove infected leaves.</p>. Has anyone tried this effectively?', NULL, '2026-01-31 04:15:20'),
(3, 1, 'Advice needed for Tomato___Late_blight', 'The AI suggested this treatment: <p>Apply fungicides containing Mandipropamid or Chlorothalonil immediately. Remove infected leaves.</p>... Has anyone tried this effectively?', NULL, '2026-01-31 04:32:01'),
(4, 1, 'Advice needed for Tomato___Late_blight', 'I am planning to use this chemical treatment: Spray <b>Mancozeb</b> (e.g., Dithane M45) or <b>Ch... Has anyone tried this?', NULL, '2026-01-31 04:43:44'),
(5, 2, 'Advice needed for Tomato___Late_blight', 'I am planning to use this chemical treatment: Spray <b>Mancozeb</b> (e.g., Dithane M45) or <b>Ch... Has anyone tried this?', NULL, '2026-01-31 04:44:50'),
(6, 2, 'Advice needed for Tomato___Late_blight', 'I am planning to use this chemical treatment: Spray <b>Mancozeb</b> (e.g., Dithane M45) or <b>Ch... Has anyone tried this?', NULL, '2026-01-31 04:52:34'),
(7, 1, 'Advice needed for Tomato___Late_blight', 'My crop has Tomato___Late_blight. I am looking for advice on the recommended treatments. Has anyone faced this?', NULL, '2026-01-31 06:39:58');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `agriculture_officers`
--
ALTER TABLE `agriculture_officers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `post_id` (`post_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `diseases`
--
ALTER TABLE `diseases`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `farmers`
--
ALTER TABLE `farmers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `agriculture_officers`
--
ALTER TABLE `agriculture_officers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `diseases`
--
ALTER TABLE `diseases`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `farmers`
--
ALTER TABLE `farmers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `farmers` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `farmers` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
