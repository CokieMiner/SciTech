"""
SciTech Ambulance Routing - UI with Configurable Functions
==========================================================

EASY INTEGRATION: Just replace the placeholder functions below with your actual implementations!
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import ttkthemes
from .Data_Import import problem_data_dict_by_each_file, problem_data_dict_by_folder  # type: ignore
from .alg import ambulance_routing_optimized  # type: ignore
from .PDF_Export import export_to_pdf as pdf_export  # type: ignore
from .graph_view import create_canvas  # type: ignore
from typing import Any, Dict, Optional, List, Tuple
import sys
import traceback
from datetime import datetime

# ============================================================================
# CONFIGURABLE FUNCTIONS - Replace these with your actual implementations
# ============================================================================


def load_data_from_folder(folder_path: str) -> Optional[Dict[str, Any]]:
    """Replace with your folder loading function"""
    return problem_data_dict_by_folder(folder_path)


def load_data_from_files(
    dados_file: str, pontos_file: str, ruas_file: str
) -> Optional[Dict[str, Any]]:
    """Replace with your individual files loading function"""
    return problem_data_dict_by_each_file(dados_file, pontos_file, ruas_file)


def run_algorithm(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Replace with your algorithm execution function"""
    if not data:
        return []
    graph = data["graph"]
    points_data = data["points_data"]
    initial_data = data["initial_data"]
    initial_point = initial_data.iloc[0]["ponto_inicial"]
    total_time = initial_data.iloc[0]["tempo_total"]
    route_log = ambulance_routing_optimized(
        graph, points_data, initial_point, total_time
    )
    return route_log


def export_to_pdf(
    data: Dict[str, Any],
    route_log: List[Dict[str, Any]],
    output_path: Optional[str] = None,
) -> bool:
    """Export results to PDF using template"""

    return pdf_export(data, route_log, output_path)


def browse_folder() -> Optional[str]:
    """File dialog for folder selection"""
    return filedialog.askdirectory(title="Select Data Folder")


def browse_file(
    title: str = "Select File", filetypes: Optional[List[Tuple[str, str]]] = None
) -> Optional[str]:
    """File dialog for file selection"""
    if filetypes is None:
        filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
    return filedialog.askopenfilename(title=title, filetypes=filetypes)


# ============================================================================
# CONFIGURATION VARIABLES - Modify these as needed
# ============================================================================


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
        self.canvas = None
        self._create_widgets()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

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
        ttk.Radiobutton(
            input_frame,
            text="Load from Folder",
            variable=self.input_mode,
            value="folder",
            command=self._toggle_input_mode,
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Radiobutton(
            input_frame,
            text="Load Separate Files",
            variable=self.input_mode,
            value="files",
            command=self._toggle_input_mode,
        ).grid(row=1, column=0, sticky=tk.W, pady=(0, 10))

        # Folder mode frame
        self.folder_frame = ttk.Frame(input_frame)
        ttk.Label(self.folder_frame, text="Folder Path:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )

        folder_input_frame = ttk.Frame(self.folder_frame)
        folder_input_frame.grid(row=1, column=0, sticky=tk.EW, pady=(0, 10))
        folder_input_frame.grid_columnconfigure(0, weight=1)

        self.folder_entry = ttk.Entry(folder_input_frame)
        self.folder_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))
        ttk.Button(folder_input_frame, text="Browse", command=self._browse_folder).grid(
            row=0, column=1
        )

        self.folder_frame.columnconfigure(0, weight=1)

        # Separate files mode frame (entries stored so we can clear them)
        self.files_frame = ttk.Frame(input_frame)
        self.files_frame.grid_columnconfigure(0, weight=1)

        # Dados Iniciais row
        ttk.Label(self.files_frame, text="Dados Iniciais:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 3)
        )
        dados_input_frame = ttk.Frame(self.files_frame)
        dados_input_frame.grid(row=1, column=0, sticky=tk.EW, pady=(0, 8))
        dados_input_frame.grid_columnconfigure(0, weight=1)
        self.dados_entry = ttk.Entry(dados_input_frame)
        self.dados_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))
        ttk.Button(
            dados_input_frame,
            text="Browse",
            command=lambda: self._browse_file(
                self.dados_entry, "Select Dados Iniciais File"
            ),
        ).grid(row=0, column=1)

        # Pontos row
        ttk.Label(self.files_frame, text="Pontos:").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 3)
        )
        pontos_input_frame = ttk.Frame(self.files_frame)
        pontos_input_frame.grid(row=3, column=0, sticky=tk.EW, pady=(0, 8))
        pontos_input_frame.grid_columnconfigure(0, weight=1)
        self.pontos_entry = ttk.Entry(pontos_input_frame)
        self.pontos_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))
        ttk.Button(
            pontos_input_frame,
            text="Browse",
            command=lambda: self._browse_file(self.pontos_entry, "Select Pontos File"),
        ).grid(row=0, column=1)

        # Ruas row
        ttk.Label(self.files_frame, text="Ruas:").grid(
            row=4, column=0, sticky=tk.W, pady=(0, 3)
        )
        ruas_input_frame = ttk.Frame(self.files_frame)
        ruas_input_frame.grid(row=5, column=0, sticky=tk.EW, pady=(0, 8))
        ruas_input_frame.grid_columnconfigure(0, weight=1)
        self.ruas_entry = ttk.Entry(ruas_input_frame)
        self.ruas_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))
        ttk.Button(
            ruas_input_frame,
            text="Browse",
            command=lambda: self._browse_file(self.ruas_entry, "Select Ruas File"),
        ).grid(row=0, column=1)

        ttk.Button(input_frame, text="Load Data", command=self._load_data).grid(
            row=3, column=0, sticky=tk.EW, pady=(8, 5)
        )
        self.status_label = ttk.Label(
            input_frame, text="Status: Not loaded", foreground="gray"
        )
        self.status_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 3))

        # Initially show folder frame
        self._toggle_input_mode()

        # Run Section
        run_frame = ttk.LabelFrame(self.sidebar, text="Run Algorithm", padding=10)
        run_frame.grid(row=1, column=0, sticky=tk.EW, pady=(0, 10))
        run_frame.grid_columnconfigure(0, weight=1)
        ttk.Button(run_frame, text="Run Algorithm", command=self._run_algorithm).grid(
            row=0, column=0, sticky=tk.EW, pady=(0, 8)
        )
        self.run_status_label = ttk.Label(
            run_frame, text="Status: Ready", foreground="gray"
        )
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
        self.patients_value = ttk.Label(
            self.patients_card, text="0", font=("Arial", 12, "bold"), foreground="blue"
        )
        self.patients_value.pack()

        self.priority_card = ttk.LabelFrame(summary_frame, text="Priority", padding=3)
        self.priority_card.grid(row=0, column=1, sticky=tk.EW, padx=(3, 3))
        self.priority_value = ttk.Label(
            self.priority_card, text="0", font=("Arial", 12, "bold"), foreground="green"
        )
        self.priority_value.pack()

        self.time_card = ttk.LabelFrame(summary_frame, text="Total Time", padding=3)
        self.time_card.grid(row=0, column=2, sticky=tk.EW, padx=(3, 0))
        self.time_value = ttk.Label(
            self.time_card, text="0.0", font=("Arial", 12, "bold"), foreground="purple"
        )
        self.time_value.pack()

        # Results table
        table_frame = ttk.Frame(results_frame)
        table_frame.grid(row=1, column=0, sticky=tk.NSEW)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        # Create Treeview for results
        columns = ("Step", "Patient", "Priority", "Time", "Acc. Priority")
        self.results_tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=8
        )

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
        tree_scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.results_tree.yview
        )
        self.results_tree.configure(yscrollcommand=tree_scrollbar.set)

        self.results_tree.grid(row=0, column=0, sticky=tk.NSEW)
        tree_scrollbar.grid(row=0, column=1, sticky=tk.NS)

        # Export Section
        export_frame = ttk.LabelFrame(self.sidebar, text="Export", padding=10)
        export_frame.grid(row=3, column=0, sticky=tk.EW)
        export_frame.grid_columnconfigure(0, weight=1)
        ttk.Button(export_frame, text="Export PDF", command=self._export_pdf).grid(
            row=0, column=0, sticky=tk.EW
        )

        # Right main area - expandable with 3 columns: node list, spacer, visualization
        main_area = ttk.Frame(self.main_frame)
        main_area.grid(row=0, column=1, sticky=tk.NSEW, padx=(5, 0))
        main_area.grid_rowconfigure(0, weight=1)
        main_area.grid_columnconfigure(0, weight=0)  # Node list - fixed width
        main_area.grid_columnconfigure(1, weight=0)  # Small spacer
        main_area.grid_columnconfigure(2, weight=1)  # Visualization - expandable

        # Node List Section (between sidebar and visualization)
        nodes_frame = ttk.LabelFrame(main_area, text="Nodes", padding=10)
        nodes_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 5))
        nodes_frame.grid_rowconfigure(0, weight=1)
        nodes_frame.grid_columnconfigure(0, weight=1)
        nodes_frame.configure(width=250)  # Increased width for node list (+5%)
        nodes_frame.grid_propagate(False)

        # Create TreeView for nodes
        nodes_tree_frame = ttk.Frame(nodes_frame)
        nodes_tree_frame.grid(row=0, column=0, sticky=tk.NSEW)
        nodes_tree_frame.grid_columnconfigure(0, weight=1)
        nodes_tree_frame.grid_rowconfigure(0, weight=1)

        # Node TreeView
        node_columns = ("ID", "Type", "Priority")
        self.nodes_tree = ttk.Treeview(
            nodes_tree_frame, columns=node_columns, show="headings", height=15
        )

        # Configure node columns
        self.nodes_tree.heading("ID", text="ID")
        self.nodes_tree.heading("Type", text="Type")
        self.nodes_tree.heading("Priority", text="Priority")

        # Set node column widths
        self.nodes_tree.column("ID", width=30, anchor="center")
        self.nodes_tree.column("Type", width=80, anchor="center")
        self.nodes_tree.column("Priority", width=60, anchor="center")

        # Add scrollbar to nodes treeview
        nodes_scrollbar = ttk.Scrollbar(
            nodes_tree_frame, orient=tk.VERTICAL, command=self.nodes_tree.yview
        )
        self.nodes_tree.configure(yscrollcommand=nodes_scrollbar.set)

        self.nodes_tree.grid(row=0, column=0, sticky=tk.NSEW)
        nodes_scrollbar.grid(row=0, column=1, sticky=tk.NS)

        # Visualization Section (reduced width by 10%)
        viz_frame = ttk.LabelFrame(main_area, text="Visualization", padding=15)
        viz_frame.grid(row=0, column=2, sticky=tk.NSEW)
        viz_frame.grid_rowconfigure(0, weight=1)
        viz_frame.grid_columnconfigure(0, weight=1)

        # Frame for matplotlib canvas
        self.viz_container = ttk.Frame(viz_frame)
        self.viz_container.grid(row=0, column=0, sticky=tk.NSEW)
        self.viz_container.grid_rowconfigure(0, weight=1)
        self.viz_container.grid_columnconfigure(0, weight=1)

        # Placeholder label (will be replaced by canvas)
        self.viz_placeholder = tk.Label(
            self.viz_container,
            text="Load data to view graph",
            background="white",
            foreground="gray",
            font=("Arial", 12),
            anchor=tk.CENTER,
        )
        self.viz_placeholder.grid(row=0, column=0, sticky=tk.NSEW)

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

    def _on_closing(self):
        """Handle window close event"""
        self.quit()
        sys.exit(0)

    def _populate_nodes_tree(self):
        """Populate the nodes TreeView with data in numerical order"""
        try:
            # Clear existing items
            for item in self.nodes_tree.get_children():
                self.nodes_tree.delete(item)

            if self.data and "points_data" in self.data:
                df_pontos = self.data["points_data"]

                # Sort by index (numerical order)
                for i in range(len(df_pontos)):
                    row = df_pontos.iloc[i]
                    node_type = row["tipo"]

                    if node_type != "hospital":
                        priority = row["prioridade"]
                        self.nodes_tree.insert(
                            "", "end", values=(i, "Patient", priority)
                        )
                    else:
                        self.nodes_tree.insert("", "end", values=(i, "Hospital", "-"))
        except Exception as e:
            print(f"Error populating nodes tree: {e}")
            traceback.print_exc()

    def _create_graph_viz(self):
        """Create the graph visualization canvas"""
        try:
            if self.data and "points_data" in self.data and "ruas_data" in self.data:
                # Remove placeholder
                self.viz_placeholder.grid_forget()
                # Create canvas
                self.canvas = create_canvas(
                    self.viz_container, self.data["points_data"], self.data["ruas_data"]
                )
                self.canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.NSEW)
                self.canvas.draw()
                # Populate nodes tree
                self._populate_nodes_tree()
            else:
                print("Data not complete for visualization")
        except Exception as e:
            print(f"Error creating graph viz: {e}")
            traceback.print_exc()

    def _update_nodes_tree_with_route(self):
        """Update nodes tree to highlight visited nodes"""
        try:
            if not self.route_log:
                return

            # Get visited patients
            visited_patients = {step["to_patient"] for step in self.route_log}

            # Update tree items to highlight visited nodes
            for item in self.nodes_tree.get_children():
                values = self.nodes_tree.item(item)["values"]
                node_id = int(values[0])
                node_type = values[1]

                if node_type == "Patient" and f"P{node_id:03d}" in visited_patients:
                    # Highlight visited patients (you can customize the highlighting)
                    self.nodes_tree.set(item, "Type", "Patient ✓")
                else:
                    # Reset highlighting for non-visited
                    if node_type == "Patient ✓":
                        self.nodes_tree.set(item, "Type", "Patient")

        except Exception as e:
            print(f"Error updating nodes tree with route: {e}")
            

            traceback.print_exc()

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
                # Create graph visualization
                self._create_graph_viz()
            else:
                self.status_label.configure(
                    text="Status: Load failed", foreground="red"
                )

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
            # Update nodes tree to highlight visited nodes (without updating graph)
            self._update_nodes_tree_with_route()

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
        total_priority = sum(step["priority"] for step in self.route_log)
        total_time = sum(step["time_needed"] for step in self.route_log)

        self.patients_value.configure(text=str(total_patients))
        self.priority_value.configure(text=str(total_priority))
        self.time_value.configure(text=f"{total_time:.1f}")

        # Populate results table
        accumulated_priority = 0
        for i, step in enumerate(self.route_log, 1):
            accumulated_priority += step["priority"]

            # Add row to treeview
            self.results_tree.insert(
                "",
                "end",
                values=(
                    i,
                    step["to_patient"],
                    step["priority"],
                    f"{step['time_needed']:.1f}",
                    accumulated_priority,
                ),
            )

        # Color code rows based on priority
        for item in self.results_tree.get_children():
            values = self.results_tree.item(item)["values"]
            priority = int(values[2])

            if priority >= 80:
                self.results_tree.set(item, "Priority", f"{priority}")  # High priority
            elif priority >= 60:
                self.results_tree.set(
                    item, "Priority", f"{priority}"
                )  # Medium priority
            else:
                self.results_tree.set(item, "Priority", f"{priority}")  # Low priority

    def _export_pdf(self):
        """Export current state to PDF"""
        try:
            if not self.route_log:
                messagebox.showerror("Error", "Please run the algorithm first")
                return

            # Open file dialog to choose save location
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"ambulance_routing_report_{timestamp}.pdf"

            file_path = filedialog.asksaveasfilename(
                title="Save PDF Report As",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=default_filename,
            )

            if not file_path:  # User cancelled the dialog
                return

            success = export_to_pdf(self.data, self.route_log, file_path)
            if success:
                messagebox.showinfo(
                    "Success", f"PDF exported successfully to:\n{file_path}"
                )
            else:
                messagebox.showerror("Error", "Failed to export PDF")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")


if __name__ == "__main__":
    app = SciTechApp()
    app.mainloop()
