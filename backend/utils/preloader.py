#
# :: preloader.py
# Preload other modules needed before other scripts 
# 

# load dotenv
from dotenv import load_dotenv 
load_dotenv(".env")

# load formats and validators
import modules.common.formats 

# create auto-incrementers 
from modules.repositories.auto_increments import auto_increments

auto_increments.init("answers")
auto_increments.init("choices")
auto_increments.init("counters") 
auto_increments.init("polls") 
auto_increments.init("users")
auto_increments.init("variables") 
auto_increments.init("verif_codes")
