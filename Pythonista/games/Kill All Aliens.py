# https://gist.github.com/bjucha81/c4d369fc53e8a31ede218a5476116fa2

from scene import *
from math import sin, cos, pi
import random, ui, time, sound

A = Action



class Boss (SpriteNode):
	def __init__(self, **kwargs):
		SpriteNode.__init__(self, 'spc:UFOBlue', **kwargs)
		self.scale = 3
		self.destroyed = False
	

class Enemy (SpriteNode):
	def __init__(self, **kwargs):
		img = random.choice(['spc:EnemyBlack1', 'spc:EnemyRed1', 'spc:EnemyBlue1' ])
		SpriteNode.__init__(self, img, **kwargs)
		self.destroyed = False
	
class SuperEnemy (SpriteNode):
	def __init__(self, **kwargs):
		SpriteNode.__init__(self, 'spc:EnemyBlack4', **kwargs)
		self.scale = 1.5
		self.destroyed = False

class PowerUp (SpriteNode):
	def __init__(self, **kwargs):
		SpriteNode.__init__(self, 'spc:PowerupRedStar', **kwargs)

class PowerUp2 (SpriteNode):
	def __init__(self, **kwargs):
		SpriteNode.__init__(self, 'spc:PowerupRedShield', **kwargs)
		


class Gamefield (Scene):
	def setup (self):
		self.items = []
		self.greenbombs = []
		self.bossfires = []
		self.background_color = '#0c1037'
		score_font = ('Futura', 20)
		self.distance_label = LabelNode('Distance to boss', score_font, parent=self)
		self.lasers = []
		self.health  = 20
		self.distance_label.z_position = +1
		self.distance_label.position = (self.size.w/3.9, 
		self.size.h - 20)
		self.distance = 2000
		self.blasers = []
		self.powers = []
		self.mlasers = []
		self.lasertime = 200
		self.ship = SpriteNode('spc:PlayerShip3Red')
		self.ship.position = (100,40)
		self.add_child(self.ship) 

	def touch_began(self, touch):
		x, y = touch.location
		move_action = Action.move_to(x, y , 0.8, TIMING_SINODIAL)
		self.ship.run_action(move_action)
		self.shoot_laser()
		
		#sound.play_effect('arcade:Laser_1', 0.05, 1.0 + 0.5)
	
	def check_laser_collisions(self):
		for laser in list(self.lasers):
			if not laser.parent:
				self.lasers.remove(laser)
				continue
			for item in self.items:
				if not isinstance(item, Enemy):
					continue
				if item.destroyed:
					continue
				if laser.position in item.frame:
					#sound.play_effect('arcade:Explosion_4', 0.05, 1.0 + 0.5)
					self.enemy_smash(item)
					
					self.lasers.remove(laser)
					
					laser.remove_from_parent()
					break
			
			
	
	def enemy_smash(self, enemy):
		
		
		enemy.destroyed = True				
		
		enemy.remove_from_parent()
		#self.score += 1
		debree = SpriteNode('spc:PlayerShip1Damage1', parent=self)
		debree.position = enemy.position
		debree.z_position = - 1
		debree.run_action(A.move_by(10, 10, 1.6, TIMING_EASE_OUT))
		debree.run_action(A.sequence(A.wait(1), A.remove()))

	def enemy_hit(self, super_enemy):											
		super_enemy.remove_from_parent()
		super_enemy.destroyed = True
						
		debree = SpriteNode('spc:PlayerShip3Damage1', parent=self)
		debree.position = super_enemy.position
		debree.z_position = - 1
		debree.run_action(A.move_by(10, 10, 1.6, TIMING_EASE_OUT))
		debree.run_action(A.sequence(A.wait(1), A.remove()))	
	


	def update(self):
		
		self.evil_laser_hit()
		self.check_item_collisions()
		
		if random.random() < 0.009:
			self.spawn_item()
			
		self.check_laser_collisions()	
		self.check_laser_hit()
		self.check_laser_hit_boss()
		self.boss_laser_hit()
		
		if random.random() < 0.004:
			self.spawn_enemy()
		if random.random() < 0.009:
			self.spawn_powerup()
			
		self.powerup_collision()
		self.multilaser_hit()
		
		self.distance -= 1
		self.distance_label.text = str(self.distance)
		
		
		if self.distance == 0:
			score_font = ('Futura', 50)
			self.distance_label.text = 'Boss appears!'
			
			self.spawn_boss()
		
		if self.distance <= 0:
			self.distance_label.text = 'Boss here!'	
		
	
	def spawn_boss(self): 
		self.background_color = '#391204' 
		boss = Boss(parent=self)
		boss.position = (random.uniform(10, self.size.w-10), self.size.h + 30) 
		h = random.uniform(2.0, 7.0)
		actions = [A.move_to(random.uniform(0, self.size.w), 700, h)]
		boss.run_action(A.sequence(actions))
		
		
	
		
		counter = 10 
		while counter != 0:
			Action.wait(2)
			self.items.append(boss)
			bossfires = SpriteNode('spc:BoltBronze', parent=self)
			bossfires.position = boss.position + (-50, 30)
			bossfires.z_position = -1
			b = random.uniform(10.0, 2500)
			actions = [A.move_to(b, 100, 2 * 2), A.remove()]
																
			bossfires.run_action(A.sequence(actions))
			self.bossfires.append(bossfires)
			Action.wait(2)
			counter = counter - 1
			
				
	
	def check_laser_hit_boss(self):
		for laser in list(self.lasers):
			if not laser.parent:
				self.lasers.remove(laser)
				continue
			for item in self.items:
				if not isinstance(item, Boss):
					continue
				if item.destroyed:
					continue
				if laser.position in item.frame:
					self.health = self.health - 1
					self.move_boss(item)
					self.kill_boss(item)
					self.lasers.remove(laser)
					
					laser.remove_from_parent()
					break
	
	def boss_laser_hit(self):
		for bossfire in list(self.bossfires):
			if not bossfire.parent:
				self.bossfires.remove(bossfire)
				continue
			
			if bossfire.position in self.ship.frame:
				exit()
				bossfire.remove_from_parent()
					
					
	
	def move_boss(self, boss):
		
		boss.run_action(A.move_by(0, -50, 1.6, TIMING_LINEAR))
		counter = 2 
		while counter != 0:
			Action.wait(2)
			self.items.append(boss)
			bossfires = SpriteNode('spc:BoltBronze', parent=self)
			bossfires.position = boss.position + (-50, 30)
			bossfires.z_position = -1
			b = random.uniform(10.0, 2500)
			actions = [A.move_to(b, 100, 2 * 2), A.remove()]
																
			bossfires.run_action(A.sequence(actions))
			self.bossfires.append(bossfires)
			Action.wait(2)
			counter = counter - 1
		
	
	def kill_boss(self, boss):
		if self.health == 0:
			#sound.play_effect('arcade:Explosion_5', 0.9, 1.0 + 0.5)
			self.background_color = '#161d65'
			boss.destroyed = True				
			self.distance_label.text = 'Boss destroyed!'	
			boss.remove_from_parent()																									
			debree = SpriteNode('shp:Explosion00', parent=self)
			debree.position = boss.position
			debree.z_position = - 1
			debree.run_action(A.move_by(10, 10, 1.6, TIMING_EASE_OUT))
			debree.run_action(A.sequence(A.wait(1), A.remove()))	
			self.distance = 2000
		else:
			boss.destroyed = False																																																													
							
	def spawn_enemy(self):
		super_enemy = SuperEnemy(parent=self)
		super_enemy.position = (random.uniform(10, self.size.w-10), self.size.h + 30) 
		h = random.uniform(2.0, 19.0)
		actions = [A.move_to(random.uniform(0, self.size.w), -100, h), A.remove()]
		super_enemy.run_action(A.sequence(actions))
	
		self.items.append(super_enemy)
		blasers = SpriteNode('spc:LaserBlue11', parent=self)
		blasers.position = super_enemy.position + (0, 30)
		blasers.z_position = -1
		b = random.uniform(10.0, 250)
		actions = [A.move_to(b, 100, 2 * 5), A.remove()]													
		blasers.run_action(A.sequence(actions))
		self.blasers.append(blasers)
		
	
				
	def check_laser_hit(self):
		for laser in list(self.lasers):
			if not laser.parent:
				self.lasers.remove(laser)
				continue
			for item in self.items:
				if not isinstance(item, SuperEnemy):
					continue
				if item.destroyed:
					continue
				if laser.position in item.frame:
					
					self.enemy_hit(item)
					
					self.lasers.remove(laser)
					laser.remove_from_parent()
					
					break
					
						
					
	def spawn_item(self):
	
		enemy = Enemy(parent=self)
		enemy.position = (random.uniform(10, self.size.w-10), self.size.h + 30) 
		
		d = random.uniform(2.0, 19.0) 
		
		actions = [A.move_by(0, -(self.size.h + 60), d), A.remove()]
		enemy.run_action(A.sequence(actions))
		
		self.items.append(enemy)
		
		
		

	def check_item_collisions(self):
		
		for item in list(self.items):
			distance = abs(item.position - self.ship.frame.center())
			if item.parent == None: 
				continue
			
			if distance < 60:
				exit()
				
	def evil_laser_hit(self):
		for blaser in list(self.blasers):
			if not blaser.parent:
				self.blasers.remove(blaser)
				continue
			
			if blaser.position in self.ship.frame:
				exit()
				blaser.remove_from_parent()
					
					
																																				
	def shoot_laser(self):
	
		lasers = SpriteNode('spc:LaserRed10', parent=self)
		lasers.position = self.ship.position + (0, 30)
		lasers.z_position = -1
		actions = [A.move_by(0, self.size.h, 1.3 * self.speed), A.remove()]
		lasers.run_action(A.sequence(actions))
		self.lasers.append(lasers)
	
	def spawn_powerup(self):
		power_up = PowerUp(parent=self)
		power_up.position = (random.uniform(10, self.size.w-10), self.size.h + 40)
		p = random.uniform(2.0, 22.0)
		actions = [A.move_to(random.uniform(0, self.size.w), -100, p), A.remove()]
		power_up.run_action(A.sequence(actions))
		
		power_up.run_action(A.move_by(10, 10, 1.6, TIMING_EASE_OUT))
		power_up.run_action(A.sequence(A.wait(5), A.remove()))
		self.powers.append(power_up)
		
	def powerup_collision(self):	
		for power in list(self.powers):
			distance = abs(power.position - self.ship.frame.center())
			if power.parent == None: 
				continue
			
			if distance < 60:
				self.multi_laser()
				self.laser_multi()
				power.remove_from_parent()
			
				
	def multi_laser(self):
			
		mlasers = SpriteNode('spc:LaserGreen13', parent=self)
		mlasers.position = self.ship.position + (10, 30)
		mlasers.z_position = -1
		actions = [A.move_by(500, self.size.h, 1.3 * self.speed), A.remove()]
		mlasers.run_action(A.sequence(actions))
		self.mlasers.append(mlasers)
			
	def laser_multi(self):
		mlasers = SpriteNode('spc:LaserGreen13', parent=self)
		mlasers.position = self.ship.position + (10, 30)
		mlasers.z_position = -1
		actions = [A.move_by(-500, self.size.h, 1.3 * self.speed), A.remove()]
		mlasers.run_action(A.sequence(actions))
		self.mlasers.append(mlasers)		
				
	def multilaser_hit(self):
		for mlaser in list(self.mlasers):
			if not mlaser.parent:
			#	self.mlasers.remove(mlaser)
				continue
			for item in self.items:
				if not isinstance(item, SuperEnemy):
					continue
				if item.destroyed:
					continue
				if mlaser.position in item.frame:
					
					self.enemy_hit(item)
					
					self.mlasers.remove(mlaser)
					mlaser.remove_from_parent()
			
			for mlaser in list(self.mlasers):
				if not mlaser.parent:
					self.mlasers.remove(mlaser)
					continue
				for item in self.items:
					if not isinstance(item, Enemy):
						continue
					if item.destroyed:
						continue
					if mlaser.position in item.frame:
						
						self.enemy_smash(item)
						
						self.mlasers.remove(mlaser)
						mlaser.remove_from_parent()		
		
	
	
	def spawn_powerup2(self):
		power_up2 = PowerUp2(parent=self)
		power_up2.position = (random.uniform(10, self.size.w-10), self.size.h + 40)
		p = random.uniform(2.0, 22.0)
		actions = [A.move_to(random.uniform(0, self.size.w), -100, p), A.remove()]
		power_up2.run_action(A.sequence(actions))
		
		power_up2.run_action(A.move_by(10, 10, 1.6, TIMING_EASE_OUT))
		power_up2.run_action(A.sequence(A.wait(5), A.remove()))
		#self.powers.append(power_up)

run(Gamefield(), PORTRAIT, show_fps=True)

		
'''		self.life = SpriteNode('plf:HudHeart_full')
		self.life.position = (300,710)
		self.life.scale = 0.5
		self.add_child(self.life) '''
