TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_calendar_event",
            "description": "Add an event to the calendar",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the event"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date of the event (DD/MM/YYYY)"
                    },
                    "time": {
                        "type": "string",
                        "description": "Time of the event"
                    }
                },
                "required": ["title", "date", "time"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_text_from_pdf",
            "description": "Extract text content from a PDF file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the PDF file"
                    }
                },
                "required": ["file_path"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_excel",
            "description": "Read an Excel file and return its contents",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the Excel file"
                    }
                },
                "required": ["file_path"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text to a file. If the file exists, overwrite it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["file_path", "content"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_chart",
            "description": "Generate a PNG chart from structured numeric data",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": { "type": "string" },
                    "x": {
                        "type": "array",
                        "items": { "type": "string" }
                    },
                    "y": {
                        "type": "array",
                        "items": { "type": "number" }
                    },
                    "x_label": { "type": "string" },
                    "y_label": { "type": "string" },
                    "file_path": { "type": "string" }
                },
                "required": ["x", "y", "file_path"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"}
                },
                "required": ["file_path"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_text_from_csv",
            "description": "Extract text from a CSV file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"}
                },
                "required": ["file_path"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to a recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": { "type": "string", "description": "Recipient email" },
                    "subject": { "type": "string", "description": "Email subject" },
                    "body": { "type": "string", "description": "Email body content" }
                },
                "required": ["to", "subject", "body"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_todo",
            "description": "Add a generic task or item to the Todo list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The description of the task to be added"
                    }
                },
                "required": ["task"],
                "additionalProperties": False
            }
        }
    }
]
