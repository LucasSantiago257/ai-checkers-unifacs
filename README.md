# ♟️ Jogo de Damas com Inteligência Artificial

> Um clássico repaginado: jogue contra um AI que pensa com o algoritmo de busca **MiniMax**, implementado do zero em Python usando **PyGame**.

---

## 📌 Sobre o projeto

Este repositório faz parte do trabalho em grupo com o tema **Inteligência Artificial aplicada ao Jogo de Damas**.  
Aqui você encontra um jogo totalmente jogável, com interface gráfica feita no **PyGame**, e um motor de decisão inteligente que analisa movimentos através do algoritmo **MiniMax**.

O que diferencia nosso jogo:

- 🎨 **Interface visual** atraente e responsiva com PyGame.
- 🧠 **IA competitiva** usando MiniMax para decidir jogadas.
- 🔄 Suporte a partidas **Jogador vs Computador**, e boa sorte vencendo esse computador 🙂.
- ⚡ Código limpo e pronto para evoluir.

---

## 🛠️ Tecnologias usadas

- [Python 3.x](https://www.python.org) – linguagem principal.
- [PyGame](https://www.pygame.org/) – criação do tabuleiro, eventos e renderização.
- **MiniMax** – algoritmo de busca para tomada de decisão da IA.

---

## 🚀 Como executar o projeto

**1. Clone este repositório**
```sh
https://github.com/LucasSantiago257/ai-checkers-unifacs.git
cd ai-checkers-unifacs
```

**2. Instale as Dependências**
```sh
pip install -r requirements.txt
```

**3. Execute o Jogo**
```sh
python main.py
```
---

🤖 Funcionamento da IA

> A Inteligência Artificial do jogo segue o algoritmo MiniMax para considerar todos os movimentos possíveis a partir da situação atual do tabuleiro e escolher aquele que maximiza suas chances de vitória e minimiza as do adversário.


Etapas na tomada de decisão:
```
Geração de todos os movimentos válidos.
Simulação e avaliação de cada movimento até uma profundidade definida.
Retorno da jogada mais vantajosa segundo a função de avaliação.
```
---

👥 Integrantes do grupo
```
Lucas Carvalho Santiago
```
