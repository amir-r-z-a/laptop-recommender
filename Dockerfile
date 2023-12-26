FROM python:3.11-slim

WORKDIR /opt/lr-ml

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./*.py ./

EXPOSE 8000

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "main:app"]
