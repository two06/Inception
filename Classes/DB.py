import sqlite3
import os
from os.path import isfile, expanduser

#globals - change these if needed
home = expanduser("~")
db_Path = home + '/.inception/DB.sq3'

#Check if the DB file esits - called from Inception.py
def Check_DB_Exists():
	return os.path.isfile(db_Path)

#creates the payload table
def Create_Schema():
	db = sqlite3.connect(db_Path)
	cursor = db.cursor()
	cursor.execute('''
	CREATE TABLE payload(encryption_key TEXT PRIMARY KEY, file_path TEXT unique, access_count INTEGER, allowed_access_count INTEGER)
	''')
	db.commit()

#insert a new payload record
def Insert_Payload(encryption_key, file_path, allowed_access_count):
	db = sqlite3.connect(db_Path)
	cursor = db.cursor()
	cursor.execute('''
	INSERT INTO payload (encryption_key, file_path, access_count, allowed_access_count)
		VALUES(?,?,?,?)''', (encryption_key, file_path, 0, allowed_access_count))
	db.commit()

#Increment the access_count value for a given payload
def Increment_Access_count(encryption_key):
	db = sqlite3.connect(db_Path)
	cursor = db.cursor()
	cursor.execute('''SELECT access_count from payload WHERE encryption_key=?''',(encryption_key,))
	current_count = cursor.fetchone()
	new_count = current_count[0] + 1
	cursor.execute('''UPDATE payload SET access_count = ? WHERE encryption_key = ?''', (new_count, encryption_key))
	db.commit()


#Get a payload entry - returns a dictionary
def Get_Payload(encryption_key):
	db = sqlite3.connect(db_Path)
	cursor = db.cursor()
	cursor.execute('''SELECT encryption_key, file_path, access_count, allowed_access_count FROM payload WHERE encryption_key = ?''', (encryption_key,))
	payload = cursor.fetchone()
	if payload is None:
		return None
	p = dict()
	p['encryption_key'] = payload[0]
	p['file_path'] = payload[1]
	p['access_count'] = payload[2]
	p['allowed_access_count'] = payload[3]
	return p

#cleanup - clear the DB file
def Cleanup():
	db = sqlite3.connect(db_Path)
	cursor = db.cursor()
	cursor.execute('''DELETE FROM payload''')
	db.execute()





