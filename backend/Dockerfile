FROM python:3.10.5-alpine3.16

WORKDIR /app/backend

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app"]