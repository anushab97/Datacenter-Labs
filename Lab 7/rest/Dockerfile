FROM python:3.8

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install flask pika redis requests jsonpickle Pillow
WORKDIR /srv
COPY rest-server-all.py /srv


#ENV	FLASK_PORT 5000
ENV FLASK_APP=rest-server-all.py
EXPOSE 5000

CMD	["python3", "rest-server-all.py"]