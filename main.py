import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.storage.jsonstore import JsonStore


import sys
import smtplib
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials


store = JsonStore('item_list.json')



class MainMenu(BoxLayout):
	pass

class ReceivingApp(App):
	pass


class ReceivingRoot(BoxLayout):
	def __init__(self, **kwargs):
		global store
		super(ReceivingRoot, self).__init__(**kwargs)
		store = JsonStore('item_list.json')

	def refresh_items(self):
		global item_list
		global store
		wks = authgoogle()
		item_list, masterlist = downloadrows(wks)
		store.clear()
		store.put('itemslist', items=masterlist)

	def items_test(self):
		global store
		print store['itemslist']




class New_Report(BoxLayout):
	pass


class Item_Scroller(ScrollView):
	def __init__(self, **kwargs):
		super(Item_Scroller, self).__init__(**kwargs)



class Item_List(GridLayout):
	
	def __init__(self, **kwargs):
		super(Item_List, self).__init__(**kwargs)
		self.add_button()
		self.bind(minimum_height=self.setter('height'))

	def item_search(self, search):
		self.clear_widgets()
		for key in store['itemslist']['items']:
			selector = (Item_Selector())
			if search in store['itemslist']['items'][key]:
				print 'hooray!'
				selector.label.text = store['itemslist']['items'][key]
				selector.id = 'code_%s' % key
				self.add_widget(selector)


	def add_button(self):
		global store
		self.clear_widgets()
		for key in store['itemslist']['items']:
			selector = (Item_Selector())
			selector.label.text = key + ':   ' + store['itemslist']['items'][key]
			selector.id = 'code_%s' % key
			self.add_widget(selector)

'''				btn = Button(
					text=store['itemslist']['items'][key],
					size_x=self.width, 
					size_y=40, 
					size_hint_y=None)
				self.add_widget(btn)
'''



class Tabs(TabbedPanel):
	pass


class Item_Selector(BoxLayout):
	pass

class Search_Bar(BoxLayout):
	search_input = ObjectProperty()


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
	uom_list = wks.col_values(2)[3:132]
	item_list = wks.col_values(3)[3:132]

	#build list of lists
	masterlist = {}

	for i in range(0, len(item_list)):
		masterlist[uom_list[i]] = item_list[i]
	print masterlist


	return item_list, masterlist





if __name__ == "__main__":
	ReceivingApp().run()