# set up environment
source /usr/local/nvm/nvm.sh

source /home/turbo_tally.backend/env/bin/activate

hostname -I > ip_address && 

# run api server
nodemon \
    --exec "./env/bin/python3 -m server" \
    --ext "*" \
    --ignore "**/__pycache__" \
    --ignore "**/*.log" &


# do not exit
sleep infinity
