import sqlalchemy as rdb
from datetime import datetime
from sqlalchemy.orm import mapper, relation, column_property
from zope.interface import implements
from marginalia.interfaces import IMarginaliaAnnotation
from marginalia.tools.SequenceRange import SequenceRange, SequencePoint
from marginalia.tools.XPathRange import XPathRange, XPathPoint

metadata = rdb.MetaData()

annotations_table = rdb.Table(
    "annotations",
    metadata,
    rdb.Column('id', rdb.Integer, primary_key=True),  
    rdb.Column("url", rdb.Unicode(), nullable=False),
    rdb.Column("start_block", rdb.Unicode(80), nullable=False),
    rdb.Column("start_xpath", rdb.Unicode(80), nullable=False),
    rdb.Column("start_word", rdb.Unicode(80), nullable=False),
    rdb.Column("start_char", rdb.Unicode(80), nullable=False),
    rdb.Column("end_block", rdb.Unicode(80), nullable=False),
    rdb.Column("end_xpath", rdb.Unicode(80), nullable=False),
    rdb.Column("end_word", rdb.Unicode(80), nullable=False),
    rdb.Column("end_char", rdb.Unicode(80), nullable=False),
    rdb.Column("note", rdb.Unicode()), 
    rdb.Column("access", rdb.Unicode(80), nullable=False),
    rdb.Column("action", rdb.Unicode(80)),
    rdb.Column("edit_type", rdb.Unicode(80), nullable=False),
    rdb.Column("quote", rdb.Unicode()),
    rdb.Column("quote_title", rdb.Unicode()),
    rdb.Column("quote_author", rdb.Unicode(80), nullable=False),
    rdb.Column("link_title", rdb.Unicode(80)),
    rdb.Column("link", rdb.Unicode()),
   )
   
class AnnotationMaster(object):
    """Annotation Master Class."""

    def __repr__(self):
        return '<Annotation %s>'%(self.id)

    def modification_date(self):
        return '2008/12/12 12:12:12'
    #def getUserName(self):
    #    # XXX haaaack replace with a view class ..
    #    return self.getOwner().getUserName()

    #def Title(self):
    #    return self.getNote()

    #def Description(self):
    #    return '"%s" annotated this text:\n\n"%s"\n\nas follows:\n\n"%s"' % ( self.getUserName(), self.getQuote(), self.getNote() )


    def indexed_url(self):
        """ There may be more than one annotatable area on a page,
        identified by fragment (#1, #2, ...). Annotations are queried
        per page (#*), so catalog under the page URL.

        Note that the URL includes the server name, so if the server is
        accessed with different names, annotations will be partitioned
        per name.
        
        TODO: Use config settings to strip server name.
        """
        url = self.url
        if url.find('#') != -1:
            url = url[:url.index('#')]
        return url

    def getLink(self):
        """Returns the reference link."""
        if hasattr(self, 'hyper_link'):
            return self.hyper_link
        return self.link
    
        
    def getSequenceRange(self):
        startBlock = self.start_block
        startWord = self.start_word
        startChar = self.start_char
        endBlock = self.end_block
        endWord = self.end_word
        endChar = self.end_char
        sequenceRange = SequenceRange()
        sequenceRange.start = SequencePoint(startBlock, startWord, startChar)
        sequenceRange.end = SequencePoint(endBlock, endWord, endChar)
        return sequenceRange
        
    def getXPathRange(self):
        startXPath = self.start_xpath
        startWord = self.start_word
        startChar = self.start_char
        endXPath = self.end_xpath
        endWord = self.end_word
        endChar = self.end_char
        xpathRange = XPathRange()
        xpathRange.start = XPathPoint(startXPath, startWord, startChar)
        xpathRange.end = XPathPoint(endXPath, endWord, endChar)
        return xpathRange


mapper(AnnotationMaster, annotations_table)
    
if __name__=='__main__':
    from sqlalchemy import create_engine    
    engine = create_engine("postgres://localhost/bungeni", echo=True)
    metadata.create_all(engine)

    
