from datetime import datetime
from pydantic import BaseModel
import datetime

# Create ToDo Schema (Pydantic Model)
class ToDo(BaseModel):
    task: str
    due_date: datetime.date
    is_completed: str
    assigned_to: str
