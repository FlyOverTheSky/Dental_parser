FROM joyzoursky/python-chromedriver:3.8

WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt
RUN pip install uvicorn
RUN pip install redis
COPY . /src

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
