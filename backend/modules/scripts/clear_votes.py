# 
# CLEAR VOTES OF POLL 
# 
import utils.preloader 
import sys 

from modules.main.voting import Voting 

poll_id = int(sys.argv[1])

Voting.clear_votes(poll_id) 

print("Cleared votes.")