# set up environment
source /usr/local/nvm/nvm.sh

hostname -I > ip_address && 

# run api server
nodemon \
    --exec "./env/bin/python3 -m server.api" \
    --ext "*" \
    --ignore "**/__pycache__" &

# run exchange rates fetcher
nodemon \
    --exec "./env/bin/python3 -m utils.fetch_exchange_rates" \
    --ext "*" \
    --ignore "**/__pycache__" &

# do not exit
sleep infinity
