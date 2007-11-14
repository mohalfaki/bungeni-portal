# -*- coding: utf-8 -*-
#
# File: testInterfaces.py
#
# Copyright (c) 2007 by []
# Generator: ArchGenXML Version 2.0-beta5
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Jean Jordaan <jean.jordaan@gmail.com>"""
__docformat__ = 'plaintext'

#
# Interface tests
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Interface import Implements

from Products.Bungeni.tests.testBungeni import testBungeni


from Interface.Verify import verifyClass


from Products.Bungeni.interfaces.IMemberOfParliament import IMemberOfParliament




from Products.Bungeni.interfaces.IClerk import IClerk





class testInterfaces(testBungeni):
        
    def testInterfacesForIMemberOfParliament(self):
        '''test interface compliance for class IMemberOfParliament'''

        
        for iface in Implements.flattenInterfaces(getattr(testInterfaces,'__implements__',[])):
            self.failUnless(verifyClass(iface, IMemberOfParliament))
        
    
            
    def testInterfacesForIClerk(self):
        '''test interface compliance for class IClerk'''

        
        for iface in Implements.flattenInterfaces(getattr(testInterfaces,'__implements__',[])):
            self.failUnless(verifyClass(iface, IClerk))
        
    
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testInterfaces))
    return suite

if __name__ == '__main__':
    framework()


