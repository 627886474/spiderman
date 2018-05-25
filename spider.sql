CREATE TABLE `jobbole_spider` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) COLLATE utf8_bin NOT NULL,
  `parise_nums` int(10) DEFAULT NULL,
  `fav_nums` int(10) DEFAULT NULL,
  `front_image_url` varchar(150) COLLATE utf8_bin DEFAULT NULL,
  `front_image_path` varchar(200) COLLATE utf8_bin DEFAULT NULL,
  `tags` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `url` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
SET FOREIGN_KEY_CHECKS = 1;

