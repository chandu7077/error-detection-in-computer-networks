import socket
class Sender:
    def __init__(self,host,port,data,enc_data=""):
        self.host=host
        self.port=port
        self.data=data
        self.enc_data=enc_data
    def parity_encoder(self):
        map_data = map(bin, bytearray(data, "utf8"))
        bin_data = list(map_data)
        bin_data = [item[2:].zfill(7) for item in bin_data]
        print(bin_data)
        for i in range(len(bin_data)):
            cnt=bin_data[i].count("1")
            bin_data[i]=bin_data[i]+(str(cnt%2))
        for i in range(len(bin_data)):
            self.enc_data=self.enc_data+bin_data[i]
        return self.enc_data
    def send(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            sock.bind((self.host,self.port))
            sock.listen()
            conn,addr=sock.accept()
            with conn:
                print("connected by:",addr)
                conn.sendall(bytearray(self.enc_data,"utf8"))
data=input("enter data to send:")
send=Sender("127.0.0.1",65432,data)
print(send.parity_encoder())
send.send()



