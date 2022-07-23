from datetime import datetime
import csv


def get_action_tuples(fichier_csv):
    """ renvoi le tableau des objets Action créés à partir des information du fichier passé en paramètre"""
    actions = [()]
    with open(fichier_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            price = int(float(row['Price']) * 100)
            profits = int(price * float(row['Benefits']) / 100)
            if price > 0 and float(row['Benefits']) > 0.0:
                actions.append((row['Action'], price, profits))
        actions.pop(0)
        return actions


def optimized(budget_total, actions_tab):
    matrix = [[0 for x in range(budget_total + 1)] for x in range(len(actions_tab) + 1)]

    for index_action in range(1, len(actions_tab) + 1):
        for budget in range(1, budget_total + 1):
            if actions_tab[index_action - 1][1] <= budget:
                matrix[index_action][budget] = max(actions_tab[index_action - 1][2] +
                                                   matrix[index_action - 1][budget - actions_tab[index_action - 1][1]],
                                                   matrix[index_action - 1][budget])
            else:
                matrix[index_action][budget] = matrix[index_action - 1][budget]

    budget = budget_total
    action_number = len(actions_tab)
    actions_selection = []

    while budget >= 0 and action_number >= 0:
        action_to_test = actions_tab[action_number - 1]

        if matrix[action_number][budget] == matrix[action_number - 1][budget - action_to_test[1]] +\
                action_to_test[2]:
            actions_selection.append(action_to_test)
            budget -= action_to_test[1]

        action_number -= 1

    return (matrix[-1][-1] / 100), actions_selection, (budget_total / 100) - (budget / 100)


time_start = datetime.now()

# name_file = "actions.csv"
# name_file = "dataset1_Python_P7.csv"
name_file = "dataset2_Python_P7.csv"

actions_tuples = get_action_tuples(name_file)
budget_base = 500

result = optimized(int(budget_base * 100), actions_tuples)

print(f"Montant total investit : {result[2]} €")
print(f"Rendement sur 2 Ans : {result[0]} €")
for action in result[1]:
    print(f"| {action[0]} | prix : {action[1] / 100} € | Rendement : {action[2] / 100} €")

time_end = datetime.now()
print(f"temps d'execution : {time_end - time_start}")

