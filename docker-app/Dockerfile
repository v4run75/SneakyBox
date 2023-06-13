From ubuntu:20.04
MAINTAINER v4run.academics@gmail.com

RUN apt-get update -y
RUN apt-get install python3-pip -y

RUN mkdir -p /home/admin/cloudsec

COPY requirements.txt requirements.txt
COPY cloudsec /home/admin/cloudsec

RUN pip install waitress
RUN pip install -r requirements.txt

WORKDIR /home/admin/


CMD ["waitress-serve", "--call", "cloudsec:create_app"]
