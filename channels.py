import json

class Channel:
    def __init__(self) -> None:
        self.categories = [
            "35", "186", "187", "188", "189", "190", "191", "192", "193",
            "215", "232", "335", "338", "339", "350", "385", "389", "392",
            "407", "420", "422", "435",
        ]

    def get_indian_channels(self) -> list:
        try:
            with open("all_channels.json") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("The file all_channels.json does not exist.")
            return []
        except json.JSONDecodeError:
            print("Error decoding JSON from all_channels.json.")
            return []

        indian_links = [item for item in data if item['category_id'] in self.categories]

        # Remove duplicates
        indian_links = [dict(t) for t in {tuple(d.items()) for d in indian_links}]

        # Write the filtered channels to indian_channels.json
        with open("indian_channels.json", "w") as file:
            json.dump(indian_links, file, indent=4)

        return indian_links

    def generate_m3u8(self) -> None:
        epg_url = "http://rstream.me/epg.xml.gz"
        channels = self.get_indian_channels()

        if not channels:
            print("No Indian channels found or error reading data.")
            return

        playlist = f"#EXTM3U x-tvg-url=\"{epg_url}\"\n"

        for channel in channels:
            stream_id = channel.get('stream_id', '')
            channel_name = channel.get('name', '')
            channel_logo = channel.get('stream_icon', '')
            channel_country = "India"
            channel_language = "Hindi"
            url = f"http://mega4k.one:8080/live/vicky123/123456/{stream_id}.ts"

            playlist += (
                f"#EXTINF:-1 tvg-id=\"{stream_id}\" tvg-name=\"{channel_name}\" "
                f"tvg-country=\"{channel_country}\" tvg-language=\"{channel_language}\" "
                f"tvg-logo=\"{channel_logo}\" tvg-chno=\"{channel.get('num', '')}\" "
                f"group-title=\"{channel_name}\",{channel_name}\n{url}\n"
            )

        # Write the M3U8 playlist to a file
        with open("indian_channels.m3u8", "w") as file:
            file.write(playlist)

        print("M3U8 playlist saved as indian_channels.m3u8")

# Instantiate the Channel class and generate the M3U8 playlist
channel = Channel()
channel.generate_m3u8()
