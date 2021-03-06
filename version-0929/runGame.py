from agent import * #导入agent.py文件中的全部函数，可以直接用函数名调用，无需模块.函数
from game import ChineseChecker
import datetime
import tkinter as tk
from UI import GameBoard
import time
from board import Board

def timeout(func, param, timeout_duration=0, default=None):
    import signal

    class TimeoutError(Exception): #自定义异常的目的：想抛一个有意义的异常，但这个异常系统没有提供，自定义一个
        print('It\'s over time!!!')                       #BaseException：所有异常的基类

    def handler(signum, frame):
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler)#SIGALRM 当一个定时器到时的时候,内核就发送这个信号.
    signal.alarm(timeout_duration)
    #as              定义异常实例(except IOError as e)
    #finally         无论是否出现异常，都执行的代码
    try:
        result = func(param)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)

# 1 second



def runGame(ccgame, agents):
    state = ccgame.startState()
    print(state)
    max_iter = 200  # deal with some stuck situations
    iter = 0
    start = datetime.datetime.now()
    while (not ccgame.isEnd(state, iter)) and iter < max_iter:
        iter += 1
        board.board = state[1]
        board.draw()
        board.update_idletasks()
        board.update()

        player = ccgame.player(state)
        agent = agents[player]
        # function agent.getAction() modify class member action

        #timeout(agent.getAction, state)#原来是这句话，agent.getAction(state)计时一秒，自动抛出异常
        agent.getAction(state)
        legal_actions = ccgame.actions(state)
        if agent.action not in legal_actions:
            agent.action = random.choice(legal_actions)
        state = ccgame.succ(state, agent.action)
    board.board = state[1]
    board.draw()
    board.update_idletasks()
    board.update()
    time.sleep(0.1)

    end = datetime.datetime.now()
    if ccgame.isEnd(state, iter):
        return state[1].isEnd(iter)[1]  # return winner
    else:  # stuck situation
        print('stuck!')
        return 0


def simulateMultipleGames(agents_dict, simulation_times, ccgame):
    win_times_P1 = 0
    win_times_P2 = 0
    tie_times = 0
    utility_sum = 0
    for i in range(simulation_times):
        run_result = runGame(ccgame, agents_dict)
        print(run_result)
        if run_result == 1:
            win_times_P1 += 1
        elif run_result == 2:
            win_times_P2 += 1
        elif run_result == 0:
            tie_times += 1
        print('game', i + 1, 'finished', 'winner is player ', run_result)
    print('In', simulation_times, 'simulations:')
    print('winning times: for player 1 is ', win_times_P1)
    print('winning times: for player 2 is ', win_times_P2)
    print('Tie times:', tie_times)

def callback(ccgame):
    B.destroy()
    simpleGreedyAgent = SimpleGreedyAgent(ccgame)
    randomAgent = RandomAgent(ccgame)
    teamAgent = TeamNameMinimaxAgent(ccgame)
    #hisAgent = MarbleFish(ccgame)
    simulateMultipleGames({1: randomAgent, 2: teamAgent}, 2, ccgame)



if __name__ == '__main__':
    ccgame = ChineseChecker(10, 4)
    root = tk.Tk()
    board = GameBoard(root,ccgame.size,ccgame.size * 2 - 1,ccgame.board)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    B = tk.Button(board, text="Start", command = lambda: callback(ccgame=ccgame))
    B.pack()
    root.mainloop()
