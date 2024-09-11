FROM python:3.10-bullseye

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /school_managment_saas 

ADD . /school_managment_saas/

# RUN apt-get update
# RUN apt-get install gcc default-libmysqlclient-dev -y

# install dependencies
# RUN pip install -U pip setuptools wheel
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

 

EXPOSE 8001

CMD ["gunicorn", "--bind", "0.0.0.0:8001", "school_managment_saas.wsgi:application"]

# Convert plain text files from Windows or Mac format to Unix
# RUN apt-get install dos2unix
# RUN dos2unix --newfile docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# # Make entrypoint executable
# RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# # Entrypoint dependencies
# RUN apt-get install netcat -y

# # run entrypoint.sh
# ENTRYPOINT ["bash", "/usr/local/bin/docker-entrypoint.sh"]