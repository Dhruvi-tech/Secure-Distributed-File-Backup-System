FROM python:3.11
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD [\"python\", \"node_service.py\"]  # Replace with your actual node service script
