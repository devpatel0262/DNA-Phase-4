#!/usr/bin/env python3
"""
MINI WORLD - GENESIS CITY
GUI Application Interface (Python + Tkinter)

A modern, minimalist GUI for the Mini World database.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime
import decimal

# ============================================================================
# CONFIGURATION & THEME
# ============================================================================

THEME = {
    "bg_dark": "#121212",
    "bg_card": "#1E1E1E",
    "fg_primary": "#FFFFFF",
    "fg_secondary": "#B0B0B0",
    "accent": "#03DAC6",      # Teal/Cyan
    "accent_hover": "#018786",
    "error": "#CF6679",
    "success": "#03DAC6",
    "font_family": "Segoe UI" if "nt" == "os.name" else "Helvetica",
}

DB_CONFIG = {
    'host': 'localhost',
    'user': '',
    'password': '',
    'database': 'decentraland_db',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}

# ============================================================================
# HELPER CLASSES
# ============================================================================

class ModernButton(tk.Button):
    """Custom styled button to match the theme."""
    def __init__(self, master, text, command, bg=THEME["accent"], fg="#000000", **kwargs):
        super().__init__(master, text=text, command=command, 
                         bg=bg, fg=fg, 
                         activebackground=THEME["accent_hover"], activeforeground="#000000",
                         relief="flat", borderwidth=0, 
                         font=(THEME["font_family"], 10, "bold"),
                         padx=15, pady=8, cursor="hand2", **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.default_bg = bg

    def on_enter(self, e):
        self['bg'] = THEME["accent_hover"]

    def on_leave(self, e):
        self['bg'] = self.default_bg

class Card(tk.Frame):
    """A card-like container for content."""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=THEME["bg_card"], padx=20, pady=20, **kwargs)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class MiniWorldApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Genesis City | Management System")
        self.geometry("1200x800")
        self.configure(bg=THEME["bg_dark"])
        
        # Configure Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure("TFrame", background=THEME["bg_dark"])
        self.style.configure("Card.TFrame", background=THEME["bg_card"])
        
        self.style.configure("TLabel", background=THEME["bg_dark"], foreground=THEME["fg_primary"], font=(THEME["font_family"], 10))
        self.style.configure("Header.TLabel", font=(THEME["font_family"], 24, "bold"), foreground=THEME["accent"])
        self.style.configure("Subheader.TLabel", font=(THEME["font_family"], 14), foreground=THEME["fg_secondary"])
        self.style.configure("Card.TLabel", background=THEME["bg_card"], foreground=THEME["fg_primary"])
        
        self.style.configure("TNotebook", background=THEME["bg_dark"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=THEME["bg_card"], foreground=THEME["fg_secondary"], padding=[15, 10], font=(THEME["font_family"], 10))
        self.style.map("TNotebook.Tab", background=[("selected", THEME["accent"])], foreground=[("selected", "#000000")])
        
        self.style.configure("Treeview", 
                             background=THEME["bg_card"], 
                             foreground=THEME["fg_primary"], 
                             fieldbackground=THEME["bg_card"],
                             borderwidth=0,
                             font=(THEME["font_family"], 10))
        self.style.configure("Treeview.Heading", 
                             background=THEME["bg_dark"], 
                             foreground=THEME["fg_primary"], 
                             font=(THEME["font_family"], 10, "bold"),
                             relief="flat")
        self.style.map("Treeview", background=[('selected', THEME["accent"])], foreground=[('selected', '#000000')])

        self.conn = None
        self.show_login()

    def get_connection(self):
        try:
            conn = pymysql.connect(**DB_CONFIG)
            conn.autocommit = False
            return conn
        except pymysql.Error as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            return None

    def show_login(self):
        """Display the login screen."""
        self.login_frame = tk.Frame(self, bg=THEME["bg_dark"])
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo / Title
        ttk.Label(self.login_frame, text="GENESIS CITY", style="Header.TLabel").pack(pady=(0, 10))
        ttk.Label(self.login_frame, text="Database Management System", style="Subheader.TLabel").pack(pady=(0, 40))

        # Form
        form_frame = Card(self.login_frame)
        form_frame.pack(fill="x", ipadx=20)

        ttk.Label(form_frame, text="MySQL Username", style="Card.TLabel").pack(anchor="w", pady=(0, 5))
        self.user_entry = tk.Entry(form_frame, font=(THEME["font_family"], 12), bg="#2C2C2C", fg="white", insertbackground="white", relief="flat")
        self.user_entry.pack(fill="x", pady=(0, 20), ipady=5)

        ttk.Label(form_frame, text="MySQL Password", style="Card.TLabel").pack(anchor="w", pady=(0, 5))
        self.pass_entry = tk.Entry(form_frame, font=(THEME["font_family"], 12), bg="#2C2C2C", fg="white", insertbackground="white", relief="flat", show="•")
        self.pass_entry.pack(fill="x", pady=(0, 20), ipady=5)

        ModernButton(form_frame, text="CONNECT TO DATABASE", command=self.attempt_login).pack(fill="x", pady=10)
        
        ttk.Label(form_frame, text="Host: localhost", style="Card.TLabel", foreground=THEME["fg_secondary"], font=(THEME["font_family"], 8)).pack(pady=10)

    def attempt_login(self):
        user = self.user_entry.get().strip()
        password = self.pass_entry.get()

        DB_CONFIG['user'] = user
        DB_CONFIG['password'] = password

        self.conn = self.get_connection()
        if self.conn:
            self.login_frame.destroy()
            self.show_dashboard()

    def show_dashboard(self):
        """Display the main application dashboard."""
        # Sidebar
        # For simplicity in Tkinter, we'll use a Notebook (Tabbed interface) but styled nicely
        
        main_container = tk.Frame(self, bg=THEME["bg_dark"])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_container, bg=THEME["bg_dark"])
        header_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(header_frame, text="DASHBOARD", style="Header.TLabel").pack(side="left")
        
        status_frame = tk.Frame(header_frame, bg=THEME["bg_dark"])
        status_frame.pack(side="right")
        tk.Label(status_frame, text="● Connected", fg=THEME["success"], bg=THEME["bg_dark"]).pack(side="left", padx=10)
        ModernButton(status_frame, text="LOGOUT", command=self.logout, bg=THEME["error"], width=10).pack(side="left")

        # Tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True)

        self.tab_overview = ttk.Frame(self.notebook, style="TFrame")
        self.tab_explorer = ttk.Frame(self.notebook, style="TFrame")
        self.tab_operations = ttk.Frame(self.notebook, style="TFrame")
        self.tab_analytics = ttk.Frame(self.notebook, style="TFrame")

        self.notebook.add(self.tab_overview, text="  OVERVIEW  ")
        self.notebook.add(self.tab_explorer, text="  DATA EXPLORER  ")
        self.notebook.add(self.tab_operations, text="  OPERATIONS  ")
        self.notebook.add(self.tab_analytics, text="  ANALYTICS  ")

        self.build_overview_tab()
        self.build_explorer_tab()
        self.build_operations_tab()
        self.build_analytics_tab()

    def logout(self):
        if self.conn:
            self.conn.close()
        self.destroy()
        # Ideally restart app, but closing is fine for now

    # ========================================================================
    # TAB: OVERVIEW
    # ========================================================================
    def build_overview_tab(self):
        # Stats Cards
        stats_frame = tk.Frame(self.tab_overview, bg=THEME["bg_dark"])
        stats_frame.pack(fill="x", pady=20)
        
        self.create_stat_card(stats_frame, "Total Users", self.get_count("User_Profile"), 0)
        self.create_stat_card(stats_frame, "Land Parcels", self.get_count("LAND_Parcel"), 1)
        self.create_stat_card(stats_frame, "Businesses", self.get_count("Business"), 2)
        self.create_stat_card(stats_frame, "Proposals", self.get_count("DAO_Proposal"), 3)

        # Recent Activity
        ttk.Label(self.tab_overview, text="Recent Transactions", style="Subheader.TLabel").pack(anchor="w", pady=(20, 10))
        
        cols = ("Time", "Item", "Price", "Buyer")
        tree = ttk.Treeview(self.tab_overview, columns=cols, show="headings", height=10)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="x")

        # Load data
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT t.Timestamp, t.Asset_ID, t.Price, u.Username 
                    FROM Transaction t 
                    JOIN User_Profile u ON t.Buyer_Address = u.Wallet_Address 
                    ORDER BY t.Timestamp DESC LIMIT 10
                """)
                for row in cursor.fetchall():
                    tree.insert("", "end", values=(row['Timestamp'], row['Asset_ID'], f"{row['Price']:.2f} MANA", row['Username']))
        except Exception as e:
            print(e)

    def create_stat_card(self, parent, title, value, col):
        card = Card(parent)
        card.grid(row=0, column=col, padx=10, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        
        ttk.Label(card, text=title, style="Card.TLabel", foreground=THEME["fg_secondary"]).pack(anchor="w")
        ttk.Label(card, text=str(value), style="Card.TLabel", font=(THEME["font_family"], 28, "bold"), foreground=THEME["accent"]).pack(anchor="w")

    def get_count(self, table):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) as c FROM {table}")
                return cursor.fetchone()['c']
        except:
            return 0

    # ========================================================================
    # TAB: EXPLORER
    # ========================================================================
    def build_explorer_tab(self):
        control_frame = tk.Frame(self.tab_explorer, bg=THEME["bg_dark"])
        control_frame.pack(fill="x", pady=20)

        ttk.Label(control_frame, text="Select Table:").pack(side="left", padx=(0, 10))
        
        self.table_var = tk.StringVar()
        tables = ["User_Profile", "Digital_Asset", "LAND_Parcel", "Wearable", "Business", "Event", "Transaction", "DAO_Proposal", "Vote"]
        self.table_combo = ttk.Combobox(control_frame, textvariable=self.table_var, values=tables, state="readonly")
        self.table_combo.pack(side="left", padx=(0, 20))
        self.table_combo.bind("<<ComboboxSelected>>", self.load_table_data)
        self.table_combo.current(0)

        ModernButton(control_frame, text="Refresh", command=self.load_table_data, width=10).pack(side="left")

        # Treeview
        self.explorer_tree = ttk.Treeview(self.tab_explorer, show="headings")
        self.explorer_tree.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.explorer_tree, orient="vertical", command=self.explorer_tree.yview)
        self.explorer_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_table_data()

    def load_table_data(self, event=None):
        table = self.table_var.get()
        if not table: return

        # Clear tree
        self.explorer_tree.delete(*self.explorer_tree.get_children())
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table} LIMIT 100")
                rows = cursor.fetchall()
                
                if not rows:
                    return

                columns = list(rows[0].keys())
                self.explorer_tree["columns"] = columns
                
                for col in columns:
                    self.explorer_tree.heading(col, text=col)
                    self.explorer_tree.column(col, width=100)

                for row in rows:
                    values = [row[col] for col in columns]
                    self.explorer_tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ========================================================================
    # TAB: OPERATIONS
    # ========================================================================
    def build_operations_tab(self):
        container = tk.Frame(self.tab_operations, bg=THEME["bg_dark"])
        container.pack(fill="both", expand=True, padx=50, pady=20)

        # Operation Selection
        left_panel = tk.Frame(container, bg=THEME["bg_dark"], width=200)
        left_panel.pack(side="left", fill="y", padx=(0, 20))

        ttk.Label(left_panel, text="ACTIONS", style="Subheader.TLabel").pack(anchor="w", pady=(0, 10))

        ModernButton(left_panel, text="Register Business", command=lambda: self.show_form("business"), width=20).pack(pady=5)
        ModernButton(left_panel, text="Record Sale", command=lambda: self.show_form("sale"), width=20).pack(pady=5)
        ModernButton(left_panel, text="Delete User", command=lambda: self.show_form("delete"), bg=THEME["error"], width=20).pack(pady=5)

        # Form Area
        self.form_area = Card(container)
        self.form_area.pack(side="left", fill="both", expand=True)
        
        self.current_form_frame = None
        self.show_form("business")

    def show_form(self, form_type):
        if self.current_form_frame:
            self.current_form_frame.destroy()
        
        self.current_form_frame = tk.Frame(self.form_area, bg=THEME["bg_card"])
        self.current_form_frame.pack(fill="both", expand=True)

        if form_type == "business":
            self.build_business_form()
        elif form_type == "sale":
            self.build_sale_form()
        elif form_type == "delete":
            self.build_delete_form()

    def build_business_form(self):
        ttk.Label(self.current_form_frame, text="Register New Business", style="Header.TLabel", background=THEME["bg_card"]).pack(anchor="w", pady=(0, 20))
        
        self.entry_biz_name = self.create_input(self.current_form_frame, "Business Name")
        self.entry_biz_type = self.create_input(self.current_form_frame, "Type (Shop/Gallery/Venue/Service)")
        self.entry_biz_owner = self.create_input(self.current_form_frame, "Owner Address")
        
        ModernButton(self.current_form_frame, text="REGISTER BUSINESS", command=self.submit_business).pack(pady=20, anchor="w")

    def build_sale_form(self):
        ttk.Label(self.current_form_frame, text="Record Asset Sale", style="Header.TLabel", background=THEME["bg_card"]).pack(anchor="w", pady=(0, 20))
        
        self.entry_sale_asset = self.create_input(self.current_form_frame, "Asset ID")
        self.entry_sale_seller = self.create_input(self.current_form_frame, "Seller Address")
        self.entry_sale_buyer = self.create_input(self.current_form_frame, "Buyer Address")
        self.entry_sale_price = self.create_input(self.current_form_frame, "Price (MANA)")
        
        ModernButton(self.current_form_frame, text="RECORD TRANSACTION", command=self.submit_sale).pack(pady=20, anchor="w")

    def build_delete_form(self):
        ttk.Label(self.current_form_frame, text="Delete User Profile", style="Header.TLabel", background=THEME["bg_card"], foreground=THEME["error"]).pack(anchor="w", pady=(0, 20))
        ttk.Label(self.current_form_frame, text="Warning: This will cascade delete votes and proposals.", style="Card.TLabel", foreground=THEME["fg_secondary"]).pack(anchor="w", pady=(0, 20))
        
        self.entry_del_wallet = self.create_input(self.current_form_frame, "Wallet Address to Delete")
        
        ModernButton(self.current_form_frame, text="PERMANENTLY DELETE USER", command=self.submit_delete, bg=THEME["error"]).pack(pady=20, anchor="w")

    def create_input(self, parent, label):
        ttk.Label(parent, text=label, style="Card.TLabel").pack(anchor="w", pady=(10, 5))
        entry = tk.Entry(parent, font=(THEME["font_family"], 11), bg="#2C2C2C", fg="white", insertbackground="white", relief="flat")
        entry.pack(fill="x", ipady=5)
        return entry

    # --- Form Actions ---
    def submit_business(self):
        name = self.entry_biz_name.get()
        btype = self.entry_biz_type.get()
        owner = self.entry_biz_owner.get()
        
        if not all([name, btype, owner]):
            messagebox.showerror("Error", "All fields required")
            return

        try:
            with self.conn.cursor() as cursor:
                # Logic from main_app.py
                cursor.execute("SELECT Asset_ID FROM LAND_Parcel lp JOIN Digital_Asset da ON lp.Asset_ID = da.Asset_ID WHERE da.Owner_Address = %s LIMIT 1", (owner,))
                parcel = cursor.fetchone()
                
                if not parcel:
                    messagebox.showerror("Error", "User must own LAND to register business")
                    return
                
                cursor.execute("INSERT INTO Business (Business_Name, Business_Type, Owner_Address, Date_Established, Parcel_ID) VALUES (%s, %s, %s, CURDATE(), %s)",
                               (name, btype, owner, parcel['Asset_ID']))
                self.conn.commit()
                messagebox.showinfo("Success", "Business Registered!")
                self.entry_biz_name.delete(0, 'end')
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))

    def submit_sale(self):
        asset = self.entry_sale_asset.get()
        seller = self.entry_sale_seller.get()
        buyer = self.entry_sale_buyer.get()
        price = self.entry_sale_price.get()
        
        try:
            with self.conn.cursor() as cursor:
                import secrets
                tx_id = '0x' + secrets.token_hex(32)
                cursor.execute("INSERT INTO Transaction (Transaction_ID, Asset_ID, Seller_Address, Buyer_Address, Price, Currency, Timestamp) VALUES (%s, %s, %s, %s, %s, 'MANA', NOW())",
                               (tx_id, asset, seller, buyer, price))
                cursor.execute("UPDATE Digital_Asset SET Owner_Address = %s WHERE Asset_ID = %s", (buyer, asset))
                self.conn.commit()
                messagebox.showinfo("Success", "Sale Recorded!")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))

    def submit_delete(self):
        wallet = self.entry_del_wallet.get()
        if not messagebox.askyesno("Confirm", "Are you sure? This cannot be undone."):
            return
            
        try:
            with self.conn.cursor() as cursor:
                # Cascading logic handled by DB constraints mostly, but we do manual cleanup as per main_app.py
                cursor.execute("DELETE FROM Vote WHERE Voter_Address = %s", (wallet,))
                cursor.execute("DELETE FROM ATTENDS WHERE Wallet_Address = %s", (wallet,))
                cursor.execute("DELETE FROM DAO_Proposal WHERE Creator_Address = %s", (wallet,))
                cursor.execute("UPDATE Business SET Owner_Address = NULL WHERE Owner_Address = %s", (wallet,))
                cursor.execute("UPDATE Event SET Organizer_Address = NULL WHERE Organizer_Address = %s", (wallet,))
                cursor.execute("UPDATE Scene_Content SET Creator_Address = NULL WHERE Creator_Address = %s", (wallet,))
                cursor.execute("UPDATE Transaction SET Seller_Address = NULL WHERE Seller_Address = %s", (wallet,))
                cursor.execute("UPDATE Transaction SET Buyer_Address = NULL WHERE Buyer_Address = %s", (wallet,))
                cursor.execute("DELETE FROM User_Profile WHERE Wallet_Address = %s", (wallet,))
                self.conn.commit()
                messagebox.showinfo("Success", "User Deleted")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))

    # ========================================================================
    # TAB: ANALYTICS
    # ========================================================================
    def build_analytics_tab(self):
        ttk.Label(self.tab_analytics, text="Voter Influence Report", style="Header.TLabel").pack(anchor="w", pady=20)
        
        cols = ("Rank", "User", "Land Owned", "Votes Cast", "Influence Score")
        tree = ttk.Treeview(self.tab_analytics, columns=cols, show="headings", height=15)
        for col in cols:
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True, pady=(0, 20))

        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        u.Username,
                        COUNT(DISTINCT da.Asset_ID) as land,
                        COUNT(DISTINCT v.Proposal_ID) as votes,
                        (COUNT(DISTINCT da.Asset_ID) * 10 + COUNT(DISTINCT v.Proposal_ID)) as score
                    FROM User_Profile u
                    LEFT JOIN Digital_Asset da ON u.Wallet_Address = da.Owner_Address
                    LEFT JOIN LAND_Parcel lp ON da.Asset_ID = lp.Asset_ID
                    LEFT JOIN Vote v ON u.Wallet_Address = v.Voter_Address
                    GROUP BY u.Wallet_Address, u.Username
                    HAVING land > 0 OR votes > 0
                    ORDER BY score DESC
                    LIMIT 20
                """)
                for idx, row in enumerate(cursor.fetchall(), 1):
                    tree.insert("", "end", values=(idx, row['Username'], row['land'], row['votes'], row['score']))
        except:
            pass

if __name__ == "__main__":
    app = MiniWorldApp()
    app.mainloop()
