FROM python:3.9.7
COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
# COPY app.py /src
# COPY buzz /src/buzz
# CMD python /src/app.py
COPY mainapp /src
CMD python /src/app.py