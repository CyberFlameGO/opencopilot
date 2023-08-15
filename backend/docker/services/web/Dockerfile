FROM continuumio/miniconda3:23.3.1-0

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y gcc logrotate g++ libtidy-dev git libmagic1 tesseract-ocr

ADD environment.yml /
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "backend-service", "/bin/bash", "-c"]

# Logrotate
COPY docker/logrotate_app_logs /etc/logrotate.d/log-file
RUN chmod 644 /etc/logrotate.d/log-file

# Create new user to not run in sudo mode
RUN useradd --create-home appuser
WORKDIR /home/appuser

COPY . /home/appuser

RUN mkdir -p /root/.ssh
RUN echo "StrictHostKeyChecking no" >> /root/.ssh/config

ENTRYPOINT ["./docker/entrypoint.sh"]