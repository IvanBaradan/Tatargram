# Makefile for Telegram CRM Service

.PHONY: help install run test db-init clean

help:
	@echo "Telegram CRM Service - Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install     Install dependencies"
	@echo "  make run         Run the service"
	@echo "  make test        Run tests"
	@echo "  make db-init     Initialize database"
	@echo "  make clean       Clean Python cache files"

install:
	pip install -r requirements.txt

run:
	python telegram_api/main.py

test:
	python -m pytest tests/

db-init:
	python init_db.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf venv/