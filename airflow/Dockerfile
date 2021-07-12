FROM apache/airflow
USER root
RUN apt update \
    && apt install -y p7zip-full \
    && apt-get install -y libreoffice libreoffice-style-breeze \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --no-cache-dir --user psycopg2 
RUN pip install --no-cache-dir --user xmltodict 
RUN pip install --no-cache-dir --user lxml



