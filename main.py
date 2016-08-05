import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from functools import partial
from kivy.clock import Clock


import sys
import smtplib
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials


store = JsonStore('item_list.json')
currentreport = []






class MainMenu(BoxLayout):
	pass

class ReceivingApp(App):
	pass


class ReceivingRoot(BoxLayout):
	def __init__(self, **kwargs):
		global store, lookup_table
		super(ReceivingRoot, self).__init__(**kwargs)

	def refresh_items(self):
		global item_list
		global store, lookuptable
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
		lookup_table = make_lookup_table()


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
	global currentreport

	
	def __init__(self, **kwargs):
		super(Item_List, self).__init__(**kwargs)
		self.add_button()
		self.bind(minimum_height=self.setter('height'))


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
				selector.id = key
				self.add_widget(selector)


	def add_button(self):
		global store
		self.clear_widgets()
		for key in store['itemslist']['items']:
			selector = (Item_Selector())
			selector.label.text = key + ':   ' + store['itemslist']['items'][key]
			selector.id = key
			self.add_widget(selector)


	def add_item(self, itemid, amount):
		global store
		global currentreport
		itemid = int(itemid)
		entry = [itemid, int(amount)]
		print 'adding item code %i, amount: %s' % (itemid, amount)
		item_exists = 0
		for i in range(0, len(currentreport)):
			if entry[0] == currentreport[i][0]:
				print entry[0]
				print currentreport[i][0]
				print 'Item already exists in current report'
				print 'prev amount: ' + str(currentreport[i][1])
				currentreport[i][1] += int(amount)
				print 'new amount: ' + str(currentreport[i][1])
				item_exists = 1
		if item_exists == 0:
				print 'New item added to current report'
				currentreport.append(entry)


		print currentreport





class Current_List_Tab(BoxLayout):
	def test(self):
		print 'test'

class Current_Scroller(ScrollView):
	pass


class Current_List(GridLayout):

	def __init__(self, **kwargs):
		super(Current_List, self).__init__(**kwargs)
		self.bind(minimum_height=self.setter('height'))
		Clock.schedule_interval(self.refreshcurrentitems, 1)

	def refreshcurrentitems(self, dt):
		self.clear_widgets()
		for entry in currentreport:
			newselector = Current_Selector()
			newselector.label.text = '%i %i' % (entry[0], entry[1])
			newselector.code = entry[0]
			self.add_widget(newselector)





class Current_Selector(BoxLayout):
	pass

class Tabs(TabbedPanel):
	def __init__(self, **kwargs):
		super(Tabs, self).__init__(**kwargs)
		self.bind(current_tab=self.content_changed_cb)

	def content_changed_cb(self, obj, value):
		print 'Tab changed (callback)'


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
	code_list = wks.col_values(2)[3:132]
	print 'code grabbed'
	item_list = wks.col_values(3)[3:132]
	print 'items grabbed'
	uom_list = wks.col_values(4)[3:132]
	#build list of lists
	masterlist = {}

	for i in range(0, len(item_list)):
		masterlist[code_list[i]] = item_list[i]
#	print masterlist
	print 'items joined'
	print masterlist
	return item_list, masterlist


def make_lookup_table():
	lookup_table = []
	for key in store['itemslist']['items']:
		lookup_table.append([int(key), store['itemslist']['items'][key]])
	print lookup_table
	return lookup_table



if __name__ == "__main__":
	lookup_table = make_lookup_table()
	ReceivingApp().run()