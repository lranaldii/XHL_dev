from pydantic import BaseModel
from typing import List, Dict, Any

class EvaluationSpec(BaseModel):
    function: str
    args: Dict[str, Any]

class TaskEvaluationRequest(BaseModel):
    task_id: str
    language: str
    evaluations: List[EvaluationSpec]
