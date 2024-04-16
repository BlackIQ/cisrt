import paramiko
import config as cf
import methods as md
import sys

def main():
    client_ip = input("Insert your client IP: ")
    try:
        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(cf.hostname, cf.hostport, cf.username, cf.password)

        switch_ip = cf.hostname
        mac = None
        
        while True:
            if switch_ip == cf.hostname:
                mac = md.showArp(ssh, client_ip)[0]
                
            port_data = md.showMacAddressTable(ssh, mac)
            port_details = md.showCdpNeighborsDetails(ssh, port_data['port'][0])
            
            if "DYNAMIC" in port_data['text']:
                print("Switch IP: {:<18s} - Port: {:<10s} - Trunk".format(switch_ip, port_data['port'][0]))
                switch_ip = port_details['ip'][0]
            else:
                print("Switch IP: {:<18s} - Port: {:<10s} - Access".format(switch_ip, port_data['port'][0]))
                print("Client IP: {:<18s} - Mac Address: {}".format(client_ip, mac))
                break
            
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print("Error:", e)
    finally:
        if ssh:
            ssh.close()

if __name__ == "__main__":
    main()
