from Receiver import *
from Transmitter import *
from HuffmanCode import *
from checksum import *
from sound import transmit, receive
#create huffman code
#huffman_compress("encode.txt","decode.txt")
a = HuffmanCode()
encode=a.compress("test.txt")

#create packet
b = Transmitter(encode)
chunks=b.chunks
packet = b.encode()
final_packet=[]
for p in packet:
    check=Packet(p)
    final_packet.append(check.get_final_packet())

print(final_packet[0])
print(final_packet[0][24:])
#print('sent')
#send file
c = Receiver()
count = 0
while not c.isDone() and count<len(packet):
    received=final_packet[count]
    #print(received)
    #print(received)
    check=Packet(received, sent = True)
    if check.check_checksum():
        #print(check.get_received_packet())
        temp=check.get_received_packet()
        if count == 0:
            print(temp)
        temp=bytearray(temp,'utf8')
        #print(temp)
        c.receive_packet(temp)
    count+=1
de=c.decoded_chunks

# #check chunks
# for i in range(len(chunks)):
#     assert len(chunks[i])==len(de[i])
#     for j in range(len(chunks[i])):
#         assert chunks[i][j]==de[i][j]

huffman=c.blocks_write()

# # check huffman code
# assert  len(huffman)==len(encode)
# for i in range(len(huffman)):
#     assert huffman[i]==encode[i]

a.decompress(huffman,"huffman.txt")
