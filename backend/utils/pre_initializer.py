from scans.repositories.channels import channels 
from scans.services.admin import Admin

if channels.count_all() == 0: 
    Admin.register_channel("UCL_PUTuqwYwTxwRzA5lJTKA")
    Admin.register_channel("UCVyNJy0q_Q2XB873gEkmgjQ")
    Admin.register_channel("UC6KOeUNz7WRZ3lVge40RnrQ")