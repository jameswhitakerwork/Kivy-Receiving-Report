import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.storage.jsonstore import JsonStore
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.bubble import Bubble
from kivy.animation import Animation, AnimationTransition
from kivy.uix.screenmanager import ScreenManager, Screen

from functools import partial
from kivy.clock import Clock
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


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
		popup = Popup(content=content, title=title, auto_dismiss=False, size_hint=(0.5, 0.5))

		# bind the on_press event of the button to the dismiss function
		content.bind(on_press=popup.dismiss)

		# open the popup
		popup.open()

	def submit_report(self):
		self.clear_widgets()
		reportpopup = Submit_Report_Popup()
		self.add_widget(reportpopup)

	def create_report(self, date, location, person):
		print date
		print location

		report = open('report.csv', 'w')
		report.write('Date, Location, Code, Item, Amount, UoM, \n')
		for entry in currentreport:
			itemname, itemuom = lookup(entry[0])
			itemname = itemname.replace(',', '')
			report.write('%s, %s, %s, %s,  %s, %s, \n' % (date, location, str(entry[0]), itemname, entry[1], itemuom))

		report.close()



		fromaddr = "jameswhitakerwork@gmail.com"
		toaddr = "jameswhitakerwork@gmail.com"
		 
		msg = MIMEMultipart()
		 
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = "New Receiving Report"
		 
		body = "A new receiving report has been created by %s and attached to this email." % person
		 
		msg.attach(MIMEText(body, 'plain'))
		 
		filename = "report.csv"
		attachment = open('report.csv', 'rb')
		 
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		 
		msg.attach(part)
		 
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, "CookieTable!1")
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()

		self.popup('Report Submitted', 'You\'ve submitted the report successfully')


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
				selector.label.text =  key + ':   ' + store['itemslist']['items'][key][0] + "  " + store['itemslist']['items'][key][1] + ")"
				selector.id = key
				self.add_widget(selector)


	def add_button(self):
		global store
		self.clear_widgets()
		for key in store['itemslist']['items']:
			selector = (Item_Selector())
			selector.label.text = key + ':   ' + store['itemslist']['items'][key][0] + " (" + store['itemslist']['items'][key][1] + ")"
			selector.id = key
			self.add_widget(selector)


	def add_item(self, itemid, amount):
		if int(amount) > 0:
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
		else:
			pass



class Item_Slider(Slider):
	secretvalue = NumericProperty()





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
		global lookup_table
		self.clear_widgets()
		for entry in currentreport:

			newselector = Current_Selector()
			name, uom = lookup(entry[0])
			newselector.label.text = '%s:    %i (%s)' % (name, entry[1], uom)
			newselector.code = entry[0]
			self.add_widget(newselector)





class Current_Selector(BoxLayout):

	def __init__(self, **kwargs):
		super(Current_Selector, self).__init__(**kwargs)
		self.code = StringProperty()

	def remove_item_on_delete(self):
		for entry in currentreport:
			if entry[0] == self.code:
				currentreport.remove(entry)


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


class Add_Button(Button):
	def change_colour(self, widgetid):
		self.anim = Animation(background_color=(0,1,0,1), size_hint_x = 0.2, t='out_circ', duration=0.2) + Animation(duration=0.5) + Animation(background_color=(0,1,0,0.5), size_hint_x = 0.1, t='out_circ')
		self.anim.start(self)
		self.text = 'Added!'
		print 'animation fired'

class Submit_Report_Popup(BoxLayout):
	pass


class Screen_Manager(ScreenManager):
	pass

class Report_Screen(Screen):
	pass

class Submit_Screen(Screen):
	pass





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
		masterlist[code_list[i]] = [item_list[i], uom_list[i]]
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

def lookup(key):
	for entry in lookup_table:
		if key == entry[0]:
			return entry[1][0], entry[1][1]

def limit_to_100(value):
	try:
		value = int(value)
		if value >= 100:
			value = 100
		return value
	except:
		return 0

def maybe_clear(widget, string):
	if int(string) == 0:
		widget.text = ""
	else:
		return string

if __name__ == "__main__":
	lookup_table = make_lookup_table()
	ReceivingApp().run()