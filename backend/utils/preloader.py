#
# :: preloader.py
# Preload other modules needed before other scripts 
# 

# load dotenv
from dotenv import load_dotenv 
load_dotenv(".env")

# load formats and validators
import modules.common.formats 