import os

from dotenv import load_dotenv

load_dotenv()

provider = dict(
    server=os.getenv("SERVER"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
)

# write json responses to files
write_files = 1

# maybe you don't want all that detail
display_series_info = 0
display_live_info = 0
display_vod_info = 1

# write the series info json responses to files
write_series_info_files = 0
write_live_info_files = 0
write_vod_info_files = 0