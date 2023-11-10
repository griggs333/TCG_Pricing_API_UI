FROM python:3.10-alpine

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt


COPY . /app
EXPOSE 7860
CMD ["python", "/app/app.py", "0.0.0.0:7860"]