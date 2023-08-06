"""Just a test of basic functinality."""
import numpy as np
from pytrr import GroTrrReader

def get_dim(lines):
    return [int(i) for i in lines.strip().split('(')[1][:-2].split('x')]

def read_dump_file(filename):
    """Read gromacs dump of trr"""
    frame = {}
    with open(filename, 'r') as fileh:
        for lines in fileh:
            if lines.find('frame') != -1:
                if 'natoms' in frame:
                    yield frame
                # reset:
                frame = {'box': np.zeros((3,3))}
                frame['frame'] = int(lines.strip().split()[-1][:-1])
            if lines.find('natoms') != -1:
                split = lines.split()
                frame['natoms'] = int(split[1])
                frame['step'] = int(split[3])
                frame['time'] = float(split[4].split('=')[1])
                frame['lambda'] = float(split[-1])
            if lines.find('box[') != -1:
                xyz = lines.strip().split('={')[1][:-1].split(',')
                idx = int(lines.split(']')[0][-1])
                frame['box'][idx] = np.array([float(i) for i in xyz])
            for key in ('x', 'v', 'f'):
                txt = '{} ('.format(key)
                txt2 = '{}['.format(key)
                if lines.find(txt) != -1 and lines.find('box') == -1:
                    dims = get_dim(lines)
                    frame[key] = np.zeros((dims[0], dims[1]))
                elif lines.find(txt2) != -1 and lines.find('box') == -1:
                    xyz = lines.strip().split('={')[1][:-1].split(',')
                    idx = int(lines.split('[')[1].split(']')[0])
                    frame[key][idx] = np.array([float(i) for i in xyz])
    if 'natoms' in frame:
        yield frame
            
                

with GroTrrReader('traj.trr') as trrfile:
    for header, dump in zip(trrfile, read_dump_file('dump.txt')):
        print('At step: {} {}'.format(header['step'], dump['step']))
        data = trrfile.get_data()
        for key in ('x', 'v', 'f'):
            okcoord = np.allclose(data[key], dump[key])
            print('Are {} ok: {}'.format(key, okcoord))
            assert okcoord

