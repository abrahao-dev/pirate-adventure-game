"""
Caca ao Tesouro - Aventura Pirata
Autor: Matheus Abrahao
Um jogo de aventura pirata top-down usando Pygame Zero
"""

import math
import random

import pgzrun
from pygame import Rect

# Game constants
TITLE = "Caca ao Tesouro - Aventura Pirata"
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 3
ENEMY_SPEED = 2
COIN_COUNT = 10
ENEMY_COUNT = 3
POWERUP_COUNT = 3
PROJECTILE_COUNT = 5

def load_seq(prefix: str, start: int, end: int):
    """Helper para gerar sequência de frames de animação"""
    return [f"{prefix}{i}" for i in range(start, end + 1)]

class Animation:
    """Classe para gerenciar animacoes de sprite"""
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
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        self.powerup_active = False
        self.powerup_timer = 0
        # Usar os 26 frames de animação idle disponíveis
        self.idle_animation = Animation([f'player/idle/{i}' for i in range(1, 27)], 15)
        # Usar os 14 frames de animação de corrida disponíveis
        self.run_animation = Animation([f'player/run/{i}' for i in range(1, 15)], 12)
        self.current_animation = self.idle_animation
    def move_to(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
        self.is_moving = True
    def update(self):
        # Atualizar invencibilidade
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        # Atualizar powerup
        if self.powerup_active:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.powerup_active = False
                self.speed = PLAYER_SPEED

        if self.is_moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > self.speed:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
                self.direction = 1 if dx > 0 else -1
                self.current_animation = self.run_animation
            else:
                self.x = self.target_x
                self.y = self.target_y
                self.is_moving = False
                self.current_animation = self.idle_animation
        else:
            self.current_animation = self.idle_animation
        self.current_animation.update()

    def activate_powerup(self):
        """Ativa powerup de velocidade"""
        self.powerup_active = True
        self.powerup_timer = 300  # 5 segundos
        self.speed = PLAYER_SPEED * 2

    def take_damage(self):
        """Jogador toma dano"""
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_timer = 120  # 2 segundos de invencibilidade
            return True
        return False

    def draw(self):
        # Piscar quando invencível
        if self.invincible and self.invincible_timer % 10 < 5:
            return

        # Obter o frame atual da animação
        current_frame = self.current_animation.get_current_frame()

        try:
            # Criar um Actor com a imagem atual e posicionar
            player_actor = Actor(current_frame)
            player_actor.x = self.x
            player_actor.y = self.y

            # Desenhar o sprite do jogador
            player_actor.draw()
        except Exception as e:
            # Fallback caso as imagens não sejam encontradas
            print(f"Erro ao carregar sprite: {e}")
            color = (0, 120, 255) if self.current_animation == self.idle_animation else (0, 180, 255)
            if self.powerup_active:
                color = (255, 255, 0)  # Dourado quando com powerup

            # Desenhar retângulo como fallback
            screen.draw.filled_rect(Rect(self.x - 15, self.y - 15, 30, 30), color)
            screen.draw.rect(Rect(self.x - 15, self.y - 15, 30, 30), (255, 255, 255))

class Enemy:
    """Classe dos inimigos com movimento de patrulha"""
    def __init__(self, x, y, territory):
        self.x = x
        self.y = y
        self.speed = ENEMY_SPEED
        self.direction = random.uniform(0, 2 * math.pi)
        self.territory = territory
        self.change_direction_timer = 0
        # Usar os 12 frames de animação de corrida disponíveis
        self.run_animation = Animation(load_seq('enemy/run/', 1, 12), 10)
        self.current_animation = self.run_animation
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

        # Inimigo está sempre "em movimento" → animação de corrida
        self.current_animation = self.run_animation
        self.current_animation.update()
    def draw(self):
        # Obter o frame atual da animação
        current_frame = self.current_animation.get_current_frame()

        try:
            # Criar um Actor com a imagem atual e posicionar
            enemy_actor = Actor(current_frame)
            enemy_actor.x = self.x
            enemy_actor.y = self.y

            # Desenhar o sprite do inimigo
            enemy_actor.draw()
        except Exception as e:
            # Fallback caso as imagens não sejam encontradas
            print(f"Erro ao carregar sprite do inimigo: {e}")
            # Desenhar retângulo como fallback
            screen.draw.filled_rect(Rect(self.x - 12, self.y - 12, 25, 25), (180, 30, 30))
            screen.draw.rect(Rect(self.x - 12, self.y - 12, 25, 25), (100, 0, 0))

class Coin:
    """Classe para as moedas coletaveis"""
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
            # Moedas com visual melhorado - efeito brilhante estatico
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

class PowerUp:
    """Classe para powerups de velocidade"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.animation = Animation(['powerup_1', 'powerup_2', 'powerup_3'], 8)
    def update(self):
        if not self.collected:
            self.animation.update()
    def draw(self):
        if not self.collected:
            # Powerup com efeito visual especial estatico
            # Sombra
            screen.draw.filled_circle((self.x + 2, self.y + 2), 12, (0, 0, 0, 60))
            # Anel externo azul
            screen.draw.filled_circle((self.x, self.y), 12, (100, 150, 255))
            # Anel interno azul claro
            screen.draw.filled_circle((self.x, self.y), 10, (150, 200, 255))
            # Centro brilhante
            screen.draw.filled_circle((self.x, self.y), 6, (255, 255, 255))
            # Borda branca
            screen.draw.circle((self.x, self.y), 12, "white")
            # Efeito de brilho
            screen.draw.circle((self.x, self.y), 8, (255, 255, 100))

class Projectile:
    """Classe para projeteis/obstaculos que se movem pelo mapa"""
    def __init__(self):
        self.reset()

    def reset(self):
        """Reseta o projetil em uma nova posicao e direcao"""
        # Escolher borda aleatoria para spawn
        side = random.randint(0, 3)
        if side == 0:  # Topo
            self.x = random.randint(0, WIDTH)
            self.y = -20
        elif side == 1:  # Direita
            self.x = WIDTH + 20
            self.y = random.randint(0, HEIGHT)
        elif side == 2:  # Baixo
            self.x = random.randint(0, WIDTH)
            self.y = HEIGHT + 20
        else:  # Esquerda
            self.x = -20
            self.y = random.randint(0, HEIGHT)

        # Direcao aleatoria
        self.direction = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(2, 4)
        self.active = True
        self.animation = Animation(['projectile_1', 'projectile_2'], 8)

    def update(self):
        if self.active:
            # Mover projetil
            self.x += math.cos(self.direction) * self.speed
            self.y += math.sin(self.direction) * self.speed

            # Verificar se saiu da tela
            if (self.x < -30 or self.x > WIDTH + 30 or
                self.y < -30 or self.y > HEIGHT + 30):
                self.reset()

            self.animation.update()

    def draw(self):
        if self.active:
            # Projetil com efeito visual
            # Sombra
            screen.draw.filled_circle((self.x + 1, self.y + 1), 8, (0, 0, 0, 80))
            # Corpo principal (laranja/vermelho)
            screen.draw.filled_circle((self.x, self.y), 8, (255, 100, 50))
            # Centro brilhante
            screen.draw.filled_circle((self.x, self.y), 4, (255, 200, 100))
            # Borda
            screen.draw.circle((self.x, self.y), 8, (255, 50, 0))
            # Efeito de rastro
            trail_x = self.x - math.cos(self.direction) * 15
            trail_y = self.y - math.sin(self.direction) * 15
            screen.draw.filled_circle((trail_x, trail_y), 4, (255, 100, 50, 100))

class Game:
    """Classe principal do jogo"""
    def __init__(self):
        self.state = "menu"
        self.score = 0
        self.music_on = True
        self.sfx_on = True
        self.countdown_active = False
        self.countdown_timer = 0
        self.countdown_number = 3
        self.fade_alpha = 0
        self.buttons = {
            "start": Rect(250, 220, 300, 70),
            "music": Rect(250, 310, 300, 60),
            "sfx": Rect(250, 390, 300, 60),
            "exit": Rect(250, 470, 300, 60)
        }
        self.button_hover = None
        self.player = None
        self.enemies = []
        self.coins = []
        self.powerups = []
        self.projectiles = []
        self.particles = []
        self.init_game()

    def init_game(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        # Territorios melhor posicionados e maiores para inimigos
        territories = [
            Rect(80, 80, 180, 120),   # Superior esquerdo
            Rect(520, 80, 180, 120),  # Superior direito
            Rect(300, 420, 200, 120)  # Inferior centro
        ]
        self.enemies = []
        for i in range(ENEMY_COUNT):
            territory = territories[i]
            # Posicionar inimigos no centro de seus territorios
            x = territory.centerx
            y = territory.centery
            self.enemies.append(Enemy(x, y, territory))
        self.coins = []
        # Melhor distribuicao das moedas evitando territorios dos inimigos
        safe_zones = [
            (150, 300), (350, 200), (450, 300), (650, 300),
            (200, 500), (600, 500), (400, 150), (700, 400),
            (100, 450), (750, 200)
        ]
        for i in range(min(COIN_COUNT, len(safe_zones))):
            x, y = safe_zones[i]
            self.coins.append(Coin(x, y))

        # Adicionar powerups
        self.powerups = []
        powerup_positions = [(250, 250), (550, 350), (450, 450)]
        for i in range(min(POWERUP_COUNT, len(powerup_positions))):
            x, y = powerup_positions[i]
            self.powerups.append(PowerUp(x, y))

        # Adicionar projeteis
        self.projectiles = []
        for i in range(PROJECTILE_COUNT):
            self.projectiles.append(Projectile())

        self.particles = []
        self.score = 0

        # Iniciar musica de fundo
        if self.music_on:
            music.play('soundtrack')

    def add_particles(self, x, y, color, count=5):
        """Adiciona efeitos de particulas"""
        for _ in range(count):
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-3, 3),
                'life': 30,
                'color': color
            })

    def start_countdown(self):
        """Inicia a contagem regressiva para o jogo"""
        self.countdown_active = True
        self.countdown_timer = 0
        self.countdown_number = 3
        self.fade_alpha = 0

    def update(self):
        if self.countdown_active:
            self.countdown_timer += 1
            if self.countdown_timer < 10:  # Fade in instantaneo
                self.fade_alpha = 255
            elif self.countdown_timer >= 30 and self.countdown_timer < 60:  # Mostrar numero
                pass
            elif self.countdown_timer >= 60:  # Proximo numero mais rapido
                self.countdown_number -= 1
                self.countdown_timer = 30
                if self.countdown_number < 0:  # GO!
                    self.countdown_active = False
                    self.state = "playing"
                    self.init_game()
            return

        if self.state == "playing":
            self.player.update()
            for enemy in self.enemies:
                enemy.update()
            for coin in self.coins:
                coin.update()
            for powerup in self.powerups:
                powerup.update()
            for projectile in self.projectiles:
                projectile.update()

            # Atualizar particulas
            for particle in self.particles[:]:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['life'] -= 1
                if particle['life'] <= 0:
                    self.particles.remove(particle)

            # Verificar colisoes
            for coin in self.coins:
                if not coin.collected:
                    distance = math.sqrt((self.player.x - coin.x)**2 + (self.player.y - coin.y)**2)
                    if distance < 25:
                        coin.collected = True
                        self.score += 10
                        self.add_particles(coin.x, coin.y, (255, 215, 0), 8)
                        # Tocar som da moeda
                        if self.sfx_on:
                            try:
                                sounds.coin.play()
                            except Exception as e:
                                print(f"Erro ao tocar som: {e}")

            # Verificar colisao com powerups
            for powerup in self.powerups:
                if not powerup.collected:
                    distance = math.sqrt((self.player.x - powerup.x)**2 + (self.player.y - powerup.y)**2)
                    if distance < 30:
                        powerup.collected = True
                        self.player.activate_powerup()
                        self.add_particles(powerup.x, powerup.y, (100, 150, 255), 12)
                        self.score += 20

            # Verificar colisao com inimigos
            for enemy in self.enemies:
                distance = math.sqrt((self.player.x - enemy.x)**2 + (self.player.y - enemy.y)**2)
                if distance < 30:
                    if self.player.take_damage():
                        self.add_particles(self.player.x, self.player.y, (255, 100, 100), 10)
                        if self.player.lives <= 0:
                            self.state = "game_over"

            # Verificar colisao com projeteis
            for projectile in self.projectiles:
                if projectile.active:
                    distance = math.sqrt((self.player.x - projectile.x)**2 + (self.player.y - projectile.y)**2)
                    if distance < 20:
                        if self.player.take_damage():
                            self.add_particles(self.player.x, self.player.y, (255, 150, 50), 8)
                            projectile.reset()  # Resetar projetil
                            if self.player.lives <= 0:
                                self.state = "game_over"

            # Verificar vitoria
            if all(coin.collected for coin in self.coins):
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

        if self.countdown_active:
            self.draw_countdown()
        elif self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "game_over":
            self.draw_game_over()

    def draw_countdown(self):
        """Desenha a tela de contagem regressiva"""
        # Fundo preto instantaneo
        overlay = Rect(0, 0, WIDTH, HEIGHT)
        screen.draw.filled_rect(overlay, (0, 0, 0, 255))

        if self.countdown_timer >= 30:
            # Numero da contagem regressiva
            if self.countdown_number > 0:
                number_text = str(self.countdown_number)
                color = (255, 255, 100)  # Amarelo
            else:
                number_text = "GO!"
                color = (100, 255, 100)  # Verde

            # Sombra do texto
            screen.draw.text(number_text, center=(WIDTH//2 + 4, HEIGHT//2 + 4),
                           fontsize=120, color=(0, 0, 0, 150))
            # Texto principal
            screen.draw.text(number_text, center=(WIDTH//2, HEIGHT//2),
                           fontsize=120, color=color)

    def draw_menu(self):
        """Desenha o menu principal com design melhorado"""
        # Fundo gradiente colorido e animado
        for y in range(0, HEIGHT, 20):
            # Gradiente de cores vibrantes
            r = int(50 + 30 * math.sin(y * 0.01 + self.countdown_timer * 0.02))
            g = int(100 + 40 * math.sin(y * 0.015 + self.countdown_timer * 0.03))
            b = int(150 + 50 * math.sin(y * 0.02 + self.countdown_timer * 0.04))
            screen.draw.filled_rect(Rect(0, y, WIDTH, 20), (r, g, b))

        # Desenhar imagem de fundo do menu com transparencia
        menu_bg.draw()

        # Titulo principal com efeitos
        title = "CACA AO TESOURO"
        subtitle = "Aventura Pirata"

        # Sombra do titulo
        screen.draw.text(title, center=(WIDTH//2 + 3, 82), fontsize=48, color=(0, 0, 0, 150))
        # Titulo principal com gradiente
        screen.draw.text(title, center=(WIDTH//2, 80), fontsize=48, color=(255, 255, 100))

        # Subtitulo
        screen.draw.text(subtitle, center=(WIDTH//2 + 2, 132), fontsize=28, color=(0, 0, 0, 100))
        screen.draw.text(subtitle, center=(WIDTH//2, 130), fontsize=28, color=(255, 200, 100))

        # Autor com estilo
        author_text = "por Matheus Abrahao"
        screen.draw.text(author_text, center=(WIDTH//2, 170), fontsize=18, color=(200, 200, 200))

        # Cores do tema pirata/tropical
        WOOD_COLOR = (107, 66, 38)      # #6B4226 - Marrom madeira
        GOLD_COLOR = (255, 215, 0)      # #FFD700 - Dourado
        TURQUOISE_HOVER = (26, 188, 156) # #1ABC9C - Turquesa suave
        DARK_WOOD = (75, 46, 28)        # #4B2E1C - Marrom escuro para bordas

        # Botoes com tema pirata/tropical
        button_configs = [
            ("INICIAR AVENTURA", "start"),
            ("MUSICA: " + ("LIGADA" if self.music_on else "DESLIGADA"), "music"),
            ("SONS: " + ("LIGADOS" if self.sfx_on else "DESLIGADOS"), "sfx"),
            ("SAIR", "exit")
        ]

        for text, key in button_configs:
            button = self.buttons[key]
            is_hovered = self.button_hover == key

            # Cor do botao baseada no hover
            current_color = TURQUOISE_HOVER if is_hovered else WOOD_COLOR

            # Sombra do botao (mais escura para profundidade)
            shadow = Rect(button.x + 3, button.y + 3, button.width, button.height)
            screen.draw.filled_rect(shadow, (0, 0, 0, 100))

            # Botao principal com cor de madeira
            screen.draw.filled_rect(button, current_color)

            # Borda em marrom escuro (2px simulada)
            border_rect = Rect(button.x - 2, button.y - 2, button.width + 4, button.height + 4)
            screen.draw.rect(border_rect, DARK_WOOD)

            # Texto dourado em negrito
            text_color = GOLD_COLOR
            # Sombra do texto para melhor legibilidade
            screen.draw.text(text, center=(button.centerx + 1, button.centery + 1),
                           fontsize=22, color=(0, 0, 0, 100))
            # Texto principal dourado
            screen.draw.text(text, center=button.center, fontsize=22, color=text_color)

        # Instrucoes na parte inferior
        instructions = "MOUSE: Clique nos botoes - OBJETIVO: Colete 10 moedas - EVITE: Piratas e projeteis!"
        screen.draw.text(instructions, center=(WIDTH//2, HEIGHT - 30), fontsize=16, color=(255, 255, 255))

    def draw_game(self):
        # Desenhar territorios dos inimigos com visual melhorado
        for enemy in self.enemies:
            # Territorio com gradiente simulado
            screen.draw.rect(enemy.territory, (180, 50, 50, 30))
            screen.draw.rect(enemy.territory, (100, 0, 0))
            # Aviso de perigo
            screen.draw.text("PIRATAS RIVAIS", center=(enemy.territory.centerx, enemy.territory.top - 15),
                           fontsize=20, color=(255, 50, 50))

        # Desenhar elementos em ordem de profundidade
        for coin in self.coins:
            coin.draw()
        for powerup in self.powerups:
            powerup.draw()
        for enemy in self.enemies:
            enemy.draw()
        for projectile in self.projectiles:
            projectile.draw()
        self.player.draw()

        # Desenhar particulas
        for particle in self.particles:
            alpha = int((particle['life'] / 30) * 255)
            screen.draw.filled_circle((particle['x'], particle['y']), 2, particle['color'])

        # UI melhorada com fundo
        ui_bg = Rect(5, 5, 200, 80)
        screen.draw.filled_rect(ui_bg, (0, 0, 0, 150))
        screen.draw.rect(ui_bg, "white")

        screen.draw.text(f"Tesouros: {self.score}", (15, 15), fontsize=28, color=(255, 255, 100))
        collected_coins = sum(1 for coin in self.coins if coin.collected)
        coin_color = (100, 255, 100) if collected_coins == COIN_COUNT else "white"
        screen.draw.text(f"Moedas: {collected_coins}/{COIN_COUNT}", (15, 45), fontsize=24, color=coin_color)

        # Mostrar vidas
        lives_text = f"Vidas: {self.player.lives}/3"
        lives_color = (255, 100, 100) if self.player.lives <= 1 else (255, 255, 255)
        screen.draw.text(lives_text, (15, 65), fontsize=20, color=lives_color)

        # Mostrar powerup ativo
        if self.player.powerup_active:
            powerup_text = f"VELOCIDADE! ({self.player.powerup_timer // 60}s)"
            screen.draw.text(powerup_text, center=(WIDTH//2, 30), fontsize=20, color=(255, 255, 0))

        # Instrucoes no canto inferior
        instructions = "MOUSE: Clique para mover - OBJETIVO: Colete todas as 10 moedas - EVITE: Piratas e projeteis!"
        screen.draw.text(instructions, center=(WIDTH//2, HEIGHT - 20), fontsize=16, color=(200, 200, 200))

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

        # Botao para voltar
        button_rect = Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 40)
        screen.draw.filled_rect(button_rect, (100, 150, 255))
        screen.draw.rect(button_rect, "white")
        screen.draw.text("Clique para voltar ao porto", center=button_rect.center, fontsize=20, color="white")

    def handle_click(self, pos):
        if self.countdown_active:
            return

        if self.state == "menu":
            # Verificar hover dos botoes
            self.button_hover = None
            for key, button in self.buttons.items():
                if button.collidepoint(pos):
                    self.button_hover = key
                    break

            if self.buttons["start"].collidepoint(pos):
                self.start_countdown()
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

    def handle_mouse_move(self, pos):
        """Atualiza o estado de hover dos botoes"""
        if self.state == "menu":
            self.button_hover = None
            for key, button in self.buttons.items():
                if button.collidepoint(pos):
                    self.button_hover = key
                    break

# Carregar imagem de fundo do menu
menu_bg = Actor('menu_background')

# Instancia global do jogo
game = Game()

def update():
    game.update()

def draw():
    game.draw()

def on_mouse_down(pos, button):
    if button == 1:
        game.handle_click(pos)

def on_mouse_move(pos):
    game.handle_mouse_move(pos)

pgzrun.go()
