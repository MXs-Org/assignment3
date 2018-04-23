import socket

def is_sucessful_command_injection(payload, response):

	if "echo" in payload:
		argument_index = payload.index("echo ") + 5
		if payload[argument_index:] in payload:
			return True

	elif "uname" in payload:
		correct_output = "Linux benchmark 4.13.0-38-generic #43~16.04.1-Ubuntu SMP"
		correct_output_2 = "x86_64 x86_64 x86_64 GNU/Linux"
		if correct_output in response and correct_output_2 in response:
			return True
	
	elif "/bin/sh" in payload or "bash" in payload:
		sock = socket.socket()
		sock.setdefaulttimeout(20)
		sock.bind(("192.168.0.124", 5555))
		try:
			sock.listen(10)
			conn, addr = sock.accept()
			response = conn.recv(256)
			if "/bin/sh" or "/bin/bash" in response:
				return True
		except:
			return False

	else:
		print("Unrecognized Payload")

	return False