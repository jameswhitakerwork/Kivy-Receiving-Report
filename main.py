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
from kivy.uix.popup import Popup


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
		self.currentreport = []

	def refresh_items(self):
		global item_list
		global store
		try:
			wks = authgoogle()
			print 'wks assigned'
			item_list, masterlist = downloadrows(wks)
			print 'downloadrows done'
			store.clear()
			store.put('itemslist', items=masterlist)
			self.popup('Success', 'Items refreshed!')
		except:
			self.popup('Failed', 'Please try again')

	def items_test(self):
		global store
		print store['itemslist']

	def popup(self, title, message):
		# create content and add to the popup
		content = Button(text=message)
		popup = Popup(content=content, title=title, auto_dismiss=False)

		# bind the on_press event of the button to the dismiss function
		content.bind(on_press=popup.dismiss)

		# open the popup
		popup.open()


class Add_Items_Tab(BoxLayout):
	pass


class Item_Scroller(ScrollView):
	def __init__(self, **kwargs):
		super(Item_Scroller, self).__init__(**kwargs)



class Item_List(GridLayout):
	global store

	
	def __init__(self, **kwargs):
		super(Item_List, self).__init__(**kwargs)
		self.add_button()
		self.bind(minimum_height=self.setter('height'))
		self.currentreport = []

	def item_search(self, search):
		self.clear_widgets()
		for key in store['itemslist']['items']:
			selector = (Item_Selector())
			if (
				search.lower() in store['itemslist']['items'][key].lower()
				or
				search in key
				):
				selector.label.text =  key + ':   ' + store['itemslist']['items'][key]
				selector.id = 'code_%s' % key
				self.add_widget(selector)


	def add_button(self):
		global store
		self.clear_widgets()
		for key in store['itemslist']['items']:
			selector = (Item_Selector())
			selector.label.text = key + ':   ' + store['itemslist']['items'][key]
			selector.id = 'XXX%s' % key
			self.add_widget(selector)


	def add_item(self, itemid, amount):
		global store
		itemid = itemid[4:]
		print itemid, amount
		entry = (itemid, int(amount))
		self.currentreport.append(entry)
		print self.currentreport


class Current_List_Tab(BoxLayout):
	pass

class Current_Scroller(ScrollView):
	pass

class Current_List(GridLayout):
	def __init__(self, **kwargs):
		super(Current_List, self).__init__(**kwargs)
		self.bind(minimum_height=self.setter('height'))
		self.currentreport = []

class Current_Selector(BoxLayout):
	pass

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
	print 'code grabbed'
	item_list = wks.col_values(3)[3:132]
	print 'items grabbed'
	#build list of lists
	masterlist = {}

	for i in range(0, len(item_list)):
		masterlist[uom_list[i]] = item_list[i]
#	print masterlist
	print 'items joined'

	return item_list, masterlist





if __name__ == "__main__":
	ReceivingApp().run()