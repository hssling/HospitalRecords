import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import pandas as pd
from datetime import datetime
import os

class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1200x700")
        
        # Initialize Excel files
        self.excel_files = {
            'OPD': 'opd_records.xlsx',
            'IPD': 'ipd_records.xlsx',
            'OT': 'ot_records.xlsx',
            'Delivery': 'delivery_records.xlsx'
        }
        
        # Create Excel files if they don't exist
        self.initialize_excel_files()
        
        # Create main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tab_control = ttk.Notebook(self.main_container)
        
        # Create tabs for each department
        self.tabs = {}
        for dept in ['OPD', 'IPD', 'OT', 'Delivery']:
            self.tabs[dept] = ctk.CTkFrame(self.tab_control)
            self.tab_control.add(self.tabs[dept], text=dept)
        
        self.tab_control.pack(expand=True, fill="both")
        
        # Initialize each department's interface
        for dept in self.tabs:
            self.setup_department_interface(dept)
    
    def initialize_excel_files(self):
        for dept, filename in self.excel_files.items():
            if not os.path.exists(filename):
                if dept == 'OPD':
                    df = pd.DataFrame(columns=['Date', 'Patient_ID', 'Patient_Name', 'Age', 'Gender', 
                                             'Contact', 'Department', 'Doctor', 'Diagnosis', 'Treatment', 'Fee'])
                elif dept == 'IPD':
                    df = pd.DataFrame(columns=['Admission_Date', 'Patient_ID', 'Patient_Name', 'Age', 'Gender',
                                             'Contact', 'Room_No', 'Admission_Reason', 'Doctor', 'Discharge_Date', 'Status'])
                elif dept == 'OT':
                    df = pd.DataFrame(columns=['Date', 'Patient_ID', 'Patient_Name', 'Age', 'Gender',
                                             'Surgery_Type', 'Surgeon', 'Anesthetist', 'Start_Time', 'End_Time', 'Status'])
                else:  # Delivery
                    df = pd.DataFrame(columns=['Date', 'Patient_ID', 'Patient_Name', 'Age', 'Gender',
                                             'Delivery_Type', 'Doctor', 'Baby_Gender', 'Weight', 'Status'])
                df.to_excel(filename, index=False)
    
    def setup_department_interface(self, dept):
        frame = self.tabs[dept]
        
        # Create input fields
        input_frame = ctk.CTkFrame(frame)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Common fields for all departments
        common_fields = ['Patient_ID', 'Patient_Name', 'Age', 'Gender', 'Contact']
        
        # Department specific fields
        dept_fields = {
            'OPD': ['Department', 'Doctor', 'Diagnosis', 'Treatment', 'Fee'],
            'IPD': ['Room_No', 'Admission_Reason', 'Doctor', 'Status'],
            'OT': ['Surgery_Type', 'Surgeon', 'Anesthetist', 'Start_Time', 'End_Time', 'Status'],
            'Delivery': ['Delivery_Type', 'Doctor', 'Baby_Gender', 'Weight', 'Status']
        }
        
        # Create entry fields
        self.entries = {}
        row = 0
        col = 0
        
        for field in common_fields + dept_fields[dept]:
            label = ctk.CTkLabel(input_frame, text=field.replace('_', ' '))
            label.grid(row=row, column=col*2, padx=5, pady=5)
            
            entry = ctk.CTkEntry(input_frame)
            entry.grid(row=row, column=col*2+1, padx=5, pady=5)
            self.entries[field] = entry
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Add buttons
        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        add_btn = ctk.CTkButton(button_frame, text="Add Record", 
                               command=lambda: self.add_record(dept))
        add_btn.pack(side="left", padx=5)
        
        view_btn = ctk.CTkButton(button_frame, text="View Records", 
                                command=lambda: self.view_records(dept))
        view_btn.pack(side="left", padx=5)
        
        search_btn = ctk.CTkButton(button_frame, text="Search", 
                                  command=lambda: self.search_records(dept))
        search_btn.pack(side="left", padx=5)
    
    def add_record(self, dept):
        try:
            # Get current date
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Prepare record data
            record = {'Date': current_date}
            for field, entry in self.entries.items():
                record[field] = entry.get()
            
            # Read existing data
            df = pd.read_excel(self.excel_files[dept])
            
            # Append new record
            df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
            
            # Save to Excel
            df.to_excel(self.excel_files[dept], index=False)
            
            messagebox.showinfo("Success", "Record added successfully!")
            
            # Clear entries
            for entry in self.entries.values():
                entry.delete(0, tk.END)
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def view_records(self, dept):
        try:
            df = pd.read_excel(self.excel_files[dept])
            
            # Create new window for displaying records
            view_window = ctk.CTkToplevel(self.root)
            view_window.title(f"{dept} Records")
            view_window.geometry("1000x600")
            
            # Create treeview
            tree = ttk.Treeview(view_window)
            tree["columns"] = list(df.columns)
            tree["show"] = "headings"
            
            # Set column headings
            for column in df.columns:
                tree.heading(column, text=column.replace('_', ' '))
                tree.column(column, width=100)
            
            # Add data
            for _, row in df.iterrows():
                tree.insert("", "end", values=list(row))
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack widgets
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def search_records(self, dept):
        try:
            # Create search window
            search_window = ctk.CTkToplevel(self.root)
            search_window.title(f"Search {dept} Records")
            search_window.geometry("400x200")
            
            # Create search frame
            search_frame = ctk.CTkFrame(search_window)
            search_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Add search field
            ctk.CTkLabel(search_frame, text="Enter Patient ID:").pack(pady=5)
            search_entry = ctk.CTkEntry(search_frame)
            search_entry.pack(pady=5)
            
            def perform_search():
                patient_id = search_entry.get()
                df = pd.read_excel(self.excel_files[dept])
                results = df[df['Patient_ID'] == patient_id]
                
                if len(results) > 0:
                    # Create results window
                    results_window = ctk.CTkToplevel(search_window)
                    results_window.title("Search Results")
                    results_window.geometry("800x400")
                    
                    # Create treeview
                    tree = ttk.Treeview(results_window)
                    tree["columns"] = list(results.columns)
                    tree["show"] = "headings"
                    
                    # Set column headings
                    for column in results.columns:
                        tree.heading(column, text=column.replace('_', ' '))
                        tree.column(column, width=100)
                    
                    # Add data
                    for _, row in results.iterrows():
                        tree.insert("", "end", values=list(row))
                    
                    tree.pack(fill="both", expand=True)
                else:
                    messagebox.showinfo("No Results", "No records found for the given Patient ID.")
            
            # Add search button
            ctk.CTkButton(search_frame, text="Search", command=perform_search).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = HospitalManagementSystem(root)
    root.mainloop() 