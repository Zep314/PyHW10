from game import Game
from player import Player

if __name__ == '__main__':
    # здесь делаем список из двух игроков и задаем им основные параметры
    players = [Player(name='Username', is_ai=False, auto_ship=True, skill=1),
               Player(name='HAL 9000', is_ai=True, auto_ship=True, skill=1)]
    # инициализация и запуск игры
    game = Game()
    game.run(players)
