import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

simulation_runs = 100000
scores_dumb = []
scores_smarter = []
scores_smartest = []
upper_count_1 = 0
upper_count_2 = 0
upper_count_3 = 0

def play_game(upper_count, smart):
    available_plays = {
        'Aces', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes', 'Yahtzee', 'Large Straight', 'Small Straight',
        'Full House', 'Four of a Kind', 'Three of a Kind', 'Chance' 
    }

    yahtzee_bonus = False
    total_score = 0
    upper_score = 0

    while len(available_plays) > 0:
        total_score, yahtzee_bonus, upper_score = play_turn(total_score, available_plays, yahtzee_bonus, upper_score, smart)
    if upper_score >= 63:
        total_score += 35
        #print('Scored ', upper_score, 'in the upper section for a BONUS')
        upper_count += 1
    #print('Final Score: ', total_score)
    return (total_score, upper_count)


def calculate_score(play, roll, dice_count, yahtzee_bonus):
    score = 0
    if play == 'Aces':
        for x in roll:
            if x == 1:
                score += x
    elif play == 'Twos':
        for x in roll:
            if x == 2:
                score += x
    elif play == 'Threes':
        for x in roll:
            if x == 3:
                score += x
    elif play == 'Fours':
        for x in roll:
            if x == 4:
                score += x
    elif play == 'Fives':
        for x in roll:
            if x == 5:
                score += x
    elif play == 'Sixes':
        for x in roll:
            if x == 6:
                score += x
    elif play == 'Yahtzee':
        score = 0
        if 5 in dice_count.values():
            score = 50
    elif play == 'Three of a Kind':
        score = 0
        for count in dice_count.values():
            if count >= 3:
                score = score + sum(roll)
    elif play == 'Four of a Kind':
        score = 0
        for count in dice_count.values():
            if count >= 4:
                score = score + sum(roll)
    elif play == 'Chance':
        score = sum(roll)
    elif play == 'Full House':
        score = 0
        if 3 in dice_count.values() and 2 in dice_count.values():
            score = 25
    elif play == "Small Straight":
        score = 0
        if 1 in roll and 2 in roll and 3 in roll and 4 in roll:
            score = 30
        elif 2 in roll and 3 in roll and 4 in roll and 5 in roll:
            score = 30
        elif 6 in roll and 3 in roll and 4 in roll and 5 in roll:
            score = 30
    elif play == "Large Straight":
        score = 0
        if 1 in roll and 2 in roll and 3 in roll and 4 in roll and 5 in roll:
            score = 40
        elif 2 in roll and 3 in roll and 4 in roll and 5 in roll and 6 in roll:
            score = 40
    
    return score

def initial_roll():
    dice = []
    for i in range(5):
        dice.append(random.randint(1,6))
    return dice

def subsequent_roll(roll, available_plays, smart):
    if 'Large Straight' in available_plays or 'Small Straight' in available_plays:
        if all(x in roll for x in range(1,6)) or all(x in roll for x in range(2,7)):
            return roll
        if all(x in roll for x in range(1,5)):
            roll = []
            for x in range(1,5):
                roll.append(x)
            roll.append(random.randint(1,6))
            return roll
        elif all(x in roll for x in range(2,6)):
            roll = []
            for x in range(2,6):
                roll.append(x)
            roll.append(random.randint(1,6))
            return roll
        elif all(x in roll for x in range(3,7)):
            roll = []
            for x in range(3,7):
                roll.append(x)
            roll.append(random.randint(1,6))
            return roll
    dice_count = get_dice_count(roll)
    roll = []
    if ("Full House" not in available_plays) and (smart > 0):
        max_count = max(dice_count.values())
        highest_count = []
        for die in [6,5,4,3,2,1]:
            if die in dice_count:
                if dice_count[die] == max_count:
                    roll = [die] * max_count
                    break
    else:
        for key, value in dice_count.items():
            if value > 1:
                for x in range(1,value+1):
                    roll.append(key)
       
            
    while len(roll) < 5:
        roll.append(random.randint(1,6))
    return roll

def get_dice_count(roll):
    dice_count = {}
    for die in roll:
        if die in dice_count.keys():
            dice_count[die] += 1
        else:
            dice_count[die] = 1
    return dice_count

def choose_joker(available_plays, number):
    if "Large Straight" in available_plays:
        return ("Large Straight", 40)
    elif "Small Straight" in available_plays:
        return ("Small Straight", 30)
    elif "Full House" in available_plays:
        return ("Full House", 25)
    elif "Four of a Kind" in available_plays:
        return ("Four of a Kind", number * 5)
    elif "Three of a Kind" in available_plays:
        return ("Three of a Kind", number * 5)  
    else:
        for play in ["Aces", "Twos", "Threes", "Fours", "Fives", "Sixes"]:
            if play in available_plays:
                return (play, 0)
    return (random.choice(list(available_plays)), 0)

def play_turn(total_score, available_plays, yahtzee_bonus, upper_score, smart):
    roll = initial_roll()
    #print('Initial roll: ')
    #print(roll)
    roll = subsequent_roll(roll, available_plays, smart)
    #print('Roll 2: ')
    #print(roll)
    roll = subsequent_roll(roll, available_plays, smart)
    #print('Roll 3: ')
    #print(roll)
    dice_count = get_dice_count(roll)
    max_score = 0
    score_calc = {}
    if 5 in dice_count.values() and yahtzee_bonus:
        #print("BONUS!")
        total_score += 100
        number = roll[0]
        if number == 1:
            if "Aces" in available_plays:
                best_play = "Aces"
                max_score = sum(roll)
            else:
                best_play, max_score = choose_joker(available_plays, number)
        elif number == 2:
            if "Twos" in available_plays:
                best_play = "Twos"
                max_score = sum(roll)
            else:
                best_play, max_score = choose_joker(available_plays, number)
        elif number == 3:
            if "Threes" in available_plays:
                best_play = "Threes"
                max_score = sum(roll)
            else:
                best_play, max_score = choose_joker(available_plays, number)
        elif number == 4:
            if "Fours" in available_plays:
                best_play = "Fours"
                max_score = sum(roll)
            else:
                best_play, max_score = choose_joker(available_plays, number)
        elif number == 5:
            if "Fives" in available_plays:
                best_play = "Fives"
                max_score = sum(roll)
            else:
                best_play, max_score = choose_joker(available_plays, number)
        elif number == 6:
            if "Sixes" in available_plays:
                best_play = "Sixes"
                max_score = sum(roll)
            else:
                best_play, max_score = choose_joker(available_plays, number)        
    else:
        for play in available_plays:
            score = calculate_score(play, roll, dice_count, yahtzee_bonus)
            score_calc[play] = score
            if max_score < score:
                max_score = score

        best_plays = []
        for play, score in score_calc.items():
            if score == max_score:
                best_plays.append(play)
        if smart > 1:
            for i, play in enumerate(["Sixes", "Fives", "Fours"]):
                if 6-i in dice_count.keys() and play in available_plays:
                    if dice_count[6-i] == 4:
                        best_plays = [play]
                        max_score = (6-i)*dice_count[6-i]
                        break


        if len(best_plays) == 1:
            best_play = best_plays[0]
        else:
            best_play = best_plays[random.randint(0,len(best_plays)-1)]
            if smart > 0:
                for play in ["Four of a Kind", "Three of a Kind", "Chance"]:
                    if play in best_plays:
                        best_play = play
                        break
            

    total_score += max_score
    available_plays.remove(best_play)
    if best_play in ["Aces", "Twos", "Threes", "Fours", "Fives", "Sixes"]:
        upper_score += max_score
    if best_play == "Yahtzee" and max_score > 0:
        yahtzee_bonus = True
    #print('Best Play: ', best_play)
    #print('Max Score:', max_score)

    return (total_score, yahtzee_bonus, upper_score)

for i in range(simulation_runs):
    score, upper_count_1 = play_game(upper_count_1, smart = 0)
    scores_dumb.append(score)
    score, upper_count_2 = play_game(upper_count_2, smart = 1)
    scores_smarter.append(score)
    score, upper_count_3 = play_game(upper_count_3, smart = 2)
    scores_smartest.append(score)

print("Average Score for Strategy 1:", np.mean(scores_dumb))
print("Variance for Strategy 1:", np.var(scores_dumb, ddof=1))
print("Upper Bonus Scored", upper_count_1, "Times")
print("Average Score for Strategy 2:", np.mean(scores_smarter))
print("Variance for Strategy 2:", np.var(scores_smarter, ddof=1))
print("Upper Bonus Scored", upper_count_2, "Times")
print("Average Score for Strategy 3:", np.mean(scores_smartest))
print("Variance for Strategy 3:", np.var(scores_smartest, ddof=1))
print("Upper Bonus Scored", upper_count_3, "Times")

stat, p_value = mannwhitneyu(scores_smarter, scores_dumb, alternative='greater')

if p_value < 0.05:
    print(stat, p_value)
    print("Statistically significant improvement from Strategy 1 to Strategy 2 at 95% confidence.")
else:
    print("No statistically significant improvement from Strategy 1 to Strategy 2 at 95% confidence.")

stat, p_value = mannwhitneyu(scores_smartest, scores_dumb, alternative='greater')

if p_value < 0.05:
    print(stat, p_value)
    print("Statistically significant improvement from Strategy 1 to Strategy 3 at 95% confidence.")
else:
    print("No statistically significant improvement from Strategy 1 to Strategy 3 at 95% confidence.")

stat, p_value = mannwhitneyu(scores_smartest, scores_smarter, alternative='greater')

if p_value < 0.05:
    print(stat, p_value)
    print("Statistically significant improvement from Strategy 2 to Strategy 3 at 95% confidence.")
else:
    print(stat, p_value)
    print("No statistically significant improvement from Strategy 2 to Strategy 3 at 95% confidence.")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].hist(scores_dumb, bins=40, color='skyblue')
axes[0].set_title('Strategy 1')
axes[0].set_xlabel('Score')
axes[0].set_ylabel('Frequency')

axes[1].hist(scores_smarter, bins=40, color='lightcoral')
axes[1].set_title('Strategy 2')
axes[1].set_xlabel('Score')
axes[1].set_ylabel('Frequency')

axes[2].hist(scores_smartest, bins=40, color='lightgreen')
axes[2].set_title('Strategy 3')
axes[2].set_xlabel('Score')
axes[2].set_ylabel('Frequency')
plt.tight_layout()
plt.show()


