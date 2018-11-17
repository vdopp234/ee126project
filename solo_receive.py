from Receiver import *
from HuffmanCode import *
from sound import transmit, receive
import reedsolo as rs
import values
a = HuffmanCode()
c = Receiver()

def solo_decode(packet,size,error=5):
    i = 0
    bits = ''
    solomon = rs.RSCodec(error)
    temp = bytearray()
    while i < size // 8:
        temp.append(int(packet[i * 8:(i + 1) * 8], 2))
        i += 1
    try:
        pack = solomon.decode(temp)
        for b in pack:
            bits += bin(b)[2:].rjust(8, '0')
        return bits
    except rs.ReedSolomonError:
        print("Fail")
        return -1


packets = receive(packet_size=8+16+16, baud=values.baud, signal_cf=values.sig_cf, clock_cf=values.clock_cf, fdev=values.delta, fs=values.fs, duration=30, taps=50, width = 200)

count=0
while not c.isDone() and count<len(packets):
    received=packets[count]
    s = ""
    for b in received:
        s+=str(b)
    if len(s) != 8+16+16:
        print('wrong number of bits')
        count+=1
        continue
    temp=solo_decode(s,8+16+16)
    if temp != -1:
        temp = bytearray(temp, 'utf8')
        c.receive_packet(temp)
    count+=1

de=c.decoded_chunks
final = c.blocks_write()
a.decompress(final,  "out.txt")
