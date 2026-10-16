FROM python:3.11-slim
WORKDIR /app
COPY backend-shared/ /app/backend_shared/
COPY backend-order/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend-order/app/ /app/app/
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]