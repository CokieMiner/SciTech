"""
SciTech Ambulance Routing - PDF Export Module
============================================

This module handles PDF export functionality using a template-based approach.
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import tempfile
from pathlib import Path

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from PyPDF2 import PdfReader, PdfWriter
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

def export_to_pdf(data: Dict[str, Any], route_log: List[Dict[str, Any]], 
                  output_path: Optional[str] = None) -> bool:
    """
    Export ambulance routing results to PDF using template
    
    Args:
        data: Problem data dictionary containing graph, points_data, initial_data
        route_log: List of routing steps from algorithm
        output_path: Optional custom output path, defaults to timestamped file
    
    Returns:
        bool: True if export successful, False otherwise
    """
    if not REPORTLAB_AVAILABLE:
        print("Error: ReportLab and PyPDF2 are required for PDF export")
        print("Install with: pip install reportlab PyPDF2")
        return False
    
    try:
        # Generate output filename if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"ambulance_routing_report_{timestamp}.pdf"
        
        # Get template path
        template_path = Path(__file__).parent.parent / "Docs" / "Pdf_Template.pdf"
        
        if template_path.exists():
            return _export_with_template(data, route_log, output_path, template_path)
        else:
            print(f"Error: Template file not found at {template_path}")
            return False
            
    except Exception as e:
        print(f"PDF export failed: {str(e)}")
        return False

def _export_with_template(data: Dict[str, Any], route_log: List[Dict[str, Any]], 
                         output_path: str, template_path: Path) -> bool:
    """Export PDF using existing template as base and fill it with data"""
    
    try:
        # Fill the template with actual data
        return _fill_template_with_data(data, route_log, template_path, output_path)
        
    except Exception as e:
        print(f"Failed to fill template: {str(e)}")
        return False



def _fill_template_with_data(data: Dict[str, Any], route_log: List[Dict[str, Any]], 
                            template_path: Path, output_path: str) -> bool:
    """Fill the template PDF with actual routing data"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        
        # Read the template
        template_reader = PdfReader(str(template_path))
        writer = PdfWriter()
        
        if len(template_reader.pages) == 0:
            return False
            
        template_page = template_reader.pages[0]
        
        # Create overlay with data
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            overlay_path = temp_file.name
        
        try:
            # Create overlay PDF with the data
            c = canvas.Canvas(overlay_path, pagesize=A4)
            width, height = A4
            
            # Add current date (top right)
            from datetime import datetime
            current_date = datetime.now().strftime("%d/%m/%Y")
            c.drawString(650, height - 213, current_date)
            
            # Fill in the table with route data
            # Move 30 pixels down from current position
            start_y = 465  # 495 - 30 = 465 (30 pixels down)
            row_height = 25  # Spacing between rows
            
            # Set font for table data
            c.setFont("Helvetica", 9)
            
            for i, step in enumerate(route_log[:15]):  # Limit to fit in template
                y_pos = start_y - (i * row_height)
                
                # Stop if we're getting too close to the bottom signature area
                if y_pos < 250:
                    break
                
                # Patient ID (column 1) - move 50 pixels right
                c.drawString(65, y_pos, str(step['to_patient']))  # 15 + 50 = 65
                
                # Priority (column 2) - move 50 pixels right
                c.drawString(165, y_pos, str(step['priority']))  # 115 + 50 = 165
                
                # Service time (column 3) - move 50 pixels right
                service_time = f"{step['time_needed']:.1f}min"
                c.drawString(300, y_pos, service_time)  # 250 + 50 = 300
                
                # Hospital arrival time (column 4) - move 50 pixels right
                cumulative_time = sum(s['time_needed'] for s in route_log[:i+1])
                hours = int(cumulative_time // 60)
                minutes = int(cumulative_time % 60)
                arrival_time = f"{hours:02d}:{minutes:02d}"
                c.drawString(495, y_pos, arrival_time)  # 445 + 50 = 495
            
            # Add accumulated priority - position it in the red box at bottom
            total_priority = sum(step['priority'] for step in route_log)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(210, 165, str(total_priority))  # Adjusted to be in the red "Prioridade acumulada" box
            
            c.save()
            
            # Merge overlay with template
            overlay_reader = PdfReader(overlay_path)
            if len(overlay_reader.pages) > 0:
                overlay_page = overlay_reader.pages[0]
                template_page.merge_page(overlay_page)
            
            writer.add_page(template_page)
            
            # Write final PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            print(f"PDF exported successfully with filled template to: {output_path}")
            return True
            
        finally:
            # Clean up overlay file
            if os.path.exists(overlay_path):
                os.unlink(overlay_path)
                
    except Exception as e:
        print(f"Failed to fill template: {str(e)}")
        return False



# Convenience function for UI integration
def export_ambulance_routing_pdf(data: Dict[str, Any], route_log: List[Dict[str, Any]]) -> bool:
    """
    Main export function for UI integration
    
    Args:
        data: Problem data dictionary
        route_log: Algorithm results
    
    Returns:
        bool: Success status
    """
    return export_to_pdf(data, route_log)