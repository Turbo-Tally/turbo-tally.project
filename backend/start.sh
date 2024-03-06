# set up environment
source /usr/local/nvm/nvm.sh

# run api server
nodemon \
    --exec "./env/bin/python3 -m api.server" \
    --ext "*" \
    --ignore "**/__pycache__" &

sleep infinity
