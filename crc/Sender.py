import socket
class Sender:
    def __init__(self,host,port,data,crc,enc_data=""):
        self.host=host
        self.port=port
        self.data=data
        self.crc=crc
        self.enc_data=enc_data
    def parity_encoder(self):
        map_data = map(bin, bytearray(data, "utf8"))
        bin_data = list(map_data)
        bin_data = [item[2:] for item in bin_data]
        for i in range(len(bin_data)):
            self.enc_data=self.enc_data+bin_data[i]
        print(self.enc_data)
        for i in range(0,len(self.crc)-1):
            self.enc_data+="0"
        return self.enc_data
    def crc_encoder(self):
        st=0
        end=len(self.crc)-1
        s1=self.enc_data[st:end+1]
        s2=self.crc
        s3=""
        remi=""
        for i in range(len(self.crc)):
            s3+="0"
        while end<len(self.enc_data):
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
            remi+=self.enc_data[end]
            s1=remi[1:]
            if end==len(self.enc_data)-1:
                if s1[0]==1:
                    s2=s3
                    return self.div(s1,s2)
                else:
                    s2=self.crc
                    return self.div(s1, s2)
                #return s1[len(s1)-(len(self.crc)-1):len(s1)]
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
    def send(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            sock.bind((self.host,self.port))
            sock.listen()
            conn,addr=sock.accept()
            with conn:
                print("connected by:",addr)
                conn.sendall(bytearray(self.data,"utf8"))

data=input("enter data to send:")
send=Sender("127.0.0.1",65432,data,"1101")
print("data in bytes:",send.parity_encoder())
d=send.crc_encoder()
send.data = ""
send.data = send.enc_data[0:len(send.enc_data) - (len(send.crc) - 1)] + d
print("REMAINDER:",d)
print("crc encoded data:",send.data)
send.send()