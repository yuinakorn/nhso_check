SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for check_death
-- ----------------------------
DROP TABLE IF EXISTS `check_death`;
CREATE TABLE `check_death_copy1` (
  `cid` varchar(13) NOT NULL,
  `date_death` date DEFAULT NULL,
  `is_death` varchar(1) DEFAULT NULL,
  `status_desc` varchar(100) DEFAULT NULL,
  `check_death_date` date DEFAULT NULL,
  `TYPE` varchar(10) DEFAULT NULL,
  `HOSPMAIN` varchar(5) DEFAULT NULL,
  `HOSPSUB` varchar(5) DEFAULT NULL,
  `CARDID` varchar(15) DEFAULT NULL,
  `REGISTER` date DEFAULT NULL,
  `DATEEXP` date DEFAULT NULL,
  PRIMARY KEY (`cid`),
  KEY `cid` (`cid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
