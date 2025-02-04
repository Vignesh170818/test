FROM python:3.11-bullseye
RUN mkdir -p /opt/app/genwiz
RUN chmod -R 777 /opt/app/genwiz
#COPY ./requirements.txt /opt/app/genwiz
COPY . /opt/app/genwiz
RUN chmod +x /opt/app/genwiz/cron.sh
WORKDIR /opt/app/genwiz
RUN apt-get update && apt-get install dos2unix && apt-get upgrade --yes && apt-get install --yes --no-install-recommends && pip install --upgrade pip && pip --no-cache-dir install -r /opt/app/genwiz/requirements.txt 
RUN dos2unix /opt/app/genwiz/*
RUN ls -ltr /opt/app/genwiz
 
ARG USERNAME=testuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID
 
# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
&& useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
&& apt-get update \
&& apt-get install -y sudo \
&& echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
&& chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME

#EXPOSE 8081
EXPOSE 8000
ENTRYPOINT ["/bin/sh","-c","/opt/app/genwiz/cron.sh >>/home/LogFiles/docker.log 2>&1"]