import heapq
import matplotlib.pyplot as plt
import numpy as np


class Plot():
    def __init__(self, *args, **kwargs):
        super(Plot, self).__init__(*args, **kwargs)
    
    def plot_user_most_played_against(self, user_data, playable_char_map, unused_idxs):
        x = [""] * (len(user_data["most_played_against"]))
        play_data = []
        
        for i, x in enumerate(user_data["most_played_against"]):
            heapq.heappush(play_data, (-x, i))

        x = []
        y = []
        
        while play_data:
            v, i = heapq.heappop(play_data)
            if i in unused_idxs:
                continue
            y.append(-v)
            x.append(playable_char_map[i])
            
        most_used_np = np.array(x)
        most_used_y = np.array(y)

        plt.figure(figsize=(20, 5))
        x_positions = np.arange(len(most_used_np))
        plt.bar(most_used_np, most_used_y, width=0.5)
        plt.xticks(x_positions, most_used_np, rotation=60)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.title("most played against")
        fig = plt.figure()
        fig.savefig("mostPlayedAgainst.png", dpi=fig.dpi)
    
    
    def plot_user_most_used_chars_data(self, user_data, playable_char_map, unsused_idxs):
        play_data = []
        
        for i, x in enumerate(user_data["most_used_arr"]):
            heapq.heappush(play_data, (-x, i))
        
        x = []
        y = []
        
        while play_data:
            v, i = heapq.heappop(play_data)
            if i in unsused_idxs:
                continue
            y.append(-v)
            x.append(playable_char_map[i])
        
        most_used_np = np.array(x)
        most_used_y = np.array(y)

        plt.figure(figsize=(20, 5))
        x_positions = np.arange(len(most_used_np))
        plt.bar(most_used_np, most_used_y, width=0.5)
        plt.xticks(x_positions, most_used_np, rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.title("character usage data")
        fig = plt.gcf()
        fig.savefig('most_used.png', dpi=fig.dpi)
    
    def plot_data(self, data, playable_char_map, unused_idxs, title, output_path, percentage=False):
        pop_data = []
        total = sum(data)
        y_label = "usage"
        if percentage:
            y_label += " percentage"

        for i in range(len(data)):
            if i in unused_idxs:
                continue
            
            heapq.heappush(pop_data, (data[i] * -1, playable_char_map[i]))

        x = []
        y = []
        
        while pop_data:
            pop, char = heapq.heappop(pop_data)
            x.append(char)
            if percentage:
                y.append(((-1 * pop) / total) * 100)
            else:
                y.append(-1 * pop)

        most_used_np = np.array(x)
        most_used_y = np.array(y)

        plt.figure(figsize=(20, 5))
        x_positions = np.arange(len(most_used_np))
        plt.bar(most_used_np, most_used_y, width=0.5)
        plt.xticks(x_positions, most_used_np, rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.ylabel(y_label)
        plt.title(title)
        fig = plt.gcf()
        output_path += ".png"
        fig.savefig(output_path, dpi=fig.dpi)
    
    
    def plot_rank_data(self, data, rank_mapping, out_path, percentage=False, title="rank distribution"):
        x = [""] * 30
        y = [0] * 30
        t = sum(data)
        
        if percentage:
            title += " expressed as percentage"
        
        for i in range(len(data)):
            x[i] = rank_mapping[i]
            if percentage:
                y[i] = (data[i] / t) * 100
            else:
                y[i] = data[i]
        
        x = np.array(x)
        y = np.array(y)
        
        plt.figure(figsize=(20, 5))
        x_positions = np.arange(len(data))
        plt.bar(x, y, width=0.5)
        plt.xticks(x_positions, x, rotation=60)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.ylim(0, 12)
        plt.title(title)
        fig = plt.gcf()
        out_path += ".png"
        fig.savefig(out_path, dpi=fig.dpi)
    
    
    def plot_char_matchup_winrates(self, data, playable_char_map, unused_idxs, title, out_path, sort=False):
    
        win_rates = [0.0] * 41
        for i in range(len(data[0])):
            if i in unused_idxs or data[0][i] == 0:
                continue
            
            win_rates[i] = data[1][i] / data[0][i]

        x = []
        y = []
        if sort:
            pop_data = []
            for i in range(len(win_rates)):
                if i in unused_idxs:
                    continue
                
                heapq.heappush(pop_data, (-win_rates[i] * 100, i))
            
            while pop_data:
                w, i = heapq.heappop(pop_data)
                x.append(playable_char_map[i])
                y.append(-w)
        else:
            for i in range(len(win_rates)):
                if i in unused_idxs:
                    continue
                
                x.append(playable_char_map[i])
                y.append(win_rates[i] * 100)
            
                
                
        
        char_names = np.array(x)
        char_win_rate_against = np.array(y)
        
        
        plt.figure(figsize=(20, 5))
        x_positions = np.arange(len(char_names))
        plt.bar(char_names, char_win_rate_against, width=0.5)
        plt.xticks(x_positions, char_names, rotation=60)
        plt.ylim(40, 55)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.title(title)
        fig = plt.gcf()
        out_path += ".png"
        fig.savefig(out_path, dpi=fig.dpi)
    
    
    def plot_char_winrates(self, char_usage, char_wins, unused_idxs, playable_char_map, title, out_path, sort=True):
        global_winrates = {}
        for i in range(len(char_usage)):
            if i in unused_idxs:
                continue
            
            char_appear_count = char_usage[i]
            char_win_count = char_wins[i]
            
            global_winrates[playable_char_map[i]] = (char_win_count / char_appear_count) * 100

        
        x = []
        y = []
        if sort:
            winrate_heap = []
            for char, w in global_winrates.items():
                heapq.heappush(winrate_heap, (-w, char))
            
            while winrate_heap:
                w, char = heapq.heappop(winrate_heap)
                x.append(char)
                y.append(-w)
        else:
            for char, w in global_winrates.items():
                x.append(char)
                y.append(w)
        
        char_names = np.array(x)
        char_win_rate = np.array(y)
        
        plt.figure(figsize=(20, 5))
        x_positions = np.arange(len(char_names))
        plt.bar(char_names, char_win_rate, width=0.5)
        plt.xticks(x_positions, char_names, rotation=60)
        plt.ylim(46, 55)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.title(title)
        fig = plt.gcf()
        out_path += ".png"
        fig.savefig(out_path, dpi=fig.dpi)
    
    
    def plot_heatmap(self, matchup_winrates, playable_char_map, unused_idxs, out_path, title):

        data_s = np.array(matchup_winrates)
        names = []
        for k, v, in playable_char_map.items():
            if k in unused_idxs:
                continue
            
            names.append(v)

        plt.figure(figsize=(20, 16))
        plt.imshow(data_s, cmap="viridis", interpolation="nearest")
        plt.colorbar()

        plt.title(title)
        plt.xlabel("opponents Character")
        plt.ylabel("winning Characters")
            
        plt.xticks(ticks=np.arange(len(names)), labels=names, rotation=90)
        plt.yticks(ticks=np.arange(len(names)), labels=names)

        for i in range(len(data_s)):
            for j in range(len(data_s)):
                plt.text(j, i, f"{data_s[i, j]:.1f}", ha='center', va='center', color='black', fontsize=12)

        plt.tight_layout()
        fig = plt.gcf()
        out_path += ".png"
        fig.savefig(out_path, dpi=fig.dpi)