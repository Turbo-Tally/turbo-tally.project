# set up environment
source /usr/local/nvm/nvm.sh

hostname -I > ip_address && 

# run api server
nodemon \
    --exec "./env/bin/python3 -m server" \
    --ext "*" \
    --ignore "**/__pycache__" \
    --ignore "**/*.log" &

# run exchange rates fetcher
nodemon \
    --exec "./env/bin/python3 -m scans.scripts.fetch_exchange_rates" \
    --ext "*" \
    --ignore "**/__pycache__" \
    --ignore "**/*.log" &

# do not exit
sleep infinity
