FROM centos:centos7

RUN yum -y update && \
    yum -y install epel-release && \
    yum -y install python-pip && \
    yum -y install gcc libffi-devel python-devel openssl-devel && \
    pip install --upgrade pip && \
    pip install virtualenv --upgrade && \
    yum clean all && \
    rm -rf /tmp/* /var/tmp/*

RUN useradd --create-home -s /bin/bash user
WORKDIR /home/user
USER user

COPY requirements.txt ./requirements.txt

RUN virtualenv ./venv && \
    ./venv/bin/pip install -r ./requirements.txt

COPY modules ./modules
COPY static ./static
COPY app.py ./app.py
COPY auth_handler.py ./auth_handler.py
COPY config_handler.py ./config_handler.py
COPY dashboard.conf ./dashboard.conf

EXPOSE 8443

COPY docker-entrypoint.sh  ./
ENTRYPOINT ["sh", "docker-entrypoint.sh"]
