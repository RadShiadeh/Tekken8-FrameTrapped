import json
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


class Extractor():
    def __init__(self, *args, **kwargs):
        super(Extractor, self).__init__(*args, **kwargs)
    

    def get_all_new_replays(self, url, url_latest, latest=None): # url_latest: "https://wank.wavu.wiki/api", url: "#"https://wank.wavu.wiki/api/replays"
        
        break_point = 0
        if latest:
            break_point = latest
        
        before = self.get_latest_api_entry(url_latest)
        latest_entry = before
        if before == -1:
            raise Exception("failed to get the latest 'before' parameter")
        
        replays = []
        log = 1
        while True:
            res = requests.get(url, params={"before": before}).json()
            if not res or before <= break_point:
                print(f"Reached the end of all new enteries\n"
                    f"number of new entries: {len(replays)}\n"
                    f"latest battle_at: {break_point}\n"
                    f"passed in 'before' parameter: {before}")
                break
            
            replays.extend(res)
                
            before = min(float(r["battle_at"]) for r in res) - 700
            if log % 10 == 0:
                print(f"fetched {len(replays)}")
            
            log += 1
        
        replays_df = pd.DataFrame(replays)
        replays_df.drop(columns=["battle_at", "battle_type", "p1_rank","battle_id", "game_version", "p1_area_id", "p2_area_id", "p1_lang", "p2_lang", "p1_power", "p2_power", "p1_rating_before", "p2_rating_before", "p2_rating_change", "p1_rating_change", "p1_region_id", "p2_region_id", "p1_rounds", "p2_rounds"], axis=1)
        
        
        return replays_df, latest_entry
            


    def get_latest_api_entry(self, url): #"https://wank.wavu.wiki/api"
        
        text = ""
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            main_section = soup.find("main", class_="document")
            if main_section:
                dl_tag = main_section.find("dl")
                if dl_tag:
                    dd_tags = dl_tag.find_all("dd")
                    text = dd_tags[0].text.strip()
                else:
                    print("No <dl> tag found in <main class='document'>.")
            else:
                print("No <main class='document'> tag found.")
        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
        
        m = re.search(r"default:\s*(\d+)", text)
        max_entry = 0
        
        if m:
            max_entry = m.group(1)   
        
        return int(max_entry) if int(max_entry) > 0 else -1