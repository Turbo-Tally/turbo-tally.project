# set up environment
source /usr/local/nvm/nvm.sh

hostname -I > ip_address && 

# run api server
nodemon \
    --exec "./env/bin/python3 -m server" \
    --ext "*" \
    --ignore "**/__pycache__" &

sleep infinity
