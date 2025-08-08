FROM python:3.13-alpine
WORKDIR /ims
COPY ims ims
COPY static static
COPY templates templates
COPY sql sql
COPY requirements.txt run.py .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "run.py", "0.0.0.0"]
EXPOSE 5000
