import random
import time

def display_health(pokemon, opponent):
    poke_hlth = pokemon['hp'] // 10
    opp_hlth = opponent['hp'] // 10
    pokemon['hlth'] = ['█' * poke_hlth]
    opponent['hlth'] = ['█' * opp_hlth]
    print(f"\n{slot.upper()}:\t{' '.join(pokemon['hlth'])} ({pokemon['hp']} HP)")
    print('------------------------------------------------')
    print(f"PIKACHU:\t{' '.join(opponent['hlth'])} ({opponent['hp']} HP)\n")
    print("=" * 50)

def attack(attacker, defender, move, damage, burn_chance=0):
    print(f"\n{slot.upper()} used {move.upper()}!")
    time.sleep(1)
    if random.randint(1, 10) > 1:  # Accuracy check
        defender['hp'] -= damage
        print(f"It's effective! {move.upper()} dealt {damage} damage.")
        if burn_chance and random.randint(1, 10) <= burn_chance:
            print("PIKACHU is burned! It hurts itself from burning.")
            defender['hp'] -= 5
    else:
        print(f"{slot.upper()} missed!")
    print("=" * 50)

def pikachu_attack(pokemon):
    moves = {
        'thundershock': 10,
        'quick attack': 15,
        'swift': 15,
        'thunder': 30
    }
    move = random.choice(list(moves.keys()))
    print(f"\nPIKACHU used {move.upper()}!")
    time.sleep(1)
    if random.randint(1, 10) > 1:  # Accuracy check
        pokemon['hp'] -= moves[move]
        print(f"It's effective! {move.upper()} dealt {moves[move]} damage.")
    else:
        print("PIKACHU missed!")
    print("=" * 50)

def switch_pokemon():
    global slot, pokemon
    print("Your team:", ", ".join(team))
    switch = input("Which Pokémon do you want to switch to? ").lower()
    if switch in team:
        slot = switch
        pokemon = party[slot]
        print(f"\n{slot.upper()} is ready to fight!")
        print("=" * 50)
    else:
        print("Invalid choice!")

# Initialize Pokémon data
charmander = {'hlth': [], 'hp': 188, 'moves': {'scratch': 10, 'ember': 10, 'metal claw': 15, 'flamethrower': 50}}
squirtle = {'hlth': [], 'hp': 198, 'moves': {'tackle': 10, 'bubble': 10, 'water gun': 20, 'bite': 20}}
bulbasaur = {'hlth': [], 'hp': 200, 'moves': {'tackle': 10, 'vine whip': 10, 'razor leaf': 20, 'solar beam': 50}}
party = {'charmander': charmander, 'squirtle': squirtle, 'bulbasaur': bulbasaur}
team = ['charmander', 'squirtle', 'bulbasaur']
slot = 'charmander'
pokemon = party[slot]
pikachu = {'hlth': [], 'hp': 180}

# Game start
print("\n" + "=" * 50)
print("A wild PIKACHU appeared!")
time.sleep(1)
print(random.choice(["CHARMANDER, I choose you!", "Go, CHARMANDER!", "CHARMANDER, you're up!"]))
time.sleep(1)
print("\n" + "=" * 50)
print("\t\t\t\t\t\t\t\t---The battle begins---")
time.sleep(1)

while True:
    display_health(pokemon, pikachu)
    print(f"What will {slot.upper()} do?")
    choice = input("fight\t\tbag\npokemon\t\trun\n").lower()

    if choice == 'fight':
        move = input(f"Choose a move: {list(pokemon['moves'].keys())} ").lower()
        if move in pokemon['moves'] and pokemon['moves'][move] > 0:
            damage = pokemon['moves'][move]
            burn_chance = 2 if move in ['ember', 'flamethrower'] else 0
            attack(pokemon, pikachu, move, damage, burn_chance)
            pokemon['moves'][move] -= 1
        else:
            print("Invalid move or out of PP!")
    elif choice == 'bag':
        print("\nYou used a potion!")
        time.sleep(1)
        pokemon['hp'] = min(pokemon['hp'] + 30, party[slot]['hp'])
        print(f"{slot.upper()} recovered 30 HP!")
        print("=" * 50)
    elif choice == 'pokemon':
        switch_pokemon()
    elif choice == 'run':
        print("\nYou ran away!")
        print("=" * 50)
        break
    else:
        print("Invalid choice!")

    if pikachu['hp'] <= 0:
        print("\nPIKACHU fainted! You won!")
        print("=" * 50)
        break

    pikachu_attack(pokemon)

    if pokemon['hp'] <= 0:
        print(f"\n{slot.upper()} fainted!")
        team.remove(slot)
        if not team:
            print("\t\t\t\t\t\t\t\t---You Lost---")
            print("=" * 50)
            break
        switch_pokemon()
