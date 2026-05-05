FROM python:3.12-slim
WORKDIR /app
COPY services/vertex_predictor/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ml ./ml
COPY models ./models
COPY services ./services
CMD ["uvicorn", "services.vertex_predictor.app:app", "--host", "0.0.0.0", "--port", "8080"]
