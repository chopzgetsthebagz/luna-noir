.PHONY: run dev prod test install clean help

help:
	@echo "Luna Noir Bot - Available Commands:"
	@echo "  make dev      - Run with Flask development server"
	@echo "  make run      - Alias for 'make dev'"
	@echo "  make prod     - Run with Gunicorn (production)"
	@echo "  make test     - Run tests with pytest"
	@echo "  make install  - Install dependencies"
	@echo "  make clean    - Clean up cache and temporary files"

dev:
	flask --app src/server/app run --port 5050 --debug

run: dev

prod:
	gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - "src.server.app:app"

test:
	pytest -q

install:
	pip install -r requirements.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

