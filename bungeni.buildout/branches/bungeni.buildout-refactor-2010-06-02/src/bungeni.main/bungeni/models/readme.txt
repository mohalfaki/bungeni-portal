-------------
Bungeni Model
-------------

Setup
-----

some setup for tests
   >>> from zope import component
   >>> from ore.alchemist import Session
   >>> from bungeni import models as model
   >>> import datetime
   >>> from sqlalchemy.orm import mapper
   >>> from bungeni.models import domain, schema
   >>> import bungeni.models.testing
   >>> db = bungeni.models.testing.setup_db()
   >>> session = Session()

region, country, province
--------------------------
get some values in those tables as they are needed later on

 >>> country = model.Country()
 >>> country.country_id = 'KE'
 >>> country.country_name = u"Kenya"
 >>> country.iso_name = u"KENYA" 
 >>> country.language = "en" 
 >>> session.add(country)
 >>> session.flush()
 >>> country.country_id
 'KE'
 >>> country.country_name
 u'Kenya'

Regions and provinces get their primary key with a db sequence:
 
 >>> region = model.Region()
 >>> region.region = u"Nairobi"
 >>> region.language = "en" 
 >>> session.add(region)
 >>> session.flush() 
 >>> region.region_id
 1L
 >>> province = model.Province()
 >>> province.province= u"Central"
 >>> province.language = "en" 
 >>> session.add(province)
 >>> session.flush()
 >>> province.province_id
 1L

Users
-----

First we can create some users.

  >>> user = model.User("jsmith")
  >>>

Members of Parliament
---------------------

  >>> mp_1 = model.User(u"mp_1", 
  ...        first_name=u"a", 
  ...        last_name=u'ab', 
  ...        birth_country="KE",
  ...        email=u"mp1@example.com", 
  ...        date_of_birth=datetime.datetime.now(),
  ...        language="en",
  ...        gender='M')
  >>> mp_2 = model.User(u"mp_2", 
  ...        first_name=u"b", 
  ...        last_name=u"bc", 
  ...        birth_country="KE",
  ...        date_of_birth=datetime.datetime.now(),
  ...        email=u"mp2@example.com",
  ...        language="en",
  ...        gender='M')
  >>> mp_3 = model.User(u"mp_3",
  ...        first_name=u"c", 
  ...        birth_country="KE",
  ...        last_name=u"cd",
  ...        date_of_birth=datetime.datetime.now(),
  ...        email=u"mp3@example.com", 
  ...        language="en",
  ...        gender='F')

Groups
------

Bungeni uses groups to model any collection of users. The relational inheritance
features of sqlalchemy to allow for subclassing group, with value storage in a 
different table. Bungeni uses this feature to model parliaments, committees, 
political parties, etc. Let's create some groups in the system to examine how
they work.

  >>> parliament = model.Parliament( short_name=u"p_1", start_date=datetime.datetime.now(), election_date=datetime.datetime.now())
  >>> parliament.language = "en"
  >>> session.add( parliament )
  >>> session.flush()
  
  >>> political_party_a = model.PoliticalParty(short_name=u"pp_1", start_date=datetime.datetime.now())
  >>> political_party_a.parent_group_id = parliament.parliament_id
  >>> political_party_a.language = "en"
  >>> political_party_b = model.PoliticalParty(short_name=u"pp_2", start_date=datetime.datetime.now())
  >>> political_party_b.parent_group_id = parliament.parliament_id
  >>> political_party_b.language = "en"
  >>> session.add(political_party_a)
  >>> session.add(political_party_b)
  >>> session.add( mp_1 )
  >>> session.add( mp_2 )
  >>> session.add( mp_3 )
  >>> session.flush()
  
  >>> committee_a = model.Committee(short_name=u"commitee_1", start_date=datetime.datetime.now())
  >>> committee_a.parent_group_id = parliament.parliament_id
  >>> committee_a.language = "en"
  >>> session.add(committee_a)
  >>> session.flush()
    
A user is associated to a group via a membership, where we can store additional properties, such
as a user's role/title in a group.

Let's create some memberships and see what we can do with them.

  >>> for mp in [ mp_1, mp_2, mp_3 ]:
  ...    membership = model.GroupMembership()
  ...    membership.user = mp
  ...    membership.group = parliament
  ...    membership.language = "en"
  ...    session.add( membership )
  ...    membership = model.GroupMembership()
  ...    membership.user = mp
  ...    membership.group = political_party_a
  ...    membership.language = "en"
  ...    session.add( membership )
  


  >>> #session.add( membership )

Check that we can access the membership through the containment object

  >>> session.flush()
  >>> len( list( parliament.members ) )
  3

Government
----------
  >>> gov = model.Government(short_name=u"gov_1", start_date=datetime.datetime.now())
  >>> gov.parent_group_id = parliament.parliament_id
  >>> gov.language = "en"
  >>> session.add(gov)
  >>> session.flush()
  >>> gov.parent_group
  <bungeni.models.domain.Parliament object at ...>


Ministries
-----------
  >>> ministry = model.Ministry(short_name=u"ministry", start_date=datetime.datetime.now())
  >>> ministry.parent_group_id = gov.group_id
  >>> ministry.language = "en"
  >>> session.add(ministry)
  >>> session.flush()
  >>> ministry.parent_group
  <bungeni.models.domain.Government object at ...>
  
  >>> gov.contained_groups
  [<bungeni.models.domain.Ministry object at ...>]


Groups in a parliament:
-----------------------
  >>> from bungeni.models.utils import get_all_group_ids_in_parliament
  >>> pgroups = get_all_group_ids_in_parliament(parliament.parliament_id)
  
  >>> len(pgroups)
  6





Constituencies
-----------------
Constituencies have a fk on regions and provinces:

  >>> constituency = model.Constituency()
  >>> constituency.name = u"Nairobi/Westlands"
  >>> constituency.region_id = region.region_id
  >>> constituency.province_id = province.province_id
  >>> constituency.start_date = datetime.datetime.now()
  >>> constituency.language = "en"

  >>> session.add(constituency)
  >>> session.flush()
 
check the pk if it was saved and pk sequence is working

 >>> constituency.constituency_id
 1L
 

 

Role title names

  >>> mrt1 = model.MemberTitle()
  >>> mrt1.user_type = 'memberofparliament'
  >>> mrt1.user_role_name = u"President"
  >>> mrt1.user_unique = True
  >>> mrt1.sort_order = 10
  >>> mrt1.language = "en"
  >>> session.add(mrt1)
  >>> session.flush()
    
 
Members of parliament
----------------------
Members of parliament are defined by their membership in
the parliaments group and additional attributes.


  >>> mp4 = model.MemberOfParliament()
  >>> mp4.group_id = parliament.group_id
  >>> mp4.user_id = mp_1.user_id
  >>> mp4.start_date = datetime.datetime.now()
  >>> mp4.constituency_id = constituency.constituency_id
  >>> mp4.constituency = constituency
  >>> mp4.elected_nominated = 'E'
  >>> mp4.language = "en"
  >>> session.add(mp4)
  >>> session.flush()
  >>> mp4.membership_id
  7L

Titles of Members
------------------
Members have a title in their groups

  >>> mt1 = model.MemberRoleTitle()
  >>> mt1.membership_id = mp4.membership_id
  >>> mt1.title_name_id = 1
  >>> mt1.start_date = datetime.datetime.now()
  >>> mt1.title_name_id = mrt1.user_role_type_id
  >>> session.add(mt1)
      
  
Sittings
--------

any group can schedule a sitting, a sitting is treated as a physical
meeting of the group by the system. 

 >>> st = model.SittingType()
 >>> st.sitting_type = u"morning"
 >>> st.start_time = datetime.time(8,30)
 >>> st.end_time = datetime.time(12,30)
 >>> st.language = "en"
 >>> session.add(st)
 >>> session.flush()
 
 >>> st.sitting_type_id
 1L
 

 >>> sit = model.GroupSitting()
 >>> sit.group_id = committee_a.group_id
 >>> sit.start_date = datetime.datetime.now()
 >>> sit.end_date = datetime.datetime.now()
 >>> sit.sitting_type_id = st.sitting_type_id
 >>> sit.language = "en"
 >>> session.add(sit)
 >>> session.flush() 

Sitting attendance
-------------------

the attendance of a member at a sitting.

 >>> at = model.AttendanceType()
 >>> at.language = "en"
 >>> at.attendance_type = u"present"
 >>> session.add(at)
 >>> session.flush()
 
 >>> gsa = model.GroupSittingAttendance()
 >>> gsa.sitting_id = sit.sitting_id
 >>> gsa.member_id = mp_1.user_id
 >>> gsa.attendance_id = at.attendance_id
 >>> session.add(gsa)
 >>> session.flush() 
 
Sessions
-----------
A parliamentary Session

 >>> sess = model.ParliamentSession()
 >>> sess.parliament_id = parliament.parliament_id
 >>> sess.short_name = u"First Session"
 >>> sess.full_name = u"First Session XXXX"
 >>> sess.start_date = datetime.datetime.now()
 >>> sess.end_date = datetime.datetime.now()
 >>> sess.language = "en"
 >>> session.add(sess)
 >>> session.flush() 
 
 >>> sess.session_id
 1L
 
Sitting in this session 
 
 >>> ssit = model.GroupSitting()
 >>> ssit.group_id = parliament.parliament_id
 >>> ssit.start_date = datetime.datetime.now()
 >>> ssit.end_date = datetime.datetime.now()
 >>> ssit.sitting_type = st
 >>> ssit.language = "en"
 >>> session.add(ssit)
 >>> session.flush() 
 
Attendance

 >>> sgsa = model.GroupSittingAttendance()
 >>> sgsa.sitting_id = ssit.sitting_id
 >>> sgsa.member_id = mp_1.user_id
 >>> sgsa.attendance_id = at.attendance_id
 >>> session.add(sgsa)
 >>> session.flush() 

Motions
-------
  >>> motion = model.Motion()
  >>> motion.short_name = u"Motion"
  >>> motion.language = 'en'
  >>> motion.owner = mp_1
  >>> session.add(motion)
  >>> session.flush()

Motions

Questions
---------

Note that the questions workflow is tested separated (see workflows/question.txt).

  >>> question = model.Question()
  >>> question.short_name = u"question"
  >>> question.language = 'en'
  >>> question.owner = mp_2
  >>> session.add(question)
  >>> session.flush()
  
  >>> question.question_id
  2L
  


  
Assignment
++++++++++

assigning a question to a ministry

Bill Type:
-----------
  >>> bt = model.BillType()
  >>> bt.bill_type_name = u"private"
  >>> #bt.language = "en"
  >>> session.add(bt)
  >>> session.flush()

Bill
----
  >>> bill = model.Bill()
  >>> bill.short_name = u"Bill"
  >>> bill.bill_type_id = bt.bill_type_id
  >>> bill.language = 'en'
  >>> bill.owner = mp_3
  >>> session.add(bill)
  >>> session.flush()


Schedule items for a sitting:
-----------------------------

we may either add the id only:

  >>> item_schedule = model.ItemSchedule()
  >>> item_schedule.item_id = bill.bill_id
  >>> item_schedule.sitting_id = sit.sitting_id
  >>> session.add(item_schedule)
  >>> session.flush()
  >>> item_schedule.item
  <bungeni.models.domain.Bill object at ...>
  >>> item_schedule.item.short_name
  u'Bill'
  >>> item_schedule.item.type
  'bill'
      
or we can add an object: 
  >>> item_schedule = model.ItemSchedule()
  >>> item_schedule.item
  
  >>> item_schedule.item = question
  >>> item_schedule.sitting_id = sit.sitting_id
  >>> session.add(item_schedule)
  >>> session.flush()
  >>> item_schedule.item
  <bungeni.models.domain.Question object at ...>
  
  >>> item_schedule.item_id == question.question_id
  True
  >>> item_schedule.item.short_name
  u'question'
  >>> item_schedule.item.type
  'question'
  
  
  
Rota Preparation
----------------
 
Debates
--------------



Clean up commit outstanding transactions
-----------------------------------------
 >>> session.flush() 
 >>> session.commit()
 >>> session.close()
 

 




