import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
from mysql.connector import Error


# Color scheme
COLORS = {
    'primary': '#2D3E50',     # Dark blue
    'secondary': '#3498DB',   # Light blue
    'background': '#4CAF50',  # Green background
    'text': '#2C3E50',       # Dark gray
    'white': '#FFFFFF',      # White
    'error': '#E74C3C',      # Red
    'success': '#2ECC71'     # Green
}

# Constants
AVAILABLE_PORTS = [
    "Batangas", "Calapan", "Bulalacao", "Caticlan", 
    "Dumangas", "Banago", "Dumaguete", "Dapitan"
]

VEHICLE_TYPES = ["Car", "Van", "Truck", "Motorcycle"]

# In-memory storage
users = {
    'admin': 'admin123',
    'test': 'test123'
}

shipments = []

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'xander123!',  # Use your MySQL password
    'database': 'shipping'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Could not connect to database: {e}")
        return None

def center_window(window):
    """Center any window on the screen"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f'+{x}+{y}')

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("Shipping Management System")
        self.geometry("1000x600")  # Increased width to accommodate the layout
        self.configure(bg='#FFE4E1')  # Light pink background
        
        # Create left panel frame (for ship image)
        self.left_panel = tk.Frame(
            self,
            bg='white',
            width=500
        )
        self.left_panel.pack(side='left', fill='both', expand=True)
        
        # Load and display the ship logo
        try:
            from PIL import Image, ImageTk
            
            # Use the full path to the image
            image_path = r"C:\Users\kujo7\OneDrive\Desktop\JAVA THE HUTT\Curry\src\img\for img and icons\Black Modern Cargo Vessel Ship Design Logo Template.png"
            
            print(f"Attempting to load image from: {image_path}")
            
            # Load and resize the image
            original_image = Image.open(image_path)
            
            # Get the left panel's size
            self.left_panel.update()
            panel_width = self.left_panel.winfo_width()
            panel_height = self.left_panel.winfo_height()
            
            # Calculate size to maintain aspect ratio while fitting the panel
            # Use 80% of the panel width to leave some margin
            target_width = int(panel_width * 0.8)
            aspect_ratio = original_image.width / original_image.height
            target_height = int(target_width / aspect_ratio)
            
            # If the height is too large, scale based on height instead
            if target_height > panel_height * 0.6:  # Use 60% of panel height
                target_height = int(panel_height * 0.6)
                target_width = int(target_height * aspect_ratio)
            
            resized_image = original_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            self.ship_img = ImageTk.PhotoImage(resized_image)
            
            # Create a label to display the image
            ship_label = tk.Label(
                self.left_panel,
                image=self.ship_img,
                bg='white'
            )
            ship_label.place(relx=0.5, rely=0.5, anchor='center')
            
            # Add dots above and below the image with more spacing
            tk.Label(
                self.left_panel,
                text="...................",
                font=('Arial', 24),
                bg='white',
                fg='black'
            ).place(relx=0.5, rely=0.15, anchor='center')  # Moved up
            
            tk.Label(
                self.left_panel,
                text="...................",
                font=('Arial', 24),
                bg='white',
                fg='black'
            ).place(relx=0.5, rely=0.85, anchor='center')  # Moved down
            
        except Exception as e:
            print(f"Error loading image: {e}")
            error_msg = f"Failed to load image: {str(e)}"
            messagebox.showerror("Error", error_msg)
            
            # Fallback text in case image fails to load
            tk.Label(
                self.left_panel,
                text="Shipping\nManagement\nSystem",
                font=('Arial', 24),
                bg='white'
            ).place(relx=0.5, rely=0.5, anchor='center')
        
        # Create right panel frame
        self.right_panel = tk.Frame(
            self,
            bg='#FFB6C1',  # Light pink
            width=500
        )
        self.right_panel.pack(side='right', fill='both', expand=True)
        
        # Add Admin and Exit buttons at top right
        button_frame = tk.Frame(self.right_panel, bg='#FFB6C1')
        button_frame.place(relx=1.0, rely=0, anchor='ne', x=-10, y=10)
        
        tk.Button(
            button_frame,
            text="Admin",
            bg='white',
            command=lambda: self.show_admin_login()
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Exit",
            bg='#FF9999',
            command=self.quit
        ).pack(side='left')
        
        # Create main content frame
        content_frame = tk.Frame(
            self.right_panel,
            bg='#FFB6C1'
        )
        content_frame.place(relx=0.5, rely=0.4, anchor='center')
        
        # Heading
        tk.Label(
            content_frame,
            text="LOGIN",
            font=('Helvetica', 24, 'bold'),
            bg='#FFB6C1',
            fg='white'
        ).pack(pady=(0, 40))
        
        # Username
        tk.Label(
            content_frame,
            text="Username",
            font=('Helvetica', 12),
            bg='#FFB6C1',
            fg='white'
        ).pack(anchor='w')
        
        self.username_entry = tk.Entry(
            content_frame,
            font=('Helvetica', 12),
            width=25,
            bg='white',
            fg='black'
        )
        self.username_entry.pack()
        
        # Username underline
        tk.Frame(
            content_frame,
            height=2,
            width=200,
            bg='white'
        ).pack(pady=(0, 20))
        
        # Password
        tk.Label(
            content_frame,
            text="Password",
            font=('Helvetica', 12),
            bg='#FFB6C1',
            fg='white'
        ).pack(anchor='w')
        
        self.password_entry = tk.Entry(
            content_frame,
            font=('Helvetica', 12),
            width=25,
            show="•",
            bg='white',
            fg='black'
        )
        self.password_entry.pack()
        
        # Password underline
        tk.Frame(
            content_frame,
            height=2,
            width=200,
            bg='white'
        ).pack(pady=(0, 10))

        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        tk.Checkbutton(
            content_frame,
            text="show password",
            variable=self.show_password_var,
            bg='#FFB6C1',
            fg='white',
            selectcolor='#FFB6C1',
            command=self.toggle_password_visibility
        ).pack(pady=(0, 20))

        # Login button
        login_button = tk.Button(
            content_frame,
            text="Login",
            bg='white',
            width=20,
            command=self.login
        )
        login_button.pack(pady=(0, 20))

        # Register link
        register_label = tk.Label(
            content_frame,
            text="New user? Register here",
            font=('Helvetica', 10, 'underline'),
            bg='#FFB6C1',
            fg='white',
            cursor="hand2"
        )
        register_label.pack()
        register_label.bind("<Button-1>", lambda e: self.show_register())

        # Center window
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        conn = get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM login WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            
            if result:
                self.withdraw()
                ClientDashboard(username)
            else:
                messagebox.showerror("Error", "Invalid credentials!")
                
        except Error as e:
            messagebox.showerror("Database Error", f"Login failed: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def show_register(self):
        RegisterWindow(self)

    def show_admin_login(self):
        AdminLoginWindow(self)

    def quit(self):
        self.destroy()

    def clear_login_fields(self):
        """Clear username and password entry fields"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.show_password_var.set(False)  # Reset show password checkbox
        self.password_entry.config(show="•")  # Reset password masking

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Register New User")
        self.geometry("400x500")
        self.configure(bg=COLORS['background'])
        
        # Create main container
        main_frame = ttk.Frame(self, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Heading
        ttk.Label(main_frame,
                 text="Create Account",
                 font=('Helvetica', 24, 'bold')).pack(pady=(0, 30))
        
        # Username
        ttk.Label(main_frame,
                 text="Username",
                 font=('Helvetica', 12)).pack(anchor='w', pady=(0, 5))
        self.username_entry = ttk.Entry(main_frame, width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Password
        ttk.Label(main_frame,
                 text="Password",
                 font=('Helvetica', 12)).pack(anchor='w', pady=(0, 5))
        self.password_entry = ttk.Entry(main_frame, show="•", width=30)
        self.password_entry.pack(fill=tk.X, pady=(0, 30))
        
        # Register Button
        ttk.Button(main_frame,
                  text="Register",
                  style='Custom.TButton',
                  command=self.register).pack(fill=tk.X)
        
        # Center the window
        center_window(self)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        conn = get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            
            # Check if username already exists
            check_query = "SELECT * FROM login WHERE username = %s"
            cursor.execute(check_query, (username,))
            
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists! Choose another one")
                return
                
            # Insert new user
            insert_query = "INSERT INTO login (username, password) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, password))
            conn.commit()
            
            messagebox.showinfo("Success", "Registration successful!")
            self.destroy()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Registration failed: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

class ClientDashboard(tk.Toplevel):
    def __init__(self, username):
        super().__init__()
        self.username = username
        
        self.title(f"Dashboard - {username}")
        self.geometry("800x600")
        self.configure(bg=COLORS['background'])
        
        # Create main container
        main_frame = ttk.Frame(self, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Heading
        ttk.Label(main_frame,
                 text=f"Welcome, {username}",
                 font=('Helvetica', 24, 'bold')).pack(pady=(0, 30))
        
        # Buttons
        ttk.Button(main_frame,
                  text="Submit Shipment",
                  style='Custom.TButton',
                  command=self.show_shipment_form).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(main_frame,
                  text="View Shipments",
                  style='Custom.TButton',
                  command=self.view_shipments).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(main_frame,
                  text="Logout",
                  style='Custom.TButton',
                  command=self.logout).pack(fill=tk.X)
        
        # Center the window
        center_window(self)

    def show_shipment_form(self):
        ShipmentForm(self, self.username)

    def view_shipments(self):
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            # Fetch shipments for the specific user
            query = """SELECT submission_date, shipment_from, shipment_to, 
                       vehicle_type, status_ship 
                       FROM shipmentsubmission 
                       WHERE user_name = %s"""
            cursor.execute(query, (self.username,))
            user_shipments = cursor.fetchall()
            
            if user_shipments:
                # Convert database results to dictionary format expected by ShipmentListWindow
                formatted_shipments = []
                for shipment in user_shipments:
                    formatted_shipments.append({
                        'date': shipment[0],
                        'from': shipment[1],
                        'to': shipment[2],
                        'vehicle': shipment[3],
                        'status': shipment[4]
                    })
                ShipmentListWindow(self, formatted_shipments)
            else:
                messagebox.showinfo("Info", "No shipments found")
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch shipments: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def logout(self):
        # Get reference to the root window before destroying this window
        root = self.master
        self.destroy()
        # Show the original login window and clear the fields
        root.deiconify()  # Show the original login window
        root.clear_login_fields()  # Clear the login fields

class AdminDashboard(tk.Toplevel):
    def __init__(self):
        super().__init__()
        
        self.title("Admin Dashboard")
        self.geometry("1000x600")
        self.configure(bg=COLORS['background'])
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        
        # Create Manage Users tab
        self.manage_users_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.manage_users_tab, text='Manage Users')
        
        # Create Manage Shipments tab
        self.manage_shipments_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.manage_shipments_tab, text='Manage Shipments')
        
        # Create Schedules tab
        self.schedules_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.schedules_tab, text='Schedules')
        
        # Setup tabs
        self.setup_manage_users_tab()
        self.setup_manage_shipments_tab()
        self.setup_schedules_tab()
        
        # Center the window
        center_window(self)
        
        # Add Logout button to bottom right
        self.logout_btn = ttk.Button(
            self,
            text="Logout",
            style='Danger.TButton',
            command=self.logout_action
        )
        self.logout_btn.pack(side='bottom', anchor='se', padx=10, pady=10)

    def setup_manage_users_tab(self):
        # Create frame for user list
        list_frame = ttk.Frame(self.manage_users_tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create Treeview for users
        columns = ("Username", "Password")
        self.users_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.users_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create control frame
        control_frame = ttk.Frame(self.manage_users_tab)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Delete button
        ttk.Button(
            control_frame,
            text="Delete User",
            command=self.delete_user
        ).pack(side='left', padx=5)
        
        # Load users
        self.load_users()

    def load_users(self):
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT username, password FROM login")
            users = cursor.fetchall()
            
            # Clear existing items
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            # Add users to treeview
            for user in users:
                self.users_tree.insert("", "end", values=user)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load users: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def delete_user(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
            
        # Get values from selected row
        values = self.users_tree.item(selected_item)['values']
        username = values[0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}'?"):
            conn = get_db_connection()
            if not conn:
                return
                
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM login WHERE username = %s", (username,))
                conn.commit()
                
                # Remove from treeview
                self.users_tree.delete(selected_item)
                messagebox.showinfo("Success", "User deleted successfully")
                
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to delete user: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

    def check_duplicate_cargo_entry(self, username, phone_number, cargo_table):
        """Check if a shipment is already assigned to a specific cargo"""
        conn = get_db_connection()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            query = f"SELECT COUNT(*) as count FROM {cargo_table} WHERE user_name = %s AND phone_number = %s"
            cursor.execute(query, (username, phone_number))
            
            result = cursor.fetchone()
            return result[0] > 0
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error checking for duplicates: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def assign_to_cargo(self, cargo_type):
        """Assign a shipment to a specific cargo"""
        # Get selected row from shipment table
        selected_item = self.shipment_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", f"Please select a shipment to assign to {cargo_type}")
            return
            
        # Get values from selected row
        values = self.shipment_tree.item(selected_item)['values']
        username = values[0]
        phone_number = values[1]
        vehicle_type = values[4]
        
        # Convert cargo_type to table name (e.g., "Cargo 1" -> "cargo_1")
        cargo_table = cargo_type.lower().replace(" ", "_")
        
        # Check for duplicate entries
        if self.check_duplicate_cargo_entry(username, phone_number, cargo_table):
            messagebox.showwarning("Duplicate Entry", f"This shipment is already assigned to {cargo_type}!")
            return
            
        conn = get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            
            # Update shipmentsubmission table
            update_query = """UPDATE shipmentsubmission 
                            SET cargo = %s 
                            WHERE user_name = %s AND phone_number = %s"""
            cursor.execute(update_query, (cargo_type, username, phone_number))
            
            # Insert into cargo-specific table
            insert_query = f"""INSERT INTO {cargo_table} 
                             (user_name, phone_number, vehicle_type) 
                             VALUES (%s, %s, %s)"""
            cursor.execute(insert_query, (username, phone_number, vehicle_type))
            
            conn.commit()
            
            # Update treeview
            values = list(values)
            values[7] = cargo_type  # Update cargo column
            self.shipment_tree.item(selected_item, values=values)
            
            messagebox.showinfo("Success", f"Shipment successfully assigned to {cargo_type}")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to assign cargo: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def setup_manage_shipments_tab(self):
        # Create frame for shipment list
        list_frame = ttk.Frame(self.manage_shipments_tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create Treeview for shipments with updated columns including Cargo
        columns = ("Username", "Phone No", "From", "To", "Vehicle Type", "Date", "Status", "Cargo")
        self.shipment_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            self.shipment_tree.heading(col, text=col)
            self.shipment_tree.column(col, width=100)  # Adjust width as needed
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.shipment_tree.yview)
        self.shipment_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.shipment_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create control frame
        control_frame = ttk.Frame(self.manage_shipments_tab)
        control_frame.pack(side='right', fill='y', padx=10, pady=10)
        
        # Delete button
        ttk.Button(
            control_frame,
            text="Delete Shipment",
            command=self.delete_shipment
        ).pack(pady=5)
        
        # Status dropdown
        self.status_var = tk.StringVar()
        status_options = ["Preparing Shipment", "Left the Department", "On the way", 
                         "Arrived at the port", "Ready for pickup", "Done"]
        self.status_combo = ttk.Combobox(
            control_frame,
            textvariable=self.status_var,
            values=status_options,
            state='readonly'
        )
        self.status_combo.pack(pady=5)
        
        # Update button
        ttk.Button(
            control_frame,
            text="Update Status",
            command=self.update_shipment_status
        ).pack(pady=5)
        
        # Add cargo assignment buttons
        cargo_frame = ttk.LabelFrame(control_frame, text="Assign to Cargo")
        cargo_frame.pack(pady=10, padx=5, fill='x')
        
        for i in range(1, 4):
            btn = ttk.Button(
                cargo_frame,
                text=f"Cargo {i}",
                command=lambda x=i: self.assign_to_cargo(f"Cargo {x}")
            )
            btn.pack(pady=2, padx=5, fill='x')
        
        # Load shipments
        self.load_shipments()

    def load_shipments(self):
        """Load all shipments into the treeview"""
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_name, phone_number, shipment_from, shipment_to, 
                       vehicle_type, submission_date, status_ship, cargo
                FROM shipmentsubmission
            """)
            shipments = cursor.fetchall()
            
            # Clear existing items
            for item in self.shipment_tree.get_children():
                self.shipment_tree.delete(item)
            
            # Add shipments to treeview
            for shipment in shipments:
                self.shipment_tree.insert("", "end", values=shipment)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load shipments: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def update_shipment_status(self):
        selected_item = self.shipment_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a shipment to update")
            return
            
        new_status = self.status_var.get()
        if not new_status:
            messagebox.showwarning("Warning", "Please select a status")
            return
            
        # Get values from selected row
        values = self.shipment_tree.item(selected_item)['values']
        username = values[0]
        phone = values[1]
        
        conn = get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            query = "UPDATE shipmentsubmission SET status_ship = %s WHERE user_name = %s AND phone_number = %s"
            cursor.execute(query, (new_status, username, phone))
            conn.commit()
            
            # Update treeview
            values = list(values)
            values[6] = new_status
            self.shipment_tree.item(selected_item, values=values)
            
            messagebox.showinfo("Success", "Shipment status updated successfully!")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to update status: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def delete_shipment(self):
        """Delete selected shipment from database and treeview"""
        selected_item = self.shipment_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a shipment to delete")
            return
            
        values = self.shipment_tree.item(selected_item)['values']
        username = values[0]
        phone_number = values[1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete shipment for '{username}'?"):
            conn = get_db_connection()
            if not conn:
                return
                
            try:
                cursor = conn.cursor()
                query = """DELETE FROM shipmentsubmission 
                          WHERE user_name = %s AND phone_number = %s"""
                cursor.execute(query, (username, phone_number))
                conn.commit()
                
                # Remove from treeview
                self.shipment_tree.delete(selected_item)
                messagebox.showinfo("Success", "Shipment deleted successfully")
                
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to delete shipment: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

    def logout_action(self):
        """Handles logout action"""
        confirm = messagebox.askyesno(
            "Select",
            "Do you want to logout??",
            icon='warning'
        )
        
        if confirm:
            # Close admin dashboard
            self.destroy()
            
            # Show the existing login window
            self.master.deiconify()  # This shows the original login window
            
            # Clear any existing entries in login window if needed
            if hasattr(self.master, 'username_entry'):
                self.master.username_entry.delete(0, 'end')
            if hasattr(self.master, 'password_entry'):
                self.master.password_entry.delete(0, 'end')

    def setup_schedules_tab(self):
        # Create frame for schedule list
        list_frame = ttk.Frame(self.schedules_tab)
        list_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Create Treeview for schedules
        columns = ("Location", "Schedules", "Travel Time", "Status")
        self.schedule_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            self.schedule_tree.heading(col, text=col)
            self.schedule_tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.schedule_tree.yview)
        self.schedule_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.schedule_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create control frame
        control_frame = ttk.Frame(self.schedules_tab)
        control_frame.pack(side='right', fill='y', padx=10, pady=10)
        
        # Status dropdown
        ttk.Label(control_frame, text="Status:").pack(pady=(0, 5))
        self.schedule_status_var = tk.StringVar()
        self.schedule_status_combo = ttk.Combobox(
            control_frame,
            textvariable=self.schedule_status_var,
            values=["Available", "Not Available"],
            state='readonly'
        )
        self.schedule_status_combo.pack(pady=(0, 10))
        
        # Update button
        ttk.Button(
            control_frame,
            text="Update Status",
            command=self.update_schedule_status
        ).pack(pady=(0, 10))
        
        # Available Cargos button
        self.available_cargos_btn = ttk.Button(
            control_frame,
            text="Available Cargos",
            command=self.jButton1ActionPerformed
        )
        self.available_cargos_btn.pack(pady=(0, 10))
        
        # Load schedules
        self.load_schedules()

    def load_schedules(self):
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT location_from, location_to, time_ship, status_ship FROM schedules")
            schedules = cursor.fetchall()
            
            # Clear existing items
            for item in self.schedule_tree.get_children():
                self.schedule_tree.delete(item)
            
            # Add schedules to treeview
            for schedule in schedules:
                self.schedule_tree.insert("", "end", values=schedule)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load schedules: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def update_schedule_status(self):
        selected_item = self.schedule_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a schedule to update")
            return
            
        new_status = self.schedule_status_var.get()
        if not new_status:
            messagebox.showwarning("Warning", "Please select a status")
            return
            
        # Get values from selected row
        values = self.schedule_tree.item(selected_item)['values']
        location = values[0]  # Location is in the first column
        
        conn = get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            query = "UPDATE schedules SET status_ship = %s WHERE location_from = %s"
            cursor.execute(query, (new_status, location))
            conn.commit()
            
            # Update treeview
            values = list(values)
            values[3] = new_status  # Status is in the fourth column
            self.schedule_tree.item(selected_item, values=values)
            
            messagebox.showinfo("Success", "Schedule status updated successfully!")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to update status: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def jButton1ActionPerformed(self, evt=None):
        """Opens the Cargos Dashboard"""
        CargosDashboard()

class ShipmentForm(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.username = username
        
        self.title("Shipment Submission")
        self.geometry("860x540")
        self.configure(bg=COLORS['background'])
        self.resizable(False, False)
        
        # Create main panels
        self.create_panels()
        self.setup_form()
        
        # Center the window
        center_window(self)

    def create_panels(self):
        # Left panel for branding
        self.left_panel = tk.Frame(self, bg=COLORS['background'], width=270)
        self.left_panel.pack(side='left', fill='y')
        self.left_panel.pack_propagate(False)
        
        # Right panel for form
        self.right_panel = tk.Frame(self, bg=COLORS['background'], width=590)
        self.right_panel.pack(side='right', fill='both', expand=True)
        
        # Branding labels
        tk.Label(
            self.left_panel, 
            text="Shipment",
            font=("Viner Hand ITC", 24, "italic"),
            fg=COLORS['white'],
            bg=COLORS['background']
        ).place(x=40, y=50)
        
        tk.Label(
            self.left_panel,
            text="Form",
            font=("Viner Hand ITC", 24, "italic"),
            fg=COLORS['white'],
            bg=COLORS['background']
        ).place(x=130, y=160)
        
    def setup_form(self):
        # Create form frame
        self.form_frame = tk.Frame(self.right_panel, bg=COLORS['white'])
        self.form_frame.place(x=50, y=56, width=300, height=300)
        
        # Form fields
        labels = ['User:', 'Phone Number:', 'Shipment From:', 'Shipment To:', 'Type of Vehicle:']
        self.entries = {}
        
        # Form fields with white backgrounds
        for i, label in enumerate(labels):
            tk.Label(
                self.form_frame,
                text=label,
                font=("Segoe UI", 11, "bold"),
                bg=COLORS['white'],
                fg=COLORS['text']
            ).place(x=23, y=18 + i*60)
        
        # Style entries with white background
        entry_config = {'bg': COLORS['white'], 'fg': COLORS['text']}
        
        # User entry
        self.entries['user'] = tk.Entry(self.form_frame, width=15, **entry_config)
        self.entries['user'].insert(0, self.username)
        self.entries['user'].configure(state='readonly')
        self.entries['user'].place(x=23, y=44)
        
        # Phone entry
        self.entries['phone'] = tk.Entry(self.form_frame, width=15, **entry_config)
        self.entries['phone'].place(x=177, y=44)
        
        # From dropdown
        self.entries['from'] = ttk.Combobox(
            self.form_frame, 
            values=AVAILABLE_PORTS,
            width=12
        )
        self.entries['from'].place(x=177, y=104)
        
        # To dropdown
        self.entries['to'] = ttk.Combobox(
            self.form_frame,
            values=AVAILABLE_PORTS,
            width=12
        )
        self.entries['to'].place(x=177, y=148)
        
        # Vehicle type dropdown
        self.entries['vehicle'] = ttk.Combobox(
            self.form_frame,
            values=VEHICLE_TYPES,
            width=12
        )
        self.entries['vehicle'].place(x=177, y=216)
        
        # Buttons
        tk.Button(
            self.form_frame,
            text="Submit",
            bg='#FFFFCC',
            font=("Segoe UI", 9, "bold"),
            command=self.submit_shipment
        ).place(x=207, y=256)
        
        tk.Button(
            self.right_panel,
            text="View Schedule",
            font=("Segoe UI", 9, "bold"),
            command=self.view_schedule
        ).place(x=470, y=20)
        
        tk.Button(
            self.right_panel,
            text="Cancel",
            font=("Segoe UI", 9, "bold"),
            command=self.destroy
        ).place(x=490, y=400)

    def submit_shipment(self):
        # Validation
        if not self.entries['phone'].get().isdigit():
            messagebox.showerror("Error", "Phone number should contain only digits")
            return
            
        if self.entries['from'].get() == self.entries['to'].get():
            messagebox.showerror("Error", "Shipment from and to locations cannot be the same")
            return
            
        # Get connection
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            # Insert into shipmentsubmission table (matching your Java admin dashboard table)
            query = """INSERT INTO shipmentsubmission 
                      (user_name, phone_number, shipment_from, shipment_to, 
                       vehicle_type, submission_date, status_ship, cargo)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                      
            values = (
                self.username,
                self.entries['phone'].get(),
                self.entries['from'].get(),
                self.entries['to'].get(),
                self.entries['vehicle'].get(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Pending',  # Initial status
                None  # Initial cargo assignment
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            # Show confirmation
            receipt = f"""
Shipment Confirmation Receipt
-------------------------
Username: {self.username}
Phone Number: {self.entries['phone'].get()}
From: {self.entries['from'].get()}
To: {self.entries['to'].get()}
Vehicle Type: {self.entries['vehicle'].get()}
-------------------------
Shipment submitted successfully!
            """
            
            messagebox.showinfo("Success", receipt)
            self.destroy()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to submit shipment: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def view_schedule(self):
        ScheduleWindow(self)

class ShipmentListWindow(tk.Toplevel):
    def __init__(self, parent, shipments_list):
        super().__init__(parent)
        
        # Add parameter to check if user is admin
        self.is_admin = isinstance(parent, AdminDashboard)
        
        self.title("Shipments")
        self.geometry("900x600")
        self.configure(bg=COLORS['background'])
        
        # Add shipment status options (only used by admin)
        self.status_options = [
            "Preparing Shipment",
            "Left the Facility",
            "On the Way",
            "Arrived at the Port",
            "Ready for Pickup",
            "Done"
        ]
        
        # Create main container
        main_frame = ttk.Frame(self, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Heading
        ttk.Label(main_frame,
                 text="Shipment History",
                 font=('Helvetica', 24, 'bold')).pack(pady=(0, 30))
        
        # Create Treeview
        columns = ("Date", "From", "To", "Vehicle", "Status")
        self.tree = ttk.Treeview(main_frame,
                                columns=columns,
                                show="headings",
                                height=15)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame,
                                orient="vertical",
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.tree.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add data
        for shipment in shipments_list:
            self.tree.insert("", "end", values=(
                shipment['date'],
                shipment['from'],
                shipment['to'],
                shipment['vehicle'],
                shipment['status']
            ))
        
        # After adding all shipments to the tree, add admin controls if user is admin
        if self.is_admin:
            # Add status update frame
            status_frame = ttk.Frame(main_frame)
            status_frame.pack(pady=20, fill=tk.X)
            
            # Status dropdown
            self.status_var = tk.StringVar()
            self.status_dropdown = ttk.Combobox(
                status_frame,
                textvariable=self.status_var,
                values=self.status_options,
                state='readonly',
                width=20
            )
            self.status_dropdown.pack(side=tk.LEFT, padx=5)
            
            # Update status button
            ttk.Button(
                status_frame,
                text="Update Status",
                style='Custom.TButton',
                command=self.update_status
            ).pack(side=tk.LEFT, padx=5)
        
        # Close button
        ttk.Button(
            main_frame,
            text="Close",
            style='Custom.TButton',
            command=self.destroy
        ).pack(pady=10)
        
        # Center the window
        center_window(self)

    def update_status(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a shipment to update")
            return
            
        new_status = self.status_var.get()
        if not new_status:
            messagebox.showwarning("Warning", "Please select a status")
            return
            
        # Update treeview
        current_values = list(self.tree.item(selected_item)['values'])
        current_values[4] = new_status  # Update status column
        self.tree.item(selected_item, values=current_values)
        
        # Update shipments list
        date = current_values[0]
        for shipment in shipments:
            if shipment['date'] == date:
                shipment['status'] = new_status
                break
        
        messagebox.showinfo("Success", "Shipment status updated successfully")

class ScheduleWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("View Schedules")
        self.geometry("800x500")
        self.configure(bg=COLORS['background'])
        
        # Create main container with pink background
        main_frame = tk.Frame(self, bg='#FFB6C1')  # Light pink background
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Heading
        tk.Label(
            main_frame,
            text="Schedule Information",
            font=('Helvetica', 24, 'bold'),
            bg='#FFB6C1',
            fg='white'
        ).pack(pady=(0, 20))
        
        # Create Treeview for schedules
        columns = ("Location From", "Location To", "Time", "Status")
        self.schedule_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            self.schedule_tree.heading(col, text=col)
            self.schedule_tree.column(col, width=150, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.schedule_tree.yview)
        self.schedule_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.schedule_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#FFB6C1')
        button_frame.pack(fill='x', pady=10)
        
        # Close button
        tk.Button(
            button_frame,
            text="Close",
            bg='white',
            width=20,
            command=self.destroy
        ).pack(pady=10)
        
        # Load schedules
        self.load_schedules()
        
        # Center the window
        center_window(self)

    def load_schedules(self):
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT location_from, location_to, time_ship, status_ship 
                FROM schedules
            """)
            schedules = cursor.fetchall()
            
            # Clear existing items
            for item in self.schedule_tree.get_children():
                self.schedule_tree.delete(item)
            
            # Add schedules to treeview
            for schedule in schedules:
                self.schedule_tree.insert("", "end", values=schedule)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load schedules: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

class AdminLoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Admin Login")
        self.geometry("400x500")
        self.configure(bg=COLORS['background'])
        
        # Create main container
        main_frame = ttk.Frame(self, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Heading
        ttk.Label(main_frame,
                 text="Admin Login",
                 font=('Helvetica', 24, 'bold')).pack(pady=(0, 30))
        
        # Username
        ttk.Label(main_frame,
                 text="Admin Username",
                 font=('Helvetica', 12)).pack(anchor='w', pady=(0, 5))
        self.username_entry = ttk.Entry(main_frame, width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Password
        ttk.Label(main_frame,
                 text="Admin Password",
                 font=('Helvetica', 12)).pack(anchor='w', pady=(0, 5))
        self.password_entry = ttk.Entry(main_frame, show="•", width=30)
        self.password_entry.pack(fill=tk.X, pady=(0, 30))
        
        # Login Button
        ttk.Button(main_frame,
                  text="Login as Admin",
                  style='Custom.TButton',
                  command=self.admin_login).pack(fill=tk.X)
        
        # Center the window
        center_window(self)

    def admin_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if username == 'admin' and password == users['admin']:
            self.master.withdraw()  # Hide the main login window
            self.destroy()  # Close the admin login window
            AdminDashboard()
        else:
            messagebox.showerror("Error", "Invalid admin credentials")

class CargosDashboard(tk.Toplevel):
    def __init__(self):
        super().__init__()
        
        self.title("Available Cargos")
        self.geometry("1000x600")
        self.configure(bg=COLORS['background'])
        
        # Create notebook for ship tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs for each ship
        self.create_ship_tab("Ship 1", "cargo_1")
        self.create_ship_tab("Ship 2", "cargo_2")
        self.create_ship_tab("Ship 3", "cargo_3")
        
        # Add Delete button frame
        self.create_control_panel()
        
        # Center window
        center_window(self)
        
    def create_ship_tab(self, ship_name, table_name):
        """Create a tab for each ship with its cargos"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=ship_name)
        
        # Create frame for table and controls
        table_frame = ttk.Frame(tab)
        table_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Create Treeview
        columns = ("Username", "Phone No", "Vehicle Type")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Store tree reference and load data
        setattr(self, f"tree_{table_name}", tree)
        self.load_ship_data(tree, table_name)
        
    def create_control_panel(self):
        """Create control panel with Delete and Back buttons"""
        control_frame = ttk.Frame(self)
        control_frame.pack(side='bottom', fill='x', padx=10, pady=5)
        
        # Delete button
        delete_btn = ttk.Button(
            control_frame,
            text="Delete",
            command=self.delete_selected
        )
        delete_btn.pack(side='left', padx=5)
        
        # Back button
        back_btn = ttk.Button(
            control_frame,
            text="Back",
            command=self.destroy
        )
        back_btn.pack(side='right', padx=5)
        
    def load_ship_data(self, tree, table_name):
        """Load cargos assigned to specific ship"""
        conn = get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT user_name, phone_number, vehicle_type 
                FROM {table_name}
                LIMIT 10
            """)
            
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
            
            # Add data to treeview
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load {table_name} data: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                
    def delete_selected(self):
        """Delete selected cargo entry"""
        try:
            # Get current tab
            current_tab = self.notebook.select()
            current_tab_index = self.notebook.index(current_tab)
            
            # Map tab index to correct cargo table name
            cargo_tables = {
                0: "cargo_1",
                1: "cargo_2",
                2: "cargo_3"
            }
            
            table_name = cargo_tables.get(current_tab_index)
            if not table_name:
                messagebox.showerror("Error", "Invalid cargo table selection")
                return
            
            tree = getattr(self, f"tree_{table_name}")
            
            # Get selected item
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a cargo to delete")
                return
            
            # Get values from selected item
            values = tree.item(selected_item)['values']
            if not values:
                messagebox.showerror("Error", "Could not retrieve cargo details.")
                return
            
            username = values[0]
            phone_number = values[1]
            
            # Confirm deletion
            if not messagebox.askyesno("Confirm", "Are you sure you want to delete this cargo?"):
                return
            
            conn = get_db_connection()
            if not conn:
                messagebox.showerror("Database Error", "Failed to connect to the database.")
                return
            
            try:
                cursor = conn.cursor()
                
                # Delete from cargo table
                cursor.execute(f"""
                    DELETE FROM {table_name} 
                    WHERE user_name = %s AND phone_number = %s
                """, (username, phone_number))
                
                # Delete from shipmentsubmission table
                cursor.execute("""
                    DELETE FROM shipmentsubmission 
                    WHERE user_name = %s AND phone_number = %s
                """, (username, phone_number))
                
                conn.commit()
                
                # Remove from treeview
                tree.delete(selected_item)
                messagebox.showinfo("Success", "Cargo and shipment deleted successfully")
                
                # Refresh the view
                self.load_ship_data(tree, table_name)
                
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to delete cargo: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
                
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def main():
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    main()