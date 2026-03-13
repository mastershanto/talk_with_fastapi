"""
FastAPI reference project — app package.

Architecture overview
---------------------
app/
  config.py          Settings (pydantic-settings, env / .env override)
  database.py        Engine, SessionLocal, Base
  dependencies.py    get_db, DBSession alias, PaginationParams
  exceptions.py      Custom exceptions + global exception handlers
  main.py            Application factory + lifespan
  models/
    base.py          TimestampMixin
    user.py          User ORM model
    item.py          Item ORM model
  schemas/
    common.py        MessageResponse, PaginatedResponse
    user.py          UserCreate / UserUpdate / UserResponse ...
    item.py          ItemCreate / ItemUpdate / ItemResponse
  crud/
    base.py          Generic CRUDBase[ModelT, CreateSchemaT, UpdateSchemaT]
    user.py          CRUDUser + user_crud singleton
    item.py          CRUDItem + item_crud singleton
  routers/
    users.py         GET / POST / PUT / DELETE /api/v1/users
    items.py         GET / POST / PUT / DELETE /api/v1/items
"""
__version__ = "2.0.0"
