import random

class Robo:
    def __init__(self, n, obstaculos):
        self.n = n
        self.obstaculos = obstaculos
        self.visitado = set()
        # posição inicial aleatória em célula livre
        while True:
            self.inicio = (random.randrange(n), random.randrange(n))
            if self.inicio not in obstaculos:
                break
        self.posicao = self.inicio
        self.visitado.add(self.posicao)
        self.caminho = [self.posicao]

    def vizinhos(self, celula):
        (x, y) = celula
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:  # direita, baixo, esquerda, cima
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.n and 0 <= ny < self.n and (nx, ny) not in self.obstaculos:
                yield (nx, ny)

    def explorar(self):
        pilha = [self.posicao]
        while pilha:
            atual = pilha[-1]
            # pega os vizinhos ainda não visitados
            nao_visitados = [v for v in self.vizinhos(atual) if v not in self.visitado]
            if nao_visitados:
                # ao invés de aleatório, segue a ordem fixa (primeiro da lista)
                proximo = nao_visitados[0]
                self.posicao = proximo
                self.visitado.add(proximo)
                self.caminho.append(proximo)
                pilha.append(proximo)
            else:
                pilha.pop()

    def estatisticas(self):
        acessiveis = self.celulas_acessiveis()
        cobertura = len(self.visitado) / len(acessiveis) * 100 if acessiveis else 0
        passos_redundantes = len(self.caminho) - len(self.visitado)
        return {
            "celulas_acessiveis": len(acessiveis),
            "unicas_visitadas": len(self.visitado),
            "percentual_cobertura": cobertura,
            "passos_totais": len(self.caminho)-1,
            "passos_redundantes": passos_redundantes,
            "sucesso_cobertura_total": cobertura == 100
        }

    def celulas_acessiveis(self):
        # busca em largura para descobrir área acessível
        fronteira = [self.inicio]
        visto = {self.inicio}
        while fronteira:
            atual = fronteira.pop()
            for v in self.vizinhos(atual):
                if v not in visto:
                    visto.add(v)
                    fronteira.append(v)
        return visto

    def imprimir_mapa(self):
        grade = [["0" for _ in range(self.n)] for _ in range(self.n)]
        for (x, y) in self.visitado:
            grade[x][y] = "."
        for (x, y) in self.obstaculos:
            grade[x][y] = "#"
        sx, sy = self.inicio
        ex, ey = self.posicao
        grade[sx][sy] = "S"
        grade[ex][ey] = "E"
        for linha in grade:
            print(" ".join(linha))
        print()

def rodar_cenario(n, obstaculos):
    robo = Robo(n, obstaculos)
    robo.explorar()
    stats = robo.estatisticas()
    robo.imprimir_mapa()
    return stats

if __name__ == "__main__":
    n = 10

    print("=== Cenário 1: sem obstáculos ===")
    stats1 = rodar_cenario(n, obstaculos=set())
    print(stats1)

    print("=== Cenário 2: obstáculos aleatórios ===")
    num_obstaculos = random.randint(5, (n*n)//3)
    obstaculos = set()
    while len(obstaculos) < num_obstaculos:
        ox, oy = random.randrange(n), random.randrange(n)
        obstaculos.add((ox, oy))
    stats2 = rodar_cenario(n, obstaculos)
    print(stats2)
