import argparse
import os
import configparser
import cmd
import requests
import sqlite3
import subprocess
import time
import shutil
import sys
import getpass

sys.stdout.flush()

# argument parser - begin
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-s", "--setup", help = "create required directories and " 
	"files. you don't need to use this option if you have run the installation script",
	action = "store_true")
args = argument_parser.parse_args()
# argument parser - end

MAIN_DIRECTORY = os.path.expanduser("~/.note0")
CONFIG_FILE = MAIN_DIRECTORY + "/drive/config.ini"
DEFAULT_URL = "http://localhost:3000"
config_parser = configparser.ConfigParser()

# custom shell - begin
class Note0Shell(cmd.Cmd):
	
	intro = "\nWelcome to note0\n"
	prompt = "\x1b[0;30;47m" + " note0> " + "\x1b[0m" + " "

	def do_create_account(self, args):
		"\nUse this command to create a note0 account which is required to make use of the sync facility\n"
		config_parser.read(CONFIG_FILE)
		url = config_parser["options"]["url"]
		email = input("\nGoogle account email: ")
		while email == "":
			email = input("Email cannot be empty. Please re-enter email: ")
		password = get_password(option = "create_account", is_logged_in = None)
		try:
			req_content = { "email" : email }
			# verbose
			print("Sending request to server..(to get authentication url)")
			r = requests.post(url + "/v1/drive/accounts/register", json = req_content)
		except requests.exceptions.ConnectionError as err:
			print("Connection error: " + str(err), flush = True)
			print("Account creation unsuccessful. Please try again later\n")
			return False
		except requests.exceptions.HTTPError as err:
			print("HTTP Request returned an unsuccessful status code: " + str(err), flush = True)
			print("Account creation unsuccessful. Please try again later\n")
			return False
		except requests.exceptions.TooManyRedirects as err:
			print("Too many redirects: " + str(err), flush = True)	
			print("Account creation unsuccessful. Please try again later\n")
			return False
		except requests.exceptions.Timeout as err:
			print("Request timed out: " + str(err), flush = True)
			print("Account creation unsuccessful. Please try again later\n")
			return False
		r_json = r.json()
		if r_json["status"] == 2:
			print("Error on the server while creating account. Please try again later\n", flush = True)
		elif r_json["status"] == 1:
			print("Email already registered\n")
		else:
			print("Please open the link given below in a web browser and paste the code that you obtain, below\n"
				  + r_json["auth_url"])
			code = input("Code: ")
			try:
				req_content = { "email" : email, "password" : password, "code" : code }
				# verbose
				print("Sending request to server..(to create an account)")
				r = requests.post(url + "/v1/drive/accounts/register", json = req_content)
			except requests.exceptions.ConnectionError as err:
				print("Connection error: " + str(err), flush = True)
				print("Account creation unsuccessful. Please try again later\n")
				return False
			except requests.exceptions.HTTPError as err:
				print("HTTP Request returned an unsuccessful status code: " + str(err), flush = True)
				print("Account creation unsuccessful. Please try again later\n")
				return False
			except requests.exceptions.TooManyRedirects as err:
				print("Too many redirects: " + str(err), flush = True)	
				print("Account creation unsuccessful. Please try again later\n")
				return False
			except requests.exceptions.Timeout as err:
				print("Request timed out: " + str(err), flush = True)
				print("Account creation unsuccessful. Please try again later\n")
				return False
			r_json = r.json()
			if r_json["status"] == 3:
				print("Error while retrieving access token. Account creation unsuccessful. Please try again later\n", flush = True)
			elif r_json["status"] == 2:
				print("Error on server while processing request. Account creation unsuccessful. Please try again later\n", flush = True)
			elif r_json["status"] == 4:
				print("Error while creating a folder in your drive. Account creation unsuccessful. Please try again later\n", flush = True)
			elif r_json["status"] == 5:
				print("Error on server while processing request. Account creation unsuccessful. Delete the folder named 'note0' in your drive and try again later\n", flush = True)
			elif r_json["status"] == 0:
				print("Registration Successful\n")
			else:
				print("Unexpected response from server\n")

	def do_delete_account(self, args):
		"\nUse this command to delete your note0 account\n"
		config_parser.read(CONFIG_FILE)
		url = config_parser["options"]["url"]
		print("\nTo delete an account you must not have any logged in sessions for that account\n"
			  "Please enter the credentials of the account that you want to delete")
		email = input("Email: ")
		while email == "":
			email = input("Email cannot be empty. Please re-enter email: ")
		password = get_password(option = "delete_account", is_logged_in = None)
		confirm = input("Are you sure you want to delete this account (y/n)?: ")
		if confirm == "y":
			try:
				req_content = { "email" : email, "password" : password } 
				# verbose
				print("Sending request to server..(to delete account)")
				r = requests.post(url + "/v1/drive/accounts/delete_account", json = req_content)
			except requests.exceptions.ConnectionError as err:
				print("Connection error: " + str(err), flush = True)
				print("Account deletion unsuccessful. Please try again later\n")
				return False
			except requests.exceptions.HTTPError as err:
				print("HTTP Request returned an unsuccessful status code: " + str(err), flush = True)
				print("Account deletion unsuccessful. Please try again later\n")
				return False
			except requests.exceptions.TooManyRedirects as err:
				print("Too many redirects: " + str(err), flush = True)	
				print("Account deletion unsuccessful. Please try again later\n")
				return False
			except requests.exceptions.Timeout as err:
				print("Request timed out: " + str(err), flush = True)
				print("Account deletion unsuccessful. Please try again later\n")
				return False
			r_json = r.json()
			if r_json["status"] == 2:
				print("Error on server while processing request. Account deletion unsuccessful. Please try again later\n")
			elif r_json["status"] == 3:
				print("Email not registered\n")
			elif r_json["status"] == 1:
				print("Incorrect password\n")
			elif r_json["status"] == 4:
				print("Atleast one logged in session exists. To delete an account you must not have any logged in sessions for that account\n")
			elif r_json["status"] == 0:
				print("Account deleted successfully\n")
			else:
				print("Unexpected response from server\n")
		elif confirm == "n":
			print("Process cancelled\n")
		else:
			print("Invalid input\n")	

	def do_change_password(self, args):
		"\nUse this command to change the password for your note0 account\n"
		config_parser.read(CONFIG_FILE)
		url = config_parser["options"]["url"]
		if config_parser["session"]["email"] == "none":
			print("\nPlease enter the credentials of the account whose password you want to change")
			email = input("Email: ")
			while email == "":
				email = input("Email cannot be empty, re-enter email: ")
			passwords = get_password(option = "change_password", is_logged_in = False)
			password = passwords[0]
			new_password = passwords[1]
			try:
				req_content = { "email" : email, "password" : password, "new_password" : new_password }
				# verbose
				print("Sending request to server..(to change password)")
				r = requests.post(url + "/v1/drive/accounts/change_password", json = req_content)
			except requests.exceptions.ConnectionError as err:
				print("Connection error: " + str(err), flush = True)
				print("Password change unsuccessful\n")
				return False
			except requests.exceptions.HTTPError as err:
				print("HTTP Request returned an unsuccessful status code: " + str(err), flush = True)
				print("Password change unsuccessful\n")
				return False
			except requests.exceptions.TooManyRedirects as err:
				print("Too many redirects: " + str(err), flush = True)
				print("Password change unsuccessful\n")	
				return False
			except requests.exceptions.Timeout as err:
				print("Request timed out: " + str(err), flush = True)
				print("Password change unsuccessful\n")
				return False
			r_json = r.json()
			if r_json["status"] == 2:
				print("Error on server while processing request. Password change unsuccessful. Please try again later\n")
			elif r_json["status"] == 3:
				print("Email not registered\n")
			elif r_json["status"] == 1:
				print("Incorrect password\n")
			elif r_json["status"] == 0:
				print("Password changed successfully\n")
			else:
				print("Unexpected response from server\n")
		else:
			passwords = get_password(option = "change_password", is_logged_in = True)
			email = config_parser["session"]["email"]
			skey = config_parser["session"]["skey"]
			tkey = config_parser["session"]["tkey"]
			try:
				req_content = { "email" : email, "skey" : skey, "tkey" : tkey, "new_password" : passwords[0] }
				# verbose
				print("Sending request to server..(to change password)")
				r = requests.post(url + "/v1/drive/accounts/change_password", json = req_content)
			except requests.exceptions.ConnectionError as err:
				print("Connection error: " + str(err), flush = True)
				print("Password change unsuccessful\n")
				return False
			except requests.exceptions.HTTPError as err:
				print("HTTP Request returned an unsuccessful status code: " + str(err), flush = True)
				print("Password change unsuccessful\n")
				return False
			except requests.exceptions.TooManyRedirects as err:
				print("Too many redirects: " + str(err), flush = True)	
				print("Password change unsuccessful\n")
				return False
			except requests.exceptions.Timeout as err:
				print("Request timed out: " + str(err), flush = True)
				print("Password change unsuccessful\n")
				return False
			r_json = r.json()
			if r_json["status"] == 2:
				print("Error on server while processing request. Password change unsuccessful. Please try again later\n")
			elif r_json["status"] == 3:
				print("Email not registered\n")
			elif r_json["status"] == 1:
				print("Incorrect password\n")
			elif r_json["status"] == 4:
				print("Invalid login credentials. You may not be logged in\n")
			elif r_json["status"] == 0:
				print("Password changed successfully\n")
			else:
				print("Unexpected response from server\n")

	def do_login(self, args):
		"\nUse this command to login to your note0 account\n"
		config_parser.read(CONFIG_FILE)
		url = config_parser["options"]["url"]
		if config_parser["session"]["email"] != "none":
			print("\nYou are already logged in as " + config_parser["session"]["email"] + "\n")
		else:
			email = input("\nGoogle account email: ")
			while email == "":
				email = input("Email cannot be empty. Please re-enter email: ")
			password = get_password(option = "login", is_logged_in = None)
			try:
				req_content = { "email" : email, "password" : password }
				# verbose
				print("Sending request to server..(to login)")
				r = requests.post(url + "/v1/drive/accounts/login", json = req_content)
			except requests.exceptions.ConnectionError as err:
				print("Connection error: " + str(err), flush = True)
				print("Login unsuccessful\n")
				return False
			except requests.exceptions.HTTPError as err:
				print("HTTP Request returned an unsuccessful status code: " + str(err), flush = True)
				print("Login unsuccessful")
				return False
			except requests.exceptions.TooManyRedirects as err:
				print("Too many redirects: " + str(err), flush = True)	
				print("Login unsuccessful")
				return False
			except requests.exceptions.Timeout as err:
				print("Request timed out: " + str(err), flush = True)
				print("Login unsuccessful")
				return False
			r_json = r.json()
			if r_json["status"] == 2:
				print("Error on server while processing request. Login unsuccessful. Please try again later\n")
			elif r_json["status"] == 3:
				print("Email not registered\n")
			elif r_json["status"] == 1:
				print("Incorrect password\n")
			elif r_json["status"] == 0:
				config_parser["session"]["email"] = email
				config_parser["session"]["skey"] = r_json["skey"]
				config_parser["session"]["tkey"] = r_json["tkey"]
				with open(CONFIG_FILE, "w") as f:
					config_parser.write(f)
				if not os.path.exists(MAIN_DIRECTORY + "/drive/" + email):
					os.makedirs(MAIN_DIRECTORY + "/drive/" + email + "/notes")
					with open(MAIN_DIRECTORY + "/drive/" + email + "/notes_info.db","w") as f:
						pass
					# verbose
					print("Modifying local database..")
					conn = sqlite3.connect(MAIN_DIRECTORY + "/drive/" + email + "/notes_info.db")
					c = conn.cursor()
					c.execute("CREATE TABLE info (file_id text, ext text, last_modified text, drive_file_status text)")
					conn.commit()
					conn.close()
				print("Successfully logged in\n")
			else:
				print("Unexpected response from server\n")

	def do_logout(self, args):
		"\nUse this command to logout of your note0 account\n"
		config_parser.read(CONFIG_FILE)
		email = config_parser["session"]["email"]
		if email == "none":
			print("\nYou are not logged in\n")
		else:
			url = config_parser["options"]["url"]
			skey = config_parser["session"]["skey"]
			try:
				req_content = { "email" : email, "skey" : skey }
				# verbose
				print("\nSending request to server..(to log out)")
				r = requests.post(url + "/v1/drive/accounts/logout", json = req_content)
			except requests.exceptions.ConnectionError as err:
				print("Connection error: " + str(err), flush = True)
				print("Logout unsuccessful\n")
				return False
			except requests.exceptions.HTTPError as err:
				print("HTTP Request returned an unsuccessful status code: " + str(err), flush = True)
				print("Logout unsuccessful\n")
				return False
			except requests.exceptions.TooManyRedirects as err:
				print("Too many redirects: " + str(err), flush = True)	
				print("Logout unsuccessful\n")
				return False
			except requests.exceptions.Timeout as err:
				print("Request timed out: " + str(err), flush = True)
				print("Logout unsuccessful\n")
				return False
			r_json = r.json()
			if r_json["status"] == 2:
				print("Error on server while processing request. Logout unsuccessful. Please try again later\n")
			elif r_json["status"] == 1:
				print("You do not seem to be logged in\n")
			elif r_json["status"] == 0:
				config_parser["session"]["email"] = "none"
				config_parser["session"]["skey"] = "none"
				config_parser["session"]["tkey"] = "none"
				with open(CONFIG_FILE, "w") as f:
					config_parser.write(f)
				print("Successfully logged out\n")
			else:
				print("Unexpected response from server\n")

	def do_new(self, args):
		"\nUse this command to create a new note.\nArgument to this command is the extension of the note which defaults to '.txt' if no argument is supplied\n"
		config_parser.read(CONFIG_FILE)
		email = config_parser["session"]["email"]
		if email == "none":
			if args == "":
				args = ".txt"
			file_path = MAIN_DIRECTORY + "/drive/no_email/notes/" + str(int(time.time())) + args
			with open(file_path, "w") as f:
				pass
			subprocess.run( [config_parser["options"]["editor"], file_path] )
			print("\nSuccessfully created new note\n")
		else:
			url = config_parser["options"]["url"]
			skey = config_parser["session"]["skey"]
			tkey = config_parser["session"]["tkey"]
			if args == "":
				args = ".txt"
			name = str(int(time.time()))
			file_path = MAIN_DIRECTORY + "/drive/" + email + "/notes/_" + name + args 
			with open(file_path, "w") as f:
				pass
			subprocess.run( [config_parser["options"]["editor"], file_path] )
			last_modified = str(int(time.time()))
			# verbose
			print("\nModifying local database..")
			conn = sqlite3.connect(MAIN_DIRECTORY + "/drive/" + email + "/notes_info.db")
			c = conn.cursor()
			c.execute("INSERT INTO info VALUES (?,?,?, '00')", ["_" + name, args, last_modified])
			conn.commit()
			conn.close()
			print("Note successfully saved locally")
			obtained_file_id = new_file_id(email = email, skey = skey, tkey = tkey)
			if obtained_file_id != "-1":
				# verbose
				print("Uploading note: " + obtained_file_id + args)
				val = file_upload(email = email, skey = skey, tkey = tkey, description = last_modified, file_id = obtained_file_id, ext = args,
				is_existing_file = "false", file_path = file_path)
				if val == 0:
					# rename from _+name to file_id+ext
					os.rename(file_path, MAIN_DIRECTORY + "/drive/" + email + "/notes/" + obtained_file_id + args)
					# update db
					# verbose
					print("Modifying local database..")
					conn = sqlite3.connect(MAIN_DIRECTORY + "/drive/" + email + "/notes_info.db")
					c = conn.cursor()
					c.execute("UPDATE info SET drive_file_status=?,file_id=? WHERE file_id=?", ['10', obtained_file_id, "_" + name])
					conn.commit()
					conn.close()
					print("Successfully uploaded note: " + obtained_file_id + args + "\n")
				else:
					print("Could not upload the note\n")
			else:
				print("Could not upload note\n")
			
	def do_sync(self, args):
		"\nUse this command to sync\n"
		config_parser.read(CONFIG_FILE)
		email = config_parser["session"]["email"]
		if email == "none":
			print("\nSync not possible since you are not logged in\n")
		else:
			url = config_parser["options"]["url"]
			skey = config_parser["session"]["skey"]
			tkey = config_parser["session"]["tkey"]
			try:
				req_content = { "email" : email, "skey" : skey, "tkey" : tkey }
				# verbose
				print("\nSending request to server..(to get list of notes in drive)")
				r = requests.post(url + "/v1/drive/files/get_list", json = req_content)
			except requests.exceptions.ConnectionError as err:
				print("Connection error: " + str(err), flush = True)
				print("Could not retrieve list of notes in drive\nSync unsuccessful\n")
				return False
			except requests.exceptions.HTTPError as err:
				print("HTTP Request returned an unsuccessful status code: " + str(err), flush = True)
				print("Could not retrieve list of notes in drive\nSync unsuccessful\n")
				return False
			except requests.exceptions.TooManyRedirects as err:
				print("Too many redirects: " + str(err), flush = True)
				print("Could not retrieve list of notes in drive\nSync unsuccessful\n")
				return False
			except requests.exceptions.Timeout as err:
				print("Request timed out: " + str(err), flush = True)
				print("Could not retrieve list of notes in drive\nSync unsuccessful\n")
				return False
			r_json = r.json()
			if r_json["status"] == 2:
				print("Error on server while processing request")
				print("Could not retrieve list of notes in drive\nSync unsuccessful\n")
			elif r_json["status"] == 1:
				print("Invalid credentials\n")
				print("Could not retrieve list of notes in drive\nSync unsuccessful\n")
			elif r_json["status"] == 3:
				print("Error while retrieving list")
				print("Sync unsuccessful\n")
			elif r_json["status"] == 0:
				# r_json["content"]["files"] is a list
				# r_json["content"]["files"][0]["id"]
				# r_json["content"]["files"][0]["description"]
				# verbose
				print("Accessing local database..")
				conn = sqlite3.connect(MAIN_DIRECTORY + "/drive/" + email + "/notes_info.db")
				c = conn.cursor()
				c.execute("SELECT * FROM info")
				local = c.fetchall()
				conn.close()
				# local is a list of tuples
				# local[0][0], local[0][1], local[0][2],      local[0][3]
				#   file_id        ext     last_modified   drive_file_status
				local_list_of_list = []
				local_list_of_tuple_length = len(local)
				for i in range(0,local_list_of_tuple_length):
					local_list_of_list.append([])
					for j in range(0,4):
						local_list_of_list[i].append(local[i][j])
					local_list_of_list[i].append(False) # match for each file present locally is set to False
				# local_list_of_list is a list of lists
				r_json_copy = []
				for x in r_json["content"]["files"]:
					r_json_copy.append(x)
				# verbose
				print("Processing..")
				for x in r_json_copy:
					match = False
					for i in range(0,local_list_of_tuple_length): # which is same as len(local_list_of_list)
						if x["id"] == local_list_of_list[i][0]:
							match = True
							local_list_of_list[i][4] = True
							if local_list_of_list[i][3][1] == "0":		
								# upload/download
								if x["description"] > local_list_of_list[i][2]:
									#download
									# verbose
									print("Downloading note: " + x["name"])
									val = file_download(email = email, skey = skey, tkey = tkey, file_id = x["id"])
									if val["status"] == 0:
										with open(MAIN_DIRECTORY + "/drive/" + email + "/notes/" + x["name"], "w") as f:
											f.write(val["content"])
										conn = sqlite3.connect(MAIN_DIRECTORY + "/drive/" + email + "/notes_info.db")
										c = conn.cursor()
										c.execute("UPDATE info SET last_modified=? WHERE file_id=?", [x["description"], x["id"]])
										conn.commit()
										conn.close()
										print("Successfully downloaded note: " + x["name"])
									else:
										print("Note download unsuccessful")
									
								elif x["description"] < local_list_of_list[i][2]:
									# upload
									# verbose
									print("Uploading note: " + x["id"] + local_list_of_list[i][1])
									val = file_upload(email = email, skey = skey, tkey = tkey, description = local_list_of_list[i][2], file_id = x["id"], 
										ext = local_list_of_list[i][1], is_existing_file = "true", file_path = MAIN_DIRECTORY + "/drive/" + email + "/notes/" + x["name"])
									if val == 0:
										# verbose
										print("Successfully uploaded note: " + x["id"] + local_list_of_list[i][1])
									else:
										print("Note upload unsuccessful")
							elif local_list_of_list[i][3][1] == "1":
								# deleted locally but due to some issue could not delete in drive
								# hence delete in drive now
								res = file_delete(email = email, skey = skey, tkey = tkey, file_id = local_list_of_list[i][0])
								if res:
									# remove from table
									print("Note deleted from drive successfully")
									print("Modifying local database..")
									conn = sqlite3.connect(MAIN_DIRECTORY + "/drive/" + email + "/notes_info.db")
									c = conn.cursor()
									c.execute("DELETE FROM info WHERE file_id=?", [local_list_of_list[i][0]])
									conn.commit()
									conn.close()
									print("Note successfully deleted")
								else:
									# set 1 to 1
									print("Note could not be deleted from drive")
							else:
								print("Unexpected value\n")
								sys.exit()
							break
					if not match:
						# download
						print("Downloading file: " + x["name"])
						val = file_download(email = email, skey = skey, tkey = tkey, file_id = x["id"])
						if val["status"] == 0:
							with open(MAIN_DIRECTORY + "/drive/" + email + "/notes/" + x["name"], "w") as f:
								f.write(val["content"])
							# verbose
							print("Modifying local database..")
							conn = sqlite3.connect(MAIN_DIRECTORY + "/drive/" + email + "/notes_info.db")
							c = conn.cursor()
							temp = (x["name"]).split(".")
							c.execute("INSERT INTO info VALUES (?,?,?,'10')", [x["id"], "." + temp[len(temp)-1], x["description"]])
							conn.commit()
							conn.close()
							print("Successfully downloaded file: " + x["name"])
						else:
							print("File download unsuccessful")
				for x in local_list_of_list:
					if not x[4]:
						if x[3][0] == "1":
							# file has been deleted in drive from some other session, so delete it here
							# verbose
							print("Modifying local database..")
							conn = sqlite3.connect(MAIN_DIRECTORY + "/drive/" + email + "/notes_info.db")
							c = conn.cursor()
							c.execute("DELETE FROM info WHERE file_id=?", [x[0]])
							conn.commit()
							conn.close()
							if x[3][1] == "0":
								os.remove(MAIN_DIRECTORY + "/drive/" + email + "/notes/" + x[0] + x[1])
							print("Successfully removed note: " + x[0] + x[1])
						elif x[3][0] == "0":
							# file hasn't been uploaded since it's creation
							if x[0][0] == "_":
								# get new file id
								file_path = MAIN_DIRECTORY + "/drive/" + email + "/notes/" + x[0] + x[1]
								obtained_file_id = new_file_id(email = email, skey = skey, tkey = tkey)
								print("Uploading note: " + obtained_file_id + x[1])
								val = file_upload(email = email, skey = skey, tkey = tkey, description = x[2], file_id = obtained_file_id, ext = x[1],
								is_existing_file = "false", file_path = file_path)
								if val == 0:
									# rename from _+name to file_id+ext
									os.rename(file_path, MAIN_DIRECTORY + "/drive/" + email + "/notes/" + obtained_file_id + x[1])
									# update db
									print("Updating local database..")
									conn = sqlite3.connect(MAIN_DIRECTORY + "/drive/" + email + "/notes_info.db")
									c = conn.cursor()
									c.execute("UPDATE info SET drive_file_status='10',file_id=? WHERE file_id=?", [obtained_file_id, x[0]])
									conn.commit()
									conn.close()
									print("Successfully uploaded note: " + obtained_file_id + x[1])
								else:
									print("Note upload unsuccessful")
							else:
								# verbose
								print("Uploading note: " + x[0] + x[1])
								val = file_upload(email = email, skey = skey, tkey = tkey, description = x[2], file_id = x[0],
									ext = x[1], is_existing_file = "false", file_path = MAIN_DIRECTORY + "/drive/" + email + "/notes/" + x[0] + x[1])
								if val == 0:
									print("Updating local database..")
									conn = sqlite3.connect(MAIN_DIRECTORY + "/drive/" + email + "/notes_info.db")
									c = conn.cursor()
									c.execute("UPDATE info SET drive_file_status='10' WHERE file_id=?", [x[0]])
									conn.commit()
									conn.close()
									print("Successfully uploaded note: " + x[0] + x[1])
								else:
									print("Note upload unsuccessful")
						else:
							print("Unexpected value\n")
							sys.exit()
				print("Sync complete\n")
			else:
				print("Unexpected response from server\n")			

	def do_open(self, args):
		"\nUse this command to view, edit notes\n"
		config_parser.read(CONFIG_FILE)
		email = config_parser["session"]["email"]
		if email == "none":
			path = MAIN_DIRECTORY + "/drive/no_email/notes"
			files = os.listdir(path)
			files_length = len(files)
			if files_length == 0:
				print("\nYou do not have any notes\n")
			else:
				menu(notes = files, is_logged_in = False)
				view_number = input("\nWhich note do you want to open (note number): ")
				try:
					view_number = int(view_number)
				except ValueError:
					print("Cancelled due to non integer input\n")
					return False
				if view_number <= files_length-1 and view_number >= 0:
					file_path = path + "/" + files[view_number]
					before = os.path.getmtime(file_path)
					subprocess.run([config_parser["options"]["editor"], file_path])
					after = os.path.getmtime(file_path)
					if before != after:
						print("Note successfully saved")
					print("")
				else:
					print("Invalid note number\n")
		else:
			skey = config_parser["session"]["skey"]
			tkey = config_parser["session"]["tkey"]
			url = config_parser["options"]["url"]
			path = MAIN_DIRECTORY + "/drive/" + email
			conn = sqlite3.connect(path + "/notes_info.db")
			c = conn.cursor()
			c.execute("SELECT * FROM info WHERE drive_file_status='00' OR drive_file_status='10'")
			db = c.fetchall()
			conn.close()
			db_length = len(db)
			if db_length == 0:
				print("\nYou do not have any notes\n")
			else:
				menu(notes = db, is_logged_in = True)
				view_number = input("\nWhich note do you want to open (note number): ")
				try:
					view_number = int(view_number)
				except ValueError:
					print("Cancelled due to non integer input\n")
					return False
				if view_number <= db_length-1 and view_number >= 0:
					file_path = path + "/notes/" + db[view_number][0] + db[view_number][1]
					before = os.path.getmtime(file_path)
					subprocess.run([config_parser["options"]["editor"], file_path])
					last_modified = str(int(time.time()))
					after = os.path.getmtime(file_path)
					if before != after:
						# file has been modified, upload it
						# verbose
						print("Note successfully saved locally")
						conn = sqlite3.connect(path + "/notes_info.db")
						c = conn.cursor()
						if db[view_number][0][0] == "_":
							# get id, modify db and then upload
							file_id = new_file_id(email = email, skey = skey, tkey = tkey)
							if file_id != "-1":
								print("Modifying local database..")
								c.execute("UPDATE info SET file_id=?, last_modified=?, drive_file_status='10' WHERE file_id=?", [file_id, last_modified, db[view_number][0]])
								os.rename(file_path, path + "/notes/" + file_id + db[view_number][1])
								file_path = path + "/notes/" + file_id + db[view_number][1]
							else:
								print("Modifying local database..")
								c.execute("UPDATE info SET last_modified=?  WHERE file_id=?", [last_modified, db[view_number][0]])
								print("Could not get file id\nCould not upload note\n")
								conn.commit()
								conn.close()
								return False;
						else:
							#modify db
							file_id = db[view_number][0]
							print("Modifying local database..")
							c.execute("UPDATE info SET last_modified=? WHERE file_id=?", [last_modified, db[view_number][0]])
						conn.commit()
						conn.close()
						# verbose
						print("Uploading note: " + file_id + db[view_number][1])
						if db[view_number][3][0] == "0":
							val = file_upload(email = email, skey = skey, tkey = tkey, description = last_modified, file_id = file_id,
								ext = db[view_number][1], is_existing_file = "false", file_path = file_path)
						else:
							val = file_upload(email = email, skey = skey, tkey = tkey, description = last_modified, file_id = file_id,
								ext = db[view_number][1], is_existing_file = "true", file_path = file_path)
						if val == 0:
							if db[view_number][3][0] == "0":
								# verbose
								print("Modifying local database..")
								conn = sqlite3.connect(path + "/notes_info.db")
								c = conn.cursor()
								c.execute("UPDATE info SET drive_file_status='10' WHERE file_id=?", [db[view_number][0]])
								conn.commit()
								conn.close()
							print("Successfully uploaded note: " + file_id + db[view_number][1])
						else:
							print("Note upload unsuccessful")
					print("")
				else:
					print("Invalid note number\n")

	def do_delete(self, args):
		"\nUse this command to delete notes\n"
		config_parser.read(CONFIG_FILE)
		email = config_parser["session"]["email"]
		if email == "none":
			path = MAIN_DIRECTORY + "/drive/no_email/notes"
			files = os.listdir(path)
			files_length = len(files)
			if files_length == 0:
				print("\nYou do not have any notes\n")
			else:
				menu(notes = files, is_logged_in = False)
				view_number = input("\nWhich note do you want to delete (note number): ")
				try:
					view_number = int(view_number)
				except ValueError:
					print("Cancelled due to non integer input\n")
					return False
				if view_number <= files_length-1 and view_number >= 0:
					confirm = input("Are you sure you want to delete note number " + str(view_number) + " (y/n)?: ")
					if confirm == "y":
						os.remove(path + "/" + files[view_number])
						print("Note successfully deleted\n")
					elif confirm == "n":
						print("Note deletion cancelled\n")
					else:
						print("Invalid input\n")
				else:
					print("Invalid note number\n")
		else:
			skey = config_parser["session"]["skey"]
			tkey = config_parser["session"]["tkey"]
			url = config_parser["options"]["url"]
			path = MAIN_DIRECTORY + "/drive/" + config_parser["session"]["email"]
			conn = sqlite3.connect(path + "/notes_info.db")
			c = conn.cursor()
			c.execute("SELECT * FROM info WHERE drive_file_status='00' OR drive_file_status='10'")
			db = c.fetchall()
			conn.close()
			db_length = len(db)
			if db_length == 0:
				print("\nYou do not have any notes\n")
			else:
				menu(notes = db, is_logged_in = True)
				view_number = input("\nWhich note do you want to delete (note number): ")
				try:
					view_number = int(view_number)
				except ValueError:
					print("Cancelled due to non integer input\n")
					return False
				if view_number <= db_length-1 and view_number >= 0:
					confirm = input("Are you sure you want to delete note number " + str(view_number) + " (y/n)?: ")
					if confirm == "y":
						# delete locally
						os.remove(path + "/notes/" + db[view_number][0] + db[view_number][1])
						# verbose
						print("Note deleted locally")
						conn = sqlite3.connect(path + "/notes_info.db")
						c = conn.cursor()
						if db[view_number][3][0] == "1":
							# delete from drive
							res = file_delete(email = email, skey = skey, tkey = tkey, file_id = db[view_number][0])
							if res:
								# remove from table
								print("Note deleted from drive successfully")
								print("Modifying local database..")
								c.execute("DELETE FROM info WHERE file_id=?", [db[view_number][0]])
								conn.commit()
								conn.close()
								print("Note successfully deleted\n")
							else:
								# set 1 to 1
								print("Note could not be deleted from drive")
								print("Modifying local database..")
								c.execute("UPDATE info SET drive_file_status=? WHERE file_id=?", ["11", db[view_number][0]])
								conn.commit()
								conn.close()
								print("Note deleted locally but not in drive\n")
						else:
							# file not in drive, remove from table
							# verbose
							print("Modifying local database..")
							c.execute("DELETE FROM info WHERE file_id=?", [db[view_number][0]])
							conn.commit()
							conn.close()
							print("Note successfully deleted\n")
					elif confirm == "n":
						print("Note deletion cancelled\n")
					else:
						print("Invalid input\n")
				else:
					print("Invalid note number\n")

	def do_set_url(self, args):
		"\nUse this command to set the URL to which requests will be made to\nIf no arguments are given URL will be set to the default value\n"
		if args == "":
			args = DEFAULT_URL
		config_parser.read(CONFIG_FILE)
		config_parser["options"]["url"] = args
		with open(CONFIG_FILE, "w") as f:
			config_parser.write(f)
		print("\nURL changed to " + args + " successfully\n")

	def do_set_editor(self, args):
		"\nUse this command to set the editor that should be used for viewing and editing notes\n"
		config_parser.read(CONFIG_FILE)
		if args != "":
			config_parser["options"]["editor"] = args
			with open(CONFIG_FILE, "w") as f:
				config_parser.write(f)
			print("\nEditor changed to " + args + " successfully\n")
		else:
			print("\nThis command requires exactly one non empty argument\n")

	def do_status(self, args):
		"\nUse this command to check whether you are logged in or not and if logged in, email of logged in account is displayed\n"
		config_parser.read(CONFIG_FILE)
		if config_parser["session"]["email"] == "none":
			print("\nYou are not logged in\n")
		else:
			print("\nYou are logged in as " + config_parser["session"]["email"] + "\n")

	def do_exit(self, args):
		"\nUse this command to exit the application\n"
		return True
# custom shell - end

# functions - begin
def file_download(email, skey, tkey, file_id):
	config_parser.read(CONFIG_FILE)
	url = config_parser["options"]["url"]
	try:
		req_content = { "email" : email, "skey" : skey, "tkey" : tkey, "file_id" : file_id }
		r = requests.post(url + "/v1/drive/files/download", json = req_content)
	except requests.exceptions.ConnectionError as err:
		print("Connection error: " + str(err), flush = True)
		return { "status" : -1 }
	except requests.exceptions.HTTPError as err:
		print("HTTP Request returned an unsuccessful status code: " + str(err), flush = True)
		return { "status" : -1 }
	except requests.exceptions.TooManyRedirects as err:
		print("Too many redirects: " + str(err), flush = True)	
		return { "status" : -1 }
	except requests.exceptions.Timeout as err:
		print("Request timed out: " + str(err), flush = True)
		return { "status" : -1 }
	r_json = r.json()
	if r_json["status"] == 2:
		print("Error on server while processing request. Please try again later")
	elif r_json["status"] == 1:
		print("Invalid credentials")
	elif r_json["status"] == 3:
		print("Error while downloading note")
	elif r_json["status"] == 0:
		pass
	else:
		print("Unexpected response from server")
		sys.exit()
	return r_json

def file_upload(email, skey, tkey, description, file_id, ext, is_existing_file, file_path):
	config_parser.read(CONFIG_FILE)
	url = config_parser["options"]["url"]
	try:
		req_content = { "email" : email, "skey" : skey, "tkey" : tkey, "description" : description, "file_id" : file_id, 
		                "ext" : ext, "is_existing_file" : is_existing_file }
		file_to_upload = { "to_upload" : open(file_path, "rb") }
		r = requests.post(url + "/v1/drive/files/upload", data = req_content, files = file_to_upload)
	except requests.exceptions.ConnectionError as err:
		print("Connection error: " + str(err), flush = True)
		return -1
	except requests.exceptions.HTTPError as err:
		print("HTTP Request returned an unsuccessful status code: " + str(err) + "\n", flush = True)
		return -1
	except requests.exceptions.TooManyRedirects as err:
		print("Too many redirects: " + str(err), flush = True)	
		return -1
	except requests.exceptions.Timeout as err:
		print("Request timed out: " + str(err), flush = True)
		return -1
	r_json = r.json()
	if r_json["status"] == 2:
		print("Error on server while processing request. Please try again later")
	elif r_json["status"] == 1:
		print("Invalid credentials")
	elif r_json["status"] == 4:
		print("Error while uploading note to drive")
	elif r_json["status"] == 3:
		print("Error while uploading note to drive")
	elif r_json["status"] == 0:
		pass
	else:
		print("Unexpected response from server")
		sys.exit()
	return r_json["status"]

def file_delete(email, skey, tkey, file_id):
	config_parser.read(CONFIG_FILE)
	url = config_parser["options"]["url"]
	try:
		req_content = { "email" : email, "skey" : skey, "tkey" : tkey, "file_id" : file_id}
		# verbose
		print("Sending request to server..(to delete the note in drive)")
		r = requests.post(url + "/v1/drive/files/delete", json = req_content)
	except requests.exceptions.ConnectionError as err:
		print("Connection error: " + str(err), flush = True)
		return False
	except requests.exceptions.HTTPError as err:
		print("HTTP Request returned an unsuccessful status code: " + str(err), flush = True)
		return False
	except requests.exceptions.TooManyRedirects as err:
		print("Too many redirects: " + str(err), flush = True)	
		return False
	except requests.exceptions.Timeout as err:
		print("Request timed out: " + str(err), flush = True)
		return False
	r_json = r.json()
	if r_json["status"] == 2:
		print("Error on server while processing request")
		return False
	elif r_json["status"] == 1:
		print("Invalid credentials")
		return False
	elif r_json["status"] == 3:
		print("Error while deleting file in drive")
		return False
	elif r_json["status"] == 0:
		return True
	else:
		print("Unexpected response from server")
		sys.exit()

def new_file_id(email, skey, tkey):
	config_parser.read(CONFIG_FILE)
	url = config_parser["options"]["url"]
	try:
		req_content = { "email" : email, "skey" : skey, "tkey" : tkey }
		# verbose
		print("Sending request to server..(to get new file id)")
		r = requests.post(url + "/v1/drive/files/get_new_file_id", json = req_content)
	except requests.exceptions.ConnectionError as err:
		print("Connection error: " + str(err), flush = True)
		print("Could not get new file id")
		return "-1"
	except requests.exceptions.HTTPError as err:
		print("HTTP Request returned an unsuccessful status code: " + str(err), flush = True)
		print("Could not get new file id")
		return "-1"
	except requests.exceptions.TooManyRedirects as err:
		print("Too many redirects: " + str(err), flush = True)
		print("Could not get new file id")
		return "-1"
	except requests.exceptions.Timeout as err:
		print("Request timed out: " + str(err), flush = True)
		print("Could not get new file id")
		return "-1"
	r_json = r.json()
	if r_json["status"] == 2:
		print("Error on server while processing request.")
		return "-1"
	elif r_json["status"] == 1:
		print("Invalid credentials")
		return "-1"
	elif r_json["status"] == 3:
		print("Error while generating file ID")
		return "-1"
	elif r_json["status"] == 0:
		return r_json["file_id"]
	else:
		print("Unexpected response from server")
		sys.exit() 

def get_password(option, is_logged_in):
	if option == "create_account":
		try:
			password = getpass.getpass(prompt = "Password for your note0 account: ")
		except getpass.GetPassWarning:
			pass
		while password == "":
			try:
				password = getpass.getpass(prompt = "Password cannot be empty. Please re-enter password: ")
			except getpass.GetPassWarning:
				pass
		try:
			reenter_password = getpass.getpass(prompt = "Please re-enter password for confirmation: ")
		except getpass.GetPassWarning:
			pass
		while reenter_password != password:
			print("Passwords do not match")
			try:
				password = getpass.getpass(prompt = "Password for your note0 account: ")
			except getpass.GetPassWarning:
				pass
			while password == "":
				try:
					password = getpass.getpass(prompt = "Password cannot be empty. Please re-enter password: ")
				except getpass.GetPassWarning:
					pass
			try:
				reenter_password = getpass.getpass(prompt = "Please re-enter password for confirmation: ")
			except getpass.GetPassWarning:
				pass
		return password
	elif option == "login":
		try:
			password = getpass.getpass(prompt = "Password for your note0 account: ")
		except getpass.GetPassWarning:
			pass
		while password == "":
			try:
				password = getpass.getpass(prompt = "Password cannot be empty. Please re-enter password: ")
			except getpass.GetPassWarning:
				pass
		return password
	elif option == "delete_account":
		try:
			password = getpass.getpass(prompt = "Password: ")
		except getpass.GetPassWarning:
			pass
		while password == "":
			try:
				password = getpass.getpass(prompt = "Password cannot be empty. Please re-enter password: ")
			except getpass.GetPassWarning:
				pass
		return password
	elif option == "change_password":
		passwords = []
		if not is_logged_in:
			try:
				password = getpass.getpass(prompt = "Current password: ")
			except getpass.GetPassWarning:
				pass
			while password == "":
				try:
					password = getpass.getpass(prompt = "Current password cannot be empty, re-enter password: ")
				except getpass.GetPassWarning:
					pass
			passwords.append(password)
		else:
			print("")
		try:
			new_password = getpass.getpass(prompt = "New password: ")
		except getpass.GetPassWarning:
				pass
		while new_password == "":
			try:
				new_password = getpass.getpass(prompt = "New password cannot be empty, re-enter new password: ")
			except getpass.GetPassWarning:
				pass
		try:
			confirm_new_password = getpass.getpass(prompt = "Enter the new password again for confirmation: ")
		except getpass.GetPassWarning:
				pass
		while confirm_new_password != new_password:
			print("Passwords do not match")
			try:
				new_password = getpass.getpass(prompt = "New password: ")
			except getpass.GetPassWarning:
				pass
			while new_password == "":
				try:
					new_password = getpass.getpass(prompt = "New password cannot be empty, re-enter new password: ")
				except getpass.GetPassWarning:
					pass
			try:
				confirm_new_password = getpass.getpass(prompt = "Enter the new password again for confirmation: ")
			except getpass.GetPassWarning:
				pass
		passwords.append(new_password)
		return passwords
	else:
		print("Unexpected argument to function")
		sys.exit()

def menu(notes, is_logged_in):
	notes_copy = []
	config_parser.read(CONFIG_FILE)
	if is_logged_in:
		path = MAIN_DIRECTORY + "/drive/" + config_parser["session"]["email"] + "/notes"
		for x in notes:
			notes_copy.append(x[0] + x[1])
	else:
		path = MAIN_DIRECTORY + "/drive/no_email/notes"
		for x in notes:
			notes_copy.append(x)
	cols = shutil.get_terminal_size()[0]
	notes_copy_length = len(notes_copy)
	for i in range(0, notes_copy_length):
		print("\nNote number: " + str(i))
		for j in range(0,cols-1):
			print("-",end = "")
		print("")
		with open(path + "/" + notes_copy[i], "r") as f:
			n = 0
			for line in f:
				print(line, end = "")
				n = n + 1
				if n == 2:
					break
		for j in range(0,cols-1):
			print("-",end = '')
		print("")

def main():
	if args.setup:
		if os.path.exists(MAIN_DIRECTORY):
			print("This program needs to create a directory named '.note0' in " + os.path.expanduser("~")
				+ "\nBut it looks like there already exists a file/directory with the same name in the same" 
				" location. \nPlease rename or move the existing file/directory such that there is no file/directory"
				" with the name '.note0' in the aforementioned location")
		else:
			os.makedirs(MAIN_DIRECTORY + "/drive/no_email/notes")
			config_parser["about"] = {
				"version" : "0.1.0"
			}
			config_parser["options"] = {
				"editor" : "vim",
				"url"    : DEFAULT_URL
			}
			config_parser["session"] = {
				"email" : "none",
				"skey"  : "none",
				"tkey"  : "none"
			}
			with open(CONFIG_FILE, "w") as f:
				config_parser.write(f)
			print("Successfully completed the required setup\n"
			      "You may now use the application")

	else:
		p = Note0Shell()
		config_parser.read(CONFIG_FILE)
		try:
			email = config_parser["session"]["email"]
			if email == "none":
				p.intro += ("Version " + config_parser["about"]["version"]
				+ "\n\nType 'help' to know more\n\nLog in status: You are not logged in\n")
			else:
				p.intro += ("Version " + config_parser["about"]["version"] 
				+ "\n\nType 'help' to know more\n\nLog in status: You are logged in as " + email + "\n")
		except KeyError:
			print("Could not read config file information\nYou are probably running the application for the first time and haven't set it up")
			sys.exit()
		p.cmdloop()
# functions - end