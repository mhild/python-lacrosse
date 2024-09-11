FROM python:3
# Or any preferred Python version.
ADD app.py .
ADD mqtt.py .
ADD config.py .
ADD jlinterface.py .
COPY pylacrosse .
COPY data .
COPY routers .

ADD requirements.txt .
RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port",  "8000"] 