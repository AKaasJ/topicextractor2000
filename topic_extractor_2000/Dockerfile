FROM python:3.11

COPY . /app

RUN pip install -r /app/requirements.txt

EXPOSE 80
WORKDIR /app
CMD streamlit run app.py --server.port 80 --server.address 0.0.0.0