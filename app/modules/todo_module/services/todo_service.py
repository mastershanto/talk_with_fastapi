from app.modules.todo_module.domain.repositories import TodoRepository


class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def list_todos(self):
        return self.repository.list()
