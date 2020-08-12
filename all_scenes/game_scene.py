import pygame
from scene import Scene
from all_scenes.gameover_scene import GameOverScene
from gui import (Label, Options)
from resources import Resources
from game_code import (Table, Pen, PenData, PenSprite, GameResult, NeuralNetwork)
from game_code.b2d import *
from game_code.units import *
import math
import random


class GameScene(Scene):
    GAME_OVER_EVENT = pygame.USEREVENT + 1
    game_over = False

    world = None
    table = None
    players = None

    enemy_ai = None

    current_player_index = -1
    winner_player_index = -1
    move_made = True

    turn_count = 0

    turn_text = None
    victory_text = None

    drag_start_pos = None
    mouse_dragging = False
    drag_end_pos = None

    player_sprites = []
    width, height = 0, 0

    def start(self, screen):
        if not self.already_loaded:
            self.width, self.height = screen.get_width(), screen.get_height()

            self.turn_text = Label(pygame.Rect(10, 10, 100, 30), "", {
                Options.BACKGROUND: (0, 51, 102),
                Options.FOREGROUND: (255, 255, 255),
                Options.BORDER_WIDTH: 0,
            })

            self.victory_text = Label(pygame.Rect(self.width / 2 - 100, self.height / 2 - 30, 200, 60), "", {
                Options.FONT: pygame.font.SysFont("Comic Sans MS", 25),
                Options.BACKGROUND: (0, 51, 102),
                Options.FOREGROUND: (255, 255, 255),
                Options.BORDER_WIDTH: 0,
            })

            self.reset_game_data()
            self.already_loaded = True

        if GameScene.game_over:
            self.reset_game_data()

    def reset_game_data(self):
        GameScene.game_over = False

        self.world = World((0, 0))

        world_center = screen_to_world((self.width / 2, self.height / 2))
        table_size = screen_to_world((self.width - 50, self.height - 100))

        self.table = Table(world_center, table_size, self.world)
        self.players = [Pen(PenData.current_pen, (world_center[0] - 35, world_center[1]), self.table.body, self.world),
                        Pen(random.choice(PenData.all_pens), (world_center[0] + 35, world_center[1]), self.table.body,
                            self.world)]

        self.enemy_ai = NeuralNetwork.create(15, 8, 2)

        self.turn_count = 0
        self.move_made = True

        self.current_player_index = 1
        self.winner_player_index = -1

        self.player_sprites = {p: PenSprite(Resources.get(p.data.image_file)) for p in self.players}

        self.next_turn()

    def update(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            Scene.push_scene(8)

        elif event.type == pygame.MOUSEBUTTONDOWN and not self.mouse_dragging:
            self.drag_start_pos = self.drag_end_pos = pygame.mouse.get_pos()
            self.mouse_dragging = True
        elif event.type == pygame.MOUSEMOTION and self.mouse_dragging:
            self.drag_end_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and self.mouse_dragging:
            self.drag_end_pos = pygame.mouse.get_pos()

            drag_start = Vec2(screen_to_world((self.drag_start_pos[0], self.height - self.drag_start_pos[1])))
            drag_end = Vec2(screen_to_world((self.drag_end_pos[0], self.height - self.drag_end_pos[1])))
            hit_point = self.cast_ray(self.players[0], drag_start, drag_end)
            if hit_point is not None:
                force = (hit_point - drag_start) * 25
                self.players[0].apply_force(hit_point, force)
                self.move_made = True

            self.mouse_dragging = False

        elif event.type == pygame.KEYDOWN and self.winner_player_index == -1 and not self.move_made:
            if event.key == pygame.K_2 and self.current_player_index == 1:
                point, force = self.evaluate_ai(self.enemy_ai)
                self.players[1].apply_force(point, force)
                self.move_made = True

        elif event.type == GameScene.GAME_OVER_EVENT:
            pygame.time.set_timer(GameScene.GAME_OVER_EVENT, 0)

            GameScene.game_over = True

            state = GameResult.VictoryState.WIN if self.winner_player_index == 0 else \
                GameResult.VictoryState.LOSE if self.winner_player_index == 1 else GameResult.VictoryState.TIE
            GameOverScene.result = GameResult(state)

            Scene.push_scene(10)

    def cast_ray(self, player, start, end):
        input = RayCastInput(p1=start, p2=end, maxFraction=1)
        output = RayCastOutput()
        if player.body.fixtures[0].RayCast(output, input, 0):
            hit_point = start + (end - start) * output.fraction
            return hit_point
        return None

    def evaluate_ai(self, neural_net):
        outputs = neural_net.predict([0.5] * 15)
        return (outputs[1], outputs[0] * 7.5), Vec2(outputs) * 10

    def draw(self, screen):
        screen.fill((0, 51, 102))

        table_rect = pygame.Rect((0, 0), world_to_screen(self.table.dimensions))
        table_rect.center = world_to_screen(self.table.center)
        pygame.draw.rect(screen, (204, 102, 0), table_rect)

        if self.winner_player_index == -1:
            self.turn_text.draw(screen)
            self.draw_player(screen, self.players[0])
            self.draw_player(screen, self.players[1])
        elif self.winner_player_index < 2:
            self.draw_player(screen, self.players[self.winner_player_index])

        if self.winner_player_index == -1 and \
                GameScene.velocity_near_zero(self.players[0]) and \
                GameScene.velocity_near_zero(self.players[1]):
            if not (self.table.contains_point(self.players[0].body.position)
                 or self.table.contains_point(self.players[1].body.position)):
                self.check_winner()
            elif self.move_made:
                self.next_turn()

        if self.mouse_dragging:
            drag_start = Vec2(screen_to_world((self.drag_start_pos[0], self.height - self.drag_start_pos[1])))
            drag_end = Vec2(screen_to_world((self.drag_end_pos[0], self.height - self.drag_end_pos[1])))

            hit_point = self.cast_ray(self.players[0], drag_start, drag_end)
            if hit_point is not None:
                end = world_to_screen(hit_point)
                end = (end[0], self.height - end[1])
                GameScene.draw_arrow(screen, (0, 255, 0), self.drag_start_pos, end)
            else:
                GameScene.draw_arrow(screen, (255, 0, 0), self.drag_start_pos, self.drag_end_pos)

        if self.winner_player_index != -1:
            self.victory_text.draw(screen)

        self.world.Step(1.0 / 60.0, 25, 25)
        self.world.ClearForces()

    @staticmethod
    def draw_arrow(surface, color, start, end, line_size=3, arrow_size=7):
        pygame.draw.line(surface, color, start, end, line_size)
        rotation = math.atan2(start[1] - end[1], end[0] - start[0]) + math.pi / 2
        pygame.draw.polygon(surface, color,
                            [(end[0] + arrow_size * math.sin(rotation), end[1] + arrow_size * math.cos(rotation)),
                             (end[0] + arrow_size * math.sin(rotation - 2.0944),
                              end[1] + arrow_size * math.cos(rotation - 2.0944)),
                             (end[0] + arrow_size * math.sin(rotation + 2.0944),
                              end[1] + arrow_size * math.cos(rotation + 2.0944))])

    def next_turn(self):
        self.move_made = False
        self.current_player_index = 1 - self.current_player_index

        self.turn_text.text = f"Player's Turn" if self.current_player_index == 0 else f"Computer's Turn"
        self.turn_text.recreate(False)

    def check_winner(self):
        player_inside = self.table.contains_point(self.players[0].body.position)
        comp_inside = self.table.contains_point(self.players[1].body.position)

        if not player_inside and not comp_inside:
            self.winner_player_index = 2
            self.victory_text.text = f"It's a tie!"
            self.victory_text.recreate()
            pygame.time.set_timer(GameScene.GAME_OVER_EVENT, 2000)
        elif not player_inside:
            self.winner_player_index = 1
            self.victory_text.text = f"Computer wins!"
            self.victory_text.recreate()
            pygame.time.set_timer(GameScene.GAME_OVER_EVENT, 2000)
        elif not comp_inside:
            self.winner_player_index = 0
            self.victory_text.text = f"Player wins!"
            self.victory_text.recreate()
            pygame.time.set_timer(GameScene.GAME_OVER_EVENT, 2000)

    def draw_player(self, screen, player):
        position = player.get_position()
        position = world_to_screen(position)
        position = (position[0], self.height - position[1])

        rotation = player.get_rotation()
        rotation = math.degrees(rotation)

        sprite = self.player_sprites[player]
        sprite.set_transform(position, rotation)
        sprite.draw(screen)

        vertices = [world_to_screen(v) for v in player.get_vertices()]
        vertices = [(v[0], screen.get_height() - v[1]) for v in vertices]
        pygame.draw.polygon(screen, (0, 255, 0), vertices)
        for v in vertices:
            pygame.draw.circle(screen, (255, 0, 0), (int(v[0]), int(v[1])), 3)
        if self.current_player_index == self.players.index(player):
            pygame.draw.polygon(screen, (0, 0, 0), vertices, 2)

    @staticmethod
    def velocity_near_zero(player, linear_threshold=0.3, angular_threshold=0.4):
        return player.body.linearVelocity.lengthSquared <= linear_threshold ** 2 \
               and player.body.angularVelocity <= angular_threshold
