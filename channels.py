import json
import os
import config
import requests

class Channel:
    def __init__(self) -> None:
        self.server = config.provider['server']
        self.username = config.provider['username']
        self.password = config.provider['password']

        # Ensure the data directory exists
        os.makedirs('data', exist_ok=True)

        # Load categories from categories.json
        with open("indian_categories.json") as file:
            self.categories = json.load(file)

    def get_all_channels(self) -> list:
        url = f"{self.server}/player_api.php?username={self.username}&password={self.password}&action=get_live_streams"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            with open("data/all_channels.json", "w") as file:
                json.dump(data, file, indent=4)
            print("Fetched and saved all channels successfully.")
            return data
        except requests.RequestException as e:
            print(f"Failed to fetch channels from the server: {e}")
            return []

    def get_category_name(self, category_id):
        return [category['category_name'] for category in self.categories if category['category_id'] == category_id][0]
    
    def get_indian_channels(self) -> list:
        try:
            with open("data/all_channels.json") as file:
                data = json.load(file)
            print("Loaded channels from data/all_channels.json.")
        except FileNotFoundError:
            print("all_channels.json not found. Fetching channels from server.")
            data = self.get_all_channels()
        except json.JSONDecodeError:
            raise Exception("Error decoding JSON from data/all_channels.json.")

        indian_links = [{**item, "category_name": self.get_category_name(item['category_id'])} for item in data if item['category_id'] in [category['category_id'] for category in self.categories]]

        # Remove duplicates
        indian_links = [dict(t) for t in {tuple(d.items()) for d in indian_links}]

        # Write the filtered channels to indian_channels.json
        with open("data/indian_channels.json", "w") as file:
            json.dump(indian_links, file, indent=4)
        print("Filtered and saved Indian channels successfully.")

        return indian_links

    def generate_m3u(self, channels, file_name) -> None:
        epg_url = "http://rstream.me/epg.xml.gz"

        if not channels:
            print("No channels found or error reading data.")
            return

        playlist = f"#EXTM3U x-tvg-url=\"{epg_url}\"\n"

        for channel in channels:
            stream_id = channel.get('stream_id', '')
            channel_name = channel.get('name', '')
            channel_logo = channel.get('stream_icon', '')
            channel_category = channel.get('category_name', '')
            channel_country = "India"
            channel_language = "Hindi"
            url = f"http://mega4k.one:8080/live/{self.username}/{self.password}/{stream_id}.ts"

            playlist += (
                f"#EXTINF:-1 tvg-id=\"{stream_id}\" tvg-name=\"{channel_name}\" "
                f"tvg-country=\"{channel_country}\" tvg-language=\"{channel_language}\" "
                f"tvg-logo=\"{channel_logo}\" tvg-chno=\"{channel.get('num', '')}\" "
                f"group-title=\"{channel_category}\",{channel_name}\n{url}\n"
            )

        # Write the m3u playlist to a file
        with open(f"data/{file_name}", "w") as file:
            file.write(playlist)
        print(f"m3u playlist saved as data/{file_name}")

    def generate_hd_m3u(self, indian_channels, file_name) -> None:
        # Check if "HD" or "4K" is in the channel name
        hd_indian_links = [item for item in indian_channels if any(term in item['name'].upper() for term in ["HD", "4K"])]

        # Write the filtered HD channels to indian_hd_channels.json
        with open("data/indian_hd_channels.json", "w") as file:
            json.dump(hd_indian_links, file, indent=4)
        print("Filtered and saved HD/4K channels to data/indian_hd_channels.json.")

        # Generate the m3u playlist for HD channels
        self.generate_m3u(hd_indian_links, file_name)
