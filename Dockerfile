FROM python:3.8.13
WORKDIR /app
COPY . .

EXPOSE 8058

RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
RUN cp ./HTMLTestRunner.py /usr/local/lib/python3.8 
# RUN ls /usr/local/lib/python3.8 | grep HTML & sleep 10

ENTRYPOINT ["python", "/app/app.py" ]
