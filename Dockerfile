FROM python:3.9

COPY ["requirements.txt", "setup.py", "setup.cfg", ".env", ".flaskenv", "./"]

ADD chatbot/ ./chatbot

RUN pip install -e . --no-cache-dir

RUN python -m spacy download en

ENV FLASK_APP=chatbot

RUN ["flask", "init-db"]

CMD ["waitress-serve", "--call", "--port=80", "chatbot:create_app"]