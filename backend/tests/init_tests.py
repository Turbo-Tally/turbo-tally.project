from dotenv import load_dotenv  
load_dotenv(".env")
import os
BASE_URL = f"http://{os.getenv('HOST_IP')}"