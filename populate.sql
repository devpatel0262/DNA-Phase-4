USE decentraland_db;

-- =======================================================
-- 1. POPULATE USERS (The Actors)
-- =======================================================
-- 12 Users representing different segments:
-- Foundation, Whales, Creators, Business Owners, Active Gamers, Inactive Users

INSERT INTO User_Profile (Wallet_Address, Username, Join_Date, Last_Seen) VALUES
('0x1111111111111111111111111111111111111111', 'DCL_Foundation', '2017-08-18', '2025-11-19 08:00:00'),
('0x2222222222222222222222222222222222222222', 'Whale_Vault_ETH', '2018-12-01', '2025-11-18 22:45:00'),
('0x3333333333333333333333333333333333333333', 'Polygonal_Mind',  '2019-05-20', '2025-11-15 14:20:00'),
('0x4444444444444444444444444444444444444444', 'Ice_Poker_Host',  '2021-09-10', '2025-11-19 02:30:00'),
('0x5555555555555555555555555555555555555555', 'Samsung_HQ',      '2022-01-05', '2025-10-30 10:00:00'),
('0x6666666666666666666666666666666666666666', 'Snoop_Dogg_DCL',  '2021-09-20', '2025-11-18 16:20:00'), -- Celebrity Partner
('0x7777777777777777777777777777777777777777', 'Binance_US',      '2021-10-15', '2025-11-01 00:00:00'), -- Corporate
('0x8888888888888888888888888888888888888888', 'WonderMine_Game', '2020-05-05', '2025-11-19 10:00:00'), -- Game Studio
('0x9999999999999999999999999999999999999999', 'Fashion_Mogul',   '2019-01-12', '2025-11-12 09:00:00'), -- Wearable Collector
('0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'Governance_Whale','2017-12-12', '2025-11-19 11:00:00'), -- DAO Politician
('0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', 'Noob_Player_1',   '2025-11-15', '2025-11-19 12:00:00'), -- New User
('0xcccccccccccccccccccccccccccccccccccccccc', 'Inactive_User_X', '2018-01-01', '2020-01-01 00:00:00'); -- For "Abandoned" tests

-- =======================================================
-- 2. POPULATE ASSETS (Superclass)
-- =======================================================
-- Added more LAND for Whales to skew the "Influence Report"

INSERT INTO Digital_Asset (Asset_ID, Token_URI, Owner_Address) VALUES
-- LAND Parcels
('LAND-000', 'https://api.decentraland.org/v2/parcels/0,0',     '0x1111111111111111111111111111111111111111'),
('LAND-100', 'https://api.decentraland.org/v2/parcels/-55,-10', '0x4444444444444444444444444444444444444444'),
('LAND-837', 'https://api.decentraland.org/v2/parcels/83,70',   '0x5555555555555555555555555555555555555555'),
('LAND-999', 'https://api.decentraland.org/v2/parcels/100,100', '0x2222222222222222222222222222222222222222'),
('LAND-001', 'https://api.decentraland.org/v2/parcels/12,45',   '0x6666666666666666666666666666666666666666'), -- Snoop's Land
('LAND-002', 'https://api.decentraland.org/v2/parcels/-29,130', '0x8888888888888888888888888888888888888888'), -- WonderMine Land
('LAND-003', 'https://api.decentraland.org/v2/parcels/50,50',   '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'), -- Gov Whale Land 1
('LAND-004', 'https://api.decentraland.org/v2/parcels/50,51',   '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'), -- Gov Whale Land 2

-- Wearables
('WEAR-001', 'https://api.decentraland.org/v2/wearables/razor_blade',  '0x3333333333333333333333333333333333333333'),
('WEAR-002', 'https://api.decentraland.org/v2/wearables/cyber_helmet', '0x2222222222222222222222222222222222222222'),
('WEAR-003', 'https://api.decentraland.org/v2/wearables/golden_wings', '0x9999999999999999999999999999999999999999'), -- Fashion Mogul
('WEAR-004', 'https://api.decentraland.org/v2/wearables/atari_shirt',  '0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'); -- New Player bought this

-- =======================================================
-- 3. POPULATE SUBCLASSES
-- =======================================================

-- LAND_Parcel
INSERT INTO LAND_Parcel (Asset_ID, X_Coordinate, Y_Coordinate, District_Name) VALUES
('LAND-000', 0, 0, NULL),
('LAND-100', -55, -10, 'Vegas City'),
('LAND-837', 83, 70, 'Fashion Street'),
('LAND-999', 100, 100, 'Dragon City'),
('LAND-001', 12, 45, NULL),             -- Snoopverse (Private Estate)
('LAND-002', -29, 130, 'Gaming Plaza'), -- WonderMine
('LAND-003', 50, 50, 'Aetheria'),
('LAND-004', 50, 51, 'Aetheria');

-- Wearable
INSERT INTO Wearable (Asset_ID, Category, Rarity) VALUES
('WEAR-001', 'Upper_Body', 'Epic'),
('WEAR-002', 'Helmet', 'Legendary'),
('WEAR-003', 'Back', 'Mythic'),
('WEAR-004', 'Upper_Body', 'Common');

-- =======================================================
-- 4. POPULATE GOVERNANCE
-- =======================================================

INSERT INTO DAO_Proposal (Proposal_ID, Title, Status, Creator_Address) VALUES
('PROP-101', 'Add Point of Interest: Samsung 837X', 'Passed', '0x5555555555555555555555555555555555555555'),
('PROP-102', 'Grant Request: Community Radio', 'Rejected', '0x3333333333333333333333333333333333333333'),
('PROP-103', 'Lower Marketplace Publication Fees', 'Active', '0x2222222222222222222222222222222222222222'),
('PROP-104', 'Ban Offensive Names List Update', 'Active', '0x1111111111111111111111111111111111111111');

-- Votes
-- Demonstrating "Influence": Gov Whale has huge weight, Noob has tiny weight.
INSERT INTO Vote (Proposal_ID, Voter_Address, Vote_Choice, Voting_Weight, Timestamp) VALUES
('PROP-103', '0x2222222222222222222222222222222222222222', 'For', 2500000.00000000, '2025-11-10 09:00:00'),
('PROP-103', '0x3333333333333333333333333333333333333333', 'Against', 5000.00000000, '2025-11-11 10:30:00'),
('PROP-101', '0x1111111111111111111111111111111111111111', 'For', 10000000.00000000, '2025-01-15 08:00:00'),
('PROP-104', '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'For', 5000000.00000000, '2025-11-19 09:00:00'),
('PROP-104', '0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', 'For', 100.00000000, '2025-11-19 12:30:00'); -- Noob voting

-- =======================================================
-- 5. POPULATE BUSINESS & CONTENT
-- =======================================================

INSERT INTO Business (Business_Name, Business_Type, Date_Established, Owner_Address, Parcel_ID) VALUES
('ICE Poker Lounge', 'Shop', '2021-10-01', '0x4444444444444444444444444444444444444444', 'LAND-100'),
('Samsung 837X Experience', 'Gallery', '2022-01-06', '0x5555555555555555555555555555555555555555', 'LAND-837'),
('Polygonal Studio HQ', 'Service', '2020-03-15', '0x3333333333333333333333333333333333333333', 'LAND-999'),
('Snoop Dogg Mansion', 'Venue', '2021-09-25', '0x6666666666666666666666666666666666666666', 'LAND-001'),
('WonderMine Crafting', 'Shop', '2020-06-01', '0x8888888888888888888888888888888888888888', 'LAND-002');

-- Scene Content
INSERT INTO Scene_Content (Parcel_ID, Scene_Version, Description, Deployment_Date, Creator_Address) VALUES
('LAND-100', 'v4.2.0', 'Stronghold Casino Interior with Blackjack', '2025-05-20', '0x4444444444444444444444444444444444444444'),
('LAND-837', 'v1.0.0', 'Sustainability Forest and NFT Quest', '2022-01-06', '0x5555555555555555555555555555555555555555'),
('LAND-000', 'v55.0', 'Genesis Plaza Spawning Point', '2020-02-20', '0x1111111111111111111111111111111111111111'),
('LAND-001', 'v2.1', 'Snoop Mansion Party House', '2025-01-01', '0x6666666666666666666666666666666666666666'),
('LAND-002', 'v3.0', 'Asteroid Mining Game Loop', '2024-08-10', '0x8888888888888888888888888888888888888888');

-- =======================================================
-- 6. POPULATE EVENTS & ATTENDANCE
-- =======================================================

INSERT INTO Event (Event_Name, Start_Timestamp, End_Timestamp, Organizer_Address, Business_ID, Scene_Parcel_ID, Scene_Version) VALUES
('Metaverse Fashion Week 2025', '2025-03-24 10:00:00', '2025-03-28 22:00:00', '0x5555555555555555555555555555555555555555', 2, 'LAND-837', 'v1.0.0'),
('ICE Poker Daily Tournament', '2025-11-20 18:00:00', '2025-11-20 20:00:00', '0x4444444444444444444444444444444444444444', 1, 'LAND-100', 'v4.2.0'),
('Snoop Dogg Live Concert', '2025-11-25 20:00:00', '2025-11-25 22:00:00', '0x6666666666666666666666666666666666666666', 4, 'LAND-001', 'v2.1');

-- Tags
INSERT INTO Event_Tags (Event_ID, Tag) VALUES
(1, 'Fashion'), (1, 'Wearables'), (1, 'Live Music'),
(2, 'Gambling'), (2, 'PlayToEarn'), (2, 'Poker'),
(3, 'Concert'), (3, 'Party'), (3, 'VIP');

-- Attendance
INSERT INTO ATTENDS (Wallet_Address, Event_ID) VALUES
('0x2222222222222222222222222222222222222222', 1), -- Whale -> Fashion
('0x3333333333333333333333333333333333333333', 1), -- Creator -> Fashion
('0x9999999999999999999999999999999999999999', 1), -- Fashion Mogul -> Fashion
('0x2222222222222222222222222222222222222222', 2), -- Whale -> Poker
('0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', 3), -- Noob -> Snoop Concert
('0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 3); -- Gov Whale -> Snoop Concert

-- =======================================================
-- 7. POPULATE TRANSACTIONS
-- =======================================================
-- Added variety: Big land sales, small wearable sales

INSERT INTO Transaction (Transaction_ID, Timestamp, Price, Currency, Asset_ID, Seller_Address, Buyer_Address) VALUES
-- Samsung bought Land from Whale
('0xaaaa0000aaaa0000aaaa0000aaaa0000aaaa0000aaaa0000aaaa0000123456', '2021-12-20 15:00:00', 150000.00000000, 'MANA', 'LAND-837', '0x2222222222222222222222222222222222222222', '0x5555555555555555555555555555555555555555'),
-- Creator sold a wearable to the Whale
('0xbbbb0000bbbb0000bbbb0000bbbb0000bbbb0000bbbb0000bbbb0000123456', '2025-10-05 12:30:00', 500.00000000, 'MANA', 'WEAR-002', '0x3333333333333333333333333333333333333333', '0x2222222222222222222222222222222222222222'),
-- Noob bought a cheap shirt from Market
('0xcccc0000cccc0000cccc0000cccc0000cccc0000cccc0000cccc0000123456', '2025-11-16 10:00:00', 5.00000000, 'MANA', 'WEAR-004', '0x3333333333333333333333333333333333333333', '0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'),
-- Fashion Mogul buying rare wings
('0xdddd0000dddd0000dddd0000dddd0000dddd0000dddd0000dddd0000123456', '2025-09-01 18:45:00', 1200.00000000, 'MANA', 'WEAR-003', '0x2222222222222222222222222222222222222222', '0x9999999999999999999999999999999999999999');