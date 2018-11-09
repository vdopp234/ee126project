from collections import Counter
from heapq import heappush, heappop

def HuffEncode(freq_dict):
    freq = []
    huffman = {}
    for key in freq_dict:
        heappush(freq, ((freq_dict[key]), [key]))
        huffman[key]= ""
    while len(freq) > 1:
        char_1 = heappop(freq)
        char_2 = heappop(freq)
        combined = (char_1[0] + char_2[0], char_1[1] + char_2[1])
        for symbol in char_1[1]:
            huffman[symbol] = "0" + huffman[symbol]
        for symbol in char_2[1]:
            huffman[symbol] = "1" + huffman[symbol]
        heappush(freq, combined)
    return huffman,{v: k for k, v in huffman.items()}
def huffman_compress(incodePath,decodePath):
     with open("sample.txt", 'r+') as file:
        text = file.read()
        text = text.rstrip()
    codes, reverse_mapping = HuffEncode(Counter(text))
    with open(incodePath, 'w') as encode,open(decodePath, 'w') as decode:
        for k, v in codes.items():
            if k=='\n': k='\\n'
            encode.write(str(k) + ' ' + str(v) + '\n')
        for k, v in reverse_mapping.items():
            if v=='\n': v='\\n'
            decode.write(str(k) + ' ' + str(v) + '\n')
def text_huffman(path,reverse=False):
    huffman_tree = {}
    with open(path) as f:
        for line in f:
            (key, val) = line.split()
            huffman_tree[key] = val
    if reverse:
        huffman_tree["10000"] = "\n"
        huffman_tree["01"] = " "
    else:
        huffman_tree["\n"]="10000"
        huffman_tree[" "]="01"
    return huffman_tree
class HuffmanCode(object):
    def compress(self,path):
        with open(path, 'r+') as file:
            text = file.read()
            text = text.rstrip()
            huffman_tree= text_huffman("encode1.txt")
            encoded=''.join([huffman_tree[c] for c in text])
        return encoded
    def decompress(self, text):
        file = "final_file.txt"
        temp = ""
        decoded = ""
        with open(file, 'w') as output:
            huffman_tree= text_huffman("decode1.txt",True)
            for bit in text:
                temp += bit
                if temp in huffman_tree:
                    decoded += huffman_tree[temp]
                    temp = ""
            output.write(decoded)
        return file
