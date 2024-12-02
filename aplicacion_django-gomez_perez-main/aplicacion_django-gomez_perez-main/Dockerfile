	FROM python:latest
	WORKDIR /app
	COPY requirements/requirements.txt requirements.txt* /app/
	RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt && rm requirements.txt; fi
	COPY /requirements/development.txt development.txt* /app/
	RUN if [ -f "development.txt" ]; then pip install --no-cache-dir -r development.txt && rm development.txt; fi
	COPY ProyectoFinal .
	EXPOSE 8000
	CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8000"]

