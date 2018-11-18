#from pyldpc.codingfunctions import Coding
from pyldpc.ldpcalgebra import BinaryProduct
from pyldpc.ldpcmatrices import RegularH
from pyldpc.decodingfunctions import Decoding_BP

from scipy.sparse import csr_matrix as c_mat
import numpy as np

'''
Code for LDPC Codes
Interested in sending x, our packet, across the chnl.
Tranmission: Augmented packet y are sent across chnl.
Decoding: Augmented packet y and prior distribution on x is used to predict what original message x was.
'''

def string_to_numpy(s):
    l = []
    for i in range(len(s)):
        l.append(int(i))
    return np.array([l])

def encode(H, x):
    '''
    H = sparse matrix to augment packet being sent across with "checksum" type vector y
    Returns y vector given packet x
    '''
    if H == None:
        H = RegularH(24, 12, 14) #want same matrix for encode, decode
    #n, k = H.shape
    d = BinaryProduct(H, x)
    return d, x

def decode(H, y, SNR = 1.5):
    '''
    Carries out Belief Propagation algorithm for 5 iterations, returns the result
    '''
    if H == None:
        H = RegularH(24, 12, 14)
    return Decoding_BP(H, y, SNR, max_iter = 5)
