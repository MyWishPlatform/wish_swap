FROM python:3.7.2

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y sudo curl git
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
RUN git clone https://github.com/binance-chain/node-binary.git .
RUN apt-get install git-lfs
RUN git lfs pull -I cli/testnet/0.7.2/linux

COPY . /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
