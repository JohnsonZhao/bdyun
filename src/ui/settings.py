from gi.repository import Gtk
import sys
from config.config import Config

class SettingsDialog(Gtk.Dialog):

	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "Settings", parent, 0, 
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_APPLY, Gtk.ResponseType.OK))
		self.set_default_size(200, 400)
		self.config = Config.get_config()
		self.__add_widget()
		self.show_all()

	def __on_modify_clicked(self, widget):
		# set the password entry to be editable
		print("Modify")

	def __on_generate_clicked(self, widget):
		# regenerate the access tokens
		print("Generate")

	def __on_save_clicked(self, widget):
		# save the uname, upass, and access token
		print("Save")

	def __on_add_clicked(self, widget):
		# append a new row in the treeview, and make it editable
		print("Add")

	def __on_delete_clicked(self, widget):
		# delete the selected row, refresh the treeview
		print("Delete")

	def __on_edit__clicked(self, widget):
		# make the selected item ba editable
		print("Edit")

	def  __add_widget(self):
		box = self.get_content_area()

		# divide to be two parts, left side for sync settings, and the right
		# part for account settings
		# so 1 * 2 table, and homogeneous, the same size each column
		table = Gtk.Table(2, 1, True)
		box.add(table)

		# now for the sync folder setting, we also choose table layout
		# the label(1), sync_folder_data(4), controls(1)
		# columns: name(1), local path(2), remote path(2) 
		sync_folder_table = Gtk.Table(5, 5, True)
		sync_folder_table.set_row_spacings(5)
		table.attach(sync_folder_table, 0, 1, 0, 1)
		# the label `Sync Folder Settings`
		label = Gtk.Label()
		label.set_markup("<b>Sync Folder Settings</b>")
		# takes up one row, two columns
		sync_folder_table.attach(label, 1, 4, 0, 1, xpadding=5)
		# the treeview
		# Initialize the liststore(name, localpath, remotepath)
		self.liststore = Gtk.ListStore(str, str, str)
		sync_folder_data = self.config.get_sync_path_data()
		for data in sync_folder_data:
			self.liststore.append([data["name"], data["local"], 
				data["remote"]])
		self.treeview = Gtk.TreeView(model=self.liststore)
		# add the header data
		# the name column
		render_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Name", render_text, text=0)
		self.treeview.append_column(column_text)
		# the local path column
		column_text = Gtk.TreeViewColumn("Local Path", render_text, text=1)
		self.treeview.append_column(column_text)
		# the remote path column
		column_text = Gtk.TreeViewColumn("Remote Path", render_text, text=2)
		self.treeview.append_column(column_text)
		# add the tree view to the sync_folder_table
		sync_folder_table.attach(self.treeview, 0, 5, 1, 4, xpadding=5)
		# now the edit controls
		add = Gtk.Button(label="Add")
		add.connect("clicked", self.__on_add_clicked)
		sync_folder_table.attach(add, 2, 3, 4, 5, xpadding=5)
		edit = Gtk.Button(label="Edit")
		edit.connect("clicked", self.__on_edit__clicked)
		sync_folder_table.attach(edit, 3, 4, 4, 5, xpadding=5)
		delete = Gtk.Button(label="Delete")
		delete.connect("clicked", self.__on_delete_clicked)
		sync_folder_table.attach(delete, 4, 5, 4, 5,xpadding=5)
		# then the account settings
		# five rows:(label, uname, upass, token, save)
		# four columns(label, entry, edit)
		"""
		+++++++++++++++++++++++++++++++++++++++++++++++++++
		+				Account Settings 				     +
		+++++++++++++++++++++++++++++++++++++++++++++++++++
		+   UserName:    +				Entry				     +
		+++++++++++++++++++++++++++++++++++++++++++++++++++
		+   Password:	   +			Entry			    +	 Modify     +
		+++++++++++++++++++++++++++++++++++++++++++++++++++
		+ Access Token: +			Entry			    +    Generate    +
		+++++++++++++++++++++++++++++++++++++++++++++++++++
		+								    +	Save         +
		+++++++++++++++++++++++++++++++++++++++++++++++++++
		"""
		account_table = Gtk.Table(5, 4, True)
		account_table.set_row_spacings(5)
		table.attach(account_table, 0, 1, 1, 2)
		# the title label
		label = Gtk.Label()
		label.set_markup("<b>Account Settings</b>")
		account_table.attach(label, 1, 3, 0, 1, xpadding=5)
		# the user name row
		label = Gtk.Label("UserName:")
		account_table.attach(label, 0, 1, 1, 2, xpadding=5)
		self.name_entry = Gtk.Entry()
		account_table.attach(self.name_entry, 1, 4, 1, 2, xpadding=5)
		# the user passwd row
		label = Gtk.Label("Password:")
		account_table.attach(label, 0, 1, 2, 3, xpadding=5)
		self.passwd_entry = Gtk.Entry()
		account_table.attach(self.passwd_entry, 1, 3, 2, 3, xpadding=5)
		modify = Gtk.Button(label="Modify")
		modify.connect("clicked", self.__on_modify_clicked)
		account_table.attach(modify, 3, 4, 2, 3, xpadding=5)
		# the token row
		label = Gtk.Label("Access Token")
		account_table.attach(label, 0, 1, 3, 4, xpadding=5)
		self.token_entry = Gtk.Entry()
		account_table.attach(self.token_entry, 1, 3, 3, 4, xpadding=5)
		gen = Gtk.Button("Generate")
		gen.connect("clicked", self.__on_generate_clicked)
		account_table.attach(gen, 3, 4, 3, 4, xpadding=5)
		# the save control
		save = Gtk.Button(label="Save")
		account_table.attach(save, 3, 4, 4, 5, xpadding=5)
		save.connect("clicked", self.__on_save_clicked)