# RAW STATES 

calendar_events = []
emails = []
todos = []
files_read = []
written_files = []
pdf_texts = []
csv_extract = []

# TOOL METRICS (OfficeBench)
# Conta quante volte un tool è stato chiamato e con successo

tool_metrics = {
    "calendar_add": {"total": 0, "success": 0},
    "email_send": {"total": 0, "success": 0},
    "todo_add": {"total": 0, "success": 0},
    "file_read": {"total": 0, "success": 0},
    "file_write": {"total": 0, "success": 0},
    "pdf_extract": {"total": 0, "success": 0},
    "csv_extract": {"total": 0, "success": 0},
    "excel_read": {"total": 0, "success": 0},  
    "chart_generate": {"total": 0, "success": 0},  
}


# TOOL METRICS (XLH Tasks)
# Separato per evitare contaminazione dei benchmark

xlh_tool_metrics = {
    "calendar_add": {"total": 0, "success": 0},
    "email_send": {"total": 0, "success": 0},
    "todo_add": {"total": 0, "success": 0},
    "file_read": {"total": 0, "success": 0},
    "file_write": {"total": 0, "success": 0},
    "pdf_extract": {"total": 0, "success": 0},
    "csv_extract": {"total": 0, "success": 0},
    "excel_read": {"total": 0, "success": 0},     
    "chart_generate": {"total": 0, "success": 0}, 
}
