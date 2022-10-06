from game import Game

if __name__ == '__main__':

    print(' Крестики - нолики (Игра с ИИ)')

    x_turn = (True if input("X - ходят первые? [y/n] ") == 'y' else False)
    bot_play_X = (False if input("Бот играет за 0? [y/n] ") == 'y' else True)

    print("Выберите алгоритм игры бота:")
    print(f"\t1. Самый тупой")  # 1 - тупо выбирает первую свободную ячейку
    print(f"\t2. Случайный")  # 2 - случайно выбирает одну из свободных ячеек
    print(f"\t3. Непобедимый")  # 3 - считает все поле, не может проиграть
    bot_algorithm = int(input("Номер алгоритма (1, 2 или 3): "))

    game = Game()
    game_result = game.run(x_turn,bot_play_X,bot_algorithm)

    print('Игра окончена')
    print(game_result)
