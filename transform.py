
class Transformer():
    def __init__(self, *args, **kwargs):
        super(Transformer, self).__init__(*args, **kwargs)
        
        
    def filter_data_for_a_player(self, player_id, data, polaris_id=None):
    
        res = []    
        for d in data:
            if not polaris_id:
                if d["p1_name"].lower() == player_id.lower():
                    polaris_id = d["p1_polaris_id"]
                elif d["p2_name"].lower() == player_id.lower():
                    polaris_id = d["p2_polaris_id"]
            else:
                if d["p1_polaris_id"] == polaris_id:
                    res.append(d)
                elif d["p2_polaris_id"] == polaris_id:
                    res.append(d)
        
        return res, polaris_id


    def find_all_replays_for_id(self, player_data, player_polaris_id): # my id is 5r4gQ4RNgNQ4

        max_index = 40
        most_used = [0] * (max_index + 1)
        most_played_against = [0] * (max_index + 1)
        won = 0
        raw_data = []

        for d in player_data:
            if d["p1_polaris_id"] == player_polaris_id:
                most_used[d["p1_chara_id"]] += 1
                most_played_against[d["p2_chara_id"]] += 1
                if d["winner"] == 1:
                    won += 1
            elif d["p2_polaris_id"] == player_polaris_id:
                most_used[d["p2_chara_id"]] += 1
                most_played_against[d["p1_chara_id"]] += 1
                if d["winner"] == 2:
                    won += 1
                
            
            raw_data.append(d)


                    

        player_data = {"most_used_arr": most_used,
                    "most_played_against": most_played_against,
                    "win_rate": f"{won * 100/ (sum(most_used))}%"}

        
        return player_data, raw_data
    
    
    def head_to_head_char_win_rates(self, indv_matchups, playable_char_map, unused_idxs, reverse_char_map):

        length = len(playable_char_map) - len(unused_idxs)
        matchup_winrates = [[0.0 for _ in range(length)] for _ in range(length)]

        off = 0
        for name, v in indv_matchups.items():
            apps, wins = v[0], v[1]
            idx = reverse_char_map[name]
            off_i = 0
            if idx == 28:
                off = 3
            elif idx == 32:
                off = 5
            elif 38 == idx:
                off = 6
            for i in range(len(apps)):
                if i in unused_idxs:
                    off_i += 1
                    continue
                
                if idx == i:
                    matchup_winrates[idx - off][i - off_i] = 50
                else:
                    wr = (wins[i] / apps[i]) * 100
                    matchup_winrates[idx - off][i - off_i] = wr
        
        
        return matchup_winrates
    
    
    def find_char_popularity(self, data, playable_char_map):
    
        char_data = [0] * 41
        not_found = set()
        flag = False
        for d in data:
            flag = False
            if d["p2_chara_id"] not in playable_char_map.keys():
                not_found.add(d["p2_chara_id"])
                flag = True
            
            elif d["p1_chara_id"] not in playable_char_map.keys():
                not_found.add(d["p1_chara_id"])
                flag = True
            
            if not flag:
                char_data[d["p1_chara_id"]] += 1
                char_data[d["p2_chara_id"]] += 1
        
        return char_data, list(not_found)
    
    def get_chars_ind_matchups_winrates(self, data, playable_char_map, unused_idxs):
    
        max_idx = max(playable_char_map.keys())
        individual = {}
        
        for i, char in playable_char_map.items():
            if i in unused_idxs:
                continue
            
            individual[char] = [[0] * (max_idx + 1), [0] * (max_idx + 1)]
            
        for d in data:
            p1_char = d["p1_chara_id"]
            p2_char = d["p2_chara_id"]
            
            char_1_app, char_1_win = individual[playable_char_map[p1_char]]
            char_2_app, char_2_win = individual[playable_char_map[p2_char]]
            
            char_1_app[p2_char] += 1
            char_2_app[p1_char] += 1
            
            if d["winner"] == 1:
                char_1_win[p2_char] += 1
            elif d["winner"] == 2:
                char_2_win[p1_char] += 1
            
            individual[playable_char_map[p1_char]] = [char_1_app, char_1_win]
            individual[playable_char_map[p2_char]] = [char_2_app, char_2_win]
        
        return individual
    
    
    def get_chars_global_winrates(self, data, playable_char_map):
        max_idx = max(playable_char_map.keys())
        appearance = [0] * (max_idx + 1)
        char_wins = [0] * (max_idx + 1)
        
        for d in data:
            appearance[d["p1_chara_id"]] += 1
            appearance[d["p2_chara_id"]] += 1
            
            if d["winner"] == 1:
                char_wins[d["p1_chara_id"]] += 1
            else:
                char_wins[d["p2_chara_id"]] += 1
        
        return appearance, char_wins
    
    def get_ranked_data(self, data):
    
        rank_data = [0] * 30
        
        for d in data:
            rank_data[d['p1_rank']] += 1
            rank_data[d['p2_rank']] += 1
        
        return rank_data
    
    
    def filter_data_based_on_rank(self, data, start_rank=0, stop_rank=29):
    
        filtered_data = []
        
        for d in data:
            if (start_rank <= d["p1_rank"] and stop_rank + 1 > d["p1_rank"]) or (start_rank <= d["p2_rank"] and stop_rank + 1 > d["p2_rank"]):
                filtered_data.append(d)
        
        return filtered_data