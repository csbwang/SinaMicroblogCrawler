/*
Navicat MySQL Data Transfer

Source Server         : root
Source Server Version : 50622
Source Host           : 127.0.0.1:3306
Source Database       : sina_microblog

Target Server Type    : MYSQL
Target Server Version : 50622
File Encoding         : 65001

Date: 2015-12-01 22:11:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for sina_microblog
-- ----------------------------
DROP TABLE IF EXISTS `microblog`;
CREATE TABLE `microblog` (
  `mid` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `text` varchar(500) COLLATE utf8_unicode_ci NOT NULL,
  `source` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `uid` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`mid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
