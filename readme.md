create automatic migration = alembic revision --autogenerate -m "description of changes"
Create Migrations = alembic revision -m "Create Migrations"
Make Migrate = alembic upgrade head

Use tests = PYTHONPATH=$(pwd) pytest tests/