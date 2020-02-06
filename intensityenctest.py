# Created by Anlan Zhang on 02/06/2020
# email: zhan6841@umn.edu

import TrakoDracoPy
import struct
import numpy as np
from time import time

class DracoCodec(object):
    def __init__(self, cl, qb):
        self.cl = cl
        self.qb = qb
        self.pc = []
        self.total_points = 0
        self.pos_buf = None
        self.intensity_buf = None
        self.decoded_pc = None

    def load_data(self, filename):
        f = open(filename, 'rb')
        self.pc = []
        self.total_points = 0
        while(True):
            point = f.read(16)
            if not point:
                break
            point = list(struct.unpack('ffff', point))
            #print(point)
            self.pc.append(point)
            self.total_points += 1
        f.close()
        self.pc = np.asarray(self.pc).astype(np.float32)
        # print(self.pc)
        # np.savetxt('result.xyz', self.pc[:, 0:4], fmt='%.6f')

    def encode(self):
        print(self.pc[:, 0:3].shape)
        input_buf = self.pc[:, 0:3].reshape((self.total_points*3, 1))
        print(input_buf.shape)
        self.pos_buf = TrakoDracoPy.encode_point_cloud_to_buffer(input_buf, position=True, 
            sequential=False, remove_duplicates=False, quantization_bits=self.qb, compression_level=self.cl,
            quantization_range=-1, quantization_origin=None, create_metadata=False)
        input_buf = self.pc[:, 3:4].reshape((self.total_points, 1))
        self.intensity_buf = TrakoDracoPy.encode_point_cloud_to_buffer(input_buf, position=False, 
            sequential=False, remove_duplicates=False, quantization_bits=self.qb, compression_level=self.cl,
            quantization_range=-1, quantization_origin=None, create_metadata=False)
        compression_percentage = (len(self.pos_buf) + len(self.intensity_buf)) / (16.0 * self.total_points)
        print('compression percentage:', compression_percentage)

    def decode(self):
        decoded_pos = TrakoDracoPy.decode_point_cloud_buffer(self.pos_buf)
        decoded_pos = np.asarray(decoded_pos.points).astype(np.float32).reshape((self.total_points, 3))
        # print(len(decoded_pos.points))
        decoded_intensity = TrakoDracoPy.decode_point_cloud_buffer(self.intensity_buf)
        decoded_intensity = np.asarray(decoded_intensity.points).astype(np.float32).reshape((self.total_points, 1))
        # print(len(decoded_intensity.points))
        self.decoded_pc = np.concatenate((decoded_pos, decoded_intensity), axis=1)
        # print(decoded_pc.shape)
        # np.savetxt('out.xyz', self.decoded_pc[:, 0:4], fmt='%.6f')

    def compare(self):
        if(self.pc.shape != self.decoded_pc.shape):
            print('The input and output have different shapes.')
            exit(-1)
        for i in range(self.pc.shape[1]):
            raw = list(self.pc[:, i:(i+1)])
            compressed = list(self.decoded_pc[:, i:(i+1)])
            raw.sort()
            compressed.sort()
            diff = []
            count = 0
            for j in range(len(raw)):
                diff.append(float(format(float(compressed[j]), '.3f')) - float(format(float(raw[j]), '.3f')))
                if(diff[-1] < 0.001 and diff[-1] > -0.001):
                    count += 1
            print('Dimension:', i)
            print('equal:', diff.count(0.0))
            print("(-0.001, 0.001)", count)

    def save_decoded_pc(self, filename, ext):
        if(ext == '.xyz'):
            np.savetxt(filename + ext, self.decoded_pc[:, 0:4], fmt='%.6f')
        elif(ext == '.bin'):
            f = open(filename + ext, 'wb')
            for i in range(self.decoded_pc.shape[0]):
                for j in range(self.decoded_pc.shape[1]):
                    item = struct.pack('f', self.decoded_pc[i][j])
                    f.write(item)
            f.close()
        else:
            print('Unknown extension.')

    def save_raw_pc(self, filename, ext):
        if(ext == '.xyz'):
            np.savetxt(filename + ext, self.pc[:, 0:4], fmt='%.6f')
        elif(ext == '.bin'):
            f = open(filename + ext, 'wb')
            for i in range(self.pc.shape[0]):
                for j in range(self.pc.shape[1]):
                    item = struct.pack('f', self.pc[i][j])
                    f.write(item)
            f.close()
        else:
            print('Unknown extension.')

if __name__ == "__main__":
    codec = DracoCodec(10, 18)
    codec.load_data('testdata_files/0000000000.bin')
    start = time()
    codec.encode()
    end = time()
    print('encoding time:', (end - start) * 1000.0)
    start = time()
    codec.decode()
    end = time()
    print('decoding time:', (end - start) * 1000.0)
    codec.compare()
    codec.save_raw_pc('testdata_files/in', '.bin')
    codec.save_decoded_pc('testdata_files/out', '.bin')
    codec.save_raw_pc('testdata_files/in', '.xyz')
    codec.save_decoded_pc('testdata_files/out', '.xyz')