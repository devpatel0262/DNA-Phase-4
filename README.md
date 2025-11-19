# Mini World - Genesis City Database Project

## Overview
This project implements a database system for "Genesis City", a metaverse-style virtual world. It includes a relational database schema, data population scripts, and two application interfaces (CLI and GUI) to interact with the data.

## Prerequisites
- Python 3.x
- MySQL Server
- `pymysql` library (`pip install pymysql`)
- `tkinter` (usually included with Python)

## Setup Instructions
1. **Database Setup**:
   - Run `schema.sql` to create the database and tables.
   - Run `populate.sql` to insert the initial dataset.
   
   ```bash
   mysql -u root -p < schema.sql
   mysql -u root -p < populate.sql
   ```

2. **Running the Application**:
   - **CLI Version**:
     ```bash
     python3 main_app.py
     ```
   - **GUI Version**:
     ```bash
     python3 gui_app.py
     ```

## Application Features

### 1. View DAO Proposals by User
Prompts for a wallet address and lists all governance proposals created by that user.

### 2. List Businesses Established After Date
Prompts for a date (YYYY-MM-DD) and lists all businesses created after that date, including "Abandoned" businesses where the owner has been deleted.

### 3. Total Land Sales (Last Quarter)
Calculates and displays statistics for land sales in MANA over the last 90 days, including Total Sales, Total Volume, Average Price, Min/Max Price.

### 4. Search Events by Name
Allows searching for events using a partial keyword match. Displays event details and location.

### 5. Voter Influence Report
Generates a report ranking users by their "Influence Score", calculated based on Land Ownership and Voting Activity.

### 6. Register New Business
A write operation that allows a user to register a new business on a land parcel they own.

### 7. Record Asset Sale
A transactional operation that records the sale of an asset (Land/Wearable) from one user to another, updating ownership and logging the transaction.

### 8. Delete User
A complex delete operation that removes a user profile. It triggers a cascade of updates:
- Deletes Votes and Proposals (Cascade)
- Sets Business/Event/Scene ownership to NULL (Set Null)
- Anonymizes past transactions

### 9. Custom SQL Query
Allows execution of raw SQL queries for testing and debugging.