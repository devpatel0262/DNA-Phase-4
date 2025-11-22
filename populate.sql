USE decentraland_db;

-- =======================================================
-- 1. POPULATE USERS (The Actors)
-- =======================================================

INSERT INTO User_Profile (Wallet_Address, Username, Join_Date, Last_Seen) VALUES
('0x1111111111111111111111111111111111111111', 'DCL_Foundation', '2017-08-18', '2025-11-19 08:00:00'),
('0x2222222222222222222222222222222222222222', 'Whale_Vault_ETH', '2018-12-01', '2025-11-18 22:45:00'),
('0x3333333333333333333333333333333333333333', 'Polygonal_Mind',  '2019-05-20', '2025-11-15 14:20:00'),
('0x4444444444444444444444444444444444444444', 'Ice_Poker_Host',  '2021-09-10', '2025-11-19 02:30:00'),
('0x5555555555555555555555555555555555555555', 'Samsung_HQ',      '2022-01-05', '2025-10-30 10:00:00'),
('0x6666666666666666666666666666666666666666', 'Snoop_Dogg_DCL',  '2021-09-20', '2025-11-18 16:20:00'),
('0x7777777777777777777777777777777777777777', 'Binance_US',      '2021-10-15', '2025-11-01 00:00:00'),
('0x8888888888888888888888888888888888888888', 'WonderMine_Game', '2020-05-05', '2025-11-19 10:00:00'),
('0x9999999999999999999999999999999999999999', 'Fashion_Mogul',   '2019-01-12', '2025-11-12 09:00:00'),
('0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'Governance_Whale','2017-12-12', '2025-11-19 11:00:00'),
('0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', 'Noob_Player_1',   '2025-11-15', '2025-11-19 12:00:00'),
('0xcccccccccccccccccccccccccccccccccccccccc', 'Inactive_User_X', '2018-01-01', '2020-01-01 00:00:00'),
('0xdddddddddddddddddddddddddddddddddddddddd', 'Asset_Less_User', '2025-11-01', '2025-11-19 15:30:00'),
('0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', 'Broke_Collector', '2024-06-15', '2025-11-18 20:10:00'); 

-- =======================================================
-- 2. POPULATE DIGITAL ASSETS (All Assets in One Place)
-- =======================================================

INSERT INTO Digital_Asset (Asset_ID, Token_URI, Owner_Address) VALUES
-- LAND Parcels
('LAND-000', 'https://api.decentraland.org/v2/parcels/0,0',     '0x1111111111111111111111111111111111111111'),
('LAND-100', 'https://api.decentraland.org/v2/parcels/-55,-10', '0x4444444444444444444444444444444444444444'),
('LAND-837', 'https://api.decentraland.org/v2/parcels/83,70',   '0x5555555555555555555555555555555555555555'),
('LAND-999', 'https://api.decentraland.org/v2/parcels/100,100', '0x2222222222222222222222222222222222222222'),
('LAND-001', 'https://api.decentraland.org/v2/parcels/12,45',   '0x6666666666666666666666666666666666666666'),
('LAND-002', 'https://api.decentraland.org/v2/parcels/-29,130', '0x8888888888888888888888888888888888888888'),
('LAND-003', 'https://api.decentraland.org/v2/parcels/50,50',   '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
('LAND-004', 'https://api.decentraland.org/v2/parcels/50,51',   '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
('LAND-005', 'https://api.decentraland.org/v2/parcels/75,25',   '0x7777777777777777777777777777777777777777'),
('LAND-006', 'https://api.decentraland.org/v2/parcels/-100,-100', '0x9999999999999999999999999999999999999999'),

-- Wearables
('WEAR-001', 'https://api.decentraland.org/v2/wearables/razor_blade',  '0x3333333333333333333333333333333333333333'),
('WEAR-002', 'https://api.decentraland.org/v2/wearables/cyber_helmet', '0x2222222222222222222222222222222222222222'),
('WEAR-003', 'https://api.decentraland.org/v2/wearables/golden_wings', '0x9999999999999999999999999999999999999999'),
('WEAR-004', 'https://api.decentraland.org/v2/wearables/atari_shirt',  '0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'),
('WEAR-005', 'https://api.decentraland.org/v2/wearables/ghost_cape',   '0xcccccccccccccccccccccccccccccccccccccccc');

-- =======================================================
-- 3. POPULATE SUBCLASSES
-- =======================================================

-- =======================================================
-- 3. POPULATE LAND PARCELS (All Land in One Place)
-- =======================================================

INSERT INTO LAND_Parcel (Asset_ID, X_Coordinate, Y_Coordinate, District_Name) VALUES
('LAND-000', 0, 0, NULL),
('LAND-100', -55, -10, 'Vegas City'),
('LAND-837', 83, 70, 'Fashion Street'),
('LAND-999', 100, 100, 'Dragon City'),
('LAND-001', 12, 45, NULL),
('LAND-002', -29, 130, 'Gaming Plaza'),
('LAND-003', 50, 50, 'Aetheria'),
('LAND-004', 50, 51, 'Aetheria'),
('LAND-005', 75, 25, NULL),
('LAND-006', -100, -100, 'Outskirts');

-- =======================================================
-- 4. POPULATE WEARABLES (All Wearables in One Place)  
-- =======================================================

INSERT INTO Wearable (Asset_ID, Category, Rarity) VALUES
('WEAR-001', 'Upper_Body', 'Epic'),
('WEAR-002', 'Helmet', 'Legendary'),
('WEAR-003', 'Back', 'Mythic'),
('WEAR-004', 'Upper_Body', 'Common'),
('WEAR-005', 'Back', 'Rare');

-- =======================================================
-- 4. POPULATE GOVERNANCE
-- =======================================================
-- 8. POPULATE DAO PROPOSALS (All Proposals in One Place)
-- =======================================================

INSERT INTO DAO_Proposal (Proposal_ID, Title, Status, Creator_Address) VALUES
('PROP-101', 'Add Point of Interest: Samsung 837X', 'Passed', '0x5555555555555555555555555555555555555555'),
('PROP-102', 'Grant Request: Community Radio', 'Rejected', '0x3333333333333333333333333333333333333333'),
('PROP-103', 'Lower Marketplace Publication Fees', 'Active', '0x2222222222222222222222222222222222222222'),
('PROP-104', 'Ban Offensive Names List Update', 'Active', '0x1111111111111111111111111111111111111111'),
('PROP-105', 'Historic Proposal from 2019', 'Enacted', '0x2222222222222222222222222222222222222222'),
('PROP-106', 'Failed Community Proposal', 'Rejected', '0xdddddddddddddddddddddddddddddddddddddddd');

-- =======================================================
-- 9. POPULATE VOTES (All Votes in One Place)
-- =======================================================

INSERT INTO Vote (Proposal_ID, Voter_Address, Vote_Choice, Voting_Weight, Timestamp) VALUES
('PROP-103', '0x2222222222222222222222222222222222222222', 'For', 2500000.00000000, '2025-11-10 09:00:00'),
('PROP-103', '0x3333333333333333333333333333333333333333', 'Against', 5000.00000000, '2025-11-11 10:30:00'),
('PROP-101', '0x1111111111111111111111111111111111111111', 'For', 10000000.00000000, '2025-01-15 08:00:00'),
('PROP-104', '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'For', 5000000.00000000, '2025-11-19 09:00:00'),
('PROP-104', '0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', 'For', 100.00000000, '2025-11-19 12:30:00'),
('PROP-105', '0x1111111111111111111111111111111111111111', 'For', 15000000.00000000, '2019-04-01 10:00:00'),
('PROP-105', '0x2222222222222222222222222222222222222222', 'For', 8000000.00000000, '2019-04-02 11:30:00'),
('PROP-106', '0xdddddddddddddddddddddddddddddddddddddddd', 'For', 1.00000000, '2025-11-18 14:00:00'),
('PROP-106', '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'Against', 7500000.00000000, '2025-11-18 15:00:00');

-- =======================================================
-- 5. POPULATE BUSINESS & CONTENT
-- =======================================================

INSERT INTO Business (Business_Name, Business_Type, Date_Established, Owner_Address, Parcel_ID) VALUES
('ICE Poker Lounge', 'Shop', '2021-10-01', '0x4444444444444444444444444444444444444444', 'LAND-100'),
('Samsung 837X Experience', 'Gallery', '2022-01-06', '0x5555555555555555555555555555555555555555', 'LAND-837'),
('Polygonal Studio HQ', 'Service', '2020-03-15', '0x3333333333333333333333333333333333333333', 'LAND-999'),
('Snoop Dogg Mansion', 'Venue', '2021-09-25', '0x6666666666666666666666666666666666666666', 'LAND-001'),
('WonderMine Crafting', 'Shop', '2020-06-01', '0x8888888888888888888888888888888888888888', 'LAND-002'),
('ICE Poker VIP Room', 'Venue', '2022-03-15', '0x4444444444444444444444444444444444444444', 'LAND-003'),
('Samsung 837Y Gallery', 'Gallery', '2023-01-01', '0x5555555555555555555555555555555555555555', 'LAND-004'),
('Abandoned Nightclub', 'Venue', '2018-05-10', NULL, 'LAND-005'),
('Ghost Mall', 'Shop', '2019-01-01', NULL, 'LAND-006');

-- Scene Content
INSERT INTO Scene_Content (Parcel_ID, Scene_Version, Description, Deployment_Date, Creator_Address) VALUES
('LAND-100', 'v4.2.0', 'Stronghold Casino Interior with Blackjack', '2025-05-20', '0x4444444444444444444444444444444444444444'),
('LAND-837', 'v1.0.0', 'Sustainability Forest and NFT Quest', '2022-01-06', '0x5555555555555555555555555555555555555555'),
('LAND-000', 'v55.0', 'Genesis Plaza Spawning Point', '2020-02-20', '0x1111111111111111111111111111111111111111'),
('LAND-001', 'v2.1', 'Snoop Mansion Party House', '2025-01-01', '0x6666666666666666666666666666666666666666'),
('LAND-002', 'v3.0', 'Asteroid Mining Game Loop', '2024-08-10', '0x8888888888888888888888888888888888888888'),
('LAND-100', 'v5.0.0', 'Updated Casino with VR Tables', '2025-10-15', '0x4444444444444444444444444444444444444444'),
('LAND-837', 'v2.0.0', 'Expanded Samsung Experience Hall', '2024-05-01', '0x5555555555555555555555555555555555555555'),
('LAND-000', 'v56.0', 'Genesis Plaza Holiday Theme', '2025-12-01', NULL),
('LAND-999', 'v1.0.0', 'Original Polygonal Studio', '2019-03-01', '0x3333333333333333333333333333333333333333');

-- =======================================================
-- 6. POPULATE EVENTS & ATTENDANCE
-- =======================================================

INSERT INTO Event (Event_Name, Start_Timestamp, End_Timestamp, Organizer_Address, Business_ID, Scene_Parcel_ID, Scene_Version) VALUES
('Metaverse Fashion Week 2025', '2025-03-24 10:00:00', '2025-03-28 22:00:00', '0x5555555555555555555555555555555555555555', 2, 'LAND-837', 'v1.0.0'),
('ICE Poker Daily Tournament', '2025-11-20 18:00:00', '2025-11-20 20:00:00', '0x4444444444444444444444444444444444444444', 1, 'LAND-100', 'v4.2.0'),
('Snoop Dogg Live Concert', '2025-11-25 20:00:00', '2025-11-25 22:00:00', '0x6666666666666666666666666666666666666666', 4, 'LAND-001', 'v2.1'),
('Community Genesis Meetup', '2025-12-01 19:00:00', '2025-12-01 21:00:00', '0x1111111111111111111111111111111111111111', NULL, 'LAND-000', 'v55.0'),
('Blockchain Developer Workshop', '2020-06-15 14:00:00', '2020-06-15 18:00:00', '0x3333333333333333333333333333333333333333', NULL, 'LAND-002', 'v3.0'),
('Genesis City Launch Party', '2017-12-01 20:00:00', '2017-12-01 23:59:00', '0x1111111111111111111111111111111111111111', NULL, 'LAND-000', 'v55.0'),
('Early Adopter Meetup 2019', '2019-03-20 16:00:00', '2019-03-20 18:00:00', '0x2222222222222222222222222222222222222222', 3, 'LAND-999', 'v1.0.0');

-- Tags
INSERT INTO Event_Tags (Event_ID, Tag) VALUES
(1, 'Fashion'), (1, 'Wearables'), (1, 'Live Music'),
(2, 'Gambling'), (2, 'PlayToEarn'), (2, 'Poker'),
(3, 'Concert'), (3, 'Party'), (3, 'VIP'),
(4, 'Community'), (4, 'Networking'), (4, 'Genesis'),
(5, 'Developer'), (5, 'Workshop'), (5, 'Blockchain'),
(6, 'Launch'), (6, 'Historic'), (6, 'Celebration'),
(7, 'Early Adopter'), (7, 'Meetup'), (7, 'Legacy');

-- Attendance
INSERT INTO ATTENDS (Wallet_Address, Event_ID) VALUES
('0x2222222222222222222222222222222222222222', 1),
('0x3333333333333333333333333333333333333333', 1),
('0x9999999999999999999999999999999999999999', 1),
('0x2222222222222222222222222222222222222222', 2),
('0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', 3),
('0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 3),
('0x4444444444444444444444444444444444444444', 4),
('0x5555555555555555555555555555555555555555', 4),
('0x6666666666666666666666666666666666666666', 4),
('0x8888888888888888888888888888888888888888', 5),
('0x3333333333333333333333333333333333333333', 5),
('0x1111111111111111111111111111111111111111', 6),
('0x2222222222222222222222222222222222222222', 7);

-- =======================================================
-- 7. POPULATE TRANSACTIONS
-- =======================================================

INSERT INTO Transaction (Transaction_ID, Timestamp, Price, Currency, Asset_ID, Seller_Address, Buyer_Address) VALUES
('0xaaaa0000aaaa0000aaaa0000aaaa0000aaaa0000aaaa0000aaaa0000123456', '2025-09-20 15:00:00', 150000.00000000, 'MANA', 'LAND-837', '0x2222222222222222222222222222222222222222', '0x5555555555555555555555555555555555555555'),
('0xbbbb0000bbbb0000bbbb0000bbbb0000bbbb0000bbbb0000bbbb0000123456', '2025-10-05 12:30:00', 500.00000000, 'MANA', 'WEAR-002', '0x3333333333333333333333333333333333333333', '0x2222222222222222222222222222222222222222'),
('0xcccc0000cccc0000cccc0000cccc0000cccc0000cccc0000cccc0000123456', '2025-11-16 10:00:00', 5.00000000, 'MANA', 'WEAR-004', '0x3333333333333333333333333333333333333333', '0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'),
('0xdddd0000dddd0000dddd0000dddd0000dddd0000dddd0000dddd0000123456', '2025-09-01 18:45:00', 1200.00000000, 'MANA', 'WEAR-003', '0x2222222222222222222222222222222222222222', '0x9999999999999999999999999999999999999999'),
('0xeeee1111eeee1111eeee1111eeee1111eeee1111eeee1111eeee1111123456', '2024-06-15 09:30:00', 45.50000000, 'ETH', 'LAND-003', '0x1111111111111111111111111111111111111111', '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
('0xffff2222ffff2222ffff2222ffff2222ffff2222ffff2222ffff2222123456', '2023-12-01 16:20:00', 12.75000000, 'ETH', 'LAND-004', '0x7777777777777777777777777777777777777777', '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
('0x1122334455667788990011223344556677889900112233445566778899', '2019-03-15 11:00:00', 25000.00000000, 'MANA', 'LAND-999', '0x1111111111111111111111111111111111111111', '0x2222222222222222222222222222222222222222'),
('0x2233445566778899001122334455667788990011223344556677889900', '2020-08-22 14:45:00', 850.00000000, 'MANA', 'WEAR-001', '0x1111111111111111111111111111111111111111', '0x3333333333333333333333333333333333333333'),
('0x3344556677889900112233445566778899001122334455667788990011', '2025-10-15 14:20:00', 32000.00000000, 'MANA', 'LAND-005', '0x1111111111111111111111111111111111111111', '0x7777777777777777777777777777777777777777'),
('0x4455667788990011223344556677889900112233445566778899001122', '2025-09-22 16:45:00', 18.75000000, 'ETH', 'LAND-006', '0x8888888888888888888888888888888888888888', '0x9999999999999999999999999999999999999999');
