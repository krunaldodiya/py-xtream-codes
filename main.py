import xtream
import config

x = xtream

x.server   = config.provider['server']
x.username = config.provider['username']
x.password = config.provider['password']

live_stream_url = x.get_live_streams_URL()

print(live_stream_url)