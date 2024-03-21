FROM joyzoursky/python-chromedriver:3.8

WORKDIR /Dental_parser/backend
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install uvicorn
RUN pip install redis
COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
