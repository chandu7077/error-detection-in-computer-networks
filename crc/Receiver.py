import socket
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
        print("recieved bytes:",self.data)
    def crc_decoder(self):
        st=0
        end=len(self.crc)-1
        s1=self.data[st:end+1]
        s2=self.crc
        s3=""
        remi=""
        for i in range(len(self.crc)):
            s3+="0"
        while end<len(self.data):
            rem=""
            for i in range(0,len(self.crc)):
                b1=int(s1[i])
                b2=int(s2[i])
                b1=b1+b2
                c=str(b1%2)
                rem+=c
                remi=rem
            if remi[1]=="0":
                s2=s3
            else:
                s2=self.crc
            end=end+1
            remi+=self.data[end]
            s1=remi[1:]
            if end==len(self.data)-1:
                if s1[0] == 1:
                    s2 = s3
                    return self.div(s1, s2)
                else:
                    s2 = self.crc
                    return self.div(s1, s2)
        return remi
    def div(self,s1,s2):
        rem=""
        for i in range(0,len(self.crc)):
            b1 = int(s1[i])
            b2 = int(s2[i])
            b1 = b1 + b2
            c = str(b1 % 2)
            rem += c
        return rem[1:]
recv=Receiver("127.0.0.1",65432,"1101")
recv.receive()
rem=recv.crc_decoder()
print("REMAINDER:",rem)
rem=int(rem)
if rem==0:
    print("data arrived successfully")
else:
    print("data corrupted")

