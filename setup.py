import subprocess


def main():
    subprocess.call('sudo systemctl enable ssh', shell=True)
    print('SSH ENABLED')
    subprocess.call('sudo systemctl start ssh', shell=True)
    print('SSH STARTED')
    subprocess.call('sudo apt-get update', shell=True)
    print('Prepared for VNC download...')
    subprocess.call('sudo apt-get install realvnc-vnc-server realvnc-vnc-viewer', shell=True)
    print('VNC Retreived')
    print('Please enable VNC in the config...')
    subprocess.call('sudo raspi-config', shell=True)

    print('Once done- restart your PI')
    return

if __name__ == '__main__':
    main()
    print('Ready for File Transfer')