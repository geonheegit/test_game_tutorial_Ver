import pygame 
from settings import *
from tile import Tile
from player import Player


class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# 스프라이트 그룹 나누기
		self.visible_sprites = Camera()
		self.obstacle_sprites = pygame.sprite.Group()

		# 맵 로딩
		self.create_map()

	def create_map(self):
		for row_index,row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'x':
					Tile((x,y),[self.visible_sprites, self.obstacle_sprites]) # visible_sprites & obstacle_sprites에 포함
				if col == 'p':
					self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites) # visible_sprites에 포함 / obstacle_sprites 그룹 제공

	def run(self): # main에서 무한 반복
		# 화면에 출력
		self.visible_sprites.new_draw(self.player) # visible_sprites에 있는 것을 화면에 출력 / new_draw로 (카메라)
		self.visible_sprites.update()

class Camera(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface() # 화면 가져오기
		self.adjusted = pygame.math.Vector2()

		# 맵
		self.zoom = 2
		self.floor_surf = pygame.image.load("map/test_map1.png").convert()
		self.map_size = self.floor_surf.get_size()
		self.floor_surf = pygame.transform.scale(self.floor_surf, (self.map_size[0] * self.zoom, self.map_size[1] * self.zoom))
		self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

	def new_draw(self, player):
		# 카메라 움직임 보정값
		self.adjusted.x = player.rect.center[0] - self.display_surface.get_width() // 2 # 카메라 가운데에 플레이어 배치 위해 화면 크기의 절반 빼주기
		self.adjusted.y = player.rect.center[1] - self.display_surface.get_height() // 2

		floor_adjusted_pos = self.floor_rect.topleft - self.adjusted
		self.display_surface.blit(self.floor_surf, floor_adjusted_pos)

		for sprite in self.sprites():
			adjusted_pos = sprite.rect.topleft - self.adjusted
			self.display_surface.blit(sprite.image, adjusted_pos)