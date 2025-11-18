DROP DATABASE IF EXISTS decentraland_db;
CREATE DATABASE decentraland_db;
USE decentraland_db;

CREATE TABLE User_Profile
(
    Wallet_Address VARCHAR(42) PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Join_Date DATE NOT NULL,
    Last_Seen TIMESTAMP NULL, -- Can be NULL if user created but never logged in
    CONSTRAINT chk_wallet_format CHECK (Wallet_Address LIKE '0x%')
);

CREATE TABLE Digital_Asset
(
    Asset_ID VARCHAR(50) PRIMARY KEY,
    Token_URI VARCHAR(255) NOT NULL,
    Owner_Address VARCHAR(42) NOT NULL,
    
    CONSTRAINT chk_token_uri CHECK (Token_URI LIKE 'http%'),
    
    FOREIGN KEY (Owner_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE RESTRICT -- Assets are valuable; prevent deleting user if they still own assets [cite: 242]
        ON UPDATE CASCADE
);

-- ==========================================
-- LEVEL 2: Subclasses
-- ==========================================

CREATE TABLE LAND_Parcel (
    Asset_ID VARCHAR(50) PRIMARY KEY,
    X_Coordinate INT NOT NULL,
    Y_Coordinate INT NOT NULL,
    District_Name VARCHAR(100) NULL, -- Nullable: Not all land is in a named district 
    
    FOREIGN KEY (Asset_ID) REFERENCES Digital_Asset(Asset_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    UNIQUE (X_Coordinate, Y_Coordinate)
);

CREATE TABLE Wearable (
    Asset_ID VARCHAR(50) PRIMARY KEY,
    Category VARCHAR(50) NOT NULL, 
    Rarity VARCHAR(50) NOT NULL,
    
    FOREIGN KEY (Asset_ID) REFERENCES Digital_Asset(Asset_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE DAO_Proposal (
    Proposal_ID VARCHAR(50) PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'Active',
    Creator_Address VARCHAR(42) NOT NULL, -- Creator must exist
    
    CONSTRAINT chk_proposal_status CHECK (Status IN ('Active', 'Passed', 'Rejected', 'Enacted')),
    
    -- Rule: If User is deleted, their proposals are deleted 
    FOREIGN KEY (Creator_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ==========================================
-- LEVEL 3: Complex Entities
-- ==========================================

CREATE TABLE Business (
    Business_ID INT AUTO_INCREMENT PRIMARY KEY,
    Business_Name VARCHAR(255) NOT NULL,
    Business_Type VARCHAR(50),
    Date_Established DATE,
    Owner_Address VARCHAR(42) NULL, -- Nullable to allow "Abandoned" state 
    Parcel_ID VARCHAR(50) NOT NULL,
    
    CONSTRAINT chk_biz_type CHECK (Business_Type IN ('Shop', 'Gallery', 'Venue', 'Service')),
    
    -- Rule: If User deleted, set owner to NULL (Abandoned) 
    FOREIGN KEY (Owner_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
        
    FOREIGN KEY (Parcel_ID) REFERENCES LAND_Parcel(Asset_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE Scene_Content (
    Parcel_ID VARCHAR(50) NOT NULL,
    Scene_Version VARCHAR(20) NOT NULL, 
    Description VARCHAR(255) NULL, -- Description is optional
    Deployment_Date DATE NOT NULL,
    Creator_Address VARCHAR(42) NULL, -- If creator leaves, scene can stay
    
    PRIMARY KEY (Parcel_ID, Scene_Version),
    
    -- Rule: Scene cannot exist without the land [cite: 127]
    FOREIGN KEY (Parcel_ID) REFERENCES LAND_Parcel(Asset_ID)
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
        
    FOREIGN KEY (Creator_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE Transaction (
    Transaction_ID VARCHAR(50) PRIMARY KEY,
    Timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Price DECIMAL(18, 8) NOT NULL, 
    Currency VARCHAR(10) NOT NULL,
    Asset_ID VARCHAR(50) NULL, -- Keep record even if asset is burned/deleted
    Seller_Address VARCHAR(42) NULL, -- Keep record even if user deleted
    Buyer_Address VARCHAR(42) NULL,  -- Keep record even if user deleted
    
    CONSTRAINT chk_price_pos CHECK (Price > 0),
    CONSTRAINT chk_currency CHECK (Currency IN ('MANA', 'ETH')),
    
    FOREIGN KEY (Asset_ID) REFERENCES Digital_Asset(Asset_ID)
        ON DELETE SET NULL,
    -- Rule: Preserve financial history even if users are deleted 
    FOREIGN KEY (Seller_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE SET NULL,
    FOREIGN KEY (Buyer_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE SET NULL
);

-- ==========================================
-- LEVEL 4: Events & Mapping
-- ==========================================

CREATE TABLE Event (
    Event_ID INT AUTO_INCREMENT PRIMARY KEY,
    Event_Name VARCHAR(255) NOT NULL,
    Start_Timestamp TIMESTAMP NOT NULL,
    End_Timestamp TIMESTAMP NOT NULL,
    Organizer_Address VARCHAR(42) NULL, -- Event can persist if organizer leaves
    Business_ID INT NULL, -- Event might not be linked to a business
    Scene_Parcel_ID VARCHAR(50),
    Scene_Version VARCHAR(20),
    
    CONSTRAINT chk_event_time CHECK (End_Timestamp > Start_Timestamp),
    
    FOREIGN KEY (Organizer_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE SET NULL,
        
    FOREIGN KEY (Business_ID) REFERENCES Business(Business_ID)
        ON DELETE SET NULL,
        
    FOREIGN KEY (Scene_Parcel_ID, Scene_Version) 
        REFERENCES Scene_Content(Parcel_ID, Scene_Version)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE Vote (
    Proposal_ID VARCHAR(50) NOT NULL,
    Voter_Address VARCHAR(42) NOT NULL,
    Vote_Choice VARCHAR(50) NOT NULL, 
    Voting_Weight DECIMAL(18, 8) NOT NULL, 
    Timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (Proposal_ID, Voter_Address),
    
    CONSTRAINT chk_vote_choice CHECK (Vote_Choice IN ('For', 'Against')),
    CONSTRAINT chk_vote_weight CHECK (Voting_Weight > 0),
    
    -- Rule: If Proposal or User is deleted, the vote is deleted 
    FOREIGN KEY (Proposal_ID) REFERENCES DAO_Proposal(Proposal_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (Voter_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE CASCADE
);

CREATE TABLE ATTENDS (
    Wallet_Address VARCHAR(42) NOT NULL,
    Event_ID INT NOT NULL,
    
    PRIMARY KEY (Wallet_Address, Event_ID),
    
    FOREIGN KEY (Wallet_Address) REFERENCES User_Profile(Wallet_Address)
        ON DELETE CASCADE, -- If user is gone, their attendance record goes
        
    FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
        ON DELETE RESTRICT -- Prevent deleting event if there is attendance history
);

CREATE TABLE Event_Tags (
    Event_ID INT NOT NULL,
    Tag VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (Event_ID, Tag),
    
    FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
        ON DELETE CASCADE
);