"""
SciTech Ambulance Routing - UI with Configurable Functions
==========================================================

EASY INTEGRATION: Just replace the placeholder functions below with your actual implementations!
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import ttkthemes
from Data_Import import problem_data_dict_by_each_file, problem_data_dict_by_folder
from alg import ambulance_routing_optimized
import pandas as pd
from typing import Any, Dict

# ============================================================================
# CONFIGURABLE FUNCTIONS - Replace these with your actual implementations
# ============================================================================

def load_data_from_folder(folder_path):
    """Replace with your folder loading function"""
    return problem_data_dict_by_folder(folder_path)

def load_data_from_files(dados_file, pontos_file, ruas_file):
    """Replace with your individual files loading function"""
    return problem_data_dict_by_each_file(dados_file, pontos_file, ruas_file)

def run_algorithm(data):
    """Replace with your algorithm execution function"""
    if not data:
        return "No data loaded"
    graph = data['graph']
    points_data = data['points_data']
    initial_data = data['initial_data']
    initial_point = initial_data.iloc[0]['ponto_inicial']
    total_time = initial_data.iloc[0]['tempo_total']
    route_log = ambulance_routing_optimized(graph, points_data, initial_point, total_time)
    return route_log

def update_visualization(current_time):
    """Replace with your visualization update function"""
    print(f"Updating visualization at time: {current_time}")
    # TODO: Replace with actual implementation
    pass

def export_to_pdf(data, route_log):
    """Replace with your PDF export function"""
    print("PDF export not implemented yet")
    return False

def browse_folder():
    """File dialog for folder selection"""
    return filedialog.askdirectory(title="Select Data Folder")

def browse_file(title="Select File", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]):
    """File dialog for file selection"""
    return filedialog.askopenfilename(title=title, filetypes=filetypes)

# ============================================================================
# CONFIGURATION VARIABLES - Modify these as needed
# ============================================================================

ANIMATION_MAX_TIME = 100  # Set to your animation duration
ANIMATION_SPEED_MS = 100  # Animation step delay in milliseconds

class SciTechApp(ttkthemes.ThemedTk):
    def __init__(self):
        super().__init__()
        self.set_theme("plastik")
        self.title("SciTech Ambulance Routing")
        self.style = ttk.Style(self)
        self.style.theme_use("plastik")
        # Set window size based on screen dimensions (90% of screen size)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(800, 600)  # Set minimum window size
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.data = None
        self.route_log = None
        self._create_widgets()

    def _create_widgets(self):
        
        # Main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        # Proper column configuration - sidebar fixed, main area expandable
        self.main_frame.grid_columnconfigure(0, weight=0)  # Sidebar column - fixed
        self.main_frame.grid_columnconfigure(1, weight=1)  # Main area - expandable

        # Left sidebar with responsive width (20% of screen, minimum 280px)
        screen_width = self.winfo_screenwidth()
        sidebar_width = max(280, int(screen_width * 0.20))
        
        self.sidebar = ttk.Frame(self.main_frame)
        self.sidebar.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 5))
        # Set calculated width for sidebar
        self.sidebar.grid_propagate(False)
        self.sidebar.configure(width=sidebar_width)
        # Configure sidebar internal layout
        self.sidebar.grid_rowconfigure(2, weight=1)  # Make results section expandable
        self.sidebar.grid_columnconfigure(0, weight=1)

        # Data Input Section
        input_frame = ttk.LabelFrame(self.sidebar, text="Data Input", padding=10)
        input_frame.grid(row=0, column=0, sticky=tk.EW, pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)

        # Choice selector
        self.input_mode = tk.StringVar(value="folder")
        ttk.Radiobutton(input_frame, text="Load from Folder", variable=self.input_mode, value="folder", command=self._toggle_input_mode).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Radiobutton(input_frame, text="Load Separate Files", variable=self.input_mode, value="files", command=self._toggle_input_mode).grid(row=1, column=0, sticky=tk.W, pady=(0, 10))

        # Folder mode frame
        self.folder_frame = ttk.Frame(input_frame)
        ttk.Label(self.folder_frame, text="Folder Path:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        folder_input_frame = ttk.Frame(self.folder_frame)
        folder_input_frame.grid(row=1, column=0, sticky=tk.EW, pady=(0, 10))
        folder_input_frame.grid_columnconfigure(0, weight=1)
        
        self.folder_entry = ttk.Entry(folder_input_frame)
        self.folder_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))
        ttk.Button(folder_input_frame, text="Browse", command=self._browse_folder).grid(row=0, column=1)
        
        self.folder_frame.columnconfigure(0, weight=1)

        # Separate files mode frame (entries stored so we can clear them)
        self.files_frame = ttk.Frame(input_frame)
        self.files_frame.grid_columnconfigure(0, weight=1)
        
        # Dados Iniciais row
        ttk.Label(self.files_frame, text="Dados Iniciais:").grid(row=0, column=0, sticky=tk.W, pady=(0, 3))
        dados_input_frame = ttk.Frame(self.files_frame)
        dados_input_frame.grid(row=1, column=0, sticky=tk.EW, pady=(0, 8))
        dados_input_frame.grid_columnconfigure(0, weight=1)
        self.dados_entry = ttk.Entry(dados_input_frame)
        self.dados_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))
        ttk.Button(dados_input_frame, text="Browse", command=lambda: self._browse_file(self.dados_entry, "Select Dados Iniciais File")).grid(row=0, column=1)
        
        # Pontos row
        ttk.Label(self.files_frame, text="Pontos:").grid(row=2, column=0, sticky=tk.W, pady=(0, 3))
        pontos_input_frame = ttk.Frame(self.files_frame)
        pontos_input_frame.grid(row=3, column=0, sticky=tk.EW, pady=(0, 8))
        pontos_input_frame.grid_columnconfigure(0, weight=1)
        self.pontos_entry = ttk.Entry(pontos_input_frame)
        self.pontos_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))
        ttk.Button(pontos_input_frame, text="Browse", command=lambda: self._browse_file(self.pontos_entry, "Select Pontos File")).grid(row=0, column=1)
        
        # Ruas row
        ttk.Label(self.files_frame, text="Ruas:").grid(row=4, column=0, sticky=tk.W, pady=(0, 3))
        ruas_input_frame = ttk.Frame(self.files_frame)
        ruas_input_frame.grid(row=5, column=0, sticky=tk.EW, pady=(0, 8))
        ruas_input_frame.grid_columnconfigure(0, weight=1)
        self.ruas_entry = ttk.Entry(ruas_input_frame)
        self.ruas_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))
        ttk.Button(ruas_input_frame, text="Browse", command=lambda: self._browse_file(self.ruas_entry, "Select Ruas File")).grid(row=0, column=1)

        ttk.Button(input_frame, text="Load Data", command=self._load_data).grid(row=3, column=0, sticky=tk.EW, pady=(8, 5))
        self.status_label = ttk.Label(input_frame, text="Status: Not loaded", foreground="gray")
        self.status_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 3))

        # Initially show folder frame
        self._toggle_input_mode()

        # Run Section
        run_frame = ttk.LabelFrame(self.sidebar, text="Run Algorithm", padding=10)
        run_frame.grid(row=1, column=0, sticky=tk.EW, pady=(0, 10))
        run_frame.grid_columnconfigure(0, weight=1)
        ttk.Button(run_frame, text="Run Algorithm", command=self._run_algorithm).grid(row=0, column=0, sticky=tk.EW, pady=(0, 8))
        self.run_status_label = ttk.Label(run_frame, text="Status: Ready", foreground="gray")
        self.run_status_label.grid(row=1, column=0, sticky=tk.W)

        # Results Section
        results_frame = ttk.LabelFrame(self.sidebar, text="Results", padding=10)
        results_frame.grid(row=2, column=0, sticky=tk.NSEW, pady=(0, 10))
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        # Summary cards frame
        summary_frame = ttk.Frame(results_frame)
        summary_frame.grid(row=0, column=0, sticky=tk.EW, pady=(0, 10))
        summary_frame.grid_columnconfigure(0, weight=1)
        summary_frame.grid_columnconfigure(1, weight=1)
        summary_frame.grid_columnconfigure(2, weight=1)
        
        # Summary cards with better styling
        self.patients_card = ttk.LabelFrame(summary_frame, text="Patients", padding=3)
        self.patients_card.grid(row=0, column=0, sticky=tk.EW, padx=(0, 3))
        self.patients_value = ttk.Label(self.patients_card, text="0", font=("Arial", 12, "bold"), foreground="blue")
        self.patients_value.pack()
        
        self.priority_card = ttk.LabelFrame(summary_frame, text="Priority", padding=3)
        self.priority_card.grid(row=0, column=1, sticky=tk.EW, padx=(3, 3))
        self.priority_value = ttk.Label(self.priority_card, text="0", font=("Arial", 12, "bold"), foreground="green")
        self.priority_value.pack()
        
        self.time_card = ttk.LabelFrame(summary_frame, text="Total Time", padding=3)
        self.time_card.grid(row=0, column=2, sticky=tk.EW, padx=(3, 0))
        self.time_value = ttk.Label(self.time_card, text="0.0", font=("Arial", 12, "bold"), foreground="purple")
        self.time_value.pack()
        
        # Results table
        table_frame = ttk.Frame(results_frame)
        table_frame.grid(row=1, column=0, sticky=tk.NSEW)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Create Treeview for results
        columns = ("Step", "Patient", "Priority", "Time", "Acc. Priority")
        self.results_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        self.results_tree.heading("Step", text="Step")
        self.results_tree.heading("Patient", text="Patient")
        self.results_tree.heading("Priority", text="Priority")
        self.results_tree.heading("Time", text="Time")
        self.results_tree.heading("Acc. Priority", text="Acc. Priority")
        
        # Set column widths
        self.results_tree.column("Step", width=40, anchor="center")
        self.results_tree.column("Patient", width=60, anchor="center")
        self.results_tree.column("Priority", width=60, anchor="center")
        self.results_tree.column("Time", width=50, anchor="center")
        self.results_tree.column("Acc. Priority", width=80, anchor="center")
        
        # Add scrollbar to treeview
        tree_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.results_tree.grid(row=0, column=0, sticky=tk.NSEW)
        tree_scrollbar.grid(row=0, column=1, sticky=tk.NS)

        # Export Section
        export_frame = ttk.LabelFrame(self.sidebar, text="Export", padding=10)
        export_frame.grid(row=3, column=0, sticky=tk.EW)
        export_frame.grid_columnconfigure(0, weight=1)
        ttk.Button(export_frame, text="Export PDF", command=self._export_pdf).grid(row=0, column=0, sticky=tk.EW)

        # Right main area - expandable
        main_area = ttk.Frame(self.main_frame)
        main_area.grid(row=0, column=1, sticky=tk.NSEW, padx=(5, 0))
        main_area.grid_rowconfigure(0, weight=1)
        main_area.grid_columnconfigure(0, weight=1)

        # Visualization Section
        viz_frame = ttk.LabelFrame(main_area, text="Visualization", padding=15)
        viz_frame.grid(row=0, column=0, sticky=tk.NSEW)
        viz_frame.grid_rowconfigure(0, weight=1)
        viz_frame.grid_columnconfigure(0, weight=1)
        
        # Placeholder for canvas
        canvas_placeholder = tk.Label(viz_frame, text="Canvas Space for Graph\n(Matplotlib will go here)", 
                                     background="white", foreground="gray", 
                                     font=("Arial", 12), anchor=tk.CENTER,
                                     relief=tk.SUNKEN, bd=1)
        canvas_placeholder.grid(row=0, column=0, sticky=tk.NSEW, pady=(0, 15))

        # Controls
        controls_frame = ttk.Frame(viz_frame)
        controls_frame.grid(row=1, column=0, sticky=tk.EW, pady=(0, 10))
        
        # Animation control buttons
        self.play_button = ttk.Button(controls_frame, text="▶ Start", command=self._start_animation)
        self.play_button.grid(row=0, column=0, padx=(0, 10))
        
        self.pause_button = ttk.Button(controls_frame, text="⏸ Pause", command=self._pause_animation, state="disabled")
        self.pause_button.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Checkbutton(controls_frame, text="Show Labels").grid(row=0, column=2, padx=(0, 10))
        
        # Add some spacing on the right
        controls_frame.grid_columnconfigure(3, weight=1)
        
        # Time slider controls
        slider_frame = ttk.Frame(viz_frame)
        slider_frame.grid(row=2, column=0, sticky=tk.EW)
        slider_frame.grid_columnconfigure(1, weight=1)
        
        # Time label and slider
        ttk.Label(slider_frame, text="Time:").grid(row=0, column=0, padx=(0, 10))
        
        self.time_var = tk.DoubleVar(value=0)
        self.time_slider = ttk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                   variable=self.time_var, command=self._on_time_change)
        self.time_slider.grid(row=0, column=1, sticky=tk.EW, padx=(0, 10))
        
        self.time_label = ttk.Label(slider_frame, text="0:00 / 10:00")
        self.time_label.grid(row=0, column=2)
        
        # Animation state
        self.animation_running = False
        self.animation_job = None
        self.current_time = 0
        self.max_time = ANIMATION_MAX_TIME

    def _toggle_input_mode(self):
        if self.input_mode.get() == "folder":
            self.files_frame.grid_forget()
            self.folder_frame.grid(row=2, column=0, sticky=tk.EW, pady=(0, 8))
            # Clear files entries
            self.dados_entry.delete(0, tk.END)
            self.pontos_entry.delete(0, tk.END)
            self.ruas_entry.delete(0, tk.END)
        else:
            self.folder_frame.grid_forget()
            self.files_frame.grid(row=2, column=0, sticky=tk.EW, pady=(0, 8))
            # Clear folder entry
            self.folder_entry.delete(0, tk.END)

    def _start_animation(self):
        """Start the visualization animation"""
        if not self.animation_running:
            self.animation_running = True
            self.play_button.configure(state="disabled")
            self.pause_button.configure(state="normal")
            self._animate_step()
            
    def _pause_animation(self):
        """Pause the visualization animation"""
        if self.animation_running:
            self.animation_running = False
            self.play_button.configure(state="normal")
            self.pause_button.configure(state="disabled")
            if self.animation_job:
                self.after_cancel(self.animation_job)
                self.animation_job = None
                
    def _animate_step(self):
        """Single animation step - placeholder for actual animation logic"""
        if self.animation_running:
            # Update current time
            self.current_time += 1
            if self.current_time > self.max_time:
                self.current_time = 0  # Loop animation
            
            # Update slider position
            self.time_var.set(self.current_time)
            self._update_time_display()
            
            # Update visualization using configurable function
            update_visualization(self.current_time)
            
            # Schedule next step
            self.animation_job = self.after(ANIMATION_SPEED_MS, self._animate_step)
            
    def _on_time_change(self, value):
        """Handle time slider changes"""
        self.current_time = float(value)
        self._update_time_display()
        # Update visualization using configurable function
        update_visualization(self.current_time)
        
    def _update_time_display(self):
        """Update the time display label"""
        current_minutes = int(self.current_time // 60)
        current_seconds = int(self.current_time % 60)
        max_minutes = int(self.max_time // 60)
        max_seconds = int(self.max_time % 60)
        
        time_text = f"{current_minutes}:{current_seconds:02d} / {max_minutes}:{max_seconds:02d}"
        self.time_label.configure(text=time_text)

    # ========================================================================
    # CALLBACK METHODS - These use the configurable functions above
    # ========================================================================
    
    def _browse_folder(self):
        """Browse for folder and update entry"""
        folder = browse_folder()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
    
    def _browse_file(self, entry_widget, title):
        """Browse for file and update entry widget"""
        file_path = browse_file(title)
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)
    
    def _load_data(self):
        """Load data using the appropriate method"""
        try:
            if self.input_mode.get() == "folder":
                folder_path = self.folder_entry.get().strip()
                if not folder_path:
                    messagebox.showerror("Error", "Please select a folder path")
                    return
                self.data = load_data_from_folder(folder_path)
            else:
                dados_file = self.dados_entry.get().strip()
                pontos_file = self.pontos_entry.get().strip()
                ruas_file = self.ruas_entry.get().strip()
                
                if not all([dados_file, pontos_file, ruas_file]):
                    messagebox.showerror("Error", "Please select all required files")
                    return
                self.data = load_data_from_files(dados_file, pontos_file, ruas_file)
            
            if self.data:
                self.status_label.configure(text="Status: Loaded", foreground="green")
            else:
                self.status_label.configure(text="Status: Load failed", foreground="red")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.status_label.configure(text="Status: Load failed", foreground="red")
    
    def _run_algorithm(self):
        """Run the algorithm"""
        try:
            if not self.data:
                messagebox.showerror("Error", "Please load data first")
                return
            
            self.run_status_label.configure(text="Status: Running", foreground="orange")
            self._clear_results()
            self.update()  # Update UI
            
            self.route_log = run_algorithm(self.data)
            
            self.run_status_label.configure(text="Status: Finished", foreground="green")
            self._display_results()
            
        except Exception as e:
            self.run_status_label.configure(text="Status: Error", foreground="red")
            messagebox.showerror("Error", f"Algorithm failed: {str(e)}")
            self._clear_results()
    
    def _clear_results(self):
        """Clear all results displays"""
        # Clear summary cards
        self.patients_value.configure(text="0")
        self.priority_value.configure(text="0")
        self.time_value.configure(text="0.0")
        
        # Clear results table
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
    
    def _display_results(self):
        """Display algorithm results in structured format"""
        if not self.route_log:
            return
        
        # Update summary cards
        total_patients = len(self.route_log)
        total_priority = sum(step['priority'] for step in self.route_log)
        total_time = sum(step['time_needed'] for step in self.route_log)
        
        self.patients_value.configure(text=str(total_patients))
        self.priority_value.configure(text=str(total_priority))
        self.time_value.configure(text=f"{total_time:.1f}")
        
        # Populate results table
        accumulated_priority = 0
        for i, step in enumerate(self.route_log, 1):
            accumulated_priority += step['priority']
            
            # Add row to treeview
            self.results_tree.insert("", "end", values=(
                i,
                step['to_patient'],
                step['priority'],
                f"{step['time_needed']:.1f}",
                accumulated_priority
            ))
        
        # Color code rows based on priority
        for item in self.results_tree.get_children():
            values = self.results_tree.item(item)['values']
            priority = int(values[2])
            
            if priority >= 80:
                self.results_tree.set(item, "Priority", f"{priority} 🔴")  # High priority
            elif priority >= 60:
                self.results_tree.set(item, "Priority", f"{priority} 🟡")  # Medium priority
            else:
                self.results_tree.set(item, "Priority", f"{priority} 🟢")  # Low priority
    
    def _export_pdf(self):
        """Export current state to PDF"""
        try:
            if not self.route_log:
                messagebox.showerror("Error", "Please run the algorithm first")
                return
            success = export_to_pdf(self.data, self.route_log)
            if success:
                messagebox.showinfo("Success", "PDF exported successfully!")
            else:
                messagebox.showerror("Error", "Failed to export PDF")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")


if __name__ == "__main__":
    app = SciTechApp()
    app.mainloop()