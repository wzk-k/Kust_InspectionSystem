/*
 Navicat MySQL Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50736
 Source Host           : localhost:3306
 Source Schema         : kust_inspection

 Target Server Type    : MySQL
 Target Server Version : 50736
 File Encoding         : 65001

 Date: 14/04/2023 23:33:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for inspection_group_membership
-- ----------------------------
DROP TABLE IF EXISTS `inspection_group_membership`;
CREATE TABLE `inspection_group_membership`  (
  `inspection_group_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `person_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`inspection_group_id`, `person_id`) USING BTREE,
  INDEX `person_id`(`person_id`) USING BTREE,
  CONSTRAINT `inspection_group_membership_ibfk_1` FOREIGN KEY (`inspection_group_id`) REFERENCES `inspectiongroup` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `inspection_group_membership_ibfk_2` FOREIGN KEY (`person_id`) REFERENCES `person` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of inspection_group_membership
-- ----------------------------
INSERT INTO `inspection_group_membership` VALUES ('0fe6e1c87b4e4cca9c89e3bbf2495ea2', '4f15553e9fc74a61963d12d26c4f6bb6');

-- ----------------------------
-- Table structure for inspectiongroup
-- ----------------------------
DROP TABLE IF EXISTS `inspectiongroup`;
CREATE TABLE `inspectiongroup`  (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '巡视组ID',
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '巡视组名称',
  `task_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '关联的巡视任务ID',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `task_id`(`task_id`) USING BTREE,
  CONSTRAINT `inspectiongroup_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `inspectiontask` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of inspectiongroup
-- ----------------------------
INSERT INTO `inspectiongroup` VALUES ('0fe6e1c87b4e4cca9c89e3bbf2495ea2', '第一巡视组', 'dac204fe83b6403d9ea81ae7e79dd5ff');

-- ----------------------------
-- Table structure for inspectiontask
-- ----------------------------
DROP TABLE IF EXISTS `inspectiontask`;
CREATE TABLE `inspectiontask`  (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '巡视任务ID',
  `administrative_division` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '行政区划',
  `term` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '届次',
  `round` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '轮次',
  `inspection_start_date` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '巡视开始时间',
  `inspection_end_date` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '巡视结束时间',
  `standard_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '标准名称',
  `inspected_unit` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '被巡单位',
  `unified_number` int(11) NOT NULL AUTO_INCREMENT COMMENT '统一编号',
  `security_classification` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密级标识',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unified_number`(`unified_number`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of inspectiontask
-- ----------------------------
INSERT INTO `inspectiontask` VALUES ('dac204fe83b6403d9ea81ae7e79dd5ff', '云南', '二十届', '第一轮', '2023年1月5日', '2023年1月9日', '二十届云南省一轮检查', '昆明理工大学', 1, '高级');

-- ----------------------------
-- Table structure for person
-- ----------------------------
DROP TABLE IF EXISTS `person`;
CREATE TABLE `person`  (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户id',
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `sex` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '性别',
  `phone` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '手机号码',
  `native_place` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '籍贯',
  `number` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `birth_place` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '出生地',
  `work_unit` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '工作单位',
  `unit_level` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '单位层级',
  `unit_location` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '单位所在地',
  `current_position` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '现任职务',
  `proposed_position` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '拟任职务',
  `proposed_dismissal_position` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '拟免职务',
  `graduation_school` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '毕业学校',
  `talent_pool_type` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '人才库类型',
  `personnel_source` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '人员来源',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_Person_id`(`id`) USING BTREE,
  UNIQUE INDEX `number`(`number`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of person
-- ----------------------------
INSERT INTO `person` VALUES ('4f15553e9fc74a61963d12d26c4f6bb6', '张三', '男', '19277621898', '昆明', 2, '上海', '云南大学', '省部级', '昆明', '副部', '副部', '副部', '北京大学', '组长库', '组织');
INSERT INTO `person` VALUES ('6f08722f9dfe438ea11005ac8af4cbee', '张二', '女', '19277621891', '上海', 3, '曲靖', '北京市政府', '省部级', '北京', '副部', '副部', '副部', '北京大学', '专业人才库', '组织');
INSERT INTO `person` VALUES ('6fd3f2ba5f9f45c8b4f18339bb219734', '李四', '男', '19877628761', '北京', 1, '昆明', '昆明市政府', '省部级', '昆明', '副部', '副部', '副部', '昆明理工大学', '专业人才库', '组织');

-- ----------------------------
-- Table structure for relatives
-- ----------------------------
DROP TABLE IF EXISTS `relatives`;
CREATE TABLE `relatives`  (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'id',
  `person_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '关联的人员ID',
  `relative_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '关联的亲属ID',
  `relation` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '关系',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_Relatives_id`(`id`) USING BTREE,
  INDEX `person_id`(`person_id`) USING BTREE,
  INDEX `relative_id`(`relative_id`) USING BTREE,
  CONSTRAINT `relatives_ibfk_1` FOREIGN KEY (`person_id`) REFERENCES `person` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `relatives_ibfk_2` FOREIGN KEY (`relative_id`) REFERENCES `person` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of relatives
-- ----------------------------
INSERT INTO `relatives` VALUES ('dac204fe83b6403d9ea81a99e79dd5ff', '4f15553e9fc74a61963d12d26c4f6bb6', '6f08722f9dfe438ea11005ac8af4cbee', '父亲');
INSERT INTO `relatives` VALUES ('dac204fe83b6403d9eaeea99e79dd5ff', '6f08722f9dfe438ea11005ac8af4cbee', '4f15553e9fc74a61963d12d26c4f6bb6', '女儿');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户id',
  `userName` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码',
  `userSex` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '性别',
  `userPhone` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '手机号码',
  `unifiedNumber` int(11) NULL DEFAULT NULL COMMENT '编号',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_User_id`(`id`) USING BTREE,
  UNIQUE INDEX `unifiedNumber`(`unifiedNumber`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
