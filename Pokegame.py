import csv
import random

class Pokemon:
    def __init__(self,name,min_cp,max_cp,level,candy,move_name,move_dmg,num_evo,_type,current_cp):
        self.name = name
        self.min_cp = int(min_cp)
        self.max_cp = int(max_cp)
        self.level = int(level)
        self.candy = int(candy)
        self.move_name = move_name
        self.move_dmg = int(move_dmg)
        self.num_evo = int(num_evo)
        self._type = _type
        self.current_cp = random.randint(int(min_cp),int(max_cp)-1)
        self.health = 100

rows = []
poke_list = []

with open(r'C:\Users\TEMP\.vscode\PokeData.csv','r') as csvfile: #USER SHOULD INPUT PUT THEIR OWN PATH TO CSV FILE TO RUN GAME WITHIN THEIR PYTHON IDE
    csvfile.readline()  #moves cursor to first line with just numbers
    poke_data = csv.reader(csvfile, delimiter=',')
    for row in poke_data:  #traverses all the rows of data
        rows.append(row)    #appendes each row of data to rows list to make 2d array


for p in rows:
    poke_list.append(Pokemon(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[2]))

trainer_list = []
current_mon = []
trainer_candy = 0

type_counters = {
    'Fighting':['Normal','Rock','Steel','Ice','Dark'],
    'Flying':['Fighting','Bug','Grass'],
    'Poison':['Grass','Fairy'],
    'Ground':['Poison','Rock','Steel','Fire','Electric'],
    'Rock':['Flying','Bug','Fire','Ice'],
    'Bug':['Grass','Psychic','Dark'],
    'Ghost':['Ghost','Psychic'],
    'Steel':['Rock','Ice','Fairy'],
    'Fire':['Bug','Steel','Grass','Ice'],
    'Water':['Ground','Rock','Fire'],
    'Grass':['Ground','Rock','Water'],
    'Electric':['Flying','Water'],
    'Psychic':['Fighting','Poison'],
    'Ice':['FLying','Ground','Grass','Dragon'],
    'Dragon':['Dragon'],
    'Fairy':['Fighting','Dragon','Dark'],
    'Dark':['Ghost','Psychic'],
    'Normal':[]
}



def main_menu():
    '''Function prints the main menu screen into the console.
    It takes in no parameters. It prints an input to determine 
    what the user would like to do next. It evaluates a string 
    to determine what to print into the console next'''
    print('---------------------------          MAIN MENU         ---------------------------')
    print('1. View current Pokemon')
    print('2. Catch a new Pokemon ')
    print('3. Select a Pokemon')
    print('4. Close game')
    choice = input('Pick 1, 2, 3, or 4 to continue: ')

    if choice == '1':
        current_pokemon(current_mon[0])
    elif choice == '2':
        current_mon[0].health = 100
        catch_pokemon(current_mon[0])
    elif choice == '3':
        pokemon_select(trainer_list)
    elif choice == '4':
        end_game()
    


def current_pokemon(pokemon):
    '''This function prints out the information of the players curent pokemon.
    The function takes in a Pokemon object as the parameter.'''

    global trainer_candy

    print('---------------------------       Current Pokemon      --------------------------- ')
    print(pokemon.name)
    print()
    print(f'Current CP: {pokemon.current_cp}')
    print(f'Current Levels: {pokemon.level}')
    print(f'Candies: {trainer_candy}')
    print()
    print()
    print('1 - Use Candy to Level-Up ')
    print('2 - Exit to Main Menu ')
    choice = input('Pick 1 or 2 to continue: ')

    if choice == '1':
        pokemon.candy += 1
        trainer_candy -= 1
        determine_level(pokemon)
        current_pokemon(pokemon)
    elif choice == '2':
        main_menu()



def pokemon_select(trainer_poke_list):
    '''This function allows the player to select a pokemon from one of the pokemon that they have caught.
    It takes in the parameter trainer_poke_list which is a list of the pokemon that the trainer has caught.
    The list has max length 6.'''
    print('---------------------------   Pokemon Selection Menu   --------------------------- ')

    for pokemon in trainer_poke_list:
        print()
        print(f'{trainer_poke_list.index(pokemon)+1}. {pokemon.name}')
        print(f'CP {pokemon.current_cp}')

    print('---------------------------------------------------------------------------------- ')
    print()
    selected = int(input('Select a new Pokemon: '))

    current_mon.pop(0)
    current_mon.append(trainer_poke_list[selected-1])

    cont = input('New pokemon selected. Click return to return to main menu: ')
    if cont:
        main_menu()



def catch_pokemon(pokemon):
    '''This function allows the player to capture a pokemon.
    It takes in a parameter which holds their current pokemon (object).'''

    enemy_index = random.randint(0,len(poke_list))
    enemy = poke_list[enemy_index]
    

    print('--------------------------------  Pokemon Battle  -------------------------------- ')
    print(f'{pokemon.name}\t\t\t\t{enemy.name}')
    print(f'Lv.{pokemon.level}\t\t\t\t\tLv.{enemy.level}')
    print(f'Health:{pokemon.health}\t\t\t\tHealth:{enemy.health}')
    print()
    print()
    print()
    print('1.Use Pokeball')
    print('3.Run')
    print()

    choice = input('Select 1, 2, or 3 to make your choice: ')

    global trainer_candy

    if choice == '1':
        if use_pokeball(is_crit(pokemon,enemy)):
            trainer_list.append(enemy)
            print(f'{enemy.name} was caught')
            trainer_candy += give_candies()
            pokemon.health = 100
            cont = input('Click enter to return to main menu: ')
            if cont == '':
                main_menu()
                return
        else:
            print(f'{enemy.name} was not caught')
            cont = input('Click enter to continue to enemy attack: ')

            if cont == '':
                enemy_attack(enemy,pokemon,is_crit(enemy,pokemon))
            return
    elif choice == '2':
        main_menu()
        return
    


def use_pokeball(crit):
    probability = random.randint(0,100)
    if crit:
        if probability >= 0 and probability <= 70:
            return True
        else:
            return False
    else:
        if probability >= 0 and probability <= 40:
            return True
        else:
            return False

    

def your_attack(e_pokemon,pokemon,crit):
    if crit:
        result = 'and was highly effective'
        e_pokemon.health -= random.randint(60,81)
    else:
        result = 'and was not effective'
        e_pokemon.health-= random.randint(20,51)

    if e_pokemon.health <= 0:
        print('------------------------------------------------------------------------------ ')
        print(f'{e_pokemon.name} has fainted')
        e_pokemon.health += 100-e_pokemon.health
        cont = input('Click enter return to main menu: ')
        if cont == '':
            main_menu()
    elif pokemon.health <= 0:
        print('------------------------------------------------------------------------------ ')
        print(f'{pokemon.name} has fainted')
        pokemon.health += 100-pokemon.health
        cont = input('Click enter return to main menu: ')
        if cont == '':
            main_menu()


    print('--------------------------------  Pokemon Battle  -------------------------------- ')
    print(f'{pokemon.name}\t\t\t\t{e_pokemon.name}')
    print(f'Lv.{pokemon.level}\t\t\t\t\tLv.{e_pokemon.level}')
    print(f'Health:{pokemon.health}\t\t\t\tHealth:{e_pokemon.health}')
    print()
    print(f'{pokemon.move_name} was used {result}')
    print()
    print(f'1.Use {pokemon.move_name}')
    print('2.Use Pokeball')
    print('3.Run')
    print()

    cont = input('Click enter to continue to enemy attack: ')

    if cont == '':
        enemy_attack(e_pokemon,pokemon,is_crit(e_pokemon,pokemon))



def enemy_attack(e_pokemon,pokemon,crit):
    if crit:
        result = 'and was highly effective'
        pokemon.health -= random.randint(60,81)
    else:
        result = 'and was not effective'
        pokemon.health-= random.randint(20,51)

    if e_pokemon.health <= 0:
        print('------------------------------------------------------------------------------ ')
        print(f'{e_pokemon.name} has fainted')
        e_pokemon.health += 100-e_pokemon.health
        cont = input('Click enter return to main menu: ')
        if cont == '':
            main_menu()
    elif pokemon.health <= 0:
        print(f'{pokemon.name} has fainted')
        pokemon.health += 100-pokemon.health
        cont = input('Click enter return to main menu: ')
        if cont == '':
            main_menu()


    print('--------------------------------  Pokemon Battle  -------------------------------- ')
    print(f'{pokemon.name}\t\t\t\t{e_pokemon.name}')
    print(f'Lv.{pokemon.level}\t\t\t\t\tLv.{e_pokemon.level}')
    print(f'Health:{pokemon.health}\t\t\t\tHealth:{e_pokemon.health}')
    print()
    print(f'{e_pokemon.move_name} was used {result}')
    print()
    print(f'1.Use {pokemon.move_name}')
    print('2.Use Pokeball')
    print('3.Run')
    print()

    choice = input('Select 1, 2, or 3 to make your choice: ')

    global trainer_candy

    if choice == '1':
        your_attack(e_pokemon,pokemon,is_crit(pokemon,e_pokemon))    
    elif choice == '2':
        if use_pokeball(is_crit(pokemon,e_pokemon)):
            trainer_list.append(e_pokemon)
            print(f'{e_pokemon.name} was caught')
            trainer_candy += give_candies()
            pokemon.health = 100
            cont = input('Click enter to return to main menu: ')
            if cont == '':
                main_menu()
        else:
            print(f'{e_pokemon.name} was not caught')
            cont = input('Click enter to continue to enemy attack: ')

            if cont == '':
                enemy_attack(e_pokemon,pokemon,is_crit(e_pokemon,pokemon))
    elif choice == '3':
        main_menu()
    


def is_crit(pokemon1,pokemon2):
    if pokemon2._type in type_counters.get(pokemon1._type):
        crit = True
    else:
         crit = False
    
    return crit



def give_candies():
    possible_candies = [3,5,10]
    index = random.randint(0,len(possible_candies)-1)
    return possible_candies[index]



def determine_level(pokemon):
    if pokemon.candy <= 25:
        pokemon.level = pokemon.candy + 5
    elif pokemon.candy > 25 and pokemon.candy <= 45:
        pokemon.level = 25 + ((45-pokemon.candy)/2).floor()



def select_starter():
    '''This functions allows the player to select a starter pokemon. 
    It does not take a parameter in.'''
    print('--------------------------------  Starter Selection  ----------------------------- ')
    print('Select your starter:')
    starter_list = [poke_list.pop(0),poke_list.pop(2),poke_list.pop(4)]
    for pokemon in starter_list:
        print(starter_list.index(pokemon)+1)
        print(f'Name: {pokemon.name}')
        print(f'Min CP: {pokemon.min_cp}')
        print(f'Max CP: {pokemon.max_cp}')
        print(f'Level: {pokemon.level}')
        print(f'Candy: {pokemon.candy}')
        print(f'Move Name: {pokemon.move_name}')
        print(f'Move Damage: {pokemon.move_dmg}')
        print(f'Type: {pokemon._type}')
        print()

    what_starter = input('Enter 1, 2,or 3 to select your starter: ')
    print()

    global trainer_list
    if what_starter == '1':
        trainer_list.append(starter_list[0])
        current_mon.append(starter_list[0])
        main_menu()
    elif what_starter == '2':
        trainer_list.append(starter_list[1])
        current_mon.append(starter_list[1])
        main_menu()
    elif what_starter == '3':
        trainer_list.append(starter_list[2])
        current_mon.append(starter_list[2])
        main_menu()



def start_game():
    '''This function initiates the game.
    It does not take in any parameters.
    it prints out an input for the user 
    to then start the game'''
    print('Pokegame')
    start = input('Click enter to start the game: ')
    if start == '':
        select_starter()



def end_game():
    print()
    print('---------------------------          GAME OVER         ---------------------------')



start_game()
