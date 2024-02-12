FROM python:3.9.18-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ENV DB_HOSTNAME=postgres
ENV DB_PORT=5432
ENV DB_USERNAME=postgres
ENV DB_PASSWORD=postgres
ENV DB_NAME=fastapi
ENV SECRET_KEY=f91ddda468f26afafee7af8851d735ad137ec41447a0b56824ede759e570a24f
ENV ALGORITHM=HS256
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]