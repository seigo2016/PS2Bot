FROM python:3.13
WORKDIR /app/
COPY . .
ARG TOKEN
RUN python -m pip install -r requirements.txt
CMD [ "python", "main.py" ]
