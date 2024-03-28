FROM ubuntu:22.04 

RUN mkdir /home/turbo_tally.backend

# create working directory
WORKDIR /home/turbo_tally.backend 
COPY . /home/turbo_tally.backend
RUN mkdir /usr/local/nvm

ENV HOME /root
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 20.11.1

# update
RUN apt update 

# install virtual environment 
RUN apt install -y python3-virtualenv 

# install curl 
RUN apt-get -y install curl 

# install node.js 
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
RUN . $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use default && \ 
    npm install -g nodemon

# activate virtual environment
# RUN . /home/turbo_tally.backend/env/bin/activate  

# export paths
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/v$NODE_VERSION/bin:$PATH