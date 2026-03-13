.PHONY: limpiar backend frontend arbol

limpiar:
	@echo "Limpiando proyecto"
	rm -rf ./app/__pycache__
	rm -rf ./frontend/__pycache__
	rm -rf ./.mypy_cache

backend:
	@echo "Comenzando el backend"
	make limpiar
	uv run fastapi dev app/main.py --port 8000

frontend:
	@echo "Comenzando el frontend"
	make limpiar
	uv run streamlit run frontend/app.py

arbol:
	LC_COLLATE=C tree