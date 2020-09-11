FROM python:3.7
COPY . /
ARG TOKEN
RUN python -m pip install -r requirements.txt
CMD [ "python", "main.py" ]
