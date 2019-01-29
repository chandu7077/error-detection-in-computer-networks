import socket
class Receiver:
    def __init__(self,host,port,data=""):
        self.host=host
        self.port=port
        self.data=data
    def receive(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            sock.connect((self.host,self.port))
            self.data=sock.recv(1024).decode("utf8")
        print("recieved bytes:",self.data)
    def decode_check(self):
        bin_data=[]
        for i in range(0,len(self.data),8):
            bin_data.append(self.data[i:i+8])
        print(bin_data)
        for i in range(0,len(bin_data)):
            cnt=bin_data[i][0:-1].count("1")
            if cnt%2==0 and bin_data[i][-1]!='0':
                print("data corrupted")
                break
            elif cnt%2==1 and bin_data[i][-1]!='1':
                print("data corrupted")
                break
            else:
                bin_data[i]=bin_data[i][0:-1]
        self.data=""
        for i in range(0,len(bin_data)):
            self.data=self.data+chr(int(bin_data[i],2))
        print("no data loss")
        return self.data
recv=Receiver("127.0.0.1",65432)
recv.receive()
print(recv.decode_check())



