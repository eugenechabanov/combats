import math
import random
import time
from dataclasses import dataclass


def integer_input(message: str, max: int) -> int:
    """Checking input to be integer and to be in range of possible answers"""

    def check_if_input_is_correct():
        try:
            if int(user_input) not in range(1, max+1):
                print(f'Input should be an integer between 1 and {max}. Please try again.')
            else:
                return True
        except ValueError:
            print('Please enter an integer.')

    input_is_correct = False

    while not input_is_correct:
        user_input = input(message)
        input_is_correct = check_if_input_is_correct()

    return int(user_input)


class bcolors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


@dataclass
class Skills:
    """Character's skills and their improvements"""
    power: int
    agility: int
    intuition: int
    strength: int
    improvements: int

    def set_skills(self, power, agility, intuition, strength):
        self.power = power
        self.agility = agility
        self.intuition = intuition
        self.strength = strength


class Character:
    """Character class"""
    def __init__(self, name, user, level=0):
        self.name = name
        self.user = user
        self.level = level
        self.skills = Skills(3, 3, 3, 3, 3)
        self.refresh_mods()

        self.punch = self.dodge = self.crit = self.hp = 0

    def improve_skill(self):
        print('Choose improvement:\n'
              '1. Power (increases damage)\n'
              '2. Agility (probability of dodging)\n'
              '3. Intuition (probability to make a critical (x2) damage)\n'
              '4. Strength (increases hit points of character)\n'
              )
        number = integer_input('Enter number: ', 4)
        skill_dict = {1: 'power',
                      2: 'agility',
                      3: 'intuition',
                      4: 'strength',
                      }

        skill = getattr(self.skills, skill_dict[number])
        setattr(self.skills, skill_dict[number], skill + 1)
        self.skills.improvements -= 1
        print(
            bcolors.OKGREEN +
            f'Skill "{str(skill_dict[number]).capitalize()}" was successfully increased.' +
            bcolors.ENDC
        )

        self.refresh_mods()

    def initial_skill_improvement(self):
        """When character is created - 3 possible skill improvements are available"""
        possible_skill_improvements = 3

        print(f"Possible skill improvements: {possible_skill_improvements}")

        while possible_skill_improvements > 0:
            self.improve_skill()
            possible_skill_improvements -= 1
            if possible_skill_improvements:
                self.print_user_profile()
                print(f'\nPossible skill improvements: {possible_skill_improvements}\n')
        self.print_user_profile(additional_info=True)

    def refresh_mods(self):
        """Re-calculate modifiers for fight-mode"""
        self.punch = 2 * self.skills.power
        self.dodge = 5 + self.skills.agility * 5
        self.crit = 4 * self.skills.intuition
        self.hp = 30 + 6 * (self.skills.strength - 3)

    def print_welcome(self):
        print(f'\nWelcome {self.name}! (character of {self.user})\n')
        time.sleep(1)

    def print_user_profile(self, additional_info=False):
        print("================================================")
        print(f"{bcolors.BOLD}{self.name} [{self.level}] [**********]  {self.hp}/{self.hp}{bcolors.ENDC}")
        print(f"({self.user}'s character)")
        print(f"Power: {self.skills.power}")
        print(f"Agility: {self.skills.agility}")
        print(f"Intuition: {self.skills.intuition}")
        print(f"Strength: {self.skills.strength} \n")

        if additional_info:
            print(f"Attack power: {self.punch}")
            print(f"Dodging modifier: {self.dodge}")
            print(f"Critical hit modifier: {self.crit}")
            print("")


class OpponentFlow:
    """At this stage of development user can choose only from a pre-defined limited set of opponents"""
    def __init__(self, char):
        self.chosen_opponent = None
        self.opponents_dict = self.get_available_opponents()

    @staticmethod
    def get_available_opponents():
        return {
                1: {'char': ['PrivateWolf', 'Corey Nicholson', 0], 'skills': (3, 4, 4, 4)},
                2: {'char': ['Pharos', 'Blake Thomson', 0], 'skills': (4, 5, 3, 3)},
                3: {'char': ['NumbLeg', 'Timothy Kinney', 2], 'skills': (6, 5, 6, 4)},
                4: {'char': ['Crucifery', 'Leonard Simmons', 3], 'skills': (9, 6, 5, 4)},
        }

    def choose_opponent(self):
        print('Looking for opponents...')
        time.sleep(3)
        print('Choose your opponent:')

        message = ''
        for index in self.opponents_dict:
            opp = self.opponents_dict[index]['char']
            opp_skills = self.opponents_dict[index]['skills']

            message += f"{index}. {opp[0]}[{opp[2]}] ({opp[1]}) [{'-'.join(str(x) for x in opp_skills)}]\n"
        print(message)
        self.chosen_opponent = integer_input('Enter number: ', 4)

        opponent = self.init_opponent()
        return opponent

    def init_opponent(self):
        opponent = Character(*self.opponents_dict[self.chosen_opponent]['char'])
        opponent.skills.set_skills(*self.opponents_dict[self.chosen_opponent]['skills'])
        opponent.refresh_mods()
        return opponent


class Fight:
    def __init__(self, char1, char2):
        self.char1 = char1
        self.char2 = char2

    def print_2_chars(self):
        print('=' * 90)
        row = f'{bcolors.BOLD}'
        row += f"{self.char1.name}[{self.char1.level}]     [{self.char1.hp_left}/{self.char1.hp}]"
        indent = 64 - len(row)
        row += " " * indent + f"{self.char2.name}[{self.char2.level}]     [{self.char2.hp_left}/{self.char2.hp}]"
        row += f'{bcolors.ENDC}'
        print(row)

        # total number of ***s is 20
        life_level = math.ceil(((self.char1.hp_left / self.char1.hp) / 5 * 100))
        row = f"[{'*' * life_level + '_' * (20 - life_level)}]"
        indent = 60 - len(row)
        row += " " * indent
        life_level = int((self.char2.hp_left / self.char2.hp) / 5 * 100)
        row += f"[{'*' * life_level + '_' * (20 - life_level)}]"
        print(row)

        for skill in ['power', 'agility', 'intuition', 'strength']:
            row = f"  {skill.capitalize()}: {getattr(self.char1.skills, skill)}"
            indent = 60 - len(row)
            row += " " * indent
            row += f"  {skill.capitalize()}: {getattr(self.char2.skills, skill)}"
            print(row)

        row = f"(character of {self.char1.user})"
        indent = 60 - len(row)
        row += " " * indent + f"(character of {self.char2.user})"
        print(row)
        print('=' * 90)

    @staticmethod
    def choose_attack():
        print('Choose attack zone:\n'
              '1. Head\n'
              '2. Chest\n'
              '3. Belly\n'
              '4. Legs\n'
              )
        return integer_input('Enter number: ', 4)

    @staticmethod
    def choose_defence():
        print('Choose defence zone:\n'
              '1. Head and chest\n'
              '2. Chest and belly\n'
              '3. Belly and legs\n'
              '4. Legs and head\n'
              )
        return integer_input('Enter number: ', 4)

    @staticmethod
    def block_outcome(attacker_move, defender_move):
        defence = {
            1: [1, 2],
            2: [2, 3],
            3: [3, 4],
            4: [4, 1],
        }
        return True if attacker_move[0] in defence[defender_move[1]] else False

    @staticmethod
    def make_damage(from_char):
        return from_char.punch + random.randint(-3, 3)

    def print_attacks_exchange(self):
        attack_dict = {
            1: 'head',
            2: 'chest',
            3: 'belly',
            4: 'legs',
        }

        mess = f'Quick {self.char1.name} decided to hit the opponent'
        if self.char2.damage_taken:
            mess += f" and made a smashing attack -{self.char2.damage_taken}HP to the enemy\'s {attack_dict[self.char1.move[0]]}. "
            mess += f"As a consequence, {self.char2.name} lost his balance and fell down. "
            mess += f"{self.char2.name} -{self.char2.damage_taken}HP [{self.char2.hp_left}/{self.char2.hp}]"
        else:
            mess += f", but prudent {self.char2.name} blocked the attack with perfect timing."
        print(mess)

        mess = f'Naughty {self.char2.name} swung at the enemy'
        if self.char1.damage_taken:
            mess += f" and и struck the {attack_dict[self.char2.move[0]]} of the enemy with his fist -{self.char1.damage_taken}HP. "
            mess += f"Hence, {self.char1.name} suddenly felt unhealthy. "
            mess += f"{self.char1.name} -{self.char1.damage_taken}HP [{self.char1.hp_left}/{self.char1.hp}]"
        else:
            mess += f", but this time the block helped {self.char1.name}."
        print(mess)

    def fight(self):
        """Fight logic. Attacks exchange and taken damage."""
        self.char1.hp_left = self.char1.hp
        self.char2.hp_left = self.char2.hp

        def attack(attacker, defender):
            if defender.blocked:
                defender.damage_taken = 0
            else:
                defender.damage_taken = self.make_damage(from_char=attacker)
                defender.hp_left -= defender.damage_taken
                if defender.hp_left < 0:
                    defender.hp_left = 0

        while not (self.char1.hp_left == 0 or self.char2.hp_left == 0):
            self.print_2_chars()
            self.char1.move = (self.choose_attack(), self.choose_defence())
            self.char2.move = (random.randint(1, 4), random.randint(1, 4))
            print('')
            # todo INTRODUCE CRITICAL HITS AND DODGES

            self.char1.blocked = self.block_outcome(self.char2.move, self.char1.move)
            self.char2.blocked = self.block_outcome(self.char1.move, self.char2.move)

            attack(self.char1, self.char2)
            attack(self.char2, self.char1)

            self.print_attacks_exchange()

        self.print_2_chars()
        winner = self.declare_winner()

        if winner:
            self.distribute_experience(winner)

    def declare_winner(self):
        """Winner declaration"""
        if self.char2.hp_left == 0 and self.char1.hp_left == 0:
            print(f'The battle is over. Draw.')
        else:
            winner = self.char1 if self.char2.hp_left == 0 else self.char2
            print(f'{bcolors.OKGREEN}The battle is over. The winner is {winner.name}.{bcolors.ENDC}')
            return winner

    @staticmethod
    def distribute_experience(winner):
        """Give XP points to a winner. Demo version"""
        print(f"Brave warrior {winner.name} has received 15XP.")


class Game:
    def __init__(self):
        self.char = None

    @staticmethod
    def log_in() -> str:
        """This will be replaced with proper login"""
        users = {
            1: 'John Doe',
            2: 'Jamie Williams',
            3: 'Toby Robinson',
            4: 'Adam Marshall',
            5: 'Luke Howard'
        }
        print('(This will be replaced by proper authorization.) Choose your account:')
        for index, name in users.items():
            print(f"{index}. {name}")

        user_number = integer_input('Input number: ', len(users))
        print("")
        return users[user_number]

    def start_game(self):
        username = self.log_in()

        self.char = Character(name=input("Your character's nickname: "), user=username)

        self.char.print_welcome()
        self.char.print_user_profile()

        self.char.initial_skill_improvement()

    def fight(self):
        """User chooses an opponent and starts a fight"""
        opponent = OpponentFlow(self.char)
        opponent = opponent.choose_opponent()

        print('Get ready to fight!')
        time.sleep(3)

        combat = Fight(self.char, opponent)
        combat.fight()
        return


def main():
    game = Game()
    game.start_game()
    game.fight()


if __name__ == '__main__':
    main()
