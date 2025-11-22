#!/usr/bin/env python3
"""
MINI WORLD - GENESIS CITY
Database Application Interface (Python)

A metaverse-style virtual ecosystem management system.
Handles users, digital assets, land parcels, businesses, events, and DAO governance.
"""

import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime, timedelta
from decimal import Decimal
import os
import re
from getpass import getpass


# ============================================================================
# CYBERPUNK TERMINAL THEME - ANSI COLOR CODES
# ============================================================================

class Style:
    """Centralized styling class for terminal colors and formatting."""
    # Colors
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Formatting
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    RESET = '\033[0m'
    
    # Status Tags
    SUCCESS = f"{GREEN}[SUCCESS]{RESET}"
    ERROR = f"{RED}[ERROR]{RESET}"
    WARNING = f"{YELLOW}[WARNING]{RESET}"
    INFO = f"{CYAN}[INFO]{RESET}"
    
    # Box Drawing Characters
    BOX_H = '─'
    BOX_V = '│'
    BOX_TL = '┌'
    BOX_TR = '┐'
    BOX_BL = '└'
    BOX_BR = '┘'
    BOX_VR = '├'
    BOX_VL = '┤'
    BOX_HU = '┴'
    BOX_HD = '┬'
    BOX_CROSS = '┼'


A_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')


FIGLET_TITLE = """ ____                      _             _                 _ 
|  _ \\  ___  ___ ___ _ __ | |_ _ __ __ _| | __ _ _ __   __| |
| | | |/ _ \\/ __/ _ \\ '_ \\| __| '__/ _` | |/ _` | '_ \\ / _` |
| |_| |  __/ (_|  __/ | | | |_| | | (_| | | (_| | | | | (_| |
|____/ \\___|\\___\\___|_| |_|\\__|_|  \\__,_|_|\\__,_|_| |_|\\__,_|
                                                             """


def clear_screen():
    """Clears the terminal screen for a clean dashboard look."""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_banner():
    """Prints a minimal dashboard banner."""
    subtitle = f"{Style.MAGENTA}by team DataBreak{Style.RESET}"
    print()
    for line in FIGLET_TITLE.splitlines():
        print(f"{Style.BOLD}{Style.CYAN}{line}{Style.RESET}")
    print(subtitle)


def visual_length(text):
    """Return printable length of text without ANSI escape sequences."""
    return len(A_ESCAPE.sub('', text))


def print_box(title, width=78):
    """Prints a fancy box header with title."""
    inner = width - 2
    centered = title.center(inner)
    print(f"\n{Style.CYAN}{Style.BOX_TL}{Style.BOX_H * inner}{Style.BOX_TR}{Style.RESET}")
    print(f"{Style.CYAN}{Style.BOX_V}{Style.RESET}{Style.BOLD}{Style.MAGENTA}{centered}{Style.RESET}{Style.CYAN}{Style.BOX_V}{Style.RESET}")
    print(f"{Style.CYAN}{Style.BOX_BL}{Style.BOX_H * inner}{Style.BOX_BR}{Style.RESET}\n")


def print_box_line(content="", width=78):
    """Print a content line inside a box with proper padding."""
    inner = width - 2
    visible = visual_length(content)
    padding = inner - visible if visible < inner else 0
    print(f"{Style.CYAN}{Style.BOX_V}{Style.RESET}{content}{' ' * padding}{Style.CYAN}{Style.BOX_V}{Style.RESET}")


def print_box_separator(width=78):
    """Prints a horizontal separator inside a box."""
    inner = width - 2
    print(f"{Style.CYAN}{Style.BOX_VR}{Style.BOX_H * inner}{Style.BOX_VL}{Style.RESET}")


def pad_colored(text, width):
    """Pad text that may contain ANSI sequences to a visible width."""
    visible = visual_length(text)
    if visible >= width:
        return text
    return text + (' ' * (width - visible))


def build_table_row(values, widths):
    """Construct a formatted table row with ANSI-safe padding."""
    padded = [pad_colored(val, width) for val, width in zip(values, widths)]
    return (
        f"{Style.CYAN}{Style.BOX_V}{Style.RESET} "
        + f" {Style.GRAY}{Style.BOX_V}{Style.RESET}".join(padded)
        + f" {Style.CYAN}{Style.BOX_V}{Style.RESET}"
    )


def print_table_border(inner_width, top=True):
    """Print the top or bottom border for a table based on inner width."""
    left = Style.BOX_TL if top else Style.BOX_BL
    right = Style.BOX_TR if top else Style.BOX_BR
    print(f"{Style.CYAN}{left}{Style.BOX_H * inner_width}{right}{Style.RESET}")


def compute_column_widths(columns, rows):
    """Compute ANSI-safe widths for table columns based on data."""
    widths = []
    for col in columns:
        max_len = len(str(col))
        for row in rows:
            value = format_value(row.get(col))
            max_len = max(max_len, visual_length(str(value)))
        widths.append(max_len + 2)
    return widths


def print_divider(width=78, char=None):
    """Prints a horizontal divider."""
    if char:
        print(f"{Style.GRAY}{char * width}{Style.RESET}")
    else:
        print(f"{Style.CYAN}{Style.BOX_H * width}{Style.RESET}")


# Global credentials storage
DB_CREDENTIALS = {
    'user': None,
    'password': None
}

# ---------------------------------------------------------------------------
# Helper Functions for Enhanced CLI
# ---------------------------------------------------------------------------

def authenticate_user():
    """Prompt for MySQL credentials and store them globally."""
    print(f"{Style.CYAN}┌{'─' * 40}┐{Style.RESET}")
    print(f"{Style.CYAN}│{Style.RESET} {Style.BOLD}{Style.MAGENTA}{'AUTHENTICATION':^38}{Style.RESET} {Style.CYAN}│{Style.RESET}")
    print(f"{Style.CYAN}└{'─' * 40}┘{Style.RESET}\n")
    print(f"{Style.INFO} Host is fixed to: {Style.BOLD}localhost{Style.RESET}\n")
    while True:
        user = input(f"{Style.CYAN}>{Style.RESET} Enter MySQL Username: ").strip()
        password = getpass(f"{Style.CYAN}>{Style.RESET} Enter MySQL Password: ")
        if user and password:
            DB_CREDENTIALS['user'] = user
            DB_CREDENTIALS['password'] = password
            conn = get_connection()
            if conn:
                print(f"{Style.SUCCESS} Database connection successful!\n")
                conn.close()
                break
            else:
                print(f"{Style.ERROR} Connection failed. Please try again.\n")
        else:
            print(f"{Style.WARNING} Both username and password are required.\n")

def get_connection():
    """Establishes and returns a database connection using stored credentials."""
    try:
        if DB_CREDENTIALS['user'] is None:
            return None
        config = {
            'host': 'localhost',
            'user': DB_CREDENTIALS['user'],
            'password': DB_CREDENTIALS['password'],
            'database': 'decentraland_db',
            'charset': 'utf8mb4',
            'cursorclass': DictCursor
        }
        conn = pymysql.connect(**config)
        conn.autocommit = False
        return conn
    except pymysql.Error as e:
        print(f"\n{Style.ERROR} Database connection failed: {e}")
        return None

def paginate_query(query, params=None, page_size=20):
    """Yield results page by page for large result sets."""
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cursor:
            offset = 0
            while True:
                paginated = f"{query} LIMIT {page_size} OFFSET {offset}"
                cursor.execute(paginated, params or ())
                rows = cursor.fetchall()
                if not rows:
                    break
                yield rows
                offset += page_size
    finally:
        conn.close()

def display_paginated_results(rows_generator, title="Results"):
    """Display paginated query results with navigation prompts."""
    page_num = 1
    for rows in rows_generator:
        print_box(f"{title} - Page {page_num}")
        if rows:
            columns = list(rows[0].keys())
            widths = compute_column_widths(columns, rows)
            inner_width = print_table_header(columns, widths)
            for row in rows:
                values = [f"{Style.WHITE}{format_value(row[col])}{Style.RESET}" for col in columns]
                print(build_table_row(values, widths))
            print_table_footer(inner_width)
        else:
            print(f"{Style.WARNING} No data to display.")
        input(f"{Style.CYAN}>{Style.RESET} Press Enter for next page (or Ctrl+C to stop)...")
        page_num += 1

def view_all_users():
    """Display a list of all user profiles."""
    query = "SELECT Wallet_Address, Username, Join_Date, Last_Seen FROM User_Profile ORDER BY Join_Date DESC"
    rows_gen = paginate_query(query)
    display_paginated_results(rows_gen, title="All Users")

def view_all_assets():
    """Display a list of all digital assets (land and wearables)."""
    query = """
        SELECT da.Asset_ID, da.Token_URI, da.Owner_Address, 
               CASE WHEN lp.Asset_ID IS NOT NULL THEN 'Land' ELSE 'Wearable' END AS Asset_Type,
               lp.X_Coordinate, lp.Y_Coordinate, w.Category, w.Rarity
        FROM Digital_Asset da
        LEFT JOIN LAND_Parcel lp ON da.Asset_ID = lp.Asset_ID
        LEFT JOIN Wearable w ON da.Asset_ID = w.Asset_ID
        ORDER BY da.Asset_ID
    """
    rows_gen = paginate_query(query)
    display_paginated_results(rows_gen, title="All Digital Assets")

def view_summary_stats():
    """Show high‑level statistics about the mini‑world."""
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total_users FROM User_Profile")
            users = cursor.fetchone()['total_users']
            cursor.execute("SELECT COUNT(*) AS total_assets FROM Digital_Asset")
            assets = cursor.fetchone()['total_assets']
            cursor.execute("SELECT COUNT(*) AS total_businesses FROM Business")
            businesses = cursor.fetchone()['total_businesses']
            cursor.execute("SELECT COUNT(*) AS total_events FROM Event")
            events = cursor.fetchone()['total_events']
        print_box("MINI-WORLD SUMMARY")
        print(f"{Style.GREEN}Users:{Style.RESET} {users}")
        print(f"{Style.CYAN}Assets:{Style.RESET} {assets}")
        print(f"{Style.MAGENTA}Businesses:{Style.RESET} {businesses}")
        print(f"{Style.YELLOW}Events:{Style.RESET} {events}")
        input(f"\n{Style.CYAN}>{Style.RESET} Press Enter to return to menu...")
    finally:
        conn.close()

# ---------------------------------------------------------------------------
# Existing Functions (unchanged) – kept for reference
# ---------------------------------------------------------------------------
# ... (the rest of the file remains unchanged) ...


def print_separator():
    """Prints a visual separator line."""
    print(f"{Style.CYAN}{'═' * 80}{Style.RESET}")


def print_table_header(columns, widths):
    """Prints formatted table headers with cyberpunk styling."""
    header_cells = [f"{Style.BOLD}{Style.GREEN}{col}{Style.RESET}" for col in columns]
    header_row = build_table_row(header_cells, widths)
    inner_width = visual_length(header_row) - 2
    print_table_border(inner_width, top=True)
    print(header_row)
    print(f"{Style.CYAN}{Style.BOX_VR}{Style.BOX_H * inner_width}{Style.BOX_VL}{Style.RESET}")
    return inner_width


def print_table_footer(inner_width):
    """Print a bottom border for tables."""
    print_table_border(inner_width, top=False)


def format_value(value):
    """Formats value for display."""
    if value is None:
        return "NULL"
    elif isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(value, Decimal):
        return f"{value:.2f}"
    else:
        return str(value)


def view_dao_proposals_by_user():
    """READ Operation 1: List all DAO proposals created by a specific user."""
    print_box("VIEW DAO PROPOSALS BY USER")
    
    wallet = input(f"{Style.CYAN}>{Style.RESET} Enter creator wallet address: ").strip()
    
    if not wallet:
        print(f"{Style.ERROR} Wallet address cannot be empty.")
        return
    
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    Proposal_ID,
                    Title,
                    Status,
                    Creator_Address
                FROM DAO_Proposal
                WHERE Creator_Address = %s
                ORDER BY Proposal_ID DESC
            """
            cursor.execute(query, (wallet,))
            results = cursor.fetchall()
            
            if not results:
                print(f"\n{Style.WARNING} No proposals found for wallet: {Style.YELLOW}{wallet}{Style.RESET}")
            else:
                print(f"\n{Style.SUCCESS} Found {Style.GREEN}{Style.BOLD}{len(results)}{Style.RESET} proposal(s):\n")
                for idx, row in enumerate(results, 1):
                    print(f"{Style.CYAN}{Style.BOX_V}{Style.RESET} {Style.MAGENTA}Proposal #{idx}{Style.RESET}")
                    print(f"  {Style.GRAY}ID:{Style.RESET} {Style.WHITE}{row['Proposal_ID']}{Style.RESET}")
                    print(f"  {Style.GRAY}Title:{Style.RESET} {Style.WHITE}{row['Title']}{Style.RESET}")
                    print(f"  {Style.GRAY}Status:{Style.RESET} {Style.GREEN}{row['Status']}{Style.RESET}")
                    print(f"  {Style.GRAY}Creator:{Style.RESET} {Style.CYAN}{row['Creator_Address']}{Style.RESET}")
                    print()
    
    except pymysql.Error as e:
        print(f"{Style.ERROR} Database error: {e}")
    finally:
        conn.close()


def list_businesses_after_date():
    """READ Operation 2: List businesses established after a given date."""
    print_box("LIST BUSINESSES ESTABLISHED AFTER DATE")
    
    date_str = input(f"{Style.CYAN}>{Style.RESET} Enter date (YYYY-MM-DD): ").strip()
    
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"{Style.ERROR} Invalid date format. Use YYYY-MM-DD.")
        return
    
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    b.Business_ID,
                    b.Business_Name,
                    b.Business_Type,
                    b.Date_Established,
                    b.Owner_Address,
                    u.Username
                FROM Business b
                LEFT JOIN User_Profile u ON b.Owner_Address = u.Wallet_Address
                WHERE b.Date_Established > %s
                ORDER BY b.Date_Established ASC
            """
            cursor.execute(query, (date_str,))
            results = cursor.fetchall()
            
            if not results:
                print(f"\n{Style.WARNING} No businesses found established after {Style.YELLOW}{date_str}{Style.RESET}")
            else:
                print(f"\n{Style.SUCCESS} Found {Style.GREEN}{Style.BOLD}{len(results)}{Style.RESET} business(es):\n")
                for idx, row in enumerate(results, 1):
                    owner_name = row['Username'] if row['Username'] else f"{Style.RED}Abandoned{Style.RESET}"
                    print(f"{Style.CYAN}{Style.BOX_V}{Style.RESET} {Style.MAGENTA}Business #{idx}{Style.RESET}")
                    print(f"  {Style.GRAY}ID:{Style.RESET} {Style.WHITE}{row['Business_ID']}{Style.RESET}")
                    print(f"  {Style.GRAY}Name:{Style.RESET} {Style.WHITE}{row['Business_Name']}{Style.RESET}")
                    print(f"  {Style.GRAY}Type:{Style.RESET} {Style.GREEN}{row['Business_Type']}{Style.RESET}")
                    print(f"  {Style.GRAY}Established:{Style.RESET} {Style.YELLOW}{format_value(row['Date_Established'])}{Style.RESET}")
                    print(f"  {Style.GRAY}Owner:{Style.RESET} {owner_name} {Style.CYAN}({row['Owner_Address']}){Style.RESET}")
                    print()
    
    except pymysql.Error as e:
        print(f"{Style.ERROR} Database error: {e}")
    finally:
        conn.close()


def total_land_sales_last_quarter():
    """READ Operation 3: Calculate total MANA land sales in the last quarter."""
    print_box("TOTAL LAND SALES (LAST QUARTER)")
    
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            three_months_ago = datetime.now() - timedelta(days=90)
            
            query = """
                SELECT 
                    COUNT(*) as total_sales,
                    SUM(t.Price) as total_mana,
                    AVG(t.Price) as avg_price,
                    MIN(t.Price) as min_price,
                    MAX(t.Price) as max_price
                FROM Transaction t
                JOIN LAND_Parcel lp ON t.Asset_ID = lp.Asset_ID
                WHERE t.Timestamp >= %s AND t.Currency = 'MANA'
            """
            cursor.execute(query, (three_months_ago,))
            result = cursor.fetchone()
            
            width = 80
            print(f"\n{Style.CYAN}{Style.BOX_TL}{Style.BOX_H * (width - 2)}{Style.BOX_TR}{Style.RESET}")
            print_box_line(f"{Style.BOLD}{Style.MAGENTA}Land Sales Report (Last 90 Days){Style.RESET}", width)
            print_box_line(
                f"{Style.GRAY}Period:{Style.RESET} {three_months_ago.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
                width
            )
            print_box_separator(width)
            
            if result['total_sales'] == 0:
                print_box_line(f"{Style.WARNING} No land sales in the last quarter.", width)
            else:
                print_box_line(f"{Style.GREEN}Total Sales:{Style.RESET} {Style.WHITE}{result['total_sales']}{Style.RESET}", width)
                print_box_line(f"{Style.GREEN}Total MANA:{Style.RESET} {Style.YELLOW}{format_value(result['total_mana'])}{Style.RESET}", width)
                print_box_line(f"{Style.GREEN}Average Price:{Style.RESET} {Style.YELLOW}{format_value(result['avg_price'])}{Style.RESET}", width)
                print_box_line(f"{Style.GREEN}Min Price:{Style.RESET} {Style.YELLOW}{format_value(result['min_price'])}{Style.RESET}", width)
                print_box_line(f"{Style.GREEN}Max Price:{Style.RESET} {Style.YELLOW}{format_value(result['max_price'])}{Style.RESET}", width)
            
            print(f"{Style.CYAN}{Style.BOX_BL}{Style.BOX_H * (width - 2)}{Style.BOX_BR}{Style.RESET}")
    
    except pymysql.Error as e:
        print(f"{Style.ERROR} Database error: {e}")
    finally:
        conn.close()


def search_events_by_name():
    """READ Operation 4: Search events by partial name match."""
    print_box("SEARCH EVENTS BY NAME")
    
    keyword = input(f"{Style.CYAN}>{Style.RESET} Enter event name keyword: ").strip()
    
    if not keyword:
        print(f"{Style.ERROR} Keyword cannot be empty.")
        return
    
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    e.Event_ID,
                    e.Event_Name,
                    e.Start_Timestamp,
                    e.End_Timestamp,
                    e.Organizer_Address,
                    u.Username as organizer_name,
                    lp.X_Coordinate,
                    lp.Y_Coordinate,
                    lp.District_Name
                FROM Event e
                LEFT JOIN User_Profile u ON e.Organizer_Address = u.Wallet_Address
                LEFT JOIN LAND_Parcel lp ON e.Scene_Parcel_ID = lp.Asset_ID
                WHERE e.Event_Name LIKE %s
                ORDER BY e.Start_Timestamp DESC
            """
            cursor.execute(query, (f"%{keyword}%",))
            results = cursor.fetchall()
            
            if not results:
                print(f"\n{Style.WARNING} No events found matching '{Style.YELLOW}{keyword}{Style.RESET}'")
            else:
                print(f"\n{Style.SUCCESS} Found {Style.GREEN}{Style.BOLD}{len(results)}{Style.RESET} event(s):\n")
                for idx, row in enumerate(results, 1):
                    organizer_name = row['organizer_name'] if row['organizer_name'] else f"{Style.RED}Unknown{Style.RESET}"
                    print(f"{Style.CYAN}{Style.BOX_V}{Style.RESET} {Style.MAGENTA}Event #{idx}{Style.RESET}")
                    print(f"  {Style.GRAY}ID:{Style.RESET} {Style.WHITE}{row['Event_ID']}{Style.RESET}")
                    print(f"  {Style.GRAY}Name:{Style.RESET} {Style.WHITE}{row['Event_Name']}{Style.RESET}")
                    print(f"  {Style.GRAY}Start:{Style.RESET} {Style.YELLOW}{format_value(row['Start_Timestamp'])}{Style.RESET}")
                    print(f"  {Style.GRAY}End:{Style.RESET} {Style.YELLOW}{format_value(row['End_Timestamp'])}{Style.RESET}")
                    print(f"  {Style.GRAY}Organizer:{Style.RESET} {organizer_name} {Style.CYAN}({row['Organizer_Address']}){Style.RESET}")
                    if row['X_Coordinate'] is not None:
                        print(f"  {Style.GRAY}Venue:{Style.RESET} {Style.GREEN}({row['X_Coordinate']}, {row['Y_Coordinate']}){Style.RESET} - {Style.MAGENTA}{row['District_Name']}{Style.RESET}")
                    print()
    
    except pymysql.Error as e:
        print(f"{Style.ERROR} Database error: {e}")
    finally:
        conn.close()


def voter_influence_report():
    """READ Operation 5: Generate voter influence report (land owned + votes cast)."""
    print_box("VOTER INFLUENCE REPORT")
    
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    u.Wallet_Address,
                    u.Username,
                    COUNT(DISTINCT da.Asset_ID) as land_parcels_owned,
                    COUNT(DISTINCT v.Proposal_ID) as votes_cast,
                    SUM(DISTINCT v.Voting_Weight) as total_voting_weight,
                    (COUNT(DISTINCT da.Asset_ID) * 10 + COUNT(DISTINCT v.Proposal_ID)) as influence_score
                FROM User_Profile u
                LEFT JOIN Digital_Asset da ON u.Wallet_Address = da.Owner_Address
                LEFT JOIN LAND_Parcel lp ON da.Asset_ID = lp.Asset_ID
                LEFT JOIN Vote v ON u.Wallet_Address = v.Voter_Address
                GROUP BY u.Wallet_Address, u.Username
                HAVING land_parcels_owned > 0 OR votes_cast > 0
                ORDER BY influence_score DESC
                LIMIT 20
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            if not results:
                print(f"\n{Style.WARNING} No voter activity found.")
            else:
                print(f"\n{Style.SUCCESS} Top {Style.GREEN}{Style.BOLD}{len(results)}{Style.RESET} Most Influential Voters:\n")
                columns = ["Rank", "Username", "Land", "Votes", "Score"]
                width_rows = []
                for idx, row in enumerate(results, 1):
                    width_rows.append({
                        "Rank": str(idx),
                        "Username": row['Username'] or "Unknown",
                        "Land": str(row['land_parcels_owned']),
                        "Votes": str(row['votes_cast']),
                        "Score": str(row['influence_score'])
                    })
                widths = compute_column_widths(columns, width_rows)
                inner_width = print_table_header(columns, widths)
                for idx, row in enumerate(results, 1):
                    rank_color = Style.YELLOW if idx <= 3 else Style.WHITE
                    values = [
                        f"{rank_color}{idx}{Style.RESET}",
                        f"{Style.MAGENTA}{row['Username'] or 'Unknown'}{Style.RESET}",
                        f"{Style.WHITE}{row['land_parcels_owned']}{Style.RESET}",
                        f"{Style.WHITE}{row['votes_cast']}{Style.RESET}",
                        f"{Style.GREEN}{row['influence_score']}{Style.RESET}"
                    ]
                    print(build_table_row(values, widths))
                print_table_footer(inner_width)
    
    except pymysql.Error as e:
        print(f"{Style.ERROR} Database error: {e}")
    finally:
        conn.close()


def reschedule_event():
    """WRITE Operation 8: Reschedule an event by updating timestamps."""
    print_box("RESCHEDULE EVENT")
    
    # First, show available events to reschedule
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # Show current events that can be rescheduled
            query = """
                SELECT 
                    e.Event_ID,
                    e.Event_Name,
                    e.Start_Timestamp,
                    e.End_Timestamp,
                    e.Organizer_Address,
                    u.Username as organizer_name
                FROM Event e
                LEFT JOIN User_Profile u ON e.Organizer_Address = u.Wallet_Address
                WHERE e.Start_Timestamp > NOW()
                ORDER BY e.Start_Timestamp ASC
            """
            cursor.execute(query)
            events = cursor.fetchall()
            
            if not events:
                print(f"\n{Style.WARNING} No upcoming events available to reschedule.")
                return
            
            print(f"\n{Style.INFO} Available events to reschedule:\n")
            for idx, event in enumerate(events, 1):
                start_time = event['Start_Timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                end_time = event['End_Timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                organizer = event['organizer_name'] or event['Organizer_Address'][:10] + '...'
                
                print(f"  {Style.GREEN}{idx}.{Style.RESET} {Style.BOLD}{event['Event_Name']}{Style.RESET}")
                print(f"     {Style.GRAY}ID: {event['Event_ID']} | Organizer: {organizer}{Style.RESET}")
                print(f"     {Style.CYAN}Current: {start_time} → {end_time}{Style.RESET}\n")
            
            # Get event selection
            try:
                choice = int(input(f"{Style.CYAN}>{Style.RESET} Select event number to reschedule (1-{len(events)}): "))
                if choice < 1 or choice > len(events):
                    print(f"{Style.ERROR} Invalid selection.")
                    return
                
                selected_event = events[choice - 1]
                event_id = selected_event['Event_ID']
                
                print(f"\n{Style.INFO} Rescheduling: {Style.BOLD}{selected_event['Event_Name']}{Style.RESET}")
                
                # Get new start datetime
                print(f"\n{Style.CYAN}Enter new start time:{Style.RESET}")
                start_date = input(f"{Style.CYAN}>{Style.RESET} Date (YYYY-MM-DD): ").strip()
                start_time = input(f"{Style.CYAN}>{Style.RESET} Time (HH:MM): ").strip()
                
                # Get new end datetime  
                print(f"\n{Style.CYAN}Enter new end time:{Style.RESET}")
                end_date = input(f"{Style.CYAN}>{Style.RESET} Date (YYYY-MM-DD): ").strip()
                end_time = input(f"{Style.CYAN}>{Style.RESET} Time (HH:MM): ").strip()
                
                # Validate datetime format
                try:
                    new_start = datetime.strptime(f"{start_date} {start_time}:00", "%Y-%m-%d %H:%M:%S")
                    new_end = datetime.strptime(f"{end_date} {end_time}:00", "%Y-%m-%d %H:%M:%S")
                    
                    # Validate that end > start (this will test our CHECK constraint)
                    if new_end <= new_start:
                        print(f"{Style.ERROR} End time must be after start time.")
                        return
                    
                    # Validate that start time is in the future
                    if new_start <= datetime.now():
                        print(f"{Style.ERROR} Start time must be in the future.")
                        return
                        
                except ValueError as e:
                    print(f"{Style.ERROR} Invalid datetime format. Use YYYY-MM-DD and HH:MM.")
                    return
                
                # Update the event
                update_query = """
                    UPDATE Event 
                    SET Start_Timestamp = %s, End_Timestamp = %s
                    WHERE Event_ID = %s
                """
                
                cursor.execute(update_query, (new_start, new_end, event_id))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    print(f"\n{Style.SUCCESS} Event '{selected_event['Event_Name']}' successfully rescheduled!")
                    print(f"{Style.INFO} New schedule:")
                    print(f"  {Style.GREEN}Start:{Style.RESET} {new_start.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"  {Style.GREEN}End:{Style.RESET}   {new_end.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Show duration
                    duration = new_end - new_start
                    hours = duration.seconds // 3600
                    minutes = (duration.seconds % 3600) // 60
                    print(f"  {Style.CYAN}Duration:{Style.RESET} {duration.days} day(s), {hours} hour(s), {minutes} minute(s)")
                else:
                    print(f"{Style.ERROR} Failed to reschedule event.")
                    
            except ValueError:
                print(f"{Style.ERROR} Please enter a valid number.")
                return
            
    except pymysql.Error as e:
        print(f"{Style.ERROR} Database error: {e}")
        if conn:
            conn.rollback()
    
    finally:
        if conn:
            conn.close()


def register_new_business():
    """WRITE Operation 6: Register a new business."""
    print_box("REGISTER NEW BUSINESS")
    
    business_name = input(f"{Style.CYAN}>{Style.RESET} Business name: ").strip()
    business_type = input(f"{Style.CYAN}>{Style.RESET} Business type (Shop/Gallery/Venue/Service): ").strip()
    owner_address = input(f"{Style.CYAN}>{Style.RESET} Owner wallet address: ").strip()
    
    if not all([business_name, business_type, owner_address]):
        print(f"{Style.ERROR} All fields are required.")
        return
    
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            check_query = "SELECT Wallet_Address FROM User_Profile WHERE Wallet_Address = %s"
            cursor.execute(check_query, (owner_address,))
            
            if not cursor.fetchone():
                print(f"{Style.ERROR} User with wallet {Style.CYAN}{owner_address}{Style.RESET} does not exist.")
                return
            
            # Get all land parcels owned by this user
            parcel_query = """
                SELECT lp.Asset_ID, lp.X_Coordinate, lp.Y_Coordinate, lp.District_Name
                FROM LAND_Parcel lp
                JOIN Digital_Asset da ON lp.Asset_ID = da.Asset_ID
                WHERE da.Owner_Address = %s
                ORDER BY lp.Asset_ID
            """
            cursor.execute(parcel_query, (owner_address,))
            parcels = cursor.fetchall()
            
            if not parcels:
                print(f"{Style.ERROR} User must own at least one land parcel to register a business.")
                return
            
            # Show available parcels and let user choose
            print(f"\n{Style.INFO} Available land parcels owned by {Style.CYAN}{owner_address[:10]}...{Style.RESET}:\n")
            
            for idx, parcel in enumerate(parcels, 1):
                district = parcel['District_Name'] or "Uncharted Territory"
                coords = f"({parcel['X_Coordinate']}, {parcel['Y_Coordinate']})"
                
                print(f"  {Style.GREEN}{idx}.{Style.RESET} {Style.BOLD}{parcel['Asset_ID']}{Style.RESET}")
                print(f"     {Style.GRAY}Location: {coords} | District: {district}{Style.RESET}\n")
            
            # Get user's parcel choice
            try:
                choice = int(input(f"{Style.CYAN}>{Style.RESET} Select parcel number for business (1-{len(parcels)}): "))
                if choice < 1 or choice > len(parcels):
                    print(f"{Style.ERROR} Invalid selection.")
                    return
                
                selected_parcel = parcels[choice - 1]
                parcel_id = selected_parcel['Asset_ID']
                
                print(f"\n{Style.INFO} Business will be registered on parcel {Style.YELLOW}{parcel_id}{Style.RESET}")
                
            except ValueError:
                print(f"{Style.ERROR} Please enter a valid number.")
                return
            
            insert_query = """
                INSERT INTO Business (Business_Name, Business_Type, Owner_Address, Date_Established, Parcel_ID)
                VALUES (%s, %s, %s, CURDATE(), %s)
            """
            cursor.execute(insert_query, (business_name, business_type, owner_address, parcel_id))
            
            business_id = cursor.lastrowid
            conn.commit()
            
            print(f"\n{Style.SUCCESS} Business registered successfully!")
            print(f"   {Style.GRAY}Business ID:{Style.RESET} {Style.WHITE}{business_id}{Style.RESET}")
            print(f"   {Style.GRAY}Name:{Style.RESET} {Style.MAGENTA}{business_name}{Style.RESET}")
            print(f"   {Style.GRAY}Type:{Style.RESET} {Style.GREEN}{business_type}{Style.RESET}")
            print(f"   {Style.GRAY}Owner:{Style.RESET} {Style.CYAN}{owner_address}{Style.RESET}")
            print(f"   {Style.GRAY}Parcel:{Style.RESET} {Style.YELLOW}{parcel_id}{Style.RESET}")
    
    except pymysql.Error as e:
        conn.rollback()
        print(f"{Style.ERROR} Failed to register business: {e}")
    finally:
        conn.close()


def record_asset_sale():
    """WRITE Operation 7: Record an asset sale transaction and update ownership."""
    print_box("RECORD ASSET SALE TRANSACTION")
    
    asset_id = input(f"{Style.CYAN}>{Style.RESET} Asset ID: ").strip()
    seller_address = input(f"{Style.CYAN}>{Style.RESET} Seller wallet address: ").strip()
    buyer_address = input(f"{Style.CYAN}>{Style.RESET} Buyer wallet address: ").strip()
    price = input(f"{Style.CYAN}>{Style.RESET} Sale price (MANA): ").strip()
    
    if not all([asset_id, seller_address, buyer_address, price]):
        print(f"{Style.ERROR} All fields are required.")
        return
    
    try:
        price = Decimal(price)
        if price <= 0:
            raise ValueError("Price must be positive")
    except ValueError as e:
        print(f"{Style.ERROR} Invalid input: {e}")
        return
    
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            check_asset = """
                SELECT Owner_Address FROM Digital_Asset 
                WHERE Asset_ID = %s
            """
            cursor.execute(check_asset, (asset_id,))
            asset = cursor.fetchone()
            
            if not asset:
                print(f"{Style.ERROR} Asset {Style.YELLOW}{asset_id}{Style.RESET} does not exist.")
                return
            
            if asset['Owner_Address'] != seller_address:
                print(f"{Style.ERROR} Seller does not own this asset. Current owner: {Style.CYAN}{asset['Owner_Address']}{Style.RESET}")
                return
            
            check_buyer = "SELECT Wallet_Address FROM User_Profile WHERE Wallet_Address = %s"
            cursor.execute(check_buyer, (buyer_address,))
            if not cursor.fetchone():
                print(f"{Style.ERROR} Buyer wallet {Style.CYAN}{buyer_address}{Style.RESET} does not exist.")
                return
            
            # Generate transaction ID (66 char blockchain hash format: 0x + 64 hex chars)
            import secrets
            transaction_id = '0x' + secrets.token_hex(32)
            
            insert_transaction = """
                INSERT INTO Transaction (Transaction_ID, Asset_ID, Seller_Address, Buyer_Address, Price, Currency, Timestamp)
                VALUES (%s, %s, %s, %s, %s, 'MANA', NOW())
            """
            cursor.execute(insert_transaction, (transaction_id, asset_id, seller_address, buyer_address, price))
            
            update_ownership = """
                UPDATE Digital_Asset 
                SET Owner_Address = %s 
                WHERE Asset_ID = %s
            """
            cursor.execute(update_ownership, (buyer_address, asset_id))
            
            conn.commit()
            
            print(f"\n{Style.SUCCESS} Transaction recorded successfully!")
            print(f"   {Style.GRAY}Transaction ID:{Style.RESET} {Style.YELLOW}{transaction_id}{Style.RESET}")
            print(f"   {Style.GRAY}Asset ID:{Style.RESET} {Style.WHITE}{asset_id}{Style.RESET}")
            print(f"   {Style.GRAY}From:{Style.RESET} {Style.CYAN}{seller_address}{Style.RESET}")
            print(f"   {Style.GRAY}To:{Style.RESET} {Style.CYAN}{buyer_address}{Style.RESET}")
            print(f"   {Style.GRAY}Price:{Style.RESET} {Style.GREEN}{price} MANA{Style.RESET}")
            print(f"   {Style.INFO} Ownership transferred to buyer.")
    
    except pymysql.Error as e:
        conn.rollback()
        print(f"{Style.ERROR} Transaction failed: {e}")
    finally:
        conn.close()


def delete_user():
    """WRITE Operation 8: Delete a user with cascading effects."""
    print_box("DELETE USER")
    
    wallet = input(f"{Style.CYAN}>{Style.RESET} Enter wallet address to delete: ").strip()
    
    if not wallet:
        print(f"{Style.ERROR} Wallet address cannot be empty.")
        return
    
    confirm = input(f"{Style.WARNING} Are you sure you want to delete user {Style.CYAN}{wallet}{Style.RESET}? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print(f"{Style.WARNING} Deletion cancelled.")
        return
    
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            check_user = "SELECT Username FROM User_Profile WHERE Wallet_Address = %s"
            cursor.execute(check_user, (wallet,))
            user = cursor.fetchone()
            
            if not user:
                print(f"{Style.ERROR} User {Style.CYAN}{wallet}{Style.RESET} does not exist.")
                return
            
            delete_votes = "DELETE FROM Vote WHERE Voter_Address = %s"
            cursor.execute(delete_votes, (wallet,))
            votes_deleted = cursor.rowcount
            
            delete_attends = "DELETE FROM ATTENDS WHERE Wallet_Address = %s"
            cursor.execute(delete_attends, (wallet,))
            attends_deleted = cursor.rowcount
            
            delete_proposals = "DELETE FROM DAO_Proposal WHERE Creator_Address = %s"
            cursor.execute(delete_proposals, (wallet,))
            proposals_deleted = cursor.rowcount
            
            set_businesses_null = "UPDATE Business SET Owner_Address = NULL WHERE Owner_Address = %s"
            cursor.execute(set_businesses_null, (wallet,))
            businesses_updated = cursor.rowcount
            
            set_events_null = "UPDATE Event SET Organizer_Address = NULL WHERE Organizer_Address = %s"
            cursor.execute(set_events_null, (wallet,))
            events_updated = cursor.rowcount
            
            set_scenes_null = "UPDATE Scene_Content SET Creator_Address = NULL WHERE Creator_Address = %s"
            cursor.execute(set_scenes_null, (wallet,))
            scenes_updated = cursor.rowcount
            
            set_transactions_null = """
                UPDATE Transaction 
                SET Seller_Address = NULL 
                WHERE Seller_Address = %s
            """
            cursor.execute(set_transactions_null, (wallet,))
            
            set_transactions_buyer_null = """
                UPDATE Transaction 
                SET Buyer_Address = NULL 
                WHERE Buyer_Address = %s
            """
            cursor.execute(set_transactions_buyer_null, (wallet,))
            
            delete_user_query = "DELETE FROM User_Profile WHERE Wallet_Address = %s"
            cursor.execute(delete_user_query, (wallet,))
            
            conn.commit()
            
            print(f"\n{Style.SUCCESS} User {Style.MAGENTA}{user['Username']}{Style.RESET} deleted successfully!")
            print(f"   {Style.GRAY}Votes deleted:{Style.RESET} {Style.WHITE}{votes_deleted}{Style.RESET}")
            print(f"   {Style.GRAY}Event attendances deleted:{Style.RESET} {Style.WHITE}{attends_deleted}{Style.RESET}")
            print(f"   {Style.GRAY}DAO proposals deleted:{Style.RESET} {Style.WHITE}{proposals_deleted}{Style.RESET}")
            print(f"   {Style.GRAY}Businesses set to abandoned:{Style.RESET} {Style.WHITE}{businesses_updated}{Style.RESET}")
            print(f"   {Style.GRAY}Events organizer cleared:{Style.RESET} {Style.WHITE}{events_updated}{Style.RESET}")
            print(f"   {Style.GRAY}Scenes creator cleared:{Style.RESET} {Style.WHITE}{scenes_updated}{Style.RESET}")
            print(f"   {Style.INFO} Digital assets remain (constraint prevents deletion)")
    
    except pymysql.Error as e:
        conn.rollback()
        print(f"{Style.ERROR} Failed to delete user: {e}")
    finally:
        conn.close()


def custom_sql_query():
    """Execute a custom SQL query."""
    print_box("CUSTOM SQL QUERY")
    print(f"{Style.WARNING} Use with caution. Only SELECT queries recommended.\n")
    
    query = input(f"{Style.CYAN}>{Style.RESET} Enter SQL query: ").strip()
    
    if not query:
        print(f"{Style.ERROR} Query cannot be empty.")
        return
    
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                
                if not results:
                    print(f"\n{Style.WARNING} Query returned no results.")
                else:
                    print(f"\n{Style.SUCCESS} Query returned {Style.GREEN}{Style.BOLD}{len(results)}{Style.RESET} row(s):\n")
                    
                    if results:
                        columns = list(results[0].keys())
                        widths = compute_column_widths(columns, results)
                        inner_width = print_table_header(columns, widths)
                        for row in results:
                            values = [f"{Style.WHITE}{format_value(row[col])}{Style.RESET}" for col in columns]
                            print(build_table_row(values, widths))
                        print_table_footer(inner_width)
            else:
                conn.commit()
                print(f"\n{Style.SUCCESS} Query executed successfully. Rows affected: {Style.GREEN}{cursor.rowcount}{Style.RESET}")
    
    except pymysql.Error as e:
        conn.rollback()
        print(f"{Style.ERROR} Query failed: {e}")
    finally:
        conn.close()


def display_menu():
    """Displays the main menu."""
    print_banner()
    width = 80
    print(f"\n{Style.CYAN}{Style.BOX_TL}{Style.BOX_H * (width - 2)}{Style.BOX_TR}{Style.RESET}")
    title = "MAIN MENU".center(width - 2)
    title_colored = title.replace("MAIN MENU", f"{Style.BOLD}{Style.MAGENTA}MAIN MENU{Style.RESET}", 1)
    print_box_line(title_colored, width)
    print_box_separator(width)
    print_box_line("", width)
    menu_items = [
        f"{Style.GREEN}1.{Style.RESET} {Style.WHITE}View all DAO proposals by a user{Style.RESET}",
        f"{Style.GREEN}2.{Style.RESET} {Style.WHITE}List businesses established after a date{Style.RESET}",
        f"{Style.GREEN}3.{Style.RESET} {Style.WHITE}Total MANA land sales in the last quarter{Style.RESET}",
        f"{Style.GREEN}4.{Style.RESET} {Style.WHITE}Search events by name keyword{Style.RESET}",
        f"{Style.GREEN}5.{Style.RESET} {Style.WHITE}Voter influence report{Style.RESET}",
        f"{Style.YELLOW}6.{Style.RESET} {Style.WHITE}Register new business{Style.RESET}",
        f"{Style.YELLOW}7.{Style.RESET} {Style.WHITE}Record an asset sale transaction{Style.RESET}",
        f"{Style.YELLOW}8.{Style.RESET} {Style.WHITE}Reschedule an event{Style.RESET}",
        f"{Style.RED}9.{Style.RESET} {Style.WHITE}Delete a user{Style.RESET}",
        f"{Style.MAGENTA}10.{Style.RESET} {Style.WHITE}Custom SQL query{Style.RESET}",
        f"{Style.GRAY}q.{Style.RESET} {Style.WHITE}Quit{Style.RESET}"
    ]
    for item in menu_items:
        print_box_line(item, width)
    print_box_line("", width)
    print(f"{Style.CYAN}{Style.BOX_BL}{Style.BOX_H * (width - 2)}{Style.BOX_BR}{Style.RESET}\n")


def main():
    """Main application loop."""
    clear_screen()
    print_banner()
    
    print(f"{Style.CYAN}┌{'─' * 40}┐{Style.RESET}")
    print(f"{Style.CYAN}│{Style.RESET} {Style.BOLD}{Style.MAGENTA}{'AUTHENTICATION':^38}{Style.RESET} {Style.CYAN}│{Style.RESET}")
    print(f"{Style.CYAN}└{'─' * 40}┘{Style.RESET}\n")
    
    print(f"{Style.INFO} Host is fixed to: {Style.BOLD}localhost{Style.RESET}")
    
    try:
        user = input(f"{Style.CYAN}>{Style.RESET} Enter MySQL Username: ").strip()
        password = getpass(f"{Style.CYAN}>{Style.RESET} Enter MySQL Password: ")
        
        DB_CREDENTIALS['user'] = user
        DB_CREDENTIALS['password'] = password
        
        print("\nConnecting to database...")
        conn = get_connection()
        
        if conn:
            print(f"{Style.SUCCESS} Database connection successful!\n")
            conn.close()
        else:
            print(f"{Style.ERROR} Failed to connect to database. Please check credentials.\n")
            return

    except KeyboardInterrupt:
        print("\nAuthentication cancelled.")
        return
    
    input(f"{Style.CYAN}>{Style.RESET} Press Enter to continue...")
    
    while True:
        display_menu()
        choice = input(f"{Style.CYAN}>{Style.RESET} Select an option: ").strip().lower()
        
        if choice == '1':
            view_dao_proposals_by_user()
        elif choice == '2':
            list_businesses_after_date()
        elif choice == '3':
            total_land_sales_last_quarter()
        elif choice == '4':
            search_events_by_name()
        elif choice == '5':
            voter_influence_report()
        elif choice == '6':
            register_new_business()
        elif choice == '7':
            record_asset_sale()
        elif choice == '8':
            reschedule_event()
        elif choice == '9':
            delete_user()
        elif choice == '10':
            custom_sql_query()
        elif choice == 'q':
            print(f"\n{Style.CYAN}{'═' * 80}{Style.RESET}")
            print(f"{Style.MAGENTA}{Style.BOLD}{'Thank you for using Decentraland DBMS!':^80}{Style.RESET}")
            print(f"{Style.GREEN}{'Goodbye!':^80}{Style.RESET}")
            print(f"{Style.CYAN}{'═' * 80}{Style.RESET}\n")
            break
        else:
            print(f"\n{Style.ERROR} Invalid option. Please try again.")
        
        input(f"\n{Style.CYAN}>{Style.RESET} Press Enter to continue...")


if __name__ == "__main__":
    main()
