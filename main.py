import json
import os
from transform import Transformer
from plot import Plot
from ingestion import Extractor
from datetime import datetime


def main():
    
    whole_process_timer = datetime.now()
    print(f"starting, curr time: {whole_process_timer}")
    
    unused_idxs = [25,26,27,30,31,37]
    unused_idxs = set(unused_idxs)


    rank_mapping = {
        0: "Beginner",
        1: "1st Dan",
        2: "2nd Dan",
        3: "Fighter",
        4: "strategist",
        5: "combatant",
        6: "Brawler",
        7: "Ranger",
        8: "Cavalry",
        9: "Warrior",
        10: "Assailant",
        11: "Dominator",
        12: "Vanquisher",
        13: "Destroyer",
        14: "Eliminator",
        15: "Garyu",
        16: "Shinryu",
        17: "Tenryu",
        18: "Mighty Ruler",
        19: "Flame Ruler",
        20: "Battle Ruler",
        21: "Fujin",
        22: "Raijin",
        23: "Kishin",
        24: "Bushin",
        25: "Tekken King",
        26: "Tekken Emperor",
        27: "Tekken God",
        28: "Tekken God Supreme",
        29: "God of Destruction"
        }



    playable_char_map = {
                0: "Paul",
                1: "Law",
                2: "King",
                3: "Yoshimitsu",
                4: "Hworang",
                5: "Ling",
                6: "Jin",
                7: "Bryan",
                8: "Kazuya",
                9: "Steve",
                10: "Jack",
                11: "Asuka",
                12: "Devil Jin",
                13: "Feng",
                14: "Lili",
                15: "Dragunov",
                16: "Leo",
                17: "Lars",
                18: "Alisa",
                19: "Claudio",
                20: "Shaheen",
                21: "Nina",
                22: "Lee",
                23: "Kuma",
                24: "Panda",
                25: "unknown1", # might be incorrectly set to zafina 
                26: "unknown2",
                27: "unknown3",
                28: "Zafina", #zafina?
                29: "Azucena", #might be incorrect
                30: "unknown4",
                31: "unknown5",
                32: "Jun",
                33: "Reina", #Reina?
                34: "Leroy", #Unknown2
                35: "Victor",
                36: "Raven", #raven?
                37: "unknown6",
                38: "Eddy", #eddy?
                39: "Lidia",
                40: "Heihachi",
                41: "Clive"
            }

    reverse_char_map = {}
    reverse_rank_map = {}

    for i, name in playable_char_map.items():
        reverse_char_map[name] = i


    for i, name in rank_mapping.items():
        reverse_rank_map[name] = i
    
    url_latest = "https://wank.wavu.wiki/api"
    url_replays = "https://wank.wavu.wiki/api/replays"
    
    
    loading_time = datetime.now()
    print("loading existing data...")
    data_path = "./data/replays.json"
    data = []
    if os.path.exists(data_path) and os.path.isfile(data_path):
        with open(data_path, 'r') as f:
            data = json.load(f)
    else:
        print("no existing data found")

    
    latest = None
    data_path_l = "./data/latest_replay.txt"
    if os.path.exists(data_path_l) and os.path.isfile(data_path_l):
        with open(data_path_l, 'r') as f:
            latest = int(f.readline())
    
    loading_time_fin = datetime.now()
    print(f"loading existing data took {loading_time_fin - loading_time}")
    
    transform = Transformer()
    pl = Plot()  
    ingestor = Extractor()  
    
    new_data_time_start = datetime.now()
    print("getting latest data...")  
    new_data = ingestor.get_all_new_replays(url_replays, url_latest, latest)
    
    for nd in new_data:
        data.append(nd)
    
    print(f"collecting new enteries took: {datetime.now() - new_data_time_start}")
    
    print(f"replay length is: {len(data)}")

    unique_ids = set()
    for d in data:
        if d["p1_polaris_id"] not in unique_ids:
            unique_ids.add(d["p1_polaris_id"])
        
        if d["p2_polaris_id"] not in unique_ids:
            unique_ids.add(d["p2_polaris_id"])


    print(f"There are {len(unique_ids)} unique players")
    
    filtering_start = datetime.now()
    print("Filtering and prepping data for visualisation...")
    
    most_pop_data, _ = transform.find_char_popularity(data, playable_char_map)
    char_usage_all_ranks, char_wins_all_ranks = transform.get_chars_global_winrates(data, playable_char_map)
    indv_matchups = transform.get_chars_ind_matchups_winrates(data, playable_char_map, unused_idxs)
    matchup_winrates = transform.head_to_head_char_win_rates(indv_matchups, playable_char_map, unused_idxs, reverse_char_map)
    
    
    fujin_onwards_data = transform.filter_data_based_on_rank(data, reverse_rank_map["Fujin"], reverse_rank_map["Tekken Emperor"])
    most_pop_fujin_onwards, _ = transform.find_char_popularity(fujin_onwards_data, playable_char_map)
    char_usage_Fujin_onwards, char_wins_Fujin_onwards = transform.get_chars_global_winrates(fujin_onwards_data, playable_char_map)
    indv_matchups_fujin = transform.get_chars_ind_matchups_winrates(fujin_onwards_data, playable_char_map, unused_idxs)
    matchup_winrates_fujin = transform.head_to_head_char_win_rates(indv_matchups_fujin, playable_char_map, unused_idxs, reverse_char_map)
    
    god_rank_data = transform.filter_data_based_on_rank(data, reverse_rank_map["Tekken God"], reverse_rank_map["God of Destruction"])
    most_pop_god_ranks, _ = transform.find_char_popularity(god_rank_data, playable_char_map)
    char_usage_god_ranks, char_wins_god_ranks = transform.get_chars_global_winrates(god_rank_data, playable_char_map)
    indv_matchups_god_ranks = transform.get_chars_ind_matchups_winrates(god_rank_data, playable_char_map, unused_idxs)
    matchup_winrates_god_ranks = transform.head_to_head_char_win_rates(indv_matchups_god_ranks, playable_char_map, unused_idxs, reverse_char_map)
    
    rank_data = transform.get_ranked_data(data)
    
    print(f"filtering done, took {datetime.now() - filtering_start}")
    
    print("plotting and saving the output...")
    
    pl.plot_data(most_pop_data, playable_char_map, unused_idxs, 
                 f"Ranked Charactar Popularity Data % (all ranks), no. of replays: {sum(most_pop_data) // 2}", "./pics/char_pop_all", percentage=True)
    
    pl.plot_rank_data(rank_data, rank_mapping, "./pics/rank_dist", True)
    
    pl.plot_char_winrates(char_usage_all_ranks, char_wins_all_ranks, unused_idxs, playable_char_map,
                          f"character winrate % sorted high to low, all ranks, data length: {sum(char_usage_all_ranks) // 2}", "./pics/char_winrate_all", True)
    
    pl.plot_data(most_pop_fujin_onwards, playable_char_map, unused_idxs, 
                 f"Ranked Charactar Popularity %, Fujin to Tekken Emperor, data length: {sum(most_pop_fujin_onwards) // 2}", "./pics/char_pop_fujin", True)
    
    pl.plot_char_winrates(char_usage_Fujin_onwards, char_wins_Fujin_onwards, unused_idxs, playable_char_map, 
                          f"Global winrate %, Fujin to Tekken Emperor, data length: {sum(char_usage_Fujin_onwards) // 2}", "./pics/char_win_fujin", True)
    
    pl.plot_data(most_pop_god_ranks, playable_char_map, unused_idxs, 
                 f"Ranked Charactar Popularity %, God Ranks, data length: {sum(most_pop_god_ranks) // 2}", "./pics/char_pop_God", True)
    
    pl.plot_char_winrates(char_usage_god_ranks, char_wins_god_ranks, unused_idxs, playable_char_map, 
                          f"God Ranks winrate %, total data: {sum(char_usage_god_ranks) // 2}", "./pics/char_win_god", True)
    
    pl.plot_heatmap(matchup_winrates, playable_char_map, unused_idxs, "./pics/heatmap_all", "character head to head win rates, all ranks")
    pl.plot_heatmap(matchup_winrates_fujin, playable_char_map, unused_idxs, "./pics/heatmap_fujin", "character head to head win rates, Fujin to Tekken Emperor")
    pl.plot_heatmap(matchup_winrates_god_ranks, playable_char_map, unused_idxs, "./pics/heatmap_god", "character head to head win rates, God ranks")
    
    update_timer = datetime.now()
    print(f"updating local enteries... {update_timer}")
    ingestor.update_local_json_replays(data_path, data)
    print(f"local data updated! took: {datetime.now() - update_timer}\n")
    
    print(f"done! whole process took: {datetime.now() - whole_process_timer}")


if __name__ == "__main__":
    main()