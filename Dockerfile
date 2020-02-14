FROM python:3
COPY . /
RUN python -m pip install -r requirements.txt
CMD [ "python", "kanshi.py" ]
