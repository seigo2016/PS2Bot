FROM python:3.7
COPY . /
ARG TOKEN
ENV token ${TOKEN}
RUN echo $token
RUN python -m pip install -r requirements.txt
CMD [ "python", "kanshi.py" ]
