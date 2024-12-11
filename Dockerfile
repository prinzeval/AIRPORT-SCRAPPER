FROM public.ecr.aws/lambda/python:3.10 as stage

RUN yum install -y -q sudo unzip

ENV CHROMIUM_VERSION=1002910

COPY install-browser.sh /tmp/
RUN /usr/bin/bash /tmp/install-browser.sh

FROM public.ecr.aws/lambda/python:3.10 as base

COPY chrome-deps.txt /tmp/
RUN yum install -y $(cat /tmp/chrome-deps.txt)

COPY requirements.txt /tmp/
RUN python3 -m pip install --upgrade pip -q
RUN python3 -m pip install -r /tmp/requirements.txt -q 


COPY --from=stage /opt/chrome /opt/chrome
COPY --from=stage /opt/chromedriver /opt/chromedriver
COPY . ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]