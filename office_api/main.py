from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse

from office_api.schemas import TaskEvaluationRequest
from evaluator.evaluate_contain import evaluate_contain

from .stats import generate_success_rate_plot
from .stats_xlh_tasks import generate_xlh_tool_plot
from .state import (
    calendar_events,
    csv_extract,
    emails,
    todos,
    files_read,
    pdf_texts,
    written_files,
    tool_metrics,
    xlh_tool_metrics
)

from .tools import (
    extract_text_from_pdf,
    read_excel,
    read_file,
    write_file,
    generate_chart,
    read_csv,
)

app = FastAPI(title="Groq Tools API", version="1.0")


# ===================== MODELS =====================

class CalendarEvent(BaseModel):
    title: str
    date: str
    time: str


class Email(BaseModel):
    to: str
    subject: str
    body: str


class Todo(BaseModel):
    task: str


class FilePath(BaseModel):
    file_path: str


class WriteFileRequest(BaseModel):
    file_path: str
    content: str


class ChartRequest(BaseModel):
    title: str | None = None
    x: list[str]
    y: list[float]
    x_label: str | None = None
    y_label: str | None = None
    file_path: str


# ===================== CALENDAR =====================

@app.post("/calendar/add")
def api_add_calendar_event(event: CalendarEvent):
    calendar_events.append(event.dict())

    tool_metrics["calendar_add"]["total"] += 1
    tool_metrics["calendar_add"]["success"] += 1
    xlh_tool_metrics["calendar_add"]["total"] += 1
    xlh_tool_metrics["calendar_add"]["success"] += 1

    return {"status": "ok", "event": event.dict()}


@app.get("/calendar")
def get_calendar_events():
    return calendar_events


# ===================== EMAIL =======================

@app.post("/email/send")
def send_email(email: Email):
    emails.append(email.dict())

    tool_metrics["email_send"]["total"] += 1
    tool_metrics["email_send"]["success"] += 1
    xlh_tool_metrics["email_send"]["total"] += 1
    xlh_tool_metrics["email_send"]["success"] += 1

    return {"status": "sent", "email": email.dict()}


@app.get("/email")
def get_emails():
    return emails


# ======================= TODO =======================

@app.post("/todo/add")
def add_todo(todo: Todo):
    todos.append(todo.dict())

    tool_metrics["todo_add"]["total"] += 1
    tool_metrics["todo_add"]["success"] += 1
    xlh_tool_metrics["todo_add"]["total"] += 1
    xlh_tool_metrics["todo_add"]["success"] += 1

    return {"status": "added", "todo": todo.dict()}


@app.get("/todo")
def get_todos():
    return todos


# ==================== FILE ==========================

@app.post("/file/read")
def api_read_file(req: FilePath):
    tool_metrics["file_read"]["total"] += 1
    xlh_tool_metrics["file_read"]["total"] += 1

    try:
        content = read_file(req.file_path)
        files_read.append(req.dict() | {"content": content})

        tool_metrics["file_read"]["success"] += 1
        xlh_tool_metrics["file_read"]["success"] += 1

        return {"content": content}
    except Exception as e:
        return {"error": str(e)}


@app.post("/file/write")
def api_write_file(req: WriteFileRequest):
    tool_metrics["file_write"]["total"] += 1
    xlh_tool_metrics["file_write"]["total"] += 1

    try:
        write_file(req.file_path, req.content)
        written_files.append(req.dict())

        tool_metrics["file_write"]["success"] += 1
        xlh_tool_metrics["file_write"]["success"] += 1

        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/file/written")
def get_written_files():
    return written_files


# ===================== PDF ==========================

@app.post("/pdf/extract")
def api_extract_pdf(req: FilePath):
    tool_metrics["pdf_extract"]["total"] += 1
    xlh_tool_metrics["pdf_extract"]["total"] += 1

    try:
        text = extract_text_from_pdf(req.file_path)
        pdf_texts.append(req.dict() | {"content": text})

        tool_metrics["pdf_extract"]["success"] += 1
        xlh_tool_metrics["pdf_extract"]["success"] += 1

        return {"text": text}
    except Exception as e:
        return {"error": str(e)}


@app.get("/pdf/texts")
def get_pdf_texts():
    return pdf_texts


# ===================== EXCEL ========================

@app.post("/excel/read")
def api_read_excel(req: FilePath):
    tool_metrics["excel_read"]["total"] += 1
    xlh_tool_metrics["excel_read"]["total"] += 1

    try:
        content = read_excel(req.file_path)
        files_read.append(req.dict() | {"content": content})

        tool_metrics["excel_read"]["success"] += 1
        xlh_tool_metrics["excel_read"]["success"] += 1

        return {"content": content}
    except Exception as e:
        return {"error": str(e)}


# ===================== CSV ==========================

@app.post("/csv/extract")
def api_extract_csv(req: FilePath):
    tool_metrics["csv_extract"]["total"] += 1
    xlh_tool_metrics["csv_extract"]["total"] += 1

    try:
        text = read_csv(req.file_path)
        csv_extract.append(req.dict() | {"content": text})
        tool_metrics["csv_extract"]["success"] += 1
        xlh_tool_metrics["csv_extract"]["success"] += 1

        return {"text": text}
    except Exception as e:
        return {"error": str(e)}


# ===================== CHART ========================

@app.post("/chart/generate")
def chart_generate(req: ChartRequest):
    tool_metrics["chart_generate"]["total"] += 1
    xlh_tool_metrics["chart_generate"]["total"] += 1
    
    try:
        result = generate_chart(req.dict())
        
        tool_metrics["chart_generate"]["success"] += 1
        xlh_tool_metrics["chart_generate"]["success"] += 1
        
        return result
    except Exception as e:
        return {"error": str(e)}

# ===================== METRICS ======================

@app.get("/state")
def get_state():
    return {
        "calendar_events": calendar_events,
        "emails": emails,
        "todos": todos,
        "files_read": files_read,
        "written_files": written_files,
        "pdf_texts": pdf_texts,
        "csv_extract": csv_extract
    }


@app.get("/metrics")
def get_metrics():
    out = {}
    for tool, stats in tool_metrics.items():
        total = stats["total"]
        success = stats["success"]
        out[tool] = {
            "total": total,
            "success": success,
            "success_rate": success / total if total > 0 else 0
        }
    return out


# ===================== XLH TASKS =====================

EVALUATION_FUNCTIONS = {
    "evaluate_contain": evaluate_contain
}

def run_evaluation(eval_spec):
    fn_name = eval_spec["function"]
    args = eval_spec["args"]

    if fn_name not in EVALUATION_FUNCTIONS:
        return {"success": False, "reason": "unknown_function"}

    return EVALUATION_FUNCTIONS[fn_name](**args)


@app.post("/xlh_tasks_state")
def evaluate_task(request: TaskEvaluationRequest):
    results = []

    for eval_spec in request.evaluations:
        result = run_evaluation(eval_spec.dict())
        results.append({
            "function": eval_spec.function,
            "result": result
        })

    success = all(r["result"]["success"] for r in results)

    return {
        "task_id": request.task_id,
        "language": request.language,
        "success": success,
        "details": results
    }


@app.get("/metrics/xlh/tools")
def get_xlh_tool_metrics():
    out = {}
    for fn, stats in xlh_tool_metrics.items():
        total = stats["total"]
        success = stats["success"]
        out[fn] = {
            "total": total,
            "success": success,
            "success_rate": success / total if total > 0 else 0
        }
    return out


# ===================== PLOTS ========================

@app.get("/metrics/plot")
def get_metrics_plot():
    path = generate_success_rate_plot()
    return FileResponse(path, media_type="image/png", filename="success_rate.png")


@app.get("/metrics/xlh/tools/plot")
def get_xlh_tool_plot():
    path = generate_xlh_tool_plot()
    return FileResponse(path, media_type="image/png", filename="xlh_tool_success_rate.png")
