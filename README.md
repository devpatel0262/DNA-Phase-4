# Mini World - Decentraland

## Prerequisites
- Python 3.x
- MySQL Server
- `pymysql` library (`pip install pymysql`)
- `tkinter` (usually included with Python)
- Do `python3 -m pip install -r requirements.txt`

## Setup Instructions
1. **Database Setup**:
   - Run `schema.sql` to create the database and tables.
   - Run `populate.sql` to insert the initial dataset.
   
   ```bash
   mysql -u root -p < schema.sql
   mysql -u root -p < populate.sql
   ```
   - Then open using
    ```bash
      mysql -u root -p decentraland_db
    ```

2. **Running the Application**:
     ```bash
     python3 main_app.py
     ```

## Demo Queries order

1. **View all DAO proposals by a user** – Prompts for a creator wallet (used `0x5555…5555`) and lists their most recent governance proposals.
  ```sql
  SELECT Proposal_ID, Title, Status, Creator_Address
  FROM DAO_Proposal
  WHERE Creator_Address = '0x5555555555555555555555555555555555555555'
  ORDER BY Proposal_ID DESC;
  ```

2. **List businesses established after a date** – Asks for a cutoff date (used `2006-08-13`) and shows businesses, their types, and owners.
  ```sql
  SELECT b.Business_ID, b.Business_Name, b.Business_Type, b.Date_Established, u.Username
  FROM Business b
  LEFT JOIN User_Profile u ON b.Owner_Address = u.Wallet_Address
  WHERE b.Date_Established > '2006-08-13'
  ORDER BY b.Date_Established ASC;
  ```

3. **Total MANA land sales in the last quarter** – Calculates land-sale stats over the past 90 days (last quarter) (sales count, total MANA, avg/min/max price).
  ```sql
  SELECT
     COUNT(*) AS total_sales,
     SUM(t.Price) AS total_mana,
     AVG(t.Price) AS avg_price,
     MIN(t.Price) AS min_price,
     MAX(t.Price) AS max_price
  FROM Transaction t
  JOIN LAND_Parcel lp ON t.Asset_ID = lp.Asset_ID
  WHERE t.Timestamp >= DATE_SUB(NOW(), INTERVAL 90 DAY)
    AND t.Currency = 'MANA';
  ```

4. **Search events by name keyword** – Prompts for a keyword (`meet`) and returns matching events with organizer and parcel metadata.
  ```sql
  SELECT
     e.Event_ID,
     e.Event_Name,
     e.Start_Timestamp,
     e.End_Timestamp,
     e.Organizer_Address,
     u.Username AS organizer_name,
     lp.X_Coordinate,
     lp.Y_Coordinate,
     lp.District_Name
  FROM Event e
  LEFT JOIN User_Profile u ON e.Organizer_Address = u.Wallet_Address
  LEFT JOIN LAND_Parcel lp ON e.Scene_Parcel_ID = lp.Asset_ID
  WHERE e.Event_Name LIKE '%meet%'
  ORDER BY e.Start_Timestamp DESC;
  ```

5. **Voter influence report** – Ranks citizens by land ownership + voting weight and displays the top 20 influence scores.
Voting weight is calculated as (No. of assets owned)*10 + No. of times vote given
  ```sql
  SELECT
     u.Wallet_Address,
     u.Username,
     COUNT(DISTINCT da.Asset_ID) AS land_parcels_owned,
     COUNT(DISTINCT v.Proposal_ID) AS votes_cast,
     SUM(DISTINCT v.Voting_Weight) AS total_voting_weight,
     (COUNT(DISTINCT da.Asset_ID) * 10 + COUNT(DISTINCT v.Proposal_ID)) AS influence_score
  FROM User_Profile u
  LEFT JOIN Digital_Asset da ON u.Wallet_Address = da.Owner_Address
  LEFT JOIN LAND_Parcel lp ON da.Asset_ID = lp.Asset_ID
  LEFT JOIN Vote v ON u.Wallet_Address = v.Voter_Address
  GROUP BY u.Wallet_Address, u.Username
  HAVING land_parcels_owned > 0 OR votes_cast > 0
  ORDER BY influence_score DESC
  LIMIT 20;
  ```

6. **Register new business** – Collects business metadata, verifies ownership, then inserts a record.
  ```sql
  INSERT INTO Business (Business_Name, Business_Type, Owner_Address, Date_Established, Parcel_ID)
  VALUES (%s, %s, %s, CURDATE(), %s);
```
  We verified this using:
  ```sql
  SELECT * FROM Business;
  ```

7. **Record an asset sale transaction** – Records a land sale, logs the transaction, and updates ownership.
  ```sql
  INSERT INTO Transaction (Transaction_ID, Asset_ID, Seller_Address, Buyer_Address, Price, Currency, Timestamp)
  VALUES (%s, %s, %s, %s, %s, 'MANA', NOW());
  UPDATE Digital_Asset SET Owner_Address = %s WHERE Asset_ID = %s;
  ```
  We verified this using:
  ```sql
  SELECT * FROM Transaction;
  ```

8. **Reschedule an event** – Lists upcoming events, prompts for new timestamps, and updates the chosen record.
  ```sql
  SELECT Event_ID, Event_Name, Start_Timestamp, End_Timestamp
  FROM Event
  WHERE Start_Timestamp > NOW()
  ORDER BY Start_Timestamp ASC;
  UPDATE Event
  SET Start_Timestamp = %s, End_Timestamp = %s
  WHERE Event_ID = %s;
  ```
  We  verified this using:
  ```sql
  SELECT * FROM Event WHERE Event_ID = %s;
  ```

9. **Delete user** – Permanently deletes a wallet (demo: `0x8888…8888`), cascading through votes, proposals, attendance, and ownership references (verified with `SELECT * FROM Event;`).
  ```sql
  DELETE FROM Vote WHERE Voter_Address = %s;
  DELETE FROM ATTENDS WHERE Wallet_Address = %s;
  DELETE FROM DAO_Proposal WHERE Creator_Address = %s;
  UPDATE Business SET Owner_Address = NULL WHERE Owner_Address = %s;
  UPDATE Event SET Organizer_Address = NULL WHERE Organizer_Address = %s;
  UPDATE Scene_Content SET Creator_Address = NULL WHERE Creator_Address = %s;
  UPDATE Transaction SET Seller_Address = NULL WHERE Seller_Address = %s;
  UPDATE Transaction SET Buyer_Address = NULL WHERE Buyer_Address = %s;
  DELETE FROM User_Profile WHERE Wallet_Address = %s;
  ```
  We verified this using:
  ```sql
  SELECT * FROM Event;
  ```

##### Note: we did not show this last operation in the demo due to time constraint.
10. **Custom SQL query** – Runs any query directly. (For safety use only SELECT query)
- For example:
  ```sql
  SELECT
  sc.Parcel_ID,
  sc.Scene_Version,
  u.Username AS Creator,
  b.Business_Name AS Linked_Business,
  lp.District_Name
  FROM Scene_Content sc
  JOIN LAND_Parcel lp ON sc.Parcel_ID = lp.Asset_ID
  LEFT JOIN User_Profile u ON sc.Creator_Address = u.Wallet_Address
  LEFT JOIN Business b ON sc.Parcel_ID = b.Parcel_ID
  ORDER BY sc.Deployment_Date DESC
  LIMIT 20;
  ```

  Returns Scene deployments with creator and linked business; containing: parcel, scene version, creator username, linked business name (if any), district.