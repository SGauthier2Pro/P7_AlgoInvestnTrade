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
            action_to_add = Action(row['Action'], row['Price'], row['Benefits'])
            actions_table.append(action_to_add)
        return actions_table


def bruteForce(action_quantity, actions_table, start_budget):
    budget = start_budget
    rent = 0
    highest_rent = 0
    list_actions = []
    list_actions_to_return = []

    # dimension de la table actions
    table_size = len(actions_table)

    # initialisation de la liste avec les indices de départ [0,1,...,p-1]
    indices = list(range(action_quantity))

    # calcule la rentabilité de la combinaison d'action
    for index in indices:
        list_actions.append(actions_table[index])
        budget -= actions_table[index].price
        rent += actions_table[index].getBenefit()

    # verifie si la combinaison est dans le budget et l'enregistre si elle produit le meilleur rendement
    if budget >= 0 and rent > highest_rent:
        highest_rent = rent
        list_actions_to_return = [list_actions, rent, start_budget - budget]

    # remise a zéro des variable de comparaison
    list_actions = []
    budget = start_budget
    rent = 0

    if action_quantity == table_size:

        return list_actions_to_return

    # on commence à definir le dernier indice de la liste
    last_index = action_quantity - 1

    # tant qu'il reste encore des indices à incrémenter
    while last_index != -1:

        # on incrémente l'indice de le derniere position
        indices[last_index] += 1

        # on recale les indices des éléments suivants par rapport à indices[last_index]
        for next_index in range(last_index + 1, action_quantity):
            indices[next_index] = indices[next_index - 1] + 1

        # si cet indice a atteint sa valeur maxi
        if indices[last_index] == (table_size - action_quantity + last_index):
            last_index = last_index - 1  # on repère l'indice précédent le dernier repère
        else:  # sinon
            last_index = action_quantity - 1  # on repère le dernier indice

        # calcule la rentabilité de la combinaison
        for index in indices:
            list_actions.append(actions_table[index])
            budget -= actions_table[index].price
            rent += actions_table[index].getBenefit()

        # verifie si la combinaison est dans le budget et l'enregistre si elle produit le meilleur rendement
        if budget >= 0 and rent > highest_rent:
            highest_rent = rent
            list_actions_to_return = [list_actions, rent, start_budget - budget]

        # remise a zéro des variable de comparaison
        list_actions = []
        budget = start_budget
        rent = 0

    return list_actions_to_return


time_start = datetime.now()

best_result = [[], 0, 0]
my_actions_table = getTableActions('./actions.csv')

for quantity_actions in range(1, len(my_actions_table) + 1):

    result_tab = bruteForce(quantity_actions, my_actions_table, 500)
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
    compléxité temporelle :
     
    O(1048575) 
     C : nombre de combinaison possible = nombre d'arrangement / nombre de permutation possible de chaque arrangement
     C(1 20) + C(2 20) + C(3 20) + ... + C(20 20)
                            |
                            20!
                          _______
                          3!(20-3)!
    compléxité spatial maximale :
    O(3n) tableau actions, tableau indices, tableau resultat
    O(60)
    
    
    resultat :
    Montant total investit : 498.0 €
    Rendement sur 2 Ans : 99.08000000000001 €
    | Action-4 | prix : 70.0 € | Rendement : 14.0 €
    | Action-5 | prix : 60.0 € | Rendement : 10.2 €
    | Action-6 | prix : 80.0 € | Rendement : 20.0 €
    | Action-8 | prix : 26.0 € | Rendement : 2.86 €
    | Action-10 | prix : 34.0 € | Rendement : 9.18 €
    | Action-11 | prix : 42.0 € | Rendement : 7.14 €
    | Action-13 | prix : 38.0 € | Rendement : 8.74 €
    | Action-18 | prix : 10.0 € | Rendement : 1.4 €
    | Action-19 | prix : 24.0 € | Rendement : 5.04 €
    | Action-20 | prix : 114.0 € | Rendement : 20.52 €
    temps d'execution : 0:00:03.274505

"""



