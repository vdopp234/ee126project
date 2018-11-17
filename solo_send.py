import reedsolo as rs
from Transmitter import *
from HuffmanCode import *
from Receiver import *
from sound import transmit, receive
from bitarray import bitarray
import sounddevice as sd
import values

def solo_encode(packet,size,error=5):
    if not isinstance(packet, str):
        packet = str(packet)[str(packet).find('\'') + 1:-2]
    i = 0
    bits = ''
    solomon = rs.RSCodec(error)
    temp = bytearray()
    while i < size // 8:
        temp.append(int(packet[i * 8:(i + 1) * 8], 2))
        i += 1
    pack = solomon.encode(temp)
    for b in pack:
        bits += bin(b)[2:].rjust(8, '0')
    return temp


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
    except:
        print("Fail")
        return -1


a = HuffmanCode()
encode=a.compress("test.txt")

b = Transmitter(encode)
chunks=b.chunks
packet = b.encode()
bits=''
packet_size=3*8
for p in packet:
    bits+=solo_encode(p, packet_size)


#
# pack=[]
# for i in range(len(bits)//(5*8)):
#     pack.append(bits[i*(5*8):(i+1)*(5*8)])
#
# final=''
# c=Receiver()
# for p in pack:
#     temp = solo_decode(p, 8 + 16 + 16)
#     if temp != -1:
#         temp = bytearray(temp, 'utf8')
#         print("received", temp)
#         c.receive_packet(temp)
#
# de=c.decoded_chunks
# f = c.blocks_write()
# a.decompress(f,  "out.txt")
#
#

print("sending")
transmit(bitarray(bits), baud=values.baud, signal_cf=values.sig_cf, clock_cf=values.clock_cf, fdev=values.delta, fs=values.fs, packet_size=32)

sd.wait()
