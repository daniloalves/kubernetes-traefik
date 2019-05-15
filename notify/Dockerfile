FROM alpine
LABEL maintainer="daniloalves/kubernetes-traefik"

LABEL NAME="eks-traefik-notify"

# Instalando dependencias
RUN apk update && \
    apk add python3 && \
    rm -rf /var/cache/apk/*

# Install aws-cli
RUN apk -Uuv add python3 
RUN pip3 install boto3
RUN pip3 install requests
RUN apk --purge -v del py-pip
RUN rm /var/cache/apk/*

COPY src/ /opt/

# Diretorio onde sera executado os scripts
WORKDIR /opt

# Iniciando aplicacao
ENTRYPOINT ["/usr/bin/python3","-u","consumer/consumer.py"]
