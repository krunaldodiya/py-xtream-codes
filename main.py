from channels import Channel


channel = Channel()
indian_channels = channel.get_indian_channels()
channel.generate_m3u(indian_channels, "indian_channels.m3u")
channel.generate_hd_m3u(indian_channels, "indian_hd_channels.m3u")