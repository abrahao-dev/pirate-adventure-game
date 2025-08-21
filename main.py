"""
Caça ao Tesouro - Aventura Pirata
Autor: Matheus Abrahão
Um jogo de aventura pirata top-down usando Pygame Zero
"""

import math
import random

import pgzrun
from pygame import Rect

# Game constants
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 3
ENEMY_SPEED = 2
COIN_COUNT = 10
ENEMY_COUNT = 3

class Animation:
    """Classe para gerenciar animações de sprite"""
    def __init__(self, frames, frame_duration=10):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.frame_counter = 0
    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_duration:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    def get_current_frame(self):
        return self.frames[self.current_frame]

class Player:
    """Classe do jogador com movimento click-to-move"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.speed = PLAYER_SPEED
        self.is_moving = False
        self.direction = 1
        self.idle_animation = Animation(['player_idle_1', 'player_idle_2'], 15)
        self.walk_animation = Animation(['player_walk_1', 'player_walk_2'], 8)
        self.current_animation = self.idle_animation
    def move_to(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
        self.is_moving = True
    def update(self):
        if self.is_moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > self.speed:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
                self.direction = 1 if dx > 0 else -1
                self.current_animation = self.walk_animation
            else:
                self.x = self.target_x
                self.y = self.target_y
                self.is_moving = False
                self.current_animation = self.idle_animation
        else:
            self.current_animation = self.idle_animation
        self.current_animation.update()
    def draw(self):
        # Player com visual melhorado - retângulo com bordas arredondadas simuladas
        color = (0, 120, 255) if self.current_animation == self.idle_animation else (0, 180, 255)
        # Sombra
        screen.draw.filled_rect(Rect(self.x - 14, self.y - 12, 30, 30), (0, 0, 0, 100))
        # Corpo principal
        screen.draw.filled_rect(Rect(self.x - 15, self.y - 15, 30, 30), color)
        # Borda
        screen.draw.rect(Rect(self.x - 15, self.y - 15, 30, 30), (255, 255, 255))
        # Olhos simples
        screen.draw.filled_circle((self.x - 5, self.y - 5), 2, "white")
        screen.draw.filled_circle((self.x + 5, self.y - 5), 2, "white")

class Enemy:
    """Classe dos inimigos com movimento de patrulha"""
    def __init__(self, x, y, territory):
        self.x = x
        self.y = y
        self.speed = ENEMY_SPEED
        self.direction = random.uniform(0, 2 * math.pi)
        self.territory = territory
        self.change_direction_timer = 0
        self.idle_animation = Animation(['enemy_idle_1', 'enemy_idle_2'], 12)
        self.walk_animation = Animation(['enemy_walk_1', 'enemy_walk_2'], 6)
        self.current_animation = self.walk_animation
    def update(self):
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        if not self.territory.collidepoint(self.x, self.y):
            self.direction += math.pi
            self.x = max(self.territory.left, min(self.territory.right, self.x))
            self.y = max(self.territory.top, min(self.territory.bottom, self.y))
        self.change_direction_timer += 1
        if self.change_direction_timer > 120:
            self.direction = random.uniform(0, 2 * math.pi)
            self.change_direction_timer = 0
        self.current_animation.update()
    def draw(self):
        # Inimigos com visual melhorado
        color = (220, 50, 50) if self.current_animation == self.idle_animation else (180, 30, 30)
        # Sombra
        screen.draw.filled_rect(Rect(self.x - 11, self.y - 10, 25, 25), (0, 0, 0, 80))
        # Corpo principal
        screen.draw.filled_rect(Rect(self.x - 12, self.y - 12, 25, 25), color)
        # Borda mais escura
        screen.draw.rect(Rect(self.x - 12, self.y - 12, 25, 25), (100, 0, 0))
        # Olhos vermelhos brilhantes
        screen.draw.filled_circle((self.x - 4, self.y - 4), 1, (255, 100, 100))
        screen.draw.filled_circle((self.x + 4, self.y - 4), 1, (255, 100, 100))

class Coin:
    """Classe para as moedas coletáveis"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.animation = Animation(['coin_1', 'coin_2', 'coin_3'], 10)
    def update(self):
        if not self.collected:
            self.animation.update()
    def draw(self):
        if not self.collected:
            # Moedas com visual melhorado - efeito brilhante
            # Sombra
            screen.draw.filled_circle((self.x + 1, self.y + 1), 10, (0, 0, 0, 50))
            # Anel externo dourado escuro
            screen.draw.filled_circle((self.x, self.y), 10, (200, 150, 0))
            # Anel interno dourado claro
            screen.draw.filled_circle((self.x, self.y), 8, (255, 215, 0))
            # Centro brilhante
            screen.draw.filled_circle((self.x, self.y), 5, (255, 255, 150))
            # Borda branca
            screen.draw.circle((self.x, self.y), 10, "white")

class Game:
    """Classe principal do jogo"""
    def __init__(self):
        self.state = "menu"
        self.score = 0
        self.music_on = True
        self.sfx_on = True
        self.buttons = {
            "start": Rect(300, 200, 200, 50),
            "music": Rect(300, 270, 200, 50),
            "sfx": Rect(300, 340, 200, 50),
            "exit": Rect(300, 410, 200, 50)
        }
        self.player = None
        self.enemies = []
        self.coins = []
        self.init_game()

    def init_game(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        # Territórios melhor posicionados e maiores para inimigos
        territories = [
            Rect(80, 80, 180, 120),   # Superior esquerdo
            Rect(520, 80, 180, 120),  # Superior direito
            Rect(300, 420, 200, 120)  # Inferior centro
        ]
        self.enemies = []
        for i in range(ENEMY_COUNT):
            territory = territories[i]
            # Posicionar inimigos no centro de seus territórios
            x = territory.centerx
            y = territory.centery
            self.enemies.append(Enemy(x, y, territory))
        self.coins = []
        # Melhor distribuição das moedas evitando territórios dos inimigos
        safe_zones = [
            (150, 300), (350, 200), (450, 300), (650, 300),
            (200, 500), (600, 500), (400, 150), (700, 400),
            (100, 450), (750, 200)
        ]
        for i in range(min(COIN_COUNT, len(safe_zones))):
            x, y = safe_zones[i]
            self.coins.append(Coin(x, y))
        self.score = 0

        # Iniciar música de fundo
        if self.music_on:
            music.play('soundtrack')
    def update(self):
        if self.state == "playing":
            self.player.update()
            for enemy in self.enemies:
                enemy.update()
            for coin in self.coins:
                coin.update()
            # Verificar colisões
            for coin in self.coins:
                if not coin.collected:
                    distance = math.sqrt((self.player.x - coin.x)**2 + (self.player.y - coin.y)**2)
                    if distance < 25:
                        coin.collected = True
                        self.score += 10
                        # Tocar som da moeda
                        if self.sfx_on:
                            try:
                                sounds.coin.play()
                            except Exception as e:
                                print(f"Erro ao tocar som: {e}")
            for enemy in self.enemies:
                distance = math.sqrt((self.player.x - enemy.x)**2 + (self.player.y - enemy.y)**2)
                if distance < 30:
                    self.state = "game_over"
            if sum(1 for coin in self.coins if coin.collected) == COIN_COUNT:
                self.state = "game_over"
    def draw(self):
        # Fundo com gradiente simulado
        screen.fill((30, 120, 30))  # Verde mais escuro

        # Adicionar textura de grama simulada
        if self.state == "playing":
            for i in range(0, WIDTH, 40):
                for j in range(0, HEIGHT, 40):
                    # Manchas de grama mais clara
                    if (i + j) % 80 == 0:
                        screen.draw.filled_rect(Rect(i, j, 20, 20), (40, 140, 40))

        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "game_over":
            self.draw_game_over()
    def draw_menu(self):
        # Desenhar imagem de fundo do menu
        menu_bg.draw()

        # Título com sombra
        screen.draw.text("Caca ao Tesouro - Aventura Pirata", center=(WIDTH//2 + 2, 102), fontsize=40, color=(0, 0, 0, 100))
        screen.draw.text("Caca ao Tesouro - Aventura Pirata", center=(WIDTH//2, 100), fontsize=40, color=(255, 255, 100))

        # Subtítulo
        screen.draw.text("por Matheus Abrahao", center=(WIDTH//2, 140), fontsize=20, color=(200, 200, 200))

        # Botões melhorados
        button_names = ["Iniciar Aventura", "Musica: LIGADA" if self.music_on else "Musica: DESLIGADA",
                       "Sons: LIGADOS" if self.sfx_on else "Sons: DESLIGADOS", "Sair"]
        button_keys = ["start", "music", "sfx", "exit"]
        button_colors = [(100, 255, 100), (100, 150, 255), (255, 150, 100), (255, 100, 100)]

        for i, (name, key, color) in enumerate(zip(button_names, button_keys, button_colors)):
            button = self.buttons[key]
            # Sombra do botão
            shadow = Rect(button.x + 3, button.y + 3, button.width, button.height)
            screen.draw.filled_rect(shadow, (0, 0, 0, 100))
            # Botão principal
            screen.draw.filled_rect(button, color)
            screen.draw.rect(button, "white")
            screen.draw.text(name, center=button.center, fontsize=24, color="white")
    def draw_game(self):
        # Desenhar territórios dos inimigos com visual melhorado
        for enemy in self.enemies:
            # Território com gradiente simulado
            screen.draw.rect(enemy.territory, (180, 50, 50, 30))
            screen.draw.rect(enemy.territory, (100, 0, 0))
            # Aviso de perigo
            screen.draw.text("PIRATAS RIVAIS", center=(enemy.territory.centerx, enemy.territory.top - 15),
                           fontsize=20, color=(255, 50, 50))

        # Desenhar elementos em ordem de profundidade
        for coin in self.coins:
            coin.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.player.draw()

        # UI melhorada com fundo
        ui_bg = Rect(5, 5, 140, 60)
        screen.draw.filled_rect(ui_bg, (0, 0, 0, 150))
        screen.draw.rect(ui_bg, "white")

        screen.draw.text(f"Tesouros: {self.score}", (15, 15), fontsize=28, color=(255, 255, 100))
        collected_coins = sum(1 for coin in self.coins if coin.collected)
        coin_color = (100, 255, 100) if collected_coins == COIN_COUNT else "white"
        screen.draw.text(f"Moedas: {collected_coins}/{COIN_COUNT}", (15, 45), fontsize=24, color=coin_color)

        # Instruções no canto inferior
        screen.draw.text("Clique para navegar - Colete todos os tesouros - Evite os piratas rivais",
                        center=(WIDTH//2, HEIGHT - 20), fontsize=18, color=(200, 200, 200))
    def draw_game_over(self):
        # Fundo semitransparente
        overlay = Rect(0, 0, WIDTH, HEIGHT)
        screen.draw.filled_rect(overlay, (0, 0, 0, 150))

        # Game Over com sombra e efeito
        collected_coins = sum(1 for coin in self.coins if coin.collected)
        is_victory = collected_coins == COIN_COUNT

        if is_victory:
            # Vitoria
            screen.draw.text("TESOURO ENCONTRADO!", center=(WIDTH//2 + 3, HEIGHT//2 - 47), fontsize=50, color=(0, 0, 0, 100))
            screen.draw.text("TESOURO ENCONTRADO!", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=50, color=(255, 255, 100))
            screen.draw.text("Voce encontrou todos os tesouros!", center=(WIDTH//2, HEIGHT//2 - 10), fontsize=25, color=(100, 255, 100))
        else:
            # Derrota
            screen.draw.text("PIRATAS TE PEGARAM!", center=(WIDTH//2 + 3, HEIGHT//2 - 47), fontsize=50, color=(0, 0, 0, 100))
            screen.draw.text("PIRATAS TE PEGARAM!", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=50, color=(255, 100, 100))
            screen.draw.text("Os piratas rivais te capturaram!", center=(WIDTH//2, HEIGHT//2 - 10), fontsize=22, color=(255, 150, 150))

        # Score com destaque
        screen.draw.text(f"Tesouros Encontrados: {self.score}", center=(WIDTH//2, HEIGHT//2 + 30), fontsize=30, color=(255, 255, 255))
        screen.draw.text(f"Moedas Coletadas: {collected_coins}/{COIN_COUNT}", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=24, color=(255, 215, 0))

        # Botão para voltar
        button_rect = Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 40)
        screen.draw.filled_rect(button_rect, (100, 150, 255))
        screen.draw.rect(button_rect, "white")
        screen.draw.text("Clique para voltar ao porto", center=button_rect.center, fontsize=20, color="white")
    def handle_click(self, pos):
        if self.state == "menu":
            if self.buttons["start"].collidepoint(pos):
                self.state = "playing"
                self.init_game()
            elif self.buttons["music"].collidepoint(pos):
                self.music_on = not self.music_on
                if self.music_on:
                    music.play('soundtrack')
                else:
                    music.stop()
            elif self.buttons["sfx"].collidepoint(pos):
                self.sfx_on = not self.sfx_on
            elif self.buttons["exit"].collidepoint(pos):
                exit()
        elif self.state == "playing":
            self.player.move_to(pos[0], pos[1])
        elif self.state == "game_over":
            self.state = "menu"

# Carregar imagem de fundo do menu
menu_bg = Actor('menu_background')

# Instância global do jogo
game = Game()

def update():
    game.update()

def draw():
    game.draw()

def on_mouse_down(pos, button):
    if button == 1:
        game.handle_click(pos)

pgzrun.go()
