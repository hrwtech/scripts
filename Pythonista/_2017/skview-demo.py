# https://github.com/jbking/pythonista-misc/blob/master/spritekit/skview-demo.py

import random
import ui
from objc_util import (
    UIColor, CGRect, CGPoint, CGSize,
    ObjCClass, ObjCInstance, NSBundle, create_objc_class)

NSBundle.bundleWithPath_("/System/Library/Frameworks/SpriteKit.framework").load()

SKView = ObjCClass('SKView')
SKScene = ObjCClass('SKScene')
SKShapeNode = ObjCClass('SKShapeNode')
SKPhysicsBody = ObjCClass('SKPhysicsBody')


def create_circle_shape(point):
	radius = random.randint(25, 45)
	node = SKShapeNode.shapeNodeWithCircleOfRadius_(radius)
	node.position = point
	node.physicsBody = SKPhysicsBody.bodyWithCircleOfRadius_(radius)
	return node
	
	
def create_box_shape(point):
	width = random.randint(42, 80)
	height = random.randint(42, 80)
	size = CGSize(width, height)
	node = SKShapeNode.shapeNodeWithRectOfSize_(size)
	node.position = point
	node.physicsBody = SKPhysicsBody.bodyWithRectangleOfSize_(size)
	return node
	
	
def DemoScene_update_(_self, _cmd, current_time):
	scene = ObjCInstance(_self)
	for child in scene.children():
		if child.position().y < 0:
			child.removeFromParent()
			
			
def random_color():
	return UIColor.color(red=random.random(), green=random.random(), blue=random.random(), alpha=1.0)
	
	
def DemoScene_touchesBegan_withEvent_(_self, _cmd, _touches, event):
	scene = ObjCInstance(_self)
	touches = ObjCInstance(_touches)
	for id, touch in enumerate(touches):
		point = touch.locationInNode_(scene)
		node = random.choice([
		create_circle_shape,
		create_box_shape
		])(point)
		node.fillColor = random_color()
		scene.addChild_(node)
		
		
DemoScene = create_objc_class(
    'DemoScene',
    SKScene,
    methods=[
        DemoScene_update_,
        DemoScene_touchesBegan_withEvent_
    ],
    protocols=[])


class DemoView(ui.View):

	debug = True
	
	def __init__(self):
	# Setup SKView
		screen_size = ui.get_screen_size()
		rect = CGRect(
		CGPoint(0, 0),
		CGSize(screen_size[0], screen_size[1]))
		skview = SKView.alloc().initWithFrame_(rect)
		# debug
		skview.showsFPS = self.debug
		skview.showsNodeCount = self.debug
		skview.showsPhysics = self.debug
		ObjCInstance(self).addSubview(skview)
		self.skview = skview
		scene = DemoScene.sceneWithSize_(rect.size)
		scene.backgroundColor = UIColor.color(red=0.2, green=0.5, blue=0.2, alpha=1.0)
		skview.presentScene_(scene)
		self.scene = scene
		
	def will_close(self):
		self.skview.paused = True
		
		
if __name__ == '__main__':
	view = DemoView()
	view.present(hide_title_bar=True)

