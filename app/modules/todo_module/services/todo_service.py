from app.modules.todo_module.domain.entities import Todo
from app.modules.todo_module.domain.repositories import TodoRepository


class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def list_todos(self):
        return self.repository.list()

    def get_todo(self, todo_id: int):
        return self.repository.get(todo_id)

    def create_todo(self, title: str, description: str | None):
        todo = Todo(id=None, title=title, description=description)
        return self.repository.create(todo)

    def update_todo(self, todo_id: int, title: str, description: str | None, completed: bool):
        todo = Todo(id=todo_id, title=title, description=description, completed=completed)
        return self.repository.update(todo_id, todo)

    def delete_todo(self, todo_id: int):
        return self.repository.delete(todo_id)

