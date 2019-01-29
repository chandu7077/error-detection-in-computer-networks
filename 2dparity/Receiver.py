import socket
class Receiver:
    def __init__(self,host,port,data=""):
        self.host=host
        self.port=port
        self.data=data
        self.error=False
    def receive(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            sock.connect((self.host,self.port))
            self.data=sock.recv(1024).decode("utf8")
        print("recieved bytes:",self.data)
    def decode_check(self):
        bin_data=[]
        error_rows=[]
        error_cols=[]
        for i in range(0,len(self.data),8):
            bin_data.append(self.data[i:i+8])
        for i in range(0,len(bin_data)):
            cnt=bin_data[i][0:-1].count("1")
            if cnt%2==0 and bin_data[i][-1]!='0':
                self.error=True
                error_rows.append(i)
            elif cnt%2==1 and bin_data[i][-1]!='1':
                self.error=True
                error_rows.append(i)
            else:
                bin_data[i]=bin_data[i][0:]
        for i in range(8):
            cnt=0
            for j in range(0,len(bin_data)-1):
                if bin_data[j][i]=="1":
                    cnt+=1
            if cnt%2==0 and bin_data[-1][i]!='0':
                self.error = True
                error_cols.append(i)
            elif cnt%2==1 and bin_data[-1][i]!='1':
                self.error = True
                error_cols.append(i)
        bin_data=[it[0:-1] for it in bin_data[0:-1]]
        self.data=""
        if self.error:
            if len(error_cols)==1 and len(error_rows)==1:
                print("data corrupted in block {0} at {1} bit".format(error_rows[0],error_cols[1]))
                print("performing error correction")
                print(bin_data[error_rows[0]])
            else:
                print("data corrupted at multiple places")
                print("data corrupted blocks:",error_rows)
                print("data corrupted bit positions:", error_cols)
        else:
            for i in range(0,len(bin_data)):
                self.data=self.data+chr(int(bin_data[i],2))
            return self.data
recv=Receiver("127.0.0.1",65432)
recv.receive()
print(recv.decode_check())



