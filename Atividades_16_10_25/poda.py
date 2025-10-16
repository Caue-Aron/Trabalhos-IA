

import ipywidgets as widgets
from IPython.display import display
import time
import copy

VAZIO = ""
JOGADOR_X = "X"
JOGADOR_O = "O"


def inicializar_tabuleiro():
    return [[VAZIO for _ in range(4)] for _ in range(4)]

def tabuleiro_cheio(tabuleiro):
    return all(cell != VAZIO for row in tabuleiro for cell in row)

def verificar_vencedor(tab):
    for i in range(4):
        if tab[i][0] != VAZIO and all(tab[i][j] == tab[i][0] for j in range(4)):
            return tab[i][0]
        if tab[0][i] != VAZIO and all(tab[j][i] == tab[0][i] for j in range(4)):
            return tab[0][i]

    if tab[0][0] != VAZIO and all(tab[i][i] == tab[0][0] for i in range(4)):
        return tab[0][0]
    if tab[0][3] != VAZIO and all(tab[i][3-i] == tab[0][3] for i in range(4)):
        return tab[0][3]

    return None


def pontuacao(tab):
    vencedor = verificar_vencedor(tab)
    if vencedor == JOGADOR_O:
        return 10
    elif vencedor == JOGADOR_X:
        return -10
    return 0

def minimax(tab, profundidade, alfa, beta, maximizando):
    vencedor = verificar_vencedor(tab)
    if vencedor or tabuleiro_cheio(tab) or profundidade == 0:
        return pontuacao(tab), None

    melhor_jogada = None

    if maximizando:
        max_avaliacao = float('-inf')
        for i in range(4):
            for j in range(4):
                if tab[i][j] == VAZIO:
                    tab[i][j] = JOGADOR_O
                    avaliacao, _ = minimax(tab, profundidade - 1, alfa, beta, False)
                    tab[i][j] = VAZIO
                    if avaliacao > max_avaliacao:
                        max_avaliacao = avaliacao
                        melhor_jogada = (i, j)
                    alfa = max(alfa, avaliacao)
                    if beta <= alfa:
                        break
        return max_avaliacao, melhor_jogada
    else:
        min_avaliacao = float('inf')
        for i in range(4):
            for j in range(4):
                if tab[i][j] == VAZIO:
                    tab[i][j] = JOGADOR_X
                    avaliacao, _ = minimax(tab, profundidade - 1, alfa, beta, True)
                    tab[i][j] = VAZIO
                    if avaliacao < min_avaliacao:
                        min_avaliacao = avaliacao
                        melhor_jogada = (i, j)
                    beta = min(beta, avaliacao)
                    if beta <= alfa:
                        break
        return min_avaliacao, melhor_jogada

def encontrar_melhor_jogada(tab):
    _, jogada = minimax(copy.deepcopy(tab), profundidade=4, alfa=float('-inf'), beta=float('inf'), maximizando=True)
    return jogada


tabuleiro = inicializar_tabuleiro()
game_over = False

status_label = widgets.HTML(value="<h2>Bem-vindo ao Jogo da Velha 4x4!</h2><p>Sua vez de jogar ('X').</p>")

button_layout = widgets.Layout(
    width='80px',
    height='80px',
    font_size='30px',
    font_weight='bold',
    border='1px solid lightgray'
)

grid_buttons = [[widgets.Button(description=VAZIO, layout=button_layout) for _ in range(4)] for _ in range(4)]

reset_button = widgets.Button(description="Reiniciar Jogo", button_style='success')

output_area = widgets.Output()

grid = widgets.GridBox(
    [btn for row in grid_buttons for btn in row],
    layout=widgets.Layout(grid_template_columns="80px 80px 80px 80px", grid_gap="0px 0px")
)

ui = widgets.VBox([status_label, grid, reset_button, output_area])


def disable_board():
    for row in grid_buttons:
        for btn in row:
            btn.disabled = True

def check_game_status():
    global game_over
    vencedor = verificar_vencedor(tabuleiro)
    if vencedor:
        status_label.value = f"<h2>Fim de Jogo!</h2><p>O jogador '{vencedor}' venceu!</p>"
        game_over = True
        disable_board()
        return True
    elif tabuleiro_cheio(tabuleiro):
        status_label.value = "<h2>Fim de Jogo!</h2><p>Empate!</p>"
        game_over = True
        disable_board()
        return True
    return False

def on_button_clicked(b):
    global tabuleiro, game_over
    if game_over:
        return

    for i in range(4):
        for j in range(4):
            if grid_buttons[i][j] == b and tabuleiro[i][j] == VAZIO:

                tabuleiro[i][j] = JOGADOR_X
                b.description = JOGADOR_X
                b.disabled = True

                if not check_game_status():
                    status_label.value = "<h3>IA ('O') está pensando...</h3>"
                    time.sleep(0.5)

                    i_ai, j_ai = encontrar_melhor_jogada(tabuleiro)
                    if i_ai is not None:
                        tabuleiro[i_ai][j_ai] = JOGADOR_O
                        grid_buttons[i_ai][j_ai].description = JOGADOR_O
                        grid_buttons[i_ai][j_ai].disabled = True
                        with output_area:
                            print(f"IA jogou na posição ({i_ai}, {j_ai})")

                    check_game_status()

                if not game_over:
                    status_label.value = "<p>Sua vez de jogar ('X').</p>"
                return

def on_reset_clicked(b):
    global tabuleiro, game_over
    tabuleiro = inicializar_tabuleiro()
    game_over = False
    status_label.value = "<h2>Novo Jogo 4x4!</h2><p>Sua vez de jogar ('X').</p>"
    output_area.clear_output()
    for i in range(4):
        for j in range(4):
            grid_buttons[i][j].description = VAZIO
            grid_buttons[i][j].disabled = False

    display(ui)

for i in range(4):
    for j in range(4):
        grid_buttons[i][j].on_click(on_button_clicked)
reset_button.on_click(on_reset_clicked)

display(ui)
