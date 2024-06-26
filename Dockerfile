FROM python:3.12

RUN mkdir /shortly_links

WORKDIR /shortly_links

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /shortly_links/docker/*.sh

# CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]