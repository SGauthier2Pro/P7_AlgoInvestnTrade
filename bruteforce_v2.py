from datetime import datetime
import csv


class Action:
    """ une action"""

    def __init__(self, name, price, percentage_gain):
        """initialisation de l'action avec son nom, son prix et son pourcentage de benefice"""
        self.name = name
        self.price = int(price)
        self.percentage_gain = int(percentage_gain)

    def getBenefit(self):
        """retourne le benefice de l'action sur 2 ans"""
        benefits = self.price * self.percentage_gain / 100
        return float(benefits)


def getTableActions(fichier_csv):
    """ renvoi le tableau des objets Action créés à partir des information du fichier passé en paramètre"""
    actions_table = []
    with open(fichier_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            action_to_add = Action(row['Action'], row['Price'], row['Benefits'][:-1])
            actions_table.append(action_to_add)
        return actions_table


def bruteForce(action_quantity, actions_table, start_budget):
    budget = start_budget
    rent = 0
    highest_rent = 0
    string_actions = ""
    list_actions_to_return = []

    # dimension de la table actions
    table_size = len(actions_table)

    # initialisation de la liste avec les indices de départ [0,1,...,p-1]
    indices = list(range(action_quantity))

    # calcule la rentabilité de la combinaison d'action
    for index in indices:
        string_actions += actions_table[index].name
        budget -= actions_table[index].price
        rent += actions_table[index].getBenefit()

    # verifie si la combinaison est dans le budget et l'enregistre si elle produit le meilleur rendement
    if budget >= 0 and rent > highest_rent:
        highest_rent = rent
        list_actions_to_return = [string_actions[:-2], rent]

    # remise a zéro des variable de comparaison
    string_actions = ""
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
            string_actions += actions_table[index].name + ", "
            budget -= actions_table[index].price
            rent += actions_table[index].getBenefit()

        # verifie si la combinaison est dans le budget et l'enregistre si elle produit le meilleur rendement
        if budget >= 0 and rent > highest_rent:
            highest_rent = rent
            list_actions_to_return = [string_actions[:-2], rent]

        # remise a zéro des variable de comparaison
        string_actions = ""
        budget = start_budget
        rent = 0

    return list_actions_to_return


time_start = datetime.now()
print(datetime.now())

best_result = ["", 0]
my_actions_table = getTableActions('./actions.csv')

for quantity_actions in range(1, len(my_actions_table) + 1):

    result_tab = bruteForce(quantity_actions, my_actions_table, 500)
    if result_tab:
        if result_tab[1] > best_result[1]:
            best_result = result_tab

print(best_result)
time_end = datetime.now()
print(datetime.now())
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
    compléxité spatial:
    O(3n) tableau actions, tableau indices, tableau resultat
    
    
    resultat :
    2022-06-28 12:52:12.550869
    ['Action-4, Action-5, Action-6, Action-8, Action-10, Action-11, Action-13, Action-18, Action-19, Action-20', 99.08000000000001]
    2022-06-28 12:52:16.897011
    temp d'execution : 0:00:04.346142

"""



