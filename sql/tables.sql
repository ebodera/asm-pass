
-- primary tables

-- TODO: surveys/polls need to be added

CREATE DATABASE IF NOT EXISTS apass;
USE apass;

CREATE TABLE IF NOT EXISTS Users (
    UserID CHAR(10) NOT NULL,
    FirstName     VARCHAR(50),
    LastName      VARCHAR(50),
    Email         VARCHAR(100),
    EntryDate     DATETIME,
    LastUpdated   DATETIME,
    LogicalDelete TINYINT NOT NULL,
    INDEX Users_1 (UserID, LogicalDelete),
    INDEX Users_2 (Email, LogicalDelete)
);

CREATE TABLE IF NOT EXISTS Events (
    EventID       CHAR(10) NOT NULL,
    Creator       CHAR(10) NOT NULL,
    Title         VARCHAR(250),
    Description   TEXT,
    StartDate     DATETIME,
    EndDate       DATETIME,
    EntryDate     DATETIME,
    LastUpdated   DATETIME,
    LogicalDelete TINYINT NOT NULL,
    INDEX Events_1 (EventID, LogicalDelete),
    INDEX Events_2 (Creator, LogicalDelete)
);

-- TODO: there is not much security
-- in the design at the moment
-- need to add web-tokens
-- and csrf to prevent abuse/ database-dos attacks

-- relational / secondary tables

CREATE TABLE IF NOT EXISTS rUserToEvent (
    UserID        CHAR(10) NOT NULL,
    EventID       CHAR(10) NOT NULL,
    Permission    TINYINT NOT NULL,
    Arrived       TINYINT NOT NULL,
    LogicalDelete TINYINT NOT NULL,
    INDEX rUserToEvent_1 (UserID, LogicalDelete, EventID),
    INDEX rUserToEvent_2 (EventID, LogicalDelete, Permission)
);
