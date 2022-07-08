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
        # reader = csv.DictReader(csvfile, delimiter=';')
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if row['Price'] != '0.0' and row['Benefits'] != '0.0' and float(row['Price']) > 0.0:
                action_to_add = Action(row['Action'], row['Price'], row['Benefits'][:-1])
                actions_table.append(action_to_add)
        return actions_table


def optimized(actions_table, index_to_skip):
    actions_table = sorted(actions_table, key=lambda action: action.percentage_gain, reverse=True)
    actions_result_table = []
    indices = list(range(len(actions_table)))
    indices.remove(index_to_skip)
    rent = 0
    start_budget = 500
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


# csv_file = './dataset2_Python_P7.csv'
csv_file = './dataset1_Python_P7.csv'
# csv_file = './actions.csv'

my_actions_table = getTableActions(csv_file)

time_start = datetime.now()

best_result = ["", 0]

for i in range(0, len(my_actions_table)):
    result_tab = optimized(my_actions_table, i)
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

"""
    
    Complexité temporelle :
    
    O(n²)
    test en enlevant 20 positions un a une
    soit O(40)
    
    Complexité spatiale :
    
    O(3n)
    tableau actions, tableau indices, tableau resultat
    soit O(60)

    resultat :
    
    Montant total investit : 498.0 €
    Rendement sur 2 Ans : 99.08000000000001 €
    | Action-10 | prix : 34.0 € | Rendement : 9.18 €
    | Action-6 | prix : 80.0 € | Rendement : 20.0 €
    | Action-13 | prix : 38.0 € | Rendement : 8.74 €
    | Action-19 | prix : 24.0 € | Rendement : 5.04 €
    | Action-4 | prix : 70.0 € | Rendement : 14.0 €
    | Action-20 | prix : 114.0 € | Rendement : 20.52 €
    | Action-5 | prix : 60.0 € | Rendement : 10.2 €
    | Action-11 | prix : 42.0 € | Rendement : 7.14 €
    | Action-18 | prix : 10.0 € | Rendement : 1.4 €
    | Action-8 | prix : 26.0 € | Rendement : 2.86 €
    temps d'execution : 0:00:00.001995



"""