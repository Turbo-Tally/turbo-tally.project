source /usr/local/nvm/nvm.sh 

# run api server
nodemon --exec python3 -m api.server --ext "*" --ignore "**/__pycache__"