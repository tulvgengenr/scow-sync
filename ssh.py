'''
Ssh connection and execute commands with singleton pattern
'''
import threading
import paramiko

class SSH:
    '''
    Ssh connection and execute commands
    '''
    _instance_lock = threading.Lock()

    def __init__(self, address, user, sshpassword_path):
        self.ssh = paramiko.SSHClient()
        self.address = address
        self.user = user
        self.__login(address, user, sshpassword_path)

    def __new__(cls, *args, **kwargs):
        if not hasattr(SSH, "_instance"):
            with SSH._instance_lock:
                if not hasattr(SSH, "_instance"):
                    SSH._instance = object.__new__(cls)
        return SSH._instance

    def __login(self, address, user, sshpassword_path):
        key = paramiko.RSAKey.from_private_key_file(sshpassword_path)
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(address, username=user, pkey=key)

    def ssh_exe_cmd(self, cmd):
        '''
        Execute command on the server
        '''
        try:
            self.ssh.exec_command(cmd)
        except SystemError as exception:
            print(f"ssh execute error:{cmd}, exception:{str(exception)}")
