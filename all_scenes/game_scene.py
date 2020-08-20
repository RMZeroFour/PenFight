import pygame
from scene import Scene
from all_scenes.gameover_scene import GameOverScene
from gui import (Label, Options)
from resources import Resources
from game_code import (Table, Pen, PenData, PenSprite, GameResult, NeuralNetwork, AIData)
from game_code.b2d import *
from game_code.units import *
import math
import random


class GameScene(Scene):
    GAME_OVER_EVENT = pygame.USEREVENT + 1
    game_over = False

    ENEMY_MOVE_DELAY = 300

    world = None
    table = None
    players = None

    enemy_ai = None
    ai_counter = 0

    current_player_index = -1
    victory_state = -1
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
            AIData.load_all_ais(Resources.get("all_ai"))

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
                        Pen(PenData.current_enemy_pen, (world_center[0] + 35, world_center[1]), self.table.body, self.world)]

        self.enemy_ai = AIData.all_ai[(PenData.current_enemy_pen.name, PenData.current_enemy_difficulty)]
        self.ai_counter = GameScene.ENEMY_MOVE_DELAY

        self.turn_count = 0
        self.move_made = True

        self.current_player_index = 1
        self.victory_state = -1

        self.player_sprites = {p: PenSprite(Resources.get(p.data.image_file)) for p in self.players}

        self.next_turn()

    def update(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            Scene.push_scene(8)

        elif self.current_player_index == 0 and not self.move_made:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.mouse_dragging:
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

        elif event.type == GameScene.GAME_OVER_EVENT:
            pygame.time.set_timer(GameScene.GAME_OVER_EVENT, 0)
            GameScene.game_over = True
            GameOverScene.result = GameResult(self.victory_state)
            Scene.push_scene(10)

    def cast_ray(self, player, start, end):
        input = RayCastInput(p1=start, p2=end, maxFraction=1)
        output = RayCastOutput()
        if player.body.fixtures[0].RayCast(output, input, 0):
            hit_point = start + (end - start) * output.fraction
            return hit_point
        return None

    def evaluate_ai(self, neural_net):
        outputs = neural_net.predict([random.random() for i in range(0, 15)])
        angle = outputs[0] * 2 * math.pi
        offset = outputs[1] * 25
        return Vec2(math.cos(angle), math.sin(angle)) * offset

    def draw(self, screen):
        screen.fill((0, 51, 102))

        table_rect = pygame.Rect((0, 0), world_to_screen(self.table.dimensions))
        table_rect.center = world_to_screen(self.table.center)
        pygame.draw.rect(screen, (204, 102, 0), table_rect)

        if self.victory_state == -1:
            self.turn_text.draw(screen)
            self.draw_player(screen, self.players[0])
            self.draw_player(screen, self.players[1])
        elif self.victory_state != GameResult.VictoryState.TIE:
            self.draw_player(screen, self.players[self.victory_state.value])

        self.check_bounds()

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

        if self.victory_state != -1:
            self.victory_text.draw(screen)

        if self.victory_state == -1 and not self.move_made and self.current_player_index == 1:
            if self.ai_counter == 0:
                self.ai_counter = GameScene.ENEMY_MOVE_DELAY

                force_origin = self.evaluate_ai(self.enemy_ai.neural_net) + self.players[1].body.position
                force_end = self.players[1].body.position
                hit_point = self.cast_ray(self.players[1], force_origin, force_end)
                if hit_point is not None:
                    force = (hit_point - force_origin) * 25
                    self.players[1].apply_force(hit_point, force)
                    self.move_made = True
            else:
                self.ai_counter -= 1

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

    def check_bounds(self):
        if self.victory_state == -1:
            player_outside = not self.table.contains_point(self.players[0].body.position)
            comp_outside = not self.table.contains_point(self.players[1].body.position)

            if player_outside and comp_outside:
                self.set_winner(GameResult.VictoryState.TIE)

            elif (GameScene.velocity_near_zero(self.players[0]) or player_outside) \
                 and (GameScene.velocity_near_zero(self.players[1]) or comp_outside):

                if player_outside:
                    self.set_winner(GameResult.VictoryState.LOSE)
                elif comp_outside:
                    self.set_winner(GameResult.VictoryState.WIN)
                elif self.move_made:
                    self.next_turn()

    def set_winner(self, result):
        self.victory_state = result

        if result == GameResult.VictoryState.TIE:
            self.victory_text.text = f"It's a tie!"
        elif result == GameResult.VictoryState.LOSE:
            self.victory_text.text = f"Computer wins!"
        elif result == GameResult.VictoryState.WIN:
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

        pygame.draw.circle(screen, (0, 255, 0), (int(position[0]), int(position[1])), 3)
        if self.current_player_index == self.players.index(player):
            pygame.draw.circle(screen, (255, 0, 0), (int(position[0]), int(position[1])), 7, 1)

        # vertices = [world_to_screen(v) for v in player.get_vertices()]
        # vertices = [(v[0], screen.get_height() - v[1]) for v in vertices]
        # pygame.draw.polygon(screen, (0, 255, 0), vertices)
        # for v in vertices:
        #     pygame.draw.circle(screen, (255, 0, 0), (int(v[0]), int(v[1])), 3)
        # if self.current_player_index == self.players.index(player):
        #     pygame.draw.polygon(screen, (0, 0, 0), vertices, 2)

    @staticmethod
    def velocity_near_zero(player, linear_threshold=0.2, angular_threshold=0.5):
        return player.body.linearVelocity.lengthSquared <= linear_threshold ** 2 \
               and player.body.angularVelocity <= angular_threshold
