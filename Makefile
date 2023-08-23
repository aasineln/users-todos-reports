SHELL=/bin/bash

setup: env-prepare venv-prepare

env-prepare:
	cp -n .env.example .env

venv-prepare:
	python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

run:
	source venv/bin/activate && python main.py
