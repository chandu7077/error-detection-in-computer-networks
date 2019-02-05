import socket
import random
class Receiver:
    def __init__(self,host,port,crc,data=""):
        self.host=host
        self.port=port
        self.data=data
        self.crc=crc
        self.error=False
    def receive(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            sock.connect((self.host,self.port))
            self.data=sock.recv(1024).decode("utf8")

    def ham_decoder(self):
        self.inject_error()
        pow2=[2**i for i in range(len(self.data)//2) if 2**i <=len(self.data)]
        cnt=0
        rr=rr=[[] for i in range(len(pow2))]
        for i in pow2:
            pow_cnt=0
            ele=list(range(i,len(self.data)+1))
            while pow_cnt<len(ele):
                rr[cnt].append(ele[pow_cnt:pow_cnt+i])
                pow_cnt+=2*i
            cnt+=1
        for i in range(len(rr)):
            rr[i]=[y for x in rr[i] for y in x]
        bits = [[] for i in range(len(rr))]
        #self.data=self.data[::-1]
        error=""
        cnt=0
        for j in range(len(rr)):
            for i in rr[j]:
                if i<=len(self.data):
                    bits[cnt].append(self.data[i-1])
            b="".join(bits[cnt])
            cnt1=list(b).count('1')
            error+=str(cnt1%2)
            cnt+=1
        error=error[::-1]
        if int(error,2)==0:
            print("data arrived successfully")
            self.get_data(pow2)
        else:
            print(error)
            print("error occured at bit {0}".format(int(error,2)))
            error = int(error, 2)
            print("performing error correction:")
            self.data = list(self.data)
            self.data[error-1]=str((int(self.data[error-1])+1)%2)
            self.data = "".join(self.data)
            self.get_data(pow2)
    def inject_error(self):
        self.data = list(self.data)
        a=random.randint(0,len(self.data))
        self.data[a] = str((int(self.data[a])+1)%2)
        self.data = "".join(self.data)
        print("recieved bytes:", self.data)
    def get_data(self,pow2):
        recv_str = ""
        for i in range(0, len(self.data)):
            if (i + 1) not in pow2:
                recv_str += self.data[i]
        recv_li = []
        recv_str = recv_str[::-1]
        for i in range(0, len(recv_str), 8):
            recv_li.append(chr(int(recv_str[i:i + 8], 2)))
        recv_str = "".join(recv_li)
        print(recv_str)
recv=Receiver("127.0.0.1",65432,"1001")
recv.receive()
recv.ham_decoder()
