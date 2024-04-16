import time
import re

def showArp(ssh, ip):
    stdin, stdout, stderr = ssh.exec_command(f"show arp {ip}\n")
    stdout.channel.recv_exit_status()
    text = stdout.read().decode("utf-8")
    mac_pattern = r'\s*([0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4})'
    return re.findall(mac_pattern, text)

def showMacAddressTable(ssh, mac):
    result = {}
    stdin, stdout, stderr = ssh.exec_command(f"show mac address-table | include {mac}\n")
    stdout.channel.recv_exit_status()
    text = stdout.read().decode("utf-8")
    result['text'] = text
    result['port'] = re.findall(r'\w+\/(?:\w+\/)*\w+', text)
    return result
    
def showCdpNeighborsDetails(ssh, port):
    result = {}
    stdin, stdout, stderr = ssh.exec_command(f"show cdp neighbors {port} detail\n")
    stdout.channel.recv_exit_status()
    text = stdout.read().decode("utf-8")
    ip_pattern = r'\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    result['ip'] = re.findall(ip_pattern, text)
    return result
