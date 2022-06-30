from datetime import datetime
import csv


def get_action_tables(fichier_csv):
    """ renvoi le tableau des objets Action créés à partir des information du fichier passé en paramètre"""
    action_names = []
    action_prices = []
    action_benefits = []
    with open(fichier_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            action_names.append(row['Action'])
            action_prices.append(float(row['Price']))
            profits = float(row['Price']) * float(row['Benefits'][:-1]) / 100
            action_benefits.append(profits)
        return action_names, action_prices, action_benefits


def optimized(budget, action_prices, action_benefits, action_names, number_action, string_actions=""):
    string_actions = string_actions

    if number_action == 0 or budget == 0:
        return 0

    if action_prices[number_action - 1] > budget:
        string_actions += action_names[number_action-1] + ", "
        return optimized(budget, action_prices, action_benefits, action_names, number_action - 1, string_actions)
    else:
        string_actions += action_names[number_action - 1] + ", "
        return max(action_benefits[number_action - 1] + optimized(budget - action_prices[number_action - 1],
                                                                  action_prices,
                                                                  action_benefits,
                                                                  action_names,
                                                                  number_action - 1,
                                                                  string_actions),
                   optimized(budget, tab_prices, tab_benefits, action_names, number_action - 1, string_actions)
                   )


time_start = datetime.now()
print(datetime.now())

name_file = "actions.csv"

tab_names = get_action_tables(name_file)[0]
tab_prices = get_action_tables(name_file)[1]
tab_benefits = get_action_tables(name_file)[2]

print(len(tab_names))

print(optimized(500, tab_prices, tab_benefits, tab_names, len(tab_names)))

time_end = datetime.now()
print(datetime.now())
print(f"temps d'execution : {time_end - time_start}")

"""
    
    Complexité temporelle :
    
    O(19)
    test en enlevant 20 positions un a une

    resultat :
    
    2022-06-28 13:22:31.035431
    ['Action-10, Action-6, Action-13, Action-19, Action-4, Action-20, Action-5, Action-11, Action-18, Action-8', 99.08000000000001]
    2022-06-28 13:22:31.036696
    temps d'execution : 0:00:00.001265


"""
