# coding: utf-8

# https://github.com/HeyItsJono/Pythonista

###############################################################################
# This is a self-extracting UI application package for Log Calculator.
# Run this script once to extract the packaged application.
# The files will be extracted to Log Calculator.py and Log Calculator.pyui.
# Make sure that these files do not exist yet.
# To update from an older version, move or delete the old files first.
# After extracting, the application can be found at Log Calculator.py.
# This bundle can be deleted after extraction.
###############################################################################
# Packaged using PackUI by dgelessus
# https://github.com/dgelessus/pythonista-scripts/blob/master/UI/PackUI.py
###############################################################################

import console, os.path

NAME     = "Log Calculator"
PYFILE   = """# coding: utf-8

import math
import ui
import clipboard
import decimal
from console import hud_alert

shows_result = False

def num(s):
	try:
		return int(s)
	except ValueError:
		return decimal.Decimal(s)

def button_tapped(sender):
	'@type sender: ui.Button'
	t = sender.title
	global shows_result
	
	labelmain = sender.superview['labelmain']
	labelbase = sender.superview['labelbase']
	segment = sender.superview['segmentedcontrol']
	
	if segment.selected_index == 0:
		if t in '0123456789':
			if shows_result or labelmain.text == '0':
				labelmain.text = t
				shows_result = False
			else:
				labelmain.text += t
		elif t == '.' and '.' not in labelmain.text:
			labelmain.text += t
		elif t == 'AC':
			labelmain.text = '0'
		elif t == 'C':
			labelmain.text = labelmain.text[:-1]
			if len(labelmain.text) < 1:
				labelmain.text = '0'
		elif t == 'e':
			labelmain.text = str(math.e)
		elif t == '+/-':
			if '-' in labelmain.text:
				labelmain.text = labelmain.text[1:]
			else:
				labelmain.text = '-' + labelmain.text
		elif t == '=':
			try:
				result = str(math.log(num(labelmain.text), num(labelbase.text)))
				labelmain.text = result
			except ValueError:
				try:
					result = str(math.log(num(labelmain.text), 10))
					labelmain.text = result
				except Exception as error:
					labelmain.text = str(error)
					print error
			shows_result = True
		elif t != '=':
			shows_result = False
	else:
		if t in '0123456789':
			if labelbase.text == '0':
				labelbase.text = t
			else:
				labelbase.text += t
		elif t == '.' and '.' not in labelbase.text:
			labelbase.text += t
		elif t == 'AC':
			labelbase.text = '0'
		elif t == 'C':
			labelbase.text = labelbase.text[:-1]
			if len(labelbase.text) < 1:
				labelbase.text = '0'
		elif t == 'e':
			labelbase.text = str(math.e)
		elif t == '+/-':
			if '-' in labelbase.text:
				labelbase.text = labelbase.text[1:]
			else:
				labelbase.text = '-' + labelbase.text
		elif t == '=':
			try:
				result = str(math.log(num(labelmain.text), num(labelbase.text)))
				labelmain.text = result
			except ValueError:
				try:
					result = str(math.log(num(labelmain.text), 10))
					labelmain.text = result
				except Exception as error:
					labelmain.text = str(error)
					print error
			shows_result = True
		elif t != '=':
			shows_result = False

def copy_action(sender):
	'@type sender: ui.Button'
	
	clipboard.set(sender.superview['labelmain'].text)
	hud_alert('Copied')

v = ui.load_view('Log Calculator')
if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('sheet')
else:
	# iPhone
	v.present(orientations=['portrait'])
"""
PYUIFILE = """[{"class":"View","attributes":{"tint_color":"RGBA(0.336735,0.664490,0.785714,1.000000)","enabled":true,"flex":"","name":"Log Calculator","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","background_color":"RGBA(1.000000,1.000000,1.000000,1.000000)","custom_class":""},"frame":"{{0, 0}, {540, 550}}","nodes":[{"class":"View","attributes":{"enabled":true,"flex":"","name":"view1","border_width":0,"alpha":1,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","background_color":"RGBA(0.928571,0.988572,1.000000,1.000000)","uuid":"212FFCAA-E549-46A5-B14D-EA6E04CA2B13"},"frame":"{{0, 47.5}, {540, 113.5}}","nodes":[]},{"class":"SegmentedControl","attributes":{"name":"segmentedcontrol","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","uuid":"51984562-5A99-4DCE-B43A-0BC901842F53","enabled":true,"segments":"Log|Base","flex":"LR"},"frame":"{{413, 169}, {120, 29}}","nodes":[]},{"class":"Label","attributes":{"font_size":30,"enabled":true,"text":"0","flex":"","name":"labelmain","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"right","uuid":"11A6CC65-8626-431D-A0C3-6BE227D3BAB2"},"frame":"{{56, 84}, {478, 77}}","nodes":[]},{"class":"Button","attributes":{"font_size":30,"enabled":true,"flex":"","font_bold":false,"name":"button7","uuid":"C9C89B89-7EAB-40DE-B76F-84BF793F813A","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"title":"7"},"frame":"{{6, 206.5}, {100.5, 78.5}}","nodes":[]},{"class":"Label","attributes":{"font_size":15,"enabled":true,"text":"0","flex":"","name":"labelbase","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"right","uuid":"FAD0321E-49BC-4079-A781-8DB39D2505B7"},"frame":"{{434, 47.5}, {100, 38}}","nodes":[]},{"class":"Label","attributes":{"font_size":16,"enabled":true,"text":"Base:","font_name":"AvenirNext-Italic","name":"labelbasetext","flex":"","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"right","uuid":"133DE789-67BF-4383-968C-81BE84354DD6"},"frame":"{{336, 47}, {100, 38}}","nodes":[]},{"class":"Button","attributes":{"font_size":30,"enabled":true,"flex":"","font_bold":false,"name":"button8","uuid":"F705EA86-58FC-4A64-AC35-C8CFC9EA97B1","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"title":"8"},"frame":"{{114.5, 206}, {100.5, 78.5}}","nodes":[]},{"class":"Button","attributes":{"font_size":30,"enabled":true,"flex":"","font_bold":false,"name":"button9","uuid":"26B5604E-8A2B-4DD9-899E-5752375F1A90","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"title":"9"},"frame":"{{223, 206}, {100.5, 78.5}}","nodes":[]},{"class":"Button","attributes":{"font_size":30,"enabled":true,"flex":"","font_bold":false,"name":"button4","uuid":"4F921C7D-A2E5-4995-9C2E-46C9D883198D","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"title":"4"},"frame":"{{6, 293}, {100.5, 78.5}}","nodes":[]},{"class":"Button","attributes":{"font_size":30,"enabled":true,"flex":"","font_bold":false,"name":"button1","uuid":"5214FDA5-AFE5-44D4-B173-1E1C6B3756FE","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"title":"1"},"frame":"{{6, 379.5}, {100.5, 78.5}}","nodes":[]},{"class":"Button","attributes":{"font_size":30,"enabled":true,"flex":"","font_bold":false,"name":"buttonpoint","uuid":"95B3C7DF-DD43-4D83-B9CA-13962747D6B5","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"title":"."},"frame":"{{6, 466}, {100.5, 78.5}}","nodes":[]},{"class":"Button","attributes":{"font_size":30,"enabled":true,"flex":"","font_bold":false,"name":"button5","uuid":"1E8A505B-B6E1-4F6A-8FBA-529FF161EB3E","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"title":"5"},"frame":"{{114.5, 293}, {100.5, 78.5}}","nodes":[]},{"class":"Button","attributes":{"font_size":30,"enabled":true,"flex":"","font_bold":false,"name":"button2","uuid":"30ABFA93-22AC-4E40-871F-BAB651B5BDAC","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"title":"2"},"frame":"{{114, 379.5}, {100.5, 78.5}}","nodes":[]},{"class":"Button","attributes":{"font_size":30,"enabled":true,"flex":"","font_bold":false,"name":"button0","uuid":"96FCBC56-14FC-4BBD-93F8-B641F698DAB0","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"title":"0"},"frame":"{{114, 466}, {100.5, 78.5}}","nodes":[]},{"class":"Button","attributes":{"font_size":30,"enabled":true,"flex":"","font_bold":false,"name":"button6","uuid":"3190246D-412A-4E1A-BB63-CEC811D1A0C0","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"title":"6"},"frame":"{{223, 292.5}, {100.5, 78.5}}","nodes":[]},{"class":"Button","attributes":{"font_size":30,"enabled":true,"flex":"","font_bold":false,"name":"button3","uuid":"8B01CE73-AE63-4A81-9360-C8F4871F6136","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"title":"3"},"frame":"{{222.5, 379}, {100.5, 78.5}}","nodes":[]},{"class":"Button","attributes":{"font_size":30,"enabled":true,"flex":"","font_bold":false,"name":"buttone","uuid":"B9192F29-44D4-4862-91CD-4F4CB8879EDA","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"title":"e"},"frame":"{{223, 465.5}, {100.5, 78.5}}","nodes":[]},{"class":"Button","attributes":{"tint_color":"RGBA(0.857143,0.338571,0.183673,1.000000)","font_size":30,"enabled":true,"font_bold":false,"name":"buttonAC","flex":"","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"uuid":"85677B20-A8E3-47EC-8170-6059BEEDFED1","title":"AC"},"frame":"{{331, 206.5}, {203, 78.5}}","nodes":[]},{"class":"Button","attributes":{"tint_color":"RGBA(0.857143,0.336379,0.183673,1.000000)","font_size":30,"enabled":true,"font_bold":false,"name":"buttonC","flex":"","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"uuid":"B241C103-DE0E-47CC-A4CE-14C631DE3E59","title":"C"},"frame":"{{331.5, 293}, {202.5, 78.5}}","nodes":[]},{"class":"Button","attributes":{"tint_color":"RGBA(0.857143,0.336379,0.183673,1.000000)","font_size":30,"enabled":true,"font_bold":false,"name":"buttonequals","flex":"","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"uuid":"A703F129-B162-468D-B32D-BF95E04A0680","title":"="},"frame":"{{331, 466}, {203, 78.5}}","nodes":[]},{"class":"Label","attributes":{"font_size":25,"enabled":true,"text":"Log Calculator","font_name":"STHeitiSC-Light","name":"labeltitle","flex":"","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"center","uuid":"25071C91-2EF5-4149-A852-FC4CA09EC1AB"},"frame":"{{174, 6}, {198, 32}}","nodes":[]},{"class":"Label","attributes":{"font_size":12,"enabled":true,"text":"Note: Base 0 is treated as Base 10 since Base 0 does not exist.","font_name":"Avenir-LightOblique","name":"label1","flex":"","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"left","uuid":"25B8ABCD-CE3A-4A5A-AAAF-9B0CE95E4917"},"frame":"{{6, 169}, {380, 29.5}}","nodes":[]},{"class":"Button","attributes":{"font_size":15,"enabled":true,"flex":"","font_bold":false,"name":"button10","uuid":"260B9996-E36C-43AB-9554-1E4599C3E67F","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"copy_action","image_name":"ionicons-clipboard-32","title":""},"frame":"{{6, 104}, {50, 57}}","nodes":[]},{"class":"Button","attributes":{"tint_color":"RGBA(0.857143,0.336379,0.183673,1.000000)","font_size":30,"enabled":true,"font_bold":false,"name":"buttonposneg","flex":"","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","action":"button_tapped","border_width":1,"uuid":"5E735020-A380-4562-A270-1957EB2D34F7","title":"+\\/-"},"frame":"{{330, 379}, {203, 78.5}}","nodes":[]}]}]"""

def fix_quotes_out(s):
    return s.replace("\\\"\\\"\\\"", "\"\"\"").replace("\\\\", "\\")

def main():
    if os.path.exists(NAME + ".py"):
        console.alert("Failed to Extract", NAME + ".py already exists.")
        return
    
    if os.path.exists(NAME + ".pyui"):
        console.alert("Failed to Extract", NAME + ".pyui already exists.")
        return
    
    with open(NAME + ".py", "w") as f:
        f.write(fix_quotes_out(PYFILE))
    
    with open(NAME + ".pyui", "w") as f:
        f.write(fix_quotes_out(PYUIFILE))
    
    msg = NAME + ".py and " + NAME + ".pyui were successfully extracted!"
    console.alert("Extraction Successful", msg, "OK", hide_cancel_button=True)
    
if __name__ == "__main__":
    main()