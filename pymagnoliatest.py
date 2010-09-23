# -*- coding: utf-8 -*-

##
# License: bsd license. 
# See 'license.txt' for more informations.
#	

import unittest
from pymagnolia import *
import time

API_KEY = 'your api key here(fail if api key is not mine...)'

class TestUtilityFunction(unittest.TestCase):

  def test_set_data_1(self):
    d = {'a': None, 'str': 'test', 'empty_str': '', 'lst': [1], 'empty_lst': []}
    param = parametalize(d)
    self.assert_(param.has_key('a') == False)
    self.assert_(param.has_key('str'))
    self.assert_(param.has_key('empty_str') == False)
    self.assert_(param.has_key('lst'))
    self.assert_(param.has_key('empty_lst') == False)

  def test_set_data_self(self) :
    d = {'a': None, 'self': 'test', 'empty_str': '', 'lst': [1], 'empty_lst': []}
    param = parametalize(d)
    self.assert_(param.has_key('a') == False)
    self.assert_(param.has_key('self') == False)
    self.assert_(param.has_key('lst'))

  def test_set_data_special_key(self) :
    d = {'a': None, 'self': 'test', 'empty_str': '', 'date_to': '2006-05-14', 'date_from': '2006-05-14'}
    param = parametalize(d)
    self.assert_(param.has_key('a') == False)
    self.assert_(param.has_key('date_to') == False)
    self.assert_(param.has_key('date_from') == False)
    self.assert_(param.has_key('to'))
    self.assert_(param.has_key('from'))

class TestBookmark(unittest.TestCase) :

  def test_default(self):
    b = Bookmark()
    self.assert_(b.created == None)
    self.assert_(b.private == False)
    self.assert_(b.updated == None)
    self.assert_(b.id == '')
    self.assert_(b.rating == '0')
    self.assert_(b.owner == '')
    self.assert_(b.title == '')
    self.assert_(b.url == '')
    self.assert_(b.description == '')
    self.assert_(b.screenshot == '')
    self.assert_(b.tags == [])

class TestApi(unittest.TestCase) :
  api = None

  def setUp(self) :
    self.api = MagnoliaApi(API_KEY)

  def test_get(self) :
    bms = self.api.bookmarks_get(id='recithe')
    self.assert_(len(bms) == 1)
    bm = bms[0]
    self.assert_(bm.created[0:10] == '2006-05-08')
    self.assert_(bm.updated[0:10] == '2006-05-23')
    self.assert_(bm.id == 'recithe')
    self.assert_(bm.rating == '4')
    self.assert_(bm.owner == 'everes')
    self.assert_(bm.title == 'everes.net | スパムとか')
    self.assert_(bm.url == 'http://www.everes.net/')
    self.assert_(bm.description == 'スパムとか')
    self.assert_(bm.screenshot == 'http://scst.srv.girafa.com/srv/i?i=sc010159&r=http://www.everes.net/&s=bf13b56ca4a1184e')
    self.assert_(len(bm.tags) == 3)
    self.assert_(bm.tags[0] == 'django' or bm.tags[1] == 'django' or bm.tags[2] == 'django')
    self.assert_(bm.tags[0] == 'rhaco' or bm.tags[1] == 'rhaco' or bm.tags[2] == 'rhaco')
    self.assert_(bm.tags[0] == 'blog' or bm.tags[1] == 'blog' or bm.tags[2] == 'blog')

  def test_get_notfound(self) :
    try :
      bms = self.api.bookmarks_get(id='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    except PyMagnoliaError, e :
      self.assert_(e.code == '1110')
      self.assert_(e.message == 'One or more bookmark not found.')

  def test_find(self) :
    bms = self.api.bookmarks_find(tags='django', limit='5')
    self.assert_(len(bms) == 5)
    for bm in bms:
      self.assert_(bm.tags.index('django') >= 0)
  def test_find_by_owner(self) :
    bms = self.api.bookmarks_find(person='myself', limit='10')
    self.assert_(len(bms) > 5)
    for bm in bms:
      self.assert_(bm.owner == 'everes')
  def test_find_by_group(self) :
    bms = self.api.bookmarks_find(group='rhaco', limit='4')
    self.assert_(len(bms) > 0)
  def test_find_by_rating(self) :
    bms = self.api.bookmarks_find(person='myself', rating='5', limit='1')
    self.assert_(len(bms) > 0)
    for bm in bms:
      self.assert_(bm.rating == '5')
  def test_find_by_data_from(self) :
    bms = self.api.bookmarks_find(date_from='2006-05-01T00:00Z', limit='5')
    self.assert_(len(bms) > 0)
    for bm in bms:
      self.assert_(bm.created[0:4] == '2006' and bm.created[5:7] == '05')
  def test_find_by_data_to(self) :
    bms = self.api.bookmarks_find(person='myself', date_to='2005-03-17T00:00Z', limit='30')
    self.assert_(len(bms) < 25)
    for bm in bms:
      self.assert_(bm.created[0:4] == '2005' and bm.created[5:7] == '03')
  def test_find_by_url(self) :
    bms = self.api.bookmarks_find(url='http://www.everes.net/', limit='30')
    self.assert_(len(bms) > 0)
    for bm in bms:
      self.assert_(bm.url == 'http://www.everes.net/')

  def test_crud(self) :
    target = self.api.bookmarks_find(url='http://sourceforge.net/projects/workstyle-py/', person='myself')
    if len(target) > 0:
      print 'test url is already exist(%d).So it should be deleted and done' % len(target)
      for t in target :
        self.api.bookmarks_delete(id=t.id)
    bms = self.api.bookmark_add(title='WorkStyle-py',
                                 description='GTD Web Application. WorkStyle with python(Django)',
                                 url='http://sourceforge.net/projects/workstyle-py/',
                                 tags='django',
                                 rating='4')
    self.assert_(len(bms) == 1)
    id = bms[0].id
    bms = self.api.bookmark_update(id=id, rating='5')
    self.assert_(bms[0].rating == '5')
    self.api.bookmarks_tags_add(id=id, tags='test')
    bms = self.api.bookmarks_get(id=id)
    self.assert_(bms[0].tags.index('test') >= 0)
    self.api.bookmarks_tags_rename(id=id, old='test', new='test2')
    bms = self.api.bookmarks_get(id=id)
    self.assert_(bms[0].tags.index('test2') >= 0)
    try :
      bms[0].tags.index('test')
    except ValueError :
      pass
    else :
      fail("test tag is not removed")
    #[10100] Method not found
    self.api.bookmarks_tags_delete(id=id, tags='test2')
    bms = self.api.bookmarks_get(id=id)
    try :
      bms[0].tags.index('test2')
    except ValueError :
      pass
    else :
      fail("test tag is not removed")
    self.api.bookmarks_delete(id=id)
    try :
      self.api.bookmarks_get(id=id)
    except PyMagnoliaError :
      pass
    else :
      fail("failed to delete bookmark")


if __name__ == '__main__':
    unittest.main()
