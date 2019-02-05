import socket
import math
class Sender:
    def __init__(self,host,port,data,enc_data=""):
        self.host=host
        self.port=port
        self.data=data
        self.enc_data=enc_data
    def parity_encoder(self):
        map_data = map(bin, bytearray(data, "utf8"))
        bin_data = list(map_data)
        bin_data = [item[2:].zfill(8) for item in bin_data]
        self.data=""
        for i in range(len(bin_data)):
            self.data=self.data+bin_data[i]
        return self.data
    def ham_encoder(self):
        m=len(self.data)
        r=0
        while (2**r-r)<(m+1):
            r+=1
        self.enc_data=""
        pow2=[2**i for i in range(0,r+1)]
        cnt=0
        for i in range(m+r-1,-1,-1):
            if i+1 in pow2:
                self.enc_data+="-"
            else:
                self.enc_data+=self.data[cnt]
                cnt+=1
        self.enc_data=list(self.enc_data[::-1])
        print(self.enc_data)
        rr=[[] for i in range(len(pow2))]
        cnt=0
        for i in pow2[0:-1]:
            pow_cnt=0
            ele=list(range(i,pow2[-1]))
            while pow_cnt<len(ele):
                rr[cnt].append(ele[pow_cnt:pow_cnt+i])
                pow_cnt+=2*i
            cnt+=1
        for i in range(len(rr)):
            rr[i]=[y for x in rr[i] for y in x]
        bits=[[] for i in range(len(rr)-1)]
        cnt=0
        for j in range(len(rr)-1):
            for i in rr[j]:
                if i<=(m+r):
                    bits[cnt].append(self.enc_data[i-1])
            b="".join(bits[cnt][1:])
            cnt1=list(b).count('1')
            self.enc_data[rr[j][0]-1]=str(cnt1%2)
            cnt+=1
        self.data="".join(self.enc_data[:])
    def send(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((self.host,self.port))
            except socket.error as e:
                pass
            sock.listen()
            conn,addr=sock.accept()
            with conn:
                print("connected by:",addr)
                conn.sendall(bytearray(self.data,"utf8"))
data=input("enter data to send:")
send=Sender("127.0.0.1",65432,data,"1001")
print("data in bytes:",send.parity_encoder())
send.ham_encoder()
print("hamming code encoded data:",send.data)
send.send()
