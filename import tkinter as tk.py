import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
from datetime import datetime

class VSIMSDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VSIMS Data Management System")
        self.root.geometry("800x600")

        # Login credentials
        self.username = "vpduntbel01"
        self.password = "Bel@0233"
        self.website_url = "https://vsims.npsuindia.org/#!"

        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Status label
        self.status_label = tk.Label(self.main_frame, text="Status: Ready", font=('Arial', 10))
        self.status_label.pack(pady=10)

        # Create buttons frame
        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=20)

        # PDF Processing Section
        self.pdf_frame = tk.LabelFrame(self.main_frame, text="PDF Processing", padx=10, pady=10)
        self.pdf_frame.pack(fill=tk.X, pady=10)

        self.select_pdf_btn = tk.Button(self.pdf_frame, text="Select PDF Files", command=self.select_pdf_files)
        self.select_pdf_btn.pack(side=tk.LEFT, padx=5)

        self.process_pdf_btn = tk.Button(self.pdf_frame, text="Process and Upload Data", command=self.process_data)
        self.process_pdf_btn.pack(side=tk.LEFT, padx=5)

        # MR Report Section
        self.mr_frame = tk.LabelFrame(self.main_frame, text="Measles-Rubella Report", padx=10, pady=10)
        self.mr_frame.pack(fill=tk.X, pady=10)

        self.download_mr_btn = tk.Button(self.mr_frame, text="Download MR Linelist", command=self.download_mr_report)
        self.download_mr_btn.pack(side=tk.LEFT, padx=5)

        self.analyze_mr_btn = tk.Button(self.mr_frame, text="Analyze MR Data", command=self.analyze_mr_data)
        self.analyze_mr_btn.pack(side=tk.LEFT, padx=5)

        # Results Text Area
        self.results_frame = tk.LabelFrame(self.main_frame, text="Analysis Results", padx=10, pady=10)
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.results_text = tk.Text(self.results_frame, height=10)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        self.selected_files = []
        self.downloaded_file_path = None

    def select_pdf_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF files", "*.pdf")]
        )
        self.selected_files = files
        self.status_label.config(text=f"Status: Selected {len(files)} PDF files")

    def extract_data_from_pdf(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            messagebox.showerror("Error", f"Error reading PDF: {str(e)}")
            return None

    def process_data(self):
        if not self.selected_files:
            messagebox.showerror("Error", "Please select PDF files first")
            return

        try:
            self.status_label.config(text="Status: Initializing browser...")
            driver = webdriver.Chrome()
            driver.get(self.website_url)

            # Login process
            self.login_to_vsims(driver)

            # Process PDFs
            for index, pdf_file in enumerate(self.selected_files, 1):
                self.status_label.config(text=f"Status: Processing file {index} of {len(self.selected_files)}")
                self.process_single_pdf(driver, pdf_file, index)

            driver.quit()
            self.status_label.config(text="Status: Processing completed")
            messagebox.showinfo("Success", "Data processing completed")

        except Exception as e:
            self.status_label.config(text="Status: Error occurred")
            messagebox.showerror("Error", f"Error during processing: {str(e)}")

    def login_to_vsims(self, driver):
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(self.username)
            
            password_field = driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            
            login_button = driver.find_element(By.ID, "login-button")
            login_button.click()
            
            time.sleep(3)
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")

    def download_mr_report(self):
        try:
            self.status_label.config(text="Status: Downloading MR report...")
            driver = webdriver.Chrome()
            driver.get(self.website_url)
            
            self.login_to_vsims(driver)
            
            # Navigate to MR report section (adjust selectors based on actual website)
            mr_report_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Measles-Rubella Report"))
            )
            mr_report_link.click()
            
            # Download linelist
            download_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "download-linelist"))
            )
            download_button.click()
            
            # Wait for download to complete
            time.sleep(5)
            
            # Get the latest downloaded file
            downloads_path = os.path.expanduser("~/Downloads")
            files = sorted(
                [os.path.join(downloads_path, f) for f in os.listdir(downloads_path)],
                key=os.path.getmtime
            )
            self.downloaded_file_path = files[-1]
            
            driver.quit()
            self.status_label.config(text="Status: MR report downloaded successfully")
            messagebox.showinfo("Success", "MR report downloaded successfully")
            
        except Exception as e:
            self.status_label.config(text="Status: Error downloading report")
            messagebox.showerror("Error", f"Error downloading MR report: {str(e)}")

    def analyze_mr_data(self):
        if not self.downloaded_file_path:
            messagebox.showerror("Error", "Please download the MR linelist first")
            return

        try:
            self.status_label.config(text="Status: Analyzing MR data...")
            df = pd.read_excel(self.downloaded_file_path)
            
            # Clear previous results
            self.results_text.delete(1.0, tk.END)
            
            # Perform analysis
            analysis_results = [
                f"Total Records: {len(df)}",
                f"Date Range: {df['Date'].min()} to {df['Date'].max()}",
                "\nAge Distribution:",
                df['Age'].describe().to_string(),
                "\nCase Distribution by Gender:",
                df['Gender'].value_counts().to_string(),
                "\nVaccination Status:",
                df['Vaccination_Status'].value_counts().to_string(),
                "\nDistrict-wise Cases:",
                df['District'].value_counts().head(10).to_string()
            ]
            
            # Display results
            self.results_text.insert(tk.END, "\n\n".join(analysis_results))
            
            # Generate summary report
            report_path = f"MR_Analysis_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with pd.ExcelWriter(report_path) as writer:
                df.describe().to_excel(writer, sheet_name='Summary Statistics')
                df.pivot_table(
                    index='District',
                    values='Case_ID',
                    aggfunc='count'
                ).to_excel(writer, sheet_name='District Summary')
            
            self.status_label.config(text="Status: Analysis completed")
            messagebox.showinfo("Success", f"Analysis completed. Report saved as {report_path}")
            
        except Exception as e:
            self.status_label.config(text="Status: Error analyzing data")
            messagebox.showerror("Error", f"Error analyzing MR data: {str(e)}")

    def process_single_pdf(self, driver, pdf_file, index):
        data = self.extract_data_from_pdf(pdf_file)
        if data:
            try:
                # Navigate to data entry form
                form_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Data Entry Form"))
                )
                form_link.click()
                
                # Fill form fields (adjust according to actual form structure)
                input_fields = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "form-input"))
                )
                
                # Submit form
                submit_button = driver.find_element(By.ID, "submit-form")
                submit_button.click()
                
                time.sleep(2)
                
            except Exception as e:
                raise Exception(f"Error processing file {index}: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VSIMSDataApp(root)
    root.mainloop()


