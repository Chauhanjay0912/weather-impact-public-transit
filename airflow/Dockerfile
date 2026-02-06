FROM apache/airflow:2.7.0-python3.9

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Jupyter and analysis packages
RUN pip install --no-cache-dir \
    jupyter \
    nbconvert \
    pandas \
    numpy \
    matplotlib \
    seaborn \
    scipy \
    sqlalchemy \
    psycopg2-binary
