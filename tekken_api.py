import json
import requests

def get_all_replays(url):
    before = 1732107578
    replays = []
    log = 1
    
    while True:
        res = requests.get(url, params={"before": before}).json()
        if not res:
            print(f"sth went wrong\n"
                  f"{res}\n")
            break
        
        replays.extend(res)
            
        before = min(float(r["battle_at"]) for r in res) - 700
        if log % 10 == 0:
            print(f"fetched {len(replays)} replays for Glonki")
        
        log += 1
    
    return replays


def main():
    rep = get_all_replays("https://wank.wavu.wiki/api/replays")
    with open("data/Rad_replays.json", "w") as f:
        json.dump(rep, f, indent=4)
    
    f.close()
    
    
if __name__ == "__main__":
    main()