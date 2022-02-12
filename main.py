from abc import ABC, abstractmethod
import random

from config import GAME_CHOICES, RULES


class PlayerBase(ABC):
    @abstractmethod
    def get_player_move(self, player_name):
        pass


class HumanPlayer(PlayerBase):
    def get_player_move(self, player_name):
        """
        get and validate player input, recursively
        """
        human_choice = input(
            '\n{}s turn:\n\tPlease enter your choice from (r: Rock, p: Paper, s: Scissor): '.format(player_name)
        )
        if human_choice not in GAME_CHOICES:
            print('oops!!, Wrong choice please try again...')
            return self.get_player_move(player_name)
        return human_choice


class SystemPlayer(PlayerBase):
    def get_player_move(self, player_name):
        """
        get random choice form GAME_CHOICES
        """
        return random.choice(GAME_CHOICES)


class FactoryGame:
    @staticmethod
    def start_game():
        """
        create new instance of player based on user choice using Factory design pattern, recursively
        :return: player1, player2 or None
        """
        selected_game_type = input("Please enter game type from ('s' for Single and 'm' for Multi player): ")
        if selected_game_type == 's':
            player1 = {
                    'name': 'player1',
                    'instance': HumanPlayer(),
                    'scores': 0
                }
            player2 = {
                    'name': 'system',
                    'instance': SystemPlayer(),
                    'scores': 0
                }
        elif selected_game_type == 'm':
            player1 = {
                'name': 'player1',
                'instance': HumanPlayer(),
                'scores': 0
            }

            player2 = {
                'name': 'player2',
                'instance': HumanPlayer(),
                'scores': 0
            }
        else:
            print('oops!!, Wrong choice please try again...')
            return FactoryGame.start_game()

        return player1, player2


def find_winner(player_one_choice, player_two_choice):
    """
    receive players choice, sort them and compare with game rules if
    they are not the same return winner choice else return None
    :return: winner choice or None
    """
    choices = {player_one_choice, player_two_choice}

    if len(choices) == 1:
        return None

    return RULES[tuple(sorted(choices))]


def play():
    """
    Game play handler
    """

    player1, player2 = FactoryGame.start_game()

    while player1['scores'] < 3 and player2['scores'] < 3:
        player_one_choice = player1['instance'].get_player_move(player_name=player1['name'])
        player_two_choice = player2['instance'].get_player_move(player_name=player2['name'])

        winner = find_winner(player_one_choice=player_one_choice,
                             player_two_choice=player_two_choice)

        if winner == player_one_choice:
            msg = '{} wins'.format(player1['name'])
            player1['scores'] += 1
        elif winner == player_two_choice:
            msg = '{} wins'.format(player2['name'])
            player2['scores'] += 1
        else:
            msg = 'Draw'

        print('{} choice: {}, {} choice: {}, Result: {}\n'.format(
            player1['name'],
            player_one_choice,
            player2['name'],
            player_two_choice,
            msg
        ))

    result_msg = '\t{}: {}, {}: {}'.format(
        player1['name'],
        player1['scores'],
        player2['name'],
        player2['scores'],
    )

    print('\n{}\n\n{}\n\n{}\n'.format('#' * 40, result_msg, '#' * 40,))

    play_again = input('Do you want to play again? (y/n) ')
    if play_again == 'y':
        play()


if __name__ == '__main__':
    play()
