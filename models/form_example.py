from typing import List
from typing import Optional

from fastapi import Request


class TaskCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.id: Optional[str] = None
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.priority: Optional[str] = None
        self.owner: Optional[str] = None
        self.status: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.title = form.get("title")
        self.priority = form.get("priority")
        self.owner = form.get("owner")
        self.description = form.get("description")

    def is_valid(self):
        if not self.title or not len(self.title) >= 4:
            self.errors.append("A valid title is required")
        if not self.priority:
            self.errors.append("A valid priority is required")
        if not self.owner or not len(self.owner) >= 1:
            self.errors.append("A valid owner is required")
        if not self.description or not len(self.description) >= 2:
            self.errors.append("Description too short")
        if not self.errors:
            return True
        return False

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'owner': self.owner,
            'status': ""
        }