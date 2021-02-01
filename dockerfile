FROM python:3 

COPY . /documentive

RUN apt-get update && apt-get install -y libgtk2.0-0 libgtk-3-0 libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb libgbm-dev
RUN pip install -r /documentive/requirements.txt

CMD [ "python", "-u", "/documentive/documentive.py" ]



