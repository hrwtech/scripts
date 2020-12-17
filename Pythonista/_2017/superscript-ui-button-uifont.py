# https://forum.omz-software.com/topic/4223/superscript-text-in-ui-button/6

import ui
from objc_util import *

class MyView(ui.View):
	def did_load(self):
		x_pow_y_button = self['x_pow_y_button']
		
		NSMutableAttributedString = ObjCClass('NSMutableAttributedString')
		attributed_string = NSMutableAttributedString.alloc().initWithString_(ns('xy'))
		range = NSRange(1, 1)
		
		UIFont = ObjCClass('UIFont')
		
		attributes = {
		ns('NSFont'): UIFont.systemFontOfSize(11),
		ns('NSBaselineOffset'): ns(5)
		}
		
		attributed_string.setAttributes_range_(attributes, range)
		
		x_pow_y_button_objc = ObjCInstance(x_pow_y_button)
		UIButton = ObjCClass('UIButton')
		for subview in x_pow_y_button_objc.subviews():
			if subview.isKindOfClass(UIButton):
				subview.setAttributedTitle_forState_(attributed_string, 0)
				
				
v = ui.load_view()
v.present('sheet')

