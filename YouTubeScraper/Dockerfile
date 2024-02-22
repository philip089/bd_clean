FROM ubuntu


# Prerequisites

RUN \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y python3 python3-pip cron sudo wget && \
  pip install --upgrade pip -i https://pypi.python.org/simple && \
  pip install docker paramiko && \
  mkdir scraper &&\
  mkdir scraper/data

COPY scraper.py scrapertodocker.py country_codes.txt api_key.txt ./scraper/



RUN \
  chmod 0644 /scraper/scraper.py && \
  crontab -l | { cat; echo "0 12 * * * python /scraper/scraper.py"; } | crontab - && \
  crontab -l | { cat; echo "5 12 * * * python /scraper/scrapertodocker.py"; } | crontab - && \
  crontab -l | { cat; echo "* * * * * echo test > output.txt"; } | crontab - && \
  touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
# Run the command on container startup

  





