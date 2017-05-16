FROM python:3-alpine
COPY requirements.txt .

ENV TERRAFORM_VERSION=0.9.5

RUN apk add -U ca-certificates curl && \
    curl -fsSLo /tmp/terraform.zip https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip /tmp/terraform.zip -d /usr/bin && \
    rm -rf /tmp/* /var/cache/apk/* /var/tmp/*

RUN pip install --no-cache-dir -r requirements.txt
ADD infra /infra

