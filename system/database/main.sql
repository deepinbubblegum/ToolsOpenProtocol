/*
 Navicat Premium Data Transfer

 Source Server         : openprotocol
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 06/09/2021 18:17:02
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for Link
-- ----------------------------
DROP TABLE IF EXISTS "Link";
CREATE TABLE "Link" (
  "ID_LINK" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "CODE" TEXT(45),
  "ID_Tools_link" integer(10) NOT NULL,
  CONSTRAINT "FK_Link.ID_Tools_link_Tools.ID_Tool" FOREIGN KEY ("ID_Tools_link") REFERENCES "Tools" ("ID_Tools") ON DELETE CASCADE ON UPDATE CASCADE
);

-- ----------------------------
-- Records of Link
-- ----------------------------
BEGIN;
INSERT INTO "Link" VALUES (1, '1', 1);
INSERT INTO "Link" VALUES (2, '1', 2);
INSERT INTO "Link" VALUES (3, '1', 3);
INSERT INTO "Link" VALUES (4, '1', 4);
INSERT INTO "Link" VALUES (5, '1', 5);
INSERT INTO "Link" VALUES (6, '2', 2);
COMMIT;

-- ----------------------------
-- Table structure for Socket
-- ----------------------------
DROP TABLE IF EXISTS "Socket";
CREATE TABLE "Socket" (
  "ID_SOCKET" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "Socket_number" integer(10) NOT NULL,
  "Socket_Tray_ID" integer(10) NOT NULL,
  CONSTRAINT "FK_Socket.Socket_Tray_ID_TRAY_ID_TRAY" FOREIGN KEY ("Socket_Tray_ID") REFERENCES "TRAY" ("ID_TRAY") ON DELETE CASCADE ON UPDATE CASCADE
);

-- ----------------------------
-- Records of Socket
-- ----------------------------
BEGIN;
INSERT INTO "Socket" VALUES (1, 1, 1);
INSERT INTO "Socket" VALUES (2, 2, 1);
INSERT INTO "Socket" VALUES (3, 3, 1);
INSERT INTO "Socket" VALUES (4, 4, 1);
INSERT INTO "Socket" VALUES (5, 5, 1);
INSERT INTO "Socket" VALUES (6, 6, 1);
INSERT INTO "Socket" VALUES (7, 7, 1);
INSERT INTO "Socket" VALUES (8, 8, 1);
INSERT INTO "Socket" VALUES (9, 1, 2);
INSERT INTO "Socket" VALUES (10, 2, 2);
INSERT INTO "Socket" VALUES (11, 3, 2);
INSERT INTO "Socket" VALUES (12, 4, 2);
INSERT INTO "Socket" VALUES (13, 5, 2);
INSERT INTO "Socket" VALUES (14, 6, 2);
INSERT INTO "Socket" VALUES (15, 7, 2);
INSERT INTO "Socket" VALUES (16, 8, 2);
INSERT INTO "Socket" VALUES (17, 1, 3);
INSERT INTO "Socket" VALUES (18, 2, 3);
INSERT INTO "Socket" VALUES (19, 3, 3);
INSERT INTO "Socket" VALUES (20, 4, 3);
INSERT INTO "Socket" VALUES (21, 5, 3);
INSERT INTO "Socket" VALUES (22, 6, 3);
INSERT INTO "Socket" VALUES (23, 7, 3);
INSERT INTO "Socket" VALUES (24, 8, 3);
INSERT INTO "Socket" VALUES (25, 1, 4);
INSERT INTO "Socket" VALUES (26, 2, 4);
INSERT INTO "Socket" VALUES (27, 3, 4);
INSERT INTO "Socket" VALUES (28, 4, 4);
INSERT INTO "Socket" VALUES (29, 5, 4);
INSERT INTO "Socket" VALUES (30, 6, 4);
INSERT INTO "Socket" VALUES (31, 7, 4);
INSERT INTO "Socket" VALUES (32, 8, 4);
COMMIT;

-- ----------------------------
-- Table structure for Step
-- ----------------------------
DROP TABLE IF EXISTS "Step";
CREATE TABLE "Step" (
  "ID_STEP" integer(10) NOT NULL,
  "ID_Link_step" integer(10) NOT NULL,
  "Step_number" integer(10) NOT NULL,
  "Socket_ID_Step" integer(10) NOT NULL,
  PRIMARY KEY ("ID_STEP", "ID_Link_step"),
  CONSTRAINT "FK_link_step" FOREIGN KEY ("ID_Link_step") REFERENCES "Link" ("ID_LINK") ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT "FK_Socket_step" FOREIGN KEY ("Socket_ID_Step") REFERENCES "Socket" ("ID_SOCKET") ON DELETE CASCADE ON UPDATE CASCADE
);

-- ----------------------------
-- Records of Step
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for TRAY
-- ----------------------------
DROP TABLE IF EXISTS "TRAY";
CREATE TABLE "TRAY" (
  "ID_TRAY" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "TRAY_Number" integer(10)
);

-- ----------------------------
-- Records of TRAY
-- ----------------------------
BEGIN;
INSERT INTO "TRAY" VALUES (1, 1);
INSERT INTO "TRAY" VALUES (2, 2);
INSERT INTO "TRAY" VALUES (3, 3);
INSERT INTO "TRAY" VALUES (4, 4);
COMMIT;

-- ----------------------------
-- Table structure for Tools
-- ----------------------------
DROP TABLE IF EXISTS "Tools";
CREATE TABLE "Tools" (
  "ID_Tools" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "Name_Tools" TEXT NOT NULL,
  "PORT_Tools" integer NOT NULL
);

-- ----------------------------
-- Records of Tools
-- ----------------------------
BEGIN;
INSERT INTO "Tools" VALUES (1, 'Tools 1', 9001);
INSERT INTO "Tools" VALUES (2, 'Tools 2', 9002);
INSERT INTO "Tools" VALUES (3, 'Tools 3', 9003);
INSERT INTO "Tools" VALUES (4, 'Tools 4', 9004);
INSERT INTO "Tools" VALUES (5, 'Tools 5', 9005);
INSERT INTO "Tools" VALUES (6, 'Tools 6', 9006);
INSERT INTO "Tools" VALUES (7, 'Tools 7', 9007);
INSERT INTO "Tools" VALUES (8, 'Tools 8', 9008);
INSERT INTO "Tools" VALUES (9, 'Tools 9', 9009);
INSERT INTO "Tools" VALUES (10, 'Tools 10', 9010);
INSERT INTO "Tools" VALUES (11, 'Tools 11', 9011);
INSERT INTO "Tools" VALUES (12, 'Tools 12', 9012);
INSERT INTO "Tools" VALUES (13, 'Tools 13', 9013);
INSERT INTO "Tools" VALUES (14, 'Tools 14', 9014);
INSERT INTO "Tools" VALUES (15, 'Tools 15', 9015);
INSERT INTO "Tools" VALUES (16, 'Tools 16', 9016);
INSERT INTO "Tools" VALUES (17, 'Tools 17', 9017);
COMMIT;

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE sqlite_sequence(name,seq);

-- ----------------------------
-- Records of sqlite_sequence
-- ----------------------------
BEGIN;
INSERT INTO "sqlite_sequence" VALUES ('Link', 6);
INSERT INTO "sqlite_sequence" VALUES ('Socket', 32);
INSERT INTO "sqlite_sequence" VALUES ('TRAY', 4);
INSERT INTO "sqlite_sequence" VALUES ('Tools', 17);
COMMIT;

-- ----------------------------
-- Auto increment value for Link
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 6 WHERE name = 'Link';

-- ----------------------------
-- Auto increment value for Socket
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 32 WHERE name = 'Socket';

-- ----------------------------
-- Auto increment value for TRAY
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 4 WHERE name = 'TRAY';

-- ----------------------------
-- Auto increment value for Tools
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 17 WHERE name = 'Tools';

PRAGMA foreign_keys = true;
