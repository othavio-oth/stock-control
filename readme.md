create automatic migration = alembic revision --autogenerate -m "description of changes"
Create Migrations = alembic revision -m "Create Migrations"
Make Migrate = alembic upgrade head

Use tests = PYTHONPATH=$(pwd) pytest tests/

| Métrica                           | Como calcular                                        |
| --------------------------------- | ---------------------------------------------------- |
| **Custo total**                   | `entry_price × quantity_ordered`                     |
| **Receita total**                 | `unit_price × quantity_sold`                         |
| **Lucro total**                   | `receita_total - custo_total`                        |
| **Lucro por unidade vendida**     | `(unit_price - entry_price)`                         |
| **% de lucro (markup)**           | `(lucro_total / custo_total) × 100`                  |
| **Perda por produto não vendido** | `(entry_price × (quantity_ordered - quantity_sold))` |
