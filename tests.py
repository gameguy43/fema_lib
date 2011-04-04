import unittest2 as unittest
import urllib

import parser


class TestFEMAParserFunctions(unittest.TestCase):
    # TODO: write a test to assert that we've found all of the metadata fields
    def setUp(self):
        self.use_live_page = False
        self.url_to_live_page = "http://www.fema.gov/photolibrary/photo_details.do?id=20000"
        self.path_to_local_copy = "samples/20000.html"
        self.expected_output = {
            'photo_date' : u"12/05/2005",
            'desc' : u"La Place, LA,  December 5, 2005 - Santa will have to land on the lawn: Shawna and Donnie White won't let a little hurricane damage spoil Christmas. They decorated their home even as they await FEMA assistance to help cover roof repairs.  Photo by Greg Henshall / FEMA", 
            'location' : u"La Place, Louisiana",
            'original_filename' : u"LA_1603_La Place Christmas_0211a.jpg",
            'size' : u"5,004.5 KB",
            'photographer' : u"Greg Henshall",
            'id' : 20000,
            'dimensions' : u"1768x2728",
            'url_to_lores_img':  u'http://www.fema.gov/photodata/low/20000.jpg',
            'url_to_hires_img':  u'http://www.fema.gov/photodata/original/20000.jpg',
            'url_to_thumb_img':  u'http://www.fema.gov/photodata/thumbnail/20000.jpg',
            
            'categories' : [
                u"Miscellaneous",
                u"Hurricane/Tropical Storm"
                ],
            'disasters' : [
                (u"Louisiana Hurricane Rita (DR-1607)",u"http://www.fema.gov/news/event.fema?id=5025"),
                (u"Louisiana Hurricane Katrina (DR-1603)",u"http://www.fema.gov/news/event.fema?id=4808")
                ],
            }
                
        if self.use_live_page:
            self.html =  urllib.urlopen(self.url_to_live_page)
        else:
            fp = open(self.path_to_local_copy,'r')
            self.html = fp.read()
        self.maxDiff = None

    def test_parser_correctness(self):
        actual_output = parser.parse_img(self.html)
        print actual_output
        print self.expected_output
        
        '''
        keys_to_compare = set(actual_output.itervalues()).union(set(self.expected_output.itervalues()))
        for key in keys_to_compare:
            print key
            self.assertEqual(actual_output[key],self.expected_output[key])
        '''
        self.assertDictEqual(parser.parse_img(self.html), self.expected_output)

if __name__ == '__main__':
    unittest.main()
