goals = []

names = ["Lost City Trek", "AOW Scuba", "White water rafting", "Paragliding", "Bungee jumping", "Waterfall absail"]
cost = [350, 256, 50, 50, 20, 20]
days = [4, 2, 1, 1, 1, 1]
importance = [1, 2, 3, 4, 5, 6]

def input_goal(goal_name, goal_cost, goal_days, goal_importance):
    goal_info = {}
    goal_info["Cost"] = goal_cost
    goal_info["Days"] = goal_days

    goals.append({goal_name: goal_info})

def goal_achieved(goals, side):
    temp_side = side
    achieved = []
    necessary = []
    for goal in goals:
        goal_info = list(goal.values())[0]
        goal_name = list(goal.keys())[0]

        if goal_info["Cost"] <= temp_side:
            temp_side -= goal_info["Cost"]
            achieved.append([goal_name, "100%"])
            necessary.append(None)
        elif achieved and achieved[-1][1] == "100%":
            percent = str(round(temp_side / goal_info["Cost"] * 100)) + "%"
            achieved.append([goal_name, percent])
            necessary.append(round(goal_info["Cost"]-temp_side,2))
            temp_side = 0
        else:
            achieved.append([goal_name, "0%"])
            necessary.append(round(necessary[-1]+goal_info["Cost"],2))
            
    return achieved, necessary

for i in range(len(names)):
    input_goal(names[i], cost[i], days[i], importance[i])

print(goal_achieved(goals, 649.8))
