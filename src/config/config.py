# when the system starts, load all the configuration
import xml.etree.ElementTree as ET

"""
	@author zhb

	this class contains the information which is saved in the
	configuration file.
	key: developer's application key
	uname: store the account user name
	upass: store the account user passwd
	access_token: authority to retrieve netdisk data
	sync_path_data: a list of {name, localpath, remotepath}

	One Important Thing:
		There should only be one instance ConfigImpl object, 
		So I wrapped it into the Config object.

	Once you import this module, you can use:
		config = Config.get_config()
	to get this instance.
"""
class ConfigImpl:

	# parse the configuration file
	def __init__(self):
		self.path = "bdyun.conf"
		self.doctree = ET.parse(self.path)
		self.root = self.doctree.getroot()

	def get_app_key(self):
		return self.root.find("dev").find("key").text

	def get_uname(self):
		return self.root.find("user").find("name").text

	def get_upass(self):
		return self.root.find("user").find("pass").text

	def get_access_token(self):
		return self.root.find("user").find("token").text

	def get_accept(self):
		return self.root.find("user").find("accept").text

	def get_sync_path_data(self):
		items = self.root.find("sync").findall("item")
		self.sync_path_data = []
		for item in items:
			self.sync_path_data.append({"name": item.attrib["name"],
				"local": item.attrib["local"], 
				"remote": item.attrib["remote"]})
		return self.sync_path_data

	def set_uname(self, name):
		self.root.find("user").find("name").text = name
		self.write_back()

	def set_upass(self, passwd):
		self.root.find("user").find("pass").text = passwd
		self.write_back()

	def set_token(self, token):
		self.root.find("user").find("token").text = token
		self.write_back()

	def set_accept(self, accept):
		self.root.find("user").find("accept").text = accept
		self.write_back()

	# manipulate the sync path data set
	# if the name already exist, just override this item
	def add_sync_path(self, name, local, remote):
		for item in self.root.find("sync").findall("item"):
			if item.attrib["name"] == name:
				item.attrib["local"] = local
				item.attrib["remote"] = remote
				self.write_back()

	# delete an entry in this item list
	def delete_sync_path(self, name):
		for item in self.root.find("sync").findall("item"):
			if item.attrib["name"] == name:
				self.root.find("sync").remove(item)
				self.write_back()
				break

	# write the path back to the configuration file
	def write_back(self):
		self.doctree.write(self.path)

# implement the single instance of ConfigImpl object
class Config:
	__config = ConfigImpl()

	@staticmethod
	def get_config():
		return Config.__config

	# Another implementation
	# @classmethod
	# def get_config(cls):
	#	return cls.__config
	

if __name__ == "__main__":
	config = Config.get_config()
	array = config.get_sync_path_data()
	for item in array:
		print("Name:", item["name"], "Local:", item["local"],
			"Remote:", item["remote"])

	# now let's midofy the home directory to be `root`
	config.add_sync_path("docs", "/root/Document", "Document")
	config.delete_sync_path("video")
