FROM python:3.7
COPY . /
ARG token
ENV token ${token}
RUN python -m pip install -r requirements.txt
CMD [ "python", "kanshi.py" ]
