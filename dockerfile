FROM python:3
# Or any preferred Python version.
ADD app.py .
ADD mqtt.py .
ADD config.py .
ADD jlinterface.py .
RUN mkdir -p pylacrosse
ADD pylacrosse/ pylacrosse
RUN mkdir -p data
ADD data/ data
RUN mkdir -p routers
ADD routers/ routers

ADD requirements.txt .
RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port",  "8000"] 
