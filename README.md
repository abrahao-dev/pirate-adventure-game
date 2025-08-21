# 🏴‍☠️ Caça ao Tesouro - Aventura Pirata

**Desenvolvido por:** Matheus Abrahão
**Teste:** Kodland Brasil - Tutores Python
**Data:** Dezembro 2024
**Versão:** 1.0.0

Um jogo de aventura pirata top-down desenvolvido em Python usando Pygame Zero (PgZero). Navegue pela ilha, colete tesouros e evite os piratas rivais!

## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido como parte do teste para tutores da **Kodland Brasil**, demonstrando habilidades em:
- Programação orientada a objetos em Python
- Desenvolvimento de jogos com Pygame Zero
- Implementação de animações de sprite
- Criação de sistemas de IA para inimigos
- Design de interfaces de usuário
- Documentação técnica em português

## 📋 Requisitos

- Python 3.6+
- Pygame Zero (pgzero)

## 🚀 Instalação

1. Clone ou baixe este repositório
2. Instale o Pygame Zero:
```bash
pip install pgzero
```

3. Execute o jogo:
```bash
pgzrun main.py
```

## 🎮 Como Jogar

### Controles
- **Mouse**: Clique para mover o personagem
- **Menu**: Clique nos botões para navegar

### Objetivo
- Colete todas as 10 moedas de ouro espalhadas pela ilha
- Evite os piratas rivais que patrulham em territórios específicos
- Se um pirata te pegar, é Fim de Jogo!

### Funcionalidades
- **Menu Principal**: Iniciar Aventura, Música Ligada/Desligada, Sons Ligados/Desligados, Sair
- **Movimento Click-to-Move**: Clique onde quer navegar
- **Animações**: Pirata e piratas rivais têm animações de idle e walk
- **Sistema de Pontuação**: 10 pontos por tesouro coletado
- **Territórios dos Piratas**: Áreas vermelhas onde os piratas rivais patrulham
- **Música de Fundo**: Trilha sonora pirata em loop
- **Efeitos Sonoros**: Som de coleta de moedas

## 🏗️ Estrutura do Código

- **Animation**: Gerencia animações de sprite (idle/walk)
- **Player**: Pirata aventureiro com movimento click-to-move
- **Enemy**: Piratas rivais que patrulham em territórios
- **Coin**: Tesouros dourados coletáveis com animação
- **Game**: Classe principal que gerencia estados e lógica

## 🎨 Características Técnicas

- **Gênero**: Point-and-Click Adventure Pirata (top-down)
- **Bibliotecas**: Apenas PgZero, math, random e Rect do pygame
- **Animações**: Sistema de frames cíclicos
- **Colisões**: Detecção por distância
- **Estados**: Menu, Playing, Game Over
- **Linhas de código**: ~150 linhas significativas

## 📁 Estrutura do Projeto

```
game-python/
├── main.py              # Arquivo principal do jogo
├── images/              # Imagens do jogo
│   └── menu_background.jpg  # Fundo do menu (800x600)
├── sounds/              # Efeitos sonoros
│   └── coin.wav         # Som de coleta de moeda
├── music/               # Músicas de fundo
│   └── soundtrack.mp3   # Trilha sonora pirata
├── README.md            # Este arquivo
└── requirements.txt     # Dependências do projeto
```

## 📝 Conformidade com Requisitos

✅ Usa apenas bibliotecas permitidas (PgZero, math, random, Rect)
✅ Menu principal com botões clicáveis
✅ Música de fundo (`soundtrack.mp3`) e sons (`coin.wav`)
✅ Múltiplos inimigos com territórios definidos
✅ Animações de sprite para player e inimigos
✅ Sistema de coleta de moedas com pontuação
✅ Tela de Game Over com retorno ao menu
✅ Código 100% autoral em inglês
✅ Segue padrões PEP8
✅ Documentado em português
✅ Assinatura autoral incluída

## 🎵 Assets e Créditos

### Sprites e Imagens
- **Kenney**: Sprites e imagens utilizados são de [Kenney](https://kenney.nl/)
- **Licença**: Creative Commons Zero (CC0) - Uso livre

### Sons e Música
- **Som de Moeda**: [Drop Coin Sound Effect](https://pixabay.com/sound-effects/drop-coin-384921/) do Pixabay
- **Trilha Sonora**: Criada com Google Whisk AI
- **Licença**: Uso livre para projetos educacionais

## 👨‍💻 Desenvolvimento

### Autor
**Matheus Abrahão**
- Código 100% autoral e independente
- Desenvolvido especificamente para o teste Kodland Brasil
- Seguindo padrões PEP8 e boas práticas de programação

### Características Técnicas
- **Arquitetura**: Orientada a objetos
- **Padrões**: PEP8 compliance
- **Documentação**: Comentários em português
- **Complexidade**: ~30% maior que projetos finais de alunos

## 🎮 Mecânicas do Jogo

- **Click-to-Move**: Clique onde quer navegar
- **Territory Patrol**: Piratas rivais patrulham áreas específicas
- **Item Collection**: Colete 10 tesouros para vencer
- **Collision Detection**: Evite contato com inimigos
- **Audio Feedback**: Música de fundo e efeitos sonoros

## 📝 Licença

Este projeto é de autoria de **Matheus Abrahão**.
Desenvolvido para o teste de tutores da **Kodland Brasil**.
- **Sprites e Imagens**: [Kenney](https://kenney.nl/) sob licença CC0
- **Som de Moeda**: [Pixabay](https://pixabay.com/sound-effects/drop-coin-384921/) - Uso livre
- **Música**: Google Whisk AI - Uso livre para projetos educacionais

---

**Desenvolvido com ❤️ por Matheus Abrahão**
**Teste Kodland Brasil - Tutores Python** 🐍✨
