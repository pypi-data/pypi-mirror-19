import unittest
import os
import sys
sys.path.insert(0, '../')
import starseqr_utils as su

path = os.path.dirname(__file__)
if path != '':
    os.chdir(path)


class SamTestCase(unittest.TestCase):
    '''Tests sam conversion'''

    def test_gtf2genepred_v1(self):
        """test gtf to genepred"""
        mysam = os.path.realpath("test_data/test.Chimeric.out.sam")
        mybam = os.path.realpath("test_data/test.Chimeric.out.bam")
        os.remove(mybam) if os.path.exists(mybam) else None
        su.common.sam_2_coord_bam(mysam, mybam, int(1))
        assert os.path.exists(mybam) == 1

if __name__ == '__main__':
    unittest.main()
