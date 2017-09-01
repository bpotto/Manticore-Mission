#Manticore Mission: A Game of Adventure and Alliteration by B. P. Otto
#Copyright B.P. Otto 2017
#Version 0.01.0 (Playable, Barely Winnable)

import random, sys, json

#Classes
class Character:
    def __init__(self, name, lname, health, strength, speed, powers):
        self.name = name
        self.lname = lname
        self.max_health = self.health = health
        self.strength = strength
        self.speed = speed
        self.powers = powers
        self.temp_strength = 0
        self.temp_speed = 0
        self.powers_used = []
        self.sex = ''
        self.sex2 = ''
        self.sex3 = ''
    def stats(self):
        print('')
        print('STATS')
        print('------------------')
        print('Name: {0}'.format(self.name))
        print('Health: {0}/{1}'.format(self.health,self.max_health))
        print('Strength: {0}'.format(self.strength))
        print('Speed: {0}'.format(self.speed))
        print('Powers: {0}'.format(self.powers))
        input('')

class Counter:
    def __init__(self,count):
        self.count = 0

#Character stats
player = Character('Max','Max',0,0,0,['Cry'])
Manticore = Character('Manticore','Manticore',666,150,150,['Sting','Lunging Bite','Hellfire'])
Boar = Character('Boar','boar',80,70,20,['Tusk','Tusk'])
B_Lizard = Character('Baby Lizard','baby lizard',50,40,120,['Flee'])
Serpent = Character('Serpent','serpent',60,55,100,['Fangs'])
Fox = Character('Fox','fox',70,60,90,['Dash', 'Flee'])
#Hadhayosh drops Hush, beverage of immortality
Hadhayosh = Character('Hadhayosh','Hadhayosh',250,100,150,['Gore'])

enemy_list = [Boar, B_Lizard, Serpent, Fox]

#Counters
#These two count misses; after three misses, there is an automatic hit.
p_miss_c = Counter(0)
e_miss_c = Counter(0)
#The same rule of three applies to fleeing.
flee_c = Counter(0)
#There is a fatigue system, where strength and speed decrease after every 5 encounters.
#The fat_c counter marks if this round of fatigue has been applied.
enc_c = Counter(0)
fat_c = Counter(0)
#Hush revives the character upon death.
hush_c = Counter(0)
#loc_c is used to determine status for saving and reloading:
#0 is shack, 1 is wilderness, 2 is battle (cannot save)
loc_c = Counter(0)

#Functions for stat effects
#Can use negative numbers to reduce stats
def stat_maxh(char, amt):
    char.max_health += amt

def stat_health(char, amt):
    char.health += amt

def stat_strength(char,amt):
    char.strength += amt

def stat_speed(char,amt):
    char.speed += amt

def stat_strength_t(char,amt):
    char.strength += amt
    char.temp_strength += amt

def stat_speed_t(char,amt):
    char.speed += amt
    char.temp_speed += amt
    

#Basic commands
def basic_commands(comm):
    if comm == "quit":
        quit()
    elif comm == 'help':
        help()
    elif comm == 'stats':
        player.stats()
        
def help():
    print('')
    print('HELP')
    print('------------------')
    print('Commands: ')
    print("Help = What's happening now")
    print('Stats = Displays your stats')
    print('Quit = Quits the game')
    print('------------------')
    print('Locations: ')
    print('Shack = Restores your health, removes temporary effects')
    print('Wilderness = Find adventure to train')
    print('Castle = Home of the Manticore')
    print('------------------')
    print("Use single words, please.  I'm a bit simple.")
    print('')

def quit():
    inp = str(input('Do you want to record your deeds? ')).lower()
    if inp == ('yes' or 'y'):
        if loc_c.count == 2:
            input("You can't save in the midst of battle!")
            battle(player,enemy,flee_c)
        else:
            p_data = {'name':player.name,'lname':player.lname,'max_health':player.max_health,
                  'health':player.health,'strength':player.strength,'speed':player.speed,
                  'powers':player.powers, 'temp_strength':player.temp_strength,
                  'temp_speed':player.temp_speed, 'powers_used':player.powers_used,
                  'sex':player.sex,'sex2':player.sex2,'sex3':player.sex3, 'loc_c':loc_c.count,
                      'enc_c':enc_c.count}
            with open('p_data.txt','w')as file:
                json.dump(p_data,file)
            input('The exploits of {0} have been recorded.  May {1} return to complete {2} quest.'.format(player.name,player.sex3,player.sex))
            sys.exit()
    if inp == ('no' or 'n'):
        input("You have abandoned the kingdom in its time of need, coward.  Begone!")
        sys.exit()
    else:
        input('The question is important.  Please be clear.')
        quit()

#Power functions
def between_the_eyes(player,enemy):
    dam = int(int(player.strength)/10 + random.randint(5,20))
    enemy.health -= dam
    if random.randint(1,20) > 17:
        input('{0} punches the {1} between the eyes for {2} damage, stunning it.'.format(player.name,enemy.lname,dam))
        between_the_eyes(player,enemy)
    else:
        input('{0} punches the {1} in the face for {2} damage.'.format(player.name,enemy.lname,dam))
        player.powers_used.append('Between the Eyes')
        player.powers.remove('Between the Eyes')
        life_check(player,enemy,1,enc_c)

def bounce_back(player,enemy):
    heal = int(int(player.max_health)/10 + random.randint(10,60))
    player.health += heal
    if player.health > player.max_health:
        player.health = player.max_health
    input("{0} shakes off the {1}'s attack and regains {2} composure, regaining {3} health.".format(player.name,enemy.lname,player.sex,heal))
    player.powers_used.append('Bounce Back')
    player.powers.remove('Bounce Back')
    e_attack(enemy,player, e_miss_c)

def cry(player,enemy):
    if random.randint(1,20) >= 19:
        input('{0} cries pitifully.  {1} has mercy and leaves {0} to {2} tears.'.format(player.name,enemy.name,player.sex))
        wild_check(enc_c,fat_c)
    else:
        input('{0} cries pitifully, but the {1} has no mercy.'.format(player.name,enemy.lname))
        e_attack(enemy, player, e_miss_c)

def dash(enemy,player):
    dam = int(int(enemy.strength)/10 + random.randint(2,10))
    stat_speed_t(enemy,15)
    player.health -= dam
    input("{0} dashes about with agility and swipes at {1} for {2} damage.".format(enemy.name,player.name,dam))
    enemy.powers_used.append('Dash')
    enemy.powers.remove('Dash')
    life_check(player,enemy,0,enc_c)
    

def double(player,enemy):
    dam1 = int(int(player.strength)/10 + random.randint(1,15))
    dam2 = int(int(player.strength)/10 + random.randint(1,15))
    enemy.health -= dam1 + dam2
    input("{0} nimbly strikes the {1} for {2} damage and then again for {3} damage.".format(player.name, enemy.lname,dam1,dam2))
    player.powers_used.append('Double')
    player.powers.remove('Double')
    life_check(player,enemy,1,enc_c)

def fangs(enemy,player):
    dam = int(int(enemy.strength)/15 + random.randint(2,10))
    stat_strength_t(player,-13)
    player.health -= dam
    input("{0} darts out and sinks its fangs into {1} for {2} damage, injecting venom into {3} veins.".format(enemy.name,player.name,dam,player.sex))
    enemy.powers_used.append('Fangs')
    enemy.powers.remove('Fangs')
    life_check(player,enemy,0,enc_c)

def flee(enemy,player):
    input('{0} has fled the battle!'.format(enemy.name))
    enc_c.count += 1
    wild_check(enc_c, fat_c)

def gore(enemy,player):
    dam = int(int(enemy.strength)/4 + random.randint(5,15))
    player.health -= dam
    input("{0} lowers its horns and gores {1} for {2}, soaking the ground in blood.".format(enemy.name,player.name,dam))
    life_check(player,enemy,0,enc_c)

def hammer_fist(player,enemy):
    dam = int(int(player.strength)/7 + random.randint(5,25))
    enemy.health -= dam
    stat_speed_t(enemy,-13)
    input("{0} brings {1} fist down onto the {2}'s head, dealing {3} damage.".format(player.name,player.sex,enemy.lname,dam))
    player.powers_used.append("Hammer Fist")
    player.powers.remove("Hammer Fist")
    life_check(player,enemy,1,enc_c)

def hellfire(enemy,player):
    dam = int(int(enemy.strength)/3 + random.randint(10,30))
    player.health -= dam
    input("{0} opens its mouth and unleashes a stream of fire from the depths of Duzakh, burning {1} for {2} damage.".format(enemy.name,player.name,dam))
    enemy.powers_used.append('Hellfire')
    enemy.powers.remove('Hellfire')
    life_check(player,enemy,0,enc_c)

def lunging_bite(enemy,player):
    dam = int(int(enemy.strength)/10 + random.randint(5,25))
    player.health -= dam
    input('{0} lunged at {1} and rips into him for {2} damage!'.format(enemy.name,player.name,dam))
    life_check(player,enemy,0,enc_c)

def prise_de_fer(player,enemy):
    stat_speed_t(enemy,-15)
    dam = int(int(player.strength)/10 + random.randint(3,15))
    enemy.health -= dam
    input("{0} skillfully cripples the {1} and attacks for {2} damage.".format(player.name, enemy.lname,dam))
    player.powers_used.append('Prise de fer')
    player.powers.remove('Prise de fer')
    life_check(player,enemy,1,enc_c)

def sting(enemy,player):
    stat_strength_t(player,-7)
    dam = int(int(enemy.strength)/10 + random.randint(1,12))
    player.health -= dam
    input('{0} darts out its stinger and stabs {1} for {2} damage.'.format(enemy.name,player.name,dam))
    life_check(player,enemy,0,enc_c)

def turtle_shell(player,enemy):
    heal = int(int(player.max_health)/12 + random.randint(2,15))
    player.health += heal
    if player.health > player.max_health:
        player.health = player.max_health
    stat_strength_t(player,random.randint(3,15))
    input('{0} withdraws {1} mind and regains {1} strength, recovering {2} health and increasing {1} might.'.format(player.name,player.sex,heal))
    player.powers_used.append('Turtle Shell')
    player.powers.remove('Turtle Shell')
    e_attack(enemy, player, e_miss_c)

def tusk(enemy,player):
    dam = int(int(enemy.strength)/8 + random.randint(3,17))
    player.health -= dam
    input('{0} impales {1} with a tusk, causing {2} damage.'.format(enemy.name,player.name,dam))
    enemy.powers_used.append('Tusk')
    enemy.powers.remove('Tusk')
    life_check(player,enemy,0,enc_c)
    
    

power_list = {'lunging bite':lunging_bite, 'prise de fer':prise_de_fer, 'cry':cry, 'double':double,
              'sting':sting, 'hellfire':hellfire, 'tusk':tusk, 'fangs': fangs, 'dash':dash,
              'gore':gore, 'between the eyes':between_the_eyes, 'hammer fist':hammer_fist,
              'bounce back':bounce_back, 'turtle shell':turtle_shell, 'flee':flee}

def power_choice(player,enemy):
    print('What power do you want to use?')
    for p in player.powers:
        print(str(p))
    p_choice = str(input('')).lower()
    p_chosen = False
    if p_choice == 'none':
        battle(player,enemy,flee_c)
    elif p_choice == 'help' or p_choice == 'stats' or p_choice == 'quit':
        loc_c.count = 2
        basic_commands(p_choice)
        power_choice(player,enemy)
    else:
        for p in player.powers:
            if p_choice == str(p).lower():
                power_list[p_choice](player,enemy)
                p_chosen = True
        if p_chosen == False:
            input("I didn't catch that.  Try again.")
            power_choice(player,enemy)


#Battle functions
def life_check(player, enemy, count, enc_c):
    if player.health <= 0 and hush_c.count > 0:
        player.health = player.max_health
        hush_c.count -= 1
        used_powers = player.powers_used[:]
        for p in used_powers:
            player.powers.append(p)
            player.powers_used.remove(p)
        input("The {0}'s blow slew {1}, but the Hush revives {2} through Ahura Mazda's power.  {1} lives to fight again.".format(enemy.lname,player.name,player.sex2))
        battle(player,enemy,flee_c)
    elif player.health <= 0 and hush_c.count == 0:
        player.max_health = player.health = 0
        player.temp_strength = player.strength = 0
        player.temp_speed = player.speed = 0
        player.powers = ['Cry']
        enemy.health = enemy.max_health
        enemy.strength -= enemy.temp_strength
        enemy.temp_strength = 0
        enemy.speed -= enemy.temp_speed
        enemy.temp_speed = 0
        used_powers = enemy.powers_used[:]
        for p in used_powers:
            enemy.powers.append(p)
            enemy.powers_used.remove(p)
        print("'Twas a noble struggle, but {0} fell in battle to the {1}.".format(player.name, enemy.name))
        if str(input("Do you want to redeem your failure? ")).lower() == 'yes':
            main()
        else:
            input("Perhaps you will save the kingdom another day.")
            sys.exit()
    elif enemy.health <= 0:
        input("{0} has slain the {1}!".format(player.name, enemy.name))
        enemy.health = enemy.max_health
        enemy.strength -= enemy.temp_strength
        enemy.temp_strength = 0
        enemy.speed -= enemy.temp_speed
        enemy.temp_speed = 0
        for p in enemy.powers_used:
            enemy.powers.append(p)
            enemy.powers_used.remove(p)
        if enemy.name == "Manticore":
            input("You have slain the Manticore and saved the kingdom of Mata'a.")
            input("As the kingdom rebuilds, {0}'s name will be feted in the mead halls.".format(player.name))
            input("Long live {0}!  Long live {0}!  Long live {0}!".format(player.name))
            input("THE END")
            sys.exit()
        elif enemy.name == 'Hadhayosh':
            print('The blood streaming from the side of the Hadhayosh glistens with an unnatural gleam.')
            ans = str(input('Will you drink the blood of the Hadhayosh? ')).lower()
            if ans == 'n' or ans == 'no':
                input('You turn away from the gleaming blood: who knows what power you have disdained? ')
                enc_c.count += 1
                wild_check(enc_c, fat_c)
            else:
                input("You drink the blood, the fabled Hush, and feel Ahura Mazda's blessing within you.")
                hush_c.count += 1
                enc_c.count += 1
                wild_check(enc_c,fat_c)
        else:
            enc_c.count += 1
            wild_check(enc_c, fat_c)
    else:
        if count == 0:
            battle(player,enemy, flee_c)
        else:
            e_attack(enemy,player, e_miss_c)

def e_attack(enemy, player,e_miss_c):
    health_p = int(enemy.health) / int(enemy.max_health)
    if health_p <= 0.1 and len(enemy.powers) > 0:
        power_use = str(enemy.powers[random.randint(0,(len(enemy.powers)-1))]).lower()
        power_list[power_use](enemy,player)
    elif health_p > 0.1 and health_p < 0.75 and len(enemy.powers) > 0:
        if random.randint(1,20) > 13:
            power_use = str(enemy.powers[random.randint(0,(len(enemy.powers)-1))]).lower()
            power_list[power_use](enemy,player)
        else:
            e_no_powers(enemy,player,e_miss_c)
    elif health_p >= 0.75 and len(enemy.powers) > 0:
        if random.randint(1,20) > 17:
            power_use = str(enemy.powers[random.randint(0,(len(enemy.powers)-1))]).lower()
            power_list[power_use](enemy,player)
        else:
            e_no_powers(enemy,player,e_miss_c)
    else:
        e_no_powers(enemy,player,e_miss_c)

def e_no_powers(enemy,player,e_miss_c):
    if (int(enemy.speed)+random.randint(1,20)) < (int(player.speed)+random.randint(1,20)) and e_miss_c.count < 3:
        input('{0} attacks and misses!'.format(enemy.name))
        e_miss_c.count += 1
        if random.randint(1,20) >= 18:
            stat_speed(player,random.randint(1,4))
            input('You feel a bit nimbler.')
        battle(player,enemy,flee_c)
    else:
        dam = int(int(enemy.strength)/10 + random.randint(1,6))
        player.health -= dam
        input('{0} attacks for {1} damage!'.format(enemy.name, dam))
        e_miss_c.count = 0
        if random.randint(1,20) >= 18:
            stat_maxh(player,random.randint(3,12))
            if player.health > 0:
                input('You feel your body toughen.')
        life_check(player, enemy, 0, enc_c)

def battle(player,enemy,flee_c):
    choice = str(input('Would you like to attack, use a power, or flee? ')).lower()
    if choice == 'stats' or choice == 'help' or choice == 'quit':
        loc_c.count = 2
        basic_commands(choice)
        battle(player,enemy,flee_c)
    elif choice == 'attack':
        attack(player, enemy, p_miss_c)
    elif choice == 'flee':
        if (int(player.speed)+random.randint(1,20)) < (int(enemy.speed)+random.randint(1,15)) and flee_c.count < 3:
            input('{0} tries to flee the {1} and fails!'.format(player.name, enemy.lname))
            flee_c.count += 1
            e_attack(enemy,player,e_miss_c)
        else:
            input('{0} successfully escapes the {1}!'.format(player.name,enemy.lname))
            if random.randint(1,20) >= 19:
                stat_speed(player,random.randint(1,4))
                input('You feel a bit nimbler.')
            flee_c.count = 0
            enc_c.count += 1
            if enemy.name == 'Manticore':
                shack()
            else:
                wild_check(enc_c, fat_c)
    elif choice == 'power' or choice == 'use a power' or choice == 'use power':
        if len(player.powers) == 0:
            input('You have no powers left to use.')
            battle(player,enemy, flee_c)
        else:
            power_choice(player,enemy)
    elif choice == 'mikoshamet':
        enemy.health = 0
        life_check(player,enemy,1,enc_c)
    else:
        input("Sorry, I didn't catch that.  Try again.")
        battle(player,enemy,flee_c)
                

def attack(player, enemy,p_miss_c):
    if (int(player.speed)+random.randint(1,20)) < (int(enemy.speed)+random.randint(1,20)) and p_miss_c.count < 3:
        input('{0} attacks and misses!'.format(player.name))
        p_miss_c.count +=1
        e_attack(enemy,player,e_miss_c)
    else:
        dam = int(int(player.strength)/10 + random.randint(1,6))
        enemy.health -= dam
        input('{0} attacks for {1} damage!'.format(player.name,dam))
        p_miss_c.count = 0
        if random.randint(1,20) >= 18:
            upgrade = random.randint(1,4)
            stat_strength(player,upgrade)
            input('You feel your muscles bulging.')
        life_check(player,enemy, 1, enc_c)
        
    

#Character creation functions
def fencer(player):
    stat_maxh(player,100)
    stat_health(player,100)
    stat_strength(player,80)
    stat_speed(player,120)
    player.powers.append('Prise de fer')
    player.powers.append('Double')

def bruiser(player):
    stat_maxh(player,80)
    stat_health(player,80)
    stat_strength(player,120)
    stat_speed(player,100)
    player.powers.append('Between the Eyes')
    player.powers.append('Hammer Fist')

def blubber(player):
    stat_maxh(player,120)
    stat_health(player,120)
    stat_strength(player,100)
    stat_speed(player,80)
    player.powers.append('Bounce Back')
    player.powers.append('Turtle Shell')

def class_choice():
    print("Choose your class: ")
    print("1. Fencer")
    print("2. Bruiser")
    print("3. Blubber")
    p_class = str(input(' ')).lower()
    if p_class == 'fencer':
        fencer(player)
    elif p_class == 'bruiser':
        bruiser(player)
    elif p_class == 'blubber':
        blubber(player)
    else:
        print("Don't speak with your mouth full.  Try again.")
        class_choice()

def sex_choice():
    sex = str(input("Are you male or female? ")).lower()
    if sex == 'male':
        player.sex = 'his'
        player.sex2 = 'him'
        player.sex3 = 'he'
    elif sex == 'female':
        player.sex = 'her'
        player.sex2 = 'her'
        player.sex3 = 'she'
    else:
        print("I didn't catch that.  Try again.")
        sex_choice()
    

#Location functions
def shack():
    enc_c.count = 0
    player.health = player.max_health
    player.strength -= player.temp_strength
    player.temp_strength = 0
    player.speed -= player.temp_speed
    player.temp_speed = 0
    used_powers = player.powers_used[:]
    for p in used_powers:
        player.powers.append(p)
        player.powers_used.remove(p)
    comm = str(input("You are in the dilapidated shack, feeling pert and peppy.  What do you do? ")).lower()
    if comm == 'help':
        help()
        shack()
    elif comm == 'quit':
        loc_c.count = 0
        quit()
    elif comm == 'stats':
        player.stats()
        shack()
    elif comm == 'shack':
        print("You're already there, twiddling your thumbs.  Get a move on!")
        shack()
    elif comm == 'castle':
        input("You enter the castle, and--behold and beware!--the Manticore attacks.")
        e_attack(Manticore,player,e_miss_c)
    elif comm == 'back door':
        ans = str(input('What is the sacred word to open the back door of the castle? ')).lower()
        if ans == 'bebakhshid':
            input("The door disbars, and you sneak into the Manticore's chamber unseen.")
            flee_c.count = 3
            battle(player,Manticore,flee_c)
        else:
            input('The door remains shut, and you creep home, crestfallen.')
            shack()
    elif comm == 'wilderness':
        print("You enter the wilderness, seeking adventure...and adventure finds you.")
        wilderness(enemy_list)
    else:
        print("Talk clearly and simply; my ears aren't too good.")
        shack()
    
def wilderness(enemy_list):
    enc_num = random.randint(1,1000)
    if enc_num == 1000:
        cthulhu(cth_counter)
    elif enc_num > 990 and enc_num < 999:
        input('Hadhayosh appears, its tail whipping, its horns gleaming.')
        enemy = Hadhayosh
        battle(player,enemy, flee_c)
    else:
        enemy = enemy_list[random.randint(0,3)]
        input('A {0} appears, ready to attack.'.format(enemy.lname))
        battle(player,enemy, flee_c)

def wild_check(enc_c, fat_c):
    if enc_c.count % 5 == 0 and fat_c.count == 0:
        stat_strength_t(player,-10)
        stat_speed_t(player,-10)
        fat_c.count += 1
        input('You feel fatigued from all your adventuring.')
    wild = str(input("Would you like to explore or return to the shack? ")).lower()
    if wild == "explore":
        fat_c.count = 0
        wilderness(enemy_list)
    elif wild == 'help' or wild == 'stats' or wild == 'quit':
        loc_c.count = 1
        basic_commands(wild)
        wild_check(enc_c, fat_c)
    elif wild == 'shack':
        fat_c.count = 0
        shack()
    else:
        input("I didn't quite catch that.  Try again.")
        wild_check(enc_c,fat_c)
        
        
    
        
#an interesting encounter
cth_counter = 0

def cthulhu(count):
    print('The Eldritch God Cthulhu appears, verdant tentacles waving, obsidian eyes flashing.')
    Cthinput = input('What will you do? ').lower()
    if Cthinput == 'cthulhu fhtagn':
        print('His deepest eyes glow, and his tentacles enthrall you.')
        print('You are imbued with the might of a thrall of Cthulhu.')
        stat_maxh(player,1000)
        stat_strength(player,1000)
        stat_speed(player,1000)
        player.stats()
        count +=1
        input(' ')
        sys.exit()
    else:
        print('His deepest eyes burn, and his tentacles ensnare you.')
        print('You are slain by the might of Cthulhu.')
        input(' ')
        sys.exit()

def main():
    print("Welcome to Manticore Mission.")
    inp = str(input('Would you like to resume an adventure? ')).lower()
    if inp == ('no' or 'n'):
        player.name = str(input('Choose your name: '))
        sex_choice()
        if player.name == '' and player.sex == 'his':
            player.name = 'Rostam'
        elif player.name == '' and player.sex == 'her':
            player.name = 'Tahmina'
        class_choice()
        player.stats()
        input("The kingdom of Mata'a is menaced by a Manticore.")
        input("Make your means mighty and murder the misfit.")
        input("The Manticore dwells in a castle.  Your base of operations is a nearby shack.  The wilderness surrounds you.")
        shack()
    elif inp == ('yes' or 'y'):
        with open('p_data.txt','r') as file:
            p_data = json.load(file)
        player.name = p_data['name']
        player.lname = p_data['lname']
        player.max_health = p_data['max_health']
        player.health = p_data['health']
        player.strength = p_data['strength']
        player.speed = p_data['speed']
        player.powers = p_data['powers']
        player.temp_strength = p_data['temp_strength']
        player.temp_speed = p_data['temp_speed']
        player.powers_used = p_data['powers_used']
        player.sex = p_data['sex']
        player.sex2 = p_data['sex2']
        player.sex3 = p_data['sex3']
        loc_c.count = p_data['loc_c']
        enc_c.count = p_data['enc_c']
        input('The adventures of {0} have been recalled.'.format(player.name))
        if loc_c.count == 0:
            shack()
        elif loc_c.count == 1:
            wild_check(enc_c, fat_c)
    else:
        input('Be clearer.')
        main()

main()


