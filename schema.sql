DROP DATABASE IF EXISTS decentraland_db;
CREATE DATABASE decentraland_db;
USE decentraland_db;

CREATE TABLE User_Profile
(
    Wallet_Address CHAR(42) PRIMARY KEY, -- Fixed length for Ethereum addresses
    Username VARCHAR(50) NOT NULL UNIQUE,
    Join_Date DATE NOT NULL,
    Last_Seen TIMESTAMP NULL, -- Can be NULL if user created but never logged in
    
    CONSTRAINT Wallet_Address_Format CHECK (Wallet_Address LIKE '0x%')
);

CREATE TABLE Digital_Asset
(
    Asset_ID VARCHAR(50) PRIMARY KEY,
    Token_URI VARCHAR(255) NOT NULL,
    Owner_Address CHAR(42) NOT NULL,
    
    CONSTRAINT Token_URI_Format CHECK (Token_URI LIKE 'http%'),
    
    FOREIGN KEY (Owner_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);

CREATE TABLE LAND_Parcel (
    Asset_ID VARCHAR(50) PRIMARY KEY,
    X_Coordinate INT NOT NULL,
    Y_Coordinate INT NOT NULL,
    District_Name VARCHAR(255) NULL,  -- District can be NULL if a parcel is not part of any district
    
    FOREIGN KEY (Asset_ID) REFERENCES Digital_Asset(Asset_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    UNIQUE (X_Coordinate, Y_Coordinate)
);

CREATE TABLE Wearable
(
    Asset_ID VARCHAR(50) PRIMARY KEY,
    Category VARCHAR(50) NOT NULL, 
    Rarity VARCHAR(50) NOT NULL,
    
    FOREIGN KEY (Asset_ID) REFERENCES Digital_Asset(Asset_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE DAO_Proposal
(
    Proposal_ID VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Status VARCHAR(8) NOT NULL,
    Creator_Address CHAR(42) NOT NULL,
    
    CONSTRAINT Proposal_Status_Domain CHECK (Status IN ('Active', 'Passed', 'Rejected', 'Enacted')),
    
    FOREIGN KEY (Creator_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Business
(
    Business_ID INT AUTO_INCREMENT PRIMARY KEY,
    Business_Name VARCHAR(255) NOT NULL,
    Business_Type VARCHAR(7) NOT NULL,
    Date_Established DATE NOT NULL,
    Owner_Address CHAR(42) NULL,
    Parcel_ID VARCHAR(50) NOT NULL,
    
    CONSTRAINT Business_Type_Domain CHECK (Business_Type IN ('Shop', 'Gallery', 'Venue', 'Service')),
    
    FOREIGN KEY (Owner_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
        
    FOREIGN KEY (Parcel_ID) REFERENCES LAND_Parcel(Asset_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE Scene_Content
(
    Parcel_ID VARCHAR(50) NOT NULL,
    Scene_Version VARCHAR(64) NOT NULL, 
    Description VARCHAR(255) NULL, -- Creator can choose to leave description empty
    Deployment_Date DATE NOT NULL,
    Creator_Address CHAR(42) NULL,
    
    PRIMARY KEY (Parcel_ID, Scene_Version),
    
    FOREIGN KEY (Parcel_ID) REFERENCES LAND_Parcel(Asset_ID)
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
        
    FOREIGN KEY (Creator_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE Transaction
(
    Transaction_ID CHAR(66) PRIMARY KEY, -- Blockchain transaction hashes are standard 66 chars
    Timestamp TIMESTAMP NOT NULL,
    Price DECIMAL(20, 10) NOT NULL, 
    Currency VARCHAR(4) NOT NULL,
    Asset_ID VARCHAR(50) NULL, 
    Seller_Address CHAR(42) NULL,
    Buyer_Address CHAR(42) NULL,
    
    CONSTRAINT Positive_Price CHECK (Price > 0),
    CONSTRAINT Currency_Domain CHECK (Currency IN ('MANA', 'ETH')),
    
    FOREIGN KEY (Asset_ID) REFERENCES Digital_Asset(Asset_ID)
        ON DELETE SET NULL,
    FOREIGN KEY (Seller_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE SET NULL,
    FOREIGN KEY (Buyer_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE SET NULL
);

CREATE TABLE Event (
    Event_ID INT AUTO_INCREMENT PRIMARY KEY,
    Event_Name VARCHAR(255) NOT NULL,
    Start_Timestamp TIMESTAMP NOT NULL,
    End_Timestamp TIMESTAMP NOT NULL,
    Organizer_Address CHAR(42) NULL,
    Business_ID INT NULL, 
    Scene_Parcel_ID VARCHAR(50),
    Scene_Version VARCHAR(64),
    
    CONSTRAINT Valid_Endtime_Check CHECK (End_Timestamp > Start_Timestamp),
    
    FOREIGN KEY (Organizer_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE SET NULL,
        
    FOREIGN KEY (Business_ID) REFERENCES Business(Business_ID)
        ON DELETE SET NULL,
        
    FOREIGN KEY (Scene_Parcel_ID, Scene_Version) 
        REFERENCES Scene_Content(Parcel_ID, Scene_Version)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE Vote
(
    Proposal_ID VARCHAR(50) NOT NULL,
    Voter_Address CHAR(42) NOT NULL,
    Vote_Choice VARCHAR(7) NOT NULL, 
    Voting_Weight DECIMAL(20, 10) NOT NULL,
    Timestamp TIMESTAMP NOT NULL,
    
    PRIMARY KEY (Proposal_ID, Voter_Address),
    
    CONSTRAINT Vote_Choice_Domain CHECK (Vote_Choice IN ('For', 'Against')),
    CONSTRAINT Vote_Weight_Positive CHECK (Voting_Weight > 0),
    
    FOREIGN KEY (Proposal_ID) REFERENCES DAO_Proposal(Proposal_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (Voter_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE CASCADE
);

CREATE TABLE ATTENDS
(
    Wallet_Address CHAR(42) NOT NULL,
    Event_ID INT NOT NULL,
    
    PRIMARY KEY (Wallet_Address, Event_ID),
    
    FOREIGN KEY (Wallet_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE CASCADE, 
        
    FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
        ON DELETE RESTRICT 
);

CREATE TABLE Event_Tags
(
    Event_ID INT NOT NULL,
    Tag VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (Event_ID, Tag),
    
    FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
        ON DELETE CASCADE
);