"""
Treasure Hunt - Pirate Adventure
Author: Matheus Abrahao
A top-down pirate adventure game using Pygame Zero
"""

import math
import random

import pgzrun
from pygame import Rect

# Game constants
TITLE = "Treasure Hunt - Pirate Adventure"
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 3
ENEMY_SPEED = 2
COIN_COUNT = 10
ENEMY_COUNT = 3
POWERUP_COUNT = 3
PROJECTILE_COUNT = 5

def load_seq(prefix: str, start: int, end: int):
    """Helper to generate animation frame sequence"""
    return [f"{prefix}{i}" for i in range(start, end + 1)]

class Animation:
    """Class to manage sprite animations"""
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
    """Player class with click-to-move movement"""
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
        # Use 26 idle animation frames
        self.idle_animation = Animation([f'player/idle/{i}' for i in range(1, 27)], 15)
        # Use 14 run animation frames
        self.run_animation = Animation([f'player/run/{i}' for i in range(1, 15)], 12)
        self.current_animation = self.idle_animation

    def move_to(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
        self.is_moving = True
    def update(self):
        # Update invincibility
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        # Update powerup
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
        """Activate speed powerup"""
        self.powerup_active = True
        self.powerup_timer = 300  # 5 seconds
        self.speed = PLAYER_SPEED * 2

    def take_damage(self):
        """Player takes damage"""
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_timer = 120  # 2 seconds of invincibility
            return True
        return False

    def draw(self):
        # Blink when invincible
        if self.invincible and self.invincible_timer % 10 < 5:
            return

        # Get current animation frame
        current_frame = self.current_animation.get_current_frame()

        try:
            # Create Actor with current image and position
            player_actor = Actor(current_frame)
            player_actor.x = self.x
            player_actor.y = self.y

            # Draw player sprite
            player_actor.draw()
        except Exception as e:
            # Fallback if images not found
            print(f"Error loading sprite: {e}")
            color = (0, 120, 255) if self.current_animation == self.idle_animation else (0, 180, 255)
            if self.powerup_active:
                color = (255, 255, 0)  # Gold when with powerup

            # Draw rectangle as fallback
            screen.draw.filled_rect(Rect(self.x - 15, self.y - 15, 30, 30), color)
            screen.draw.rect(Rect(self.x - 15, self.y - 15, 30, 30), (255, 255, 255))

class Enemy:
    """Enemy class with patrol movement"""
    def __init__(self, x, y, territory):
        self.x = x
        self.y = y
        self.speed = ENEMY_SPEED
        self.direction = random.uniform(0, 2 * math.pi)
        self.territory = territory
        self.change_direction_timer = 0
        # Use 12 run animation frames
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

        # Enemy is always "moving" → run animation
        self.current_animation = self.run_animation
        self.current_animation.update()
    def draw(self):
        # Get current animation frame
        current_frame = self.current_animation.get_current_frame()

        try:
            # Create Actor with current image and position
            enemy_actor = Actor(current_frame)
            enemy_actor.x = self.x
            enemy_actor.y = self.y

            # Draw enemy sprite
            enemy_actor.draw()
        except Exception as e:
            # Fallback if images not found
            print(f"Error loading enemy sprite: {e}")
            # Draw rectangle as fallback
            screen.draw.filled_rect(Rect(self.x - 12, self.y - 12, 25, 25), (180, 30, 30))
            screen.draw.rect(Rect(self.x - 12, self.y - 12, 25, 25), (100, 0, 0))

class Coin:
    """Class for collectible coins"""
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
            # Coins with improved visual - static shine effect
            # Shadow
            screen.draw.filled_circle((self.x + 1, self.y + 1), 10, (0, 0, 0, 50))
            # Dark gold outer ring
            screen.draw.filled_circle((self.x, self.y), 10, (200, 150, 0))
            # Light gold inner ring
            screen.draw.filled_circle((self.x, self.y), 8, (255, 215, 0))
            # Bright center
            screen.draw.filled_circle((self.x, self.y), 5, (255, 255, 150))
            # White border
            screen.draw.circle((self.x, self.y), 10, "white")

class PowerUp:
    """Class for speed powerups"""
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
            # Powerup with special static visual effect
            # Shadow
            screen.draw.filled_circle((self.x + 2, self.y + 2), 12, (0, 0, 0, 60))
            # Blue outer ring
            screen.draw.filled_circle((self.x, self.y), 12, (100, 150, 255))
            # Light blue inner ring
            screen.draw.filled_circle((self.x, self.y), 10, (150, 200, 255))
            # Bright center
            screen.draw.filled_circle((self.x, self.y), 6, (255, 255, 255))
            # White border
            screen.draw.circle((self.x, self.y), 12, "white")
            # Glow effect
            screen.draw.circle((self.x, self.y), 8, (255, 255, 100))

class Projectile:
    """Class for projectiles/obstacles that move around the map"""
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset projectile to new position and direction"""
        # Choose random border for spawn
        side = random.randint(0, 3)
        if side == 0:  # Top
            self.x = random.randint(0, WIDTH)
            self.y = -20
        elif side == 1:  # Right
            self.x = WIDTH + 20
            self.y = random.randint(0, HEIGHT)
        elif side == 2:  # Bottom
            self.x = random.randint(0, WIDTH)
            self.y = HEIGHT + 20
        else:  # Left
            self.x = -20
            self.y = random.randint(0, HEIGHT)

        # Random direction
        self.direction = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(2, 4)
        self.active = True
        self.animation = Animation(['projectile_1', 'projectile_2'], 8)

    def update(self):
        if self.active:
            # Move projectile
            self.x += math.cos(self.direction) * self.speed
            self.y += math.sin(self.direction) * self.speed

            # Check if left screen
            if (self.x < -30 or self.x > WIDTH + 30 or
                self.y < -30 or self.y > HEIGHT + 30):
                self.reset()

            self.animation.update()

    def draw(self):
        if self.active:
            # Projectile with visual effect
            # Shadow
            screen.draw.filled_circle((self.x + 1, self.y + 1), 8, (0, 0, 0, 80))
            # Main body (orange/red)
            screen.draw.filled_circle((self.x, self.y), 8, (255, 100, 50))
            # Bright center
            screen.draw.filled_circle((self.x, self.y), 4, (255, 200, 100))
            # Border
            screen.draw.circle((self.x, self.y), 8, (255, 50, 0))
            # Trail effect
            trail_x = self.x - math.cos(self.direction) * 15
            trail_y = self.y - math.sin(self.direction) * 15
            screen.draw.filled_circle((trail_x, trail_y), 4, (255, 100, 50, 100))

class Game:
    """Main game class"""
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
        # Better positioned and larger territories for enemies
        territories = [
            Rect(80, 80, 180, 120),   # Upper left
            Rect(520, 80, 180, 120),  # Upper right
            Rect(300, 420, 200, 120)  # Lower center
        ]
        self.enemies = []
        for i in range(ENEMY_COUNT):
            territory = territories[i]
            # Position enemies at center of their territories
            x = territory.centerx
            y = territory.centery
            self.enemies.append(Enemy(x, y, territory))
        self.coins = []
        # Better coin distribution avoiding enemy territories
        safe_zones = [
            (150, 300), (350, 200), (450, 300), (650, 300),
            (200, 500), (600, 500), (400, 150), (700, 400),
            (100, 450), (750, 200)
        ]
        for i in range(min(COIN_COUNT, len(safe_zones))):
            x, y = safe_zones[i]
            self.coins.append(Coin(x, y))

        # Add powerups
        self.powerups = []
        powerup_positions = [(250, 250), (550, 350), (450, 450)]
        for i in range(min(POWERUP_COUNT, len(powerup_positions))):
            x, y = powerup_positions[i]
            self.powerups.append(PowerUp(x, y))

        # Add projectiles
        self.projectiles = []
        for i in range(PROJECTILE_COUNT):
            self.projectiles.append(Projectile())

        self.particles = []
        self.score = 0

        # Start background music
        if self.music_on:
            music.play('soundtrack')

    def add_particles(self, x, y, color, count=5):
        """Add particle effects"""
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
        """Start countdown for the game"""
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

            # Check collisions
            for coin in self.coins:
                if not coin.collected:
                    distance = math.sqrt((self.player.x - coin.x)**2 + (self.player.y - coin.y)**2)
                    if distance < 25:
                        coin.collected = True
                        self.score += 10
                        self.add_particles(coin.x, coin.y, (255, 215, 0), 8)
                        # Play coin sound
                        if self.sfx_on:
                            try:
                                sounds.coin.play()
                            except Exception as e:
                                print(f"Error playing sound: {e}")

            # Check powerup collision
            for powerup in self.powerups:
                if not powerup.collected:
                    distance = math.sqrt((self.player.x - powerup.x)**2 + (self.player.y - powerup.y)**2)
                    if distance < 30:
                        powerup.collected = True
                        self.player.activate_powerup()
                        self.add_particles(powerup.x, powerup.y, (100, 150, 255), 12)
                        self.score += 20

            # Check enemy collision
            for enemy in self.enemies:
                distance = math.sqrt((self.player.x - enemy.x)**2 + (self.player.y - enemy.y)**2)
                if distance < 30:
                    if self.player.take_damage():
                        self.add_particles(self.player.x, self.player.y, (255, 100, 100), 10)
                        if self.player.lives <= 0:
                            self.state = "game_over"

            # Check projectile collision
            for projectile in self.projectiles:
                if projectile.active:
                    distance = math.sqrt((self.player.x - projectile.x)**2 + (self.player.y - projectile.y)**2)
                    if distance < 20:
                        if self.player.take_damage():
                            self.add_particles(self.player.x, self.player.y, (255, 150, 50), 8)
                            projectile.reset()  # Reset projectile
                            if self.player.lives <= 0:
                                self.state = "game_over"

            # Check victory
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
        """Draw countdown screen"""
        # Instant black background
        overlay = Rect(0, 0, WIDTH, HEIGHT)
        screen.draw.filled_rect(overlay, (0, 0, 0, 255))

        if self.countdown_timer >= 30:
            # Countdown number
            if self.countdown_number > 0:
                number_text = str(self.countdown_number)
                color = (255, 255, 100)  # Yellow
            else:
                number_text = "GO!"
                color = (100, 255, 100)  # Green

            # Text shadow
            screen.draw.text(number_text, center=(WIDTH//2 + 4, HEIGHT//2 + 4),
                           fontsize=120, color=(0, 0, 0, 150))
            # Main text
            screen.draw.text(number_text, center=(WIDTH//2, HEIGHT//2),
                           fontsize=120, color=color)

    def draw_menu(self):
        """Draw main menu with improved design"""
        # Animated colored gradient background
        for y in range(0, HEIGHT, 20):
            # Vibrant color gradient
            r = int(50 + 30 * math.sin(y * 0.01 + self.countdown_timer * 0.02))
            g = int(100 + 40 * math.sin(y * 0.015 + self.countdown_timer * 0.03))
            b = int(150 + 50 * math.sin(y * 0.02 + self.countdown_timer * 0.04))
            screen.draw.filled_rect(Rect(0, y, WIDTH, 20), (r, g, b))

        # Draw menu background image with transparency
        menu_bg.draw()

        # Main title with effects
        title = "TREASURE HUNT"
        subtitle = "Pirate Adventure"

        # Title shadow
        screen.draw.text(title, center=(WIDTH//2 + 3, 82), fontsize=48, color=(0, 0, 0, 150))
        # Main title with gradient
        screen.draw.text(title, center=(WIDTH//2, 80), fontsize=48, color=(255, 255, 100))

        # Subtitle
        screen.draw.text(subtitle, center=(WIDTH//2 + 2, 132), fontsize=28, color=(0, 0, 0, 100))
        screen.draw.text(subtitle, center=(WIDTH//2, 130), fontsize=28, color=(255, 200, 100))

        # Author with style
        author_text = "por Matheus Abrahao"
        screen.draw.text(author_text, center=(WIDTH//2, 170), fontsize=18, color=(200, 200, 200))

        # Pirate/tropical theme colors
        WOOD_COLOR = (107, 66, 38)      # #6B4226 - Wood brown
        GOLD_COLOR = (255, 215, 0)      # #FFD700 - Gold
        TURQUOISE_HOVER = (26, 188, 156) # #1ABC9C - Soft turquoise
        DARK_WOOD = (75, 46, 28)        # #4B2E1C - Dark brown for borders

        # Buttons with pirate/tropical theme
        button_configs = [
            ("START ADVENTURE", "start"),
            ("MUSIC: " + ("ON" if self.music_on else "OFF"), "music"),
            ("SOUND: " + ("ON" if self.sfx_on else "OFF"), "sfx"),
            ("EXIT", "exit")
        ]

        for text, key in button_configs:
            button = self.buttons[key]
            is_hovered = self.button_hover == key

            # Button color based on hover
            current_color = TURQUOISE_HOVER if is_hovered else WOOD_COLOR

            # Button shadow (darker for depth)
            shadow = Rect(button.x + 3, button.y + 3, button.width, button.height)
            screen.draw.filled_rect(shadow, (0, 0, 0, 100))

            # Main button with wood color
            screen.draw.filled_rect(button, current_color)

            # Dark brown border (2px simulated)
            border_rect = Rect(button.x - 2, button.y - 2, button.width + 4, button.height + 4)
            screen.draw.rect(border_rect, DARK_WOOD)

            # Bold gold text
            text_color = GOLD_COLOR
            # Text shadow for better readability
            screen.draw.text(text, center=(button.centerx + 1, button.centery + 1),
                           fontsize=22, color=(0, 0, 0, 100))
            # Main gold text
            screen.draw.text(text, center=button.center, fontsize=22, color=text_color)

        # Instructions at bottom
        instructions = "MOUSE: Click buttons - OBJECTIVE: Collect 10 coins - AVOID: Pirates and projectiles!"
        screen.draw.text(instructions, center=(WIDTH//2, HEIGHT - 30), fontsize=16, color=(255, 255, 255))

    def draw_game(self):
        # Draw enemy territories with improved visual
        for enemy in self.enemies:
            # Territory with simulated gradient
            screen.draw.rect(enemy.territory, (180, 50, 50, 30))
            screen.draw.rect(enemy.territory, (100, 0, 0))
            # Danger warning
            screen.draw.text("RIVAL PIRATES", center=(enemy.territory.centerx, enemy.territory.top - 15),
                           fontsize=20, color=(255, 50, 50))

        # Draw elements in depth order
        for coin in self.coins:
            coin.draw()
        for powerup in self.powerups:
            powerup.draw()
        for enemy in self.enemies:
            enemy.draw()
        for projectile in self.projectiles:
            projectile.draw()
        self.player.draw()

        # Draw particles
        for particle in self.particles:
            alpha = int((particle['life'] / 30) * 255)
            screen.draw.filled_circle((particle['x'], particle['y']), 2, particle['color'])

        # Improved UI with background
        ui_bg = Rect(5, 5, 200, 80)
        screen.draw.filled_rect(ui_bg, (0, 0, 0, 150))
        screen.draw.rect(ui_bg, "white")

        screen.draw.text(f"Score: {self.score}", (15, 15), fontsize=28, color=(255, 255, 100))
        collected_coins = sum(1 for coin in self.coins if coin.collected)
        coin_color = (100, 255, 100) if collected_coins == COIN_COUNT else "white"
        screen.draw.text(f"Coins: {collected_coins}/{COIN_COUNT}", (15, 45), fontsize=24, color=coin_color)

        # Show lives
        lives_text = f"Lives: {self.player.lives}/3"
        lives_color = (255, 100, 100) if self.player.lives <= 1 else (255, 255, 255)
        screen.draw.text(lives_text, (15, 65), fontsize=20, color=lives_color)

        # Show active powerup
        if self.player.powerup_active:
            powerup_text = f"SPEED! ({self.player.powerup_timer // 60}s)"
            screen.draw.text(powerup_text, center=(WIDTH//2, 30), fontsize=20, color=(255, 255, 0))

        # Instructions in bottom corner
        instructions = "MOUSE: Click to move - OBJECTIVE: Collect all 10 coins - AVOID: Pirates and projectiles!"
        screen.draw.text(instructions, center=(WIDTH//2, HEIGHT - 20), fontsize=16, color=(200, 200, 200))

    def draw_game_over(self):
        # Semi-transparent background
        overlay = Rect(0, 0, WIDTH, HEIGHT)
        screen.draw.filled_rect(overlay, (0, 0, 0, 150))

        # Game Over with shadow and effect
        collected_coins = sum(1 for coin in self.coins if coin.collected)
        is_victory = collected_coins == COIN_COUNT

        if is_victory:
            # Victory
            screen.draw.text("TREASURE FOUND!", center=(WIDTH//2 + 3, HEIGHT//2 - 47), fontsize=50, color=(0, 0, 0, 100))
            screen.draw.text("TREASURE FOUND!", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=50, color=(255, 255, 100))
            screen.draw.text("You found all treasures!", center=(WIDTH//2, HEIGHT//2 - 10), fontsize=25, color=(100, 255, 100))
        else:
            # Defeat
            screen.draw.text("PIRATES CAUGHT YOU!", center=(WIDTH//2 + 3, HEIGHT//2 - 47), fontsize=50, color=(0, 0, 0, 100))
            screen.draw.text("PIRATES CAUGHT YOU!", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=50, color=(255, 100, 100))
            screen.draw.text("The rival pirates captured you!", center=(WIDTH//2, HEIGHT//2 - 10), fontsize=22, color=(255, 150, 150))

        # Score with highlight
        screen.draw.text(f"Treasures Found: {self.score}", center=(WIDTH//2, HEIGHT//2 + 30), fontsize=30, color=(255, 255, 255))
        screen.draw.text(f"Coins Collected: {collected_coins}/{COIN_COUNT}", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=24, color=(255, 215, 0))

        # Return button
        button_rect = Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 40)
        screen.draw.filled_rect(button_rect, (100, 150, 255))
        screen.draw.rect(button_rect, "white")
        screen.draw.text("Click to return to port", center=button_rect.center, fontsize=20, color="white")

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
        """Update button hover state"""
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
