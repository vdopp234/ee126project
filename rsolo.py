import reedsolo as rs

class RS:
    def __init__(self, encode):
        self.encode = encode #Boolean
        self.packet_len = 16+8
        self.codec = rs.RSCodec(self.packet_len)
    def encode(self, m):
        if not self.encode:
            return 'Not Encoder'
        return self.codec.encode(m)
    def decode(self, m):
        '''
        Returns none if message is not decodable (>n/2 errors)
        Else, returns message
        '''
        if self.encode:
            return 'not decoder'
        try:
            a = self.codec.decode(m)
        except rs.ReedSolomonError():
            return None
        return a
