FROM joyzoursky/python-chromedriver:3.8

WORKDIR /backend
COPY requirements.txt /backend
RUN pip install -r requirements.txt
RUN pip install uvicorn
RUN pip install redis
COPY . /backend

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
