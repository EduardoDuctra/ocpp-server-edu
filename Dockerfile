FROM python:3.10 as base


FROM base 
WORKDIR /app
COPY ./ ./

RUN pip3 install -r requirements.txt

EXPOSE 9000
EXPOSE 8080
ENTRYPOINT ["python3", "main.py"]

