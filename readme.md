## Tekken 8 replay stats -- Jan 17th to Jan 31st

Wrote some code to collect ranked replay data from "wavu wank" api: https://wank.wavu.wiki/api

**There are over 5 million replay data, with almost 250,000 players who have played at least one game of ranked**:
- Ranked replays from Jan 14th to Jan 31st
- Ranked matches only

**Data is put into 3 categories**:
- All ranks
- Fujin to Tekken Emperor
- God ranks (Tekken King to max rank)

**The images have the following for all of the categories above**:
- Character popularity
- Character win rates
- Character head - to - head win rates


**Rank distribution**: 
- showcasing where most matches are being played (note that this does not mean most people are ranked there.... it indicates where matches are being played)

![replay distribution](./pics/rank_dist.png "character popularity, all ranks")


**Character popularity**
- Most popular characters at each category, expressed as a percentage

![All Ranks](./pics/char_pop_all.png "character popularity, all ranks")

![Fujin to Emperor](./pics/char_pop_Fujin.png "char pop, Fujin to Emperor")

![God Ranks](./pics/char_pop_God.png "char pop, God Ranks")


**Character Winrates**
- Overall winrates of a character, for each category

![All Ranks](./pics/char_winrate_all.png "character winrates, all ranks")

![Fujin to Emperor](./pics/char_win_fujin.png "char winrates, Fujin to Emperor")

![God Ranks](./pics/char_win_god.png "char winrates, God Ranks")


**Character head to head heatmap**
- The character on the left is the winner
- Example: Paul on the left and Law on the bottom with grid value x -> "Paul wins x% of matches against Law"


![All Ranks](./pics/heatmap_all.png "character head to heads, all ranks")

![Fujin to Emperor](./pics/heatmap_fujin.png "character head to heads, Fujin to Emperor")

![God Ranks](./pics/heatmap_god.png "character head to heads, God Ranks")