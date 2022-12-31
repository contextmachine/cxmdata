FROM python:latest
COPY . /cxmdata
RUN python -m pip install ./cxmdata
ENTRYPOINT ["python"]
