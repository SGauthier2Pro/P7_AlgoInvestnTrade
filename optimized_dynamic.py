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

name_file = "actions.csv"
# name_file = "dataset1_Python_P7.csv"
# name_file = "dataset2_Python_P7.csv"

actions_tuples = get_action_tuples(name_file)
budget_base = 500

result = optimized(budget_base * 100, actions_tuples)

print(f"Montant total investit : {result[2]} €")
print(f"Rendement sur 2 Ans : {result[0]} €")
for action in result[1]:
    print(f"| {action[0]} | prix : {action[1] / 100} € | Rendement : {action[2] / 100} €")

time_end = datetime.now()
print(f"temps d'execution : {time_end - time_start}")

"""

    Complexité temporelle :

    soit n le nombre d'action et w le budget en centime d'euros
    suivant cette algorithme nous avons n * w calcul
    soit O(20 * 50000)
    O(1000000)

    resultat :

    Montat total investit : 498.0 €
    Rendement sur 2 Ans : 99.08 €
    | Action-20 | prix : 114.0 € | Rendement : 20.52 €
    | Action-19 | prix : 24.0 € | Rendement : 5.04 €
    | Action-18 | prix : 10.0 € | Rendement : 1.4 €
    | Action-13 | prix : 38.0 € | Rendement : 8.74 €
    | Action-11 | prix : 42.0 € | Rendement : 7.14 €
    | Action-10 | prix : 34.0 € | Rendement : 9.18 €
    | Action-8 | prix : 26.0 € | Rendement : 2.86 €
    | Action-6 | prix : 80.0 € | Rendement : 20.0 €
    | Action-5 | prix : 60.0 € | Rendement : 10.2 €
    | Action-4 | prix : 70.0 € | Rendement : 14.0 €
    temps d'execution : 0:00:00.387964



"""
