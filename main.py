import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

import sys
import smtplib
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

item_list = []
master_list = []



class MainMenu(BoxLayout):
	pass

class ReceivingApp(App):
	pass


class ReceivingRoot(BoxLayout):
	def new_report(self):
		global item_list
		self.clear_widgets()
		self.add_widget(New_Report())
		wks = authgoogle()
		item_list, masterlist = downloadrows(wks)




class New_Report(BoxLayout):
	pass


class Item_Scroller(ScrollView):
	def __init__(self, **kwargs):
		super(Item_Scroller, self).__init__(**kwargs)
		print 'New Report built'



class Item_List(GridLayout):
	
	def __init__(self, **kwargs):
		super(Item_List, self).__init__(**kwargs)
		self.bind(minimum_height=self.setter('height'))
		self.add_button()



	def add_button(self):
		print item_list
		for i in range(1, len(item_list)):
			btn = Button(
				text=item_list[i],
				size_x=self.width, 
				size_y=40, 
				size_hint_y=None)
			self.add_widget(btn)








def authgoogle():


	#connect to google
	scope = ['https://spreadsheets.google.com/feeds']

	credentials = ServiceAccountCredentials.from_json_keyfile_name('Receiving Reports-b234d394a35b.json', scope)

	gc = gspread.authorize(credentials)

	wks = gc.open("Item Codes").sheet1

	#test edit a cell
	wks.update_acell('F1', 'Python Edit Test Cell')

	return wks


def downloadrows(wks):

	#get length of lists
	'''TOTO'''


	#grab lists
	code_list = wks.col_values(2)[3:132]
	item_list = wks.col_values(3)[3:132]
	uoms_list = wks.col_values(4)[3:132]

	#build list of lists
	masterlist = []

	for i in range(0, len(code_list)):
		minilist = []
		minilist.append(code_list[i])
		minilist.append(item_list[i])
		minilist.append(uoms_list[i])
		masterlist.append(minilist)


	return item_list, masterlist





if __name__ == "__main__":
	ReceivingApp().run()