import numpy as np
import random

class Packet:
    def __init__(self, input, sent = False):
        '''
        input = String input of bits, length 16 + 8 + 16 + 8 representing xor of packets
            - Last 32 bits corresponds to the metadata
        '''
        self.sent=sent
        if not isinstance(input, str):
            self.input = byte2str = str(input)[str(input).find('\'') + 1:-2]
        else:
            self.input = input
        if not sent:
            self.extra_bits = ''
            for _ in range(16):
                self.extra_bits += str(random.randint(0, 1))
            self.chunk_size = 8
            self.data_len = self.chunk_size * 2
            self.data = [self.input[:self.chunk_size], self.input[self.chunk_size:self.chunk_size*2]]
            self.meta_data = self.input[self.data_len:]
            self.total_data = list(self.data)
            self.total_data.append(self.meta_data)
            self.total_data.append(self.extra_bits[:self.chunk_size])
            self.total_data.append(self.extra_bits[self.chunk_size:])
            #self.total_data.append(self.meta_data[self.chunk_size:])
            self.checksum = self.get_checksum() #16 bits
        else:
            self.packet_size = 16
            self.chunk_size = 8
            self.sent = True
            self.extra_bits = self.input[:self.chunk_size*2]
            self.checksum = self.input[self.chunk_size*2:self.chunk_size*3]
            self.data = [self.input[self.chunk_size*3:self.chunk_size*4], self.input[self.chunk_size*4:self.chunk_size*5]]
            self.total_data = list(self.data)
            self.total_data.append(self.checksum)
            self.total_data.append(self.extra_bits[:self.chunk_size])
            self.total_data.append(self.extra_bits[self.chunk_size:])
            self.meta_data = self.input[self.chunk_size*5:]
            self.total_data.append(self.meta_data)

    def get_final_packet(self):
        '''
        Returns packet in the following order:
        extra_bits + checksum + data + meta_data
        '''
        out = ''
        for d in self.data:
            out += d
        #print(self.checksum)
        c = ''
        for a in self.checksum:
            c += str(a)
        return self.extra_bits + c + out + self.meta_data

    def get_received_packet(self):
        '''
        Returns data+metadata of received packet, in that order
        '''
        if self.sent == False:
            raise Exception('Must be received packet')

        #return self.input[self.chunk_size*3:self.chunk_size*5]
        return self.input[len(self.extra_bits) + len(self.checksum):]

    def get_complement_sum(self, one, two):
        '''
        Determines complement sum of two equal-sized binary numbers
        Helper function for get_checksum
        '''
        out = [0 for _ in range(self.chunk_size)]
        carry = 0
        #print(one, two)
        one = [int(i) for i in one]
        x = list(two)
        two = [int(i) for i in two[0]]
        #Regular bitwise addition
        for i in range(self.chunk_size):
            i = -(i+1) % self.chunk_size
            out[i] = (one[i] + two[i] + carry) % 2
            carry = max(0, (one[i] + two[i] + carry)//2)

        #Preprocessing for carryover
        one = list(out)
        two = bin(carry)[2:]
        new_two = ''
        for i in range(len(two)):
            if i == len(two) - 1:
                new_two += two[i]
            else:
                new_two += (two[i] + ' ')
        two = new_two.split()
        two = [int(i) for i in two]
        #Carryover addition
        carry = 0
        x = [0 for _ in range(self.chunk_size - len(two))]
        x.extend(two)
        two = x
        #print(out, two)
        for i in range(self.chunk_size):
            i = -(i+1)%self.chunk_size
            out[i] = (one[i] + two[i] + carry) % 2
            carry = max(0, (one[i] + two[i] + carry) - 1)
        #print(out)
        return np.array(out)

    def get_checksum(self):
        '''
        Input: Chunks xor'd together, broken into 16-bit length strings
        Output: Internet checksum of these chunks
        '''
        curr_checksum = np.zeros(self.chunk_size)
        chunks = self.total_data
        # for i in range(len(self.data)//self.chunk_size):
        #     chunks.append(self.data[self.chunk_size*i:self.chunk_size*(i+1)])
        # Converts string to bit array
        for i in range(len(chunks)):
            new_chunk = ''
            chunk = chunks[i]
            for j in range(len(chunk)):
                new_chunk += (chunk[j] + ' ')
            chunks[i] = new_chunk
        chunks = [np.array([chunk.split()]) for chunk in chunks]
        #print(len(chunks))
        #print(chunks)
        # print(chunks.pop())
        # print(chunks.pop())
        # print(chunks.pop())
        #print(len(chunks))
        #print(chunks)
        for chunk in chunks:
            curr_checksum = self.get_complement_sum(curr_checksum, chunk)
        for i in range(len(curr_checksum)):
            curr_checksum[i] = 1 - curr_checksum[i]
        return curr_checksum

    def check_checksum(self):
        '''
        Checks to see if packet was corrupted in transmission
        '''
        if not self.sent:
            return None
        chunks = list(self.total_data)
        for i in range(len(chunks)):
            new_chunk = ''
            chunk = chunks[i]
            for j in range(len(chunk)):
                new_chunk += (chunk[j] + ' ')
            chunks[i] = new_chunk
        chunks = [np.array([chunk.split()]) for chunk in chunks]
        h = np.zeros(self.chunk_size)
        #print(chunks)
        for chunk in chunks:
            h = self.get_complement_sum(h,chunk)
        return all(h == np.ones(self.chunk_size))
#Debugging
#
#
input = '100010101010001101010101'
a = Packet(input)
s = ''
c = (a.checksum)
for c1 in c:
    s += str(c1)
x = a.extra_bits
#
# print(type(x))
# print(type(c))
# print(type(input))
#
b = Packet(x+s+input, sent = True)
print(b.check_checksum())
