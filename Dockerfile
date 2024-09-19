FROM python:3.9

RUN mkdir -p /app

WORKDIR /app

ADD . /app

RUN pip3 install -r requirements.txt
EXPOSE 8501

CMD streamlit run main.py