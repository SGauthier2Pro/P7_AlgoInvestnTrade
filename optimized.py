from datetime import datetime
import csv


class Action:
    """ une action"""

    def __init__(self, name, price, percentage_gain):
        """initialisation de l'action avec son nom, son prix et son pourcentage de benefice"""
        self.name = name
        self.price = float(price)
        self.percentage_gain = float(percentage_gain)
        self.rent = self.getBenefit()

    def getBenefit(self):
        """retourne le benefice de l'action sur 2 ans"""
        benefits = self.price * self.percentage_gain / 100
        return float(benefits)


def getTableActions(fichier_csv):
    """ renvoi le tableau des objets Action créés à partir des information du fichier passé en paramètre"""
    actions_table = []
    with open(fichier_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if float(row['Price']) > 0.0 and float(row['Benefits']) > 0.0:
                action_to_add = Action(row['Action'], row['Price'], row['Benefits'])
                actions_table.append(action_to_add)
        return actions_table


def optimized(actions_table, index_to_skip, start_budget):
    actions_table = sorted(actions_table, key=lambda action: action.percentage_gain, reverse=True)
    actions_result_table = []
    indices = list(range(len(actions_table)))
    indices.remove(index_to_skip)
    rent = 0
    budget = start_budget
    for index in indices:
        if (budget - actions_table[index].price) >= 0:
            actions_result_table.append(actions_table[index])
            budget -= actions_table[index].price
            rent += actions_table[index].getBenefit()

        else:
            continue

    result = [actions_result_table, rent, start_budget - budget]

    return result


csv_file = './dataset2_Python_P7.csv'
# csv_file = './dataset1_Python_P7.csv'
# csv_file = './actions.csv'

my_actions_table = getTableActions(csv_file)

time_start = datetime.now()

best_result = ["", 0, 0]
original_budget = 500

for i in range(len(my_actions_table)):
    result_tab = optimized(my_actions_table, i, original_budget)
    if result_tab:
        if result_tab[1] > best_result[1]:
            best_result = result_tab

"""
print report 
"""
print(f"Montant total investit : {best_result[2]} €")
print(f"Rendement sur 2 Ans : {best_result[1]} €")
for action in best_result[0]:
    print(f"| {action.name} | prix : {action.price} € | Rendement : {action.rent} €")

time_end = datetime.now()
print(f"temps d'execution : {time_end - time_start}")
