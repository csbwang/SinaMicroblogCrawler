/*
Navicat MySQL Data Transfer

Source Server         : root
Source Server Version : 50622
Source Host           : 127.0.0.1:3306
Source Database       : sina_microblog

Target Server Type    : MYSQL
Target Server Version : 50622
File Encoding         : 65001

Date: 2015-12-01 22:11:38
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `uid` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `screen_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `province` int(11) NOT NULL,
  `city` int(11) NOT NULL,
  `location` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL,
  `profile_image_url` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL,
  `domain` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `gender` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `followersnum` int(11) NOT NULL,
  `friendsnum` int(11) NOT NULL,
  `statusesnum` int(11) NOT NULL,
  `favouritesnum` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `allow_all_act_msg` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `geo_enabled` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `verified` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
