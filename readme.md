Strategy Inventory API (FastAPI)

Visão geral
- API de inventário/estoque, produtos, tickets e usuários construída com FastAPI, SQLAlchemy e PostgreSQL.
- Autenticação via JWT Bearer. Por padrão, todas as rotas estão protegidas, exceto `/ping` e `/authentication/login`.

Estrutura do projeto
- App: `app/api/main.py` (aplicação FastAPI)
- Rotas: `app/routes/**`
- Serviços/Regra de negócio: `app/service/**`
- Repositórios/DAO: `app/repository/**`
- Modelos ORM: `app/models/**`, Base em `app/database/base.py`
- Middleware (Auth/DB): `app/middleware/**`
- Migrations (Alembic): `alembic/**` e `alembic.ini`

Stack
- Python 3.12, FastAPI, SQLAlchemy 2.x, Alembic, Uvicorn
- PostgreSQL 16
- Docker/Docker Compose

Requisitos
- Python 3.12+ ou Docker
- PostgreSQL acessível via `DATABASE_URL`

Variáveis de ambiente (.env)
- `DATABASE_URL`: ex. `postgresql+psycopg2://user:password@localhost:5432/strategy`
- `SECRET_KEY`: chave secreta do JWT
- `ALGORITHM`: algoritmo do JWT (ex.: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: expiração do token (ex.: `1500`)
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `TZ` (para Docker Compose)

Como rodar (Docker Compose)
1) Copie `.env.example` para `.env` e preencha as variáveis.
2) Suba os serviços:
   - `docker-compose up -d`
3) Aplique as migrations (primeira vez):
   - `docker-compose exec strategy_backend_inventory alembic upgrade head`
4) API em `http://localhost:8000`

Como rodar (local)
1) Crie e ative um venv e instale deps:
   - `python -m venv .venv && source .venv/bin/activate` (Linux/Mac)
   - `.\u005cvenv\Scripts\activate` (Windows)
   - `pip install -r requirements.txt`
2) Configure `.env` com `DATABASE_URL`, `SECRET_KEY`, etc.
3) Rode migrations:
   - `alembic upgrade head`
4) Inicie a API:
   - `uvicorn app.api.main:app --host 0.0.0.0 --port 8000`

Autenticação
- Login: `POST /authentication/login` body: `{"username": "admin", "password": "admin"}`
- Resposta: `{ "access_token": "<JWT>", "token_type": "bearer" }`
- Use o token nas chamadas protegidas:
  - Header: `Authorization: Bearer <JWT>`
- Validar token: `GET /authentication/validate-token` (precisa header `Authorization: Bearer ...`)

Rotas principais (prefixos)
- Usuários: `/users`
- Permissões: `/permissions_adm`
- Papéis: `/roles_adm`
- Vendedores: `/sellers_adm`
- Cadeias (retail chain): `/chains_adm`
- Unidades: `/units_adm`
- Conversões: `/conversions_adm`
- Categorias: `/categories_adm`
- Produtos: `/products_adm`
- Preços de produtos: `/products_adm/prices`
- Fornecedores: `/suppliers_adm`
- Tickets: `/tickets_adm`
- Centros de custo: `/cost_centers_adm`
- Estoque: `/stock_adm`
- Vendas: `/sales`

Pontos públicos
- `GET /ping` — healthcheck
- `POST /authentication/login` — obtém token

Exemplos de uso
- Ping:
  - `curl http://localhost:8000/ping`
- Login:
  - `curl -X POST http://localhost:8000/authentication/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin"}'`
- Listar produtos (protegido):
  - `curl http://localhost:8000/products_adm/products -H "Authorization: Bearer $TOKEN"`

Migrations (Alembic)
- Criar migração automática: `alembic revision --autogenerate -m "descricao"`
- Criar migração vazia: `alembic revision -m "descricao"`
- Aplicar: `alembic upgrade head`

Testes
- Executar: `PYTHONPATH=$(pwd) pytest tests/`
- Windows PowerShell: `$env:PYTHONPATH=(Get-Location); pytest tests/`

CORS
- Origens permitidas definidas em `app/api/main.py` (Vercel/localhost:3000). Ajuste conforme necessário.

Build/Deploy com Docker
- Build local da imagem: `docker build -t strategy-inventory:local .`
- Rodar localmente: `docker run --env-file .env -p 8000:8000 strategy-inventory:local`
- Compose já provisiona Postgres e API; imagem padrão em `docker-compose.yml` é `ghcr.io/othavio-oth/strategy:latest`.

Notas de segurança
- A maior parte das rotas está protegida via `Depends(get_current_user)` aplicado no `include_router` em `app/api/main.py`.
- Para acesso administrativo, algumas rotas usam `is_admin`. Ajuste/expanda permissões em `app/middleware/permission.py`.

Problemas comuns
- 404 com barra final: `redirect_slashes=False` está ativo; as rotas aceitam as duas formas (com e sem `/`).
- 401 Unauthorized: verifique o header `Authorization: Bearer <JWT>` e as variáveis `SECRET_KEY`/`ALGORITHM`.
- Conexão DB: confira `DATABASE_URL` e se as migrations foram aplicadas.

Licença
- Uso interno. Adapte este README às políticas do seu projeto.
