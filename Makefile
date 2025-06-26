db:
	docker compose up -d --build strategy_db_inventory

start:
	python3 app/api/main.py