.PHONY: up down demo test eval langsmith-push-eval costreport seed reset logs

up:
	docker compose up --build -d
	@echo "Waiting for services..."
	@sleep 8
	$(MAKE) seed

down:
	docker compose down

demo:
	RUNTIME_MODE=local PYTHONPATH=src python scripts/run_demo.py

costreport:
	RUNTIME_MODE=local PYTHONPATH=src python scripts/cost_report.py

seed:
	RUNTIME_MODE=local DATABASE_URL=postgresql+psycopg://falcon:falcon_local@localhost:5432/falcon_grounds PYTHONPATH=src python scripts/seed_data.py

test:
	PYTHONPATH=src pytest tests/ -v

eval:
	RUNTIME_MODE=local PYTHONPATH=src python eval/run_eval.py

langsmith-push-eval:
	RUNTIME_MODE=local LANGCHAIN_TRACING_V2=true PYTHONPATH=src python eval/langsmith_eval.py

reset:
	RUNTIME_MODE=local PYTHONPATH=src python scripts/reset.py
	docker compose down -v

logs:
	docker compose logs -f api
