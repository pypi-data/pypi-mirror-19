from unittest.mock import MagicMock

from datetime import datetime,date

import pytest
from objdict import (ObjDict)
from viewmodel.viewFields import (IdField, TxtField, EnumForeignField, IntField,
            DateField, TimeField, Case,
            viewModelDB )

#import saltMongDB
#from sbextend import SaltReq
from viewmodel.viewModel import BaseView
from viewmodel.memberView import MemberView, CardView

@pytest.fixture
def req():
    res=MagicMock(spec=SaltReq)
    res.getData={}
    res.postData={}
    res.hostName='salt'
    res.saltScript='register'
    return res

@pytest.fixture
def testmid():
    return 8

class SampleView(BaseView):
    models_ = None
    id          = IntField(name='sqlid', cases={})
    salt        = IntField(cases={})
    label       = TxtField('Label for Profile', 8)
    date       =  DateField('Date')
    country     = EnumForeignField('Default Country',  session=viewModelDB,
                                   dispFields=('countries.countryName', ),
                                   values='countries.phoneCode'
                                  )
    #favourites  = FavField('theFavs!')
    #extra = TxtField('used as a dummy',src=None)
    def getRows_(self):
        row = ObjDict(id=1)
        row.salt = 5
        row.label = 'Label'
        row.country = '061'
        row.date = datetime(16, 2, 1)
        return [ObjDict(((self.row_name_, row), ))]

@pytest.fixture
def sampleView():
    return SampleView()

class TestFields:
    def testText(self, sampleView):
        assert sampleView.label == 'Label'
        assert sampleView[0]['label'].value == 'Label'

    def testDateFld(self, sampleView):
        assert sampleView.date == datetime(16, 2, 1)
        assert sampleView[0]['date'].strvalue == ' 1/02/0016'


    def testTimeFld(self,sampleView):
        assert sampleView.label == 'Label'

    def testEnumKey(self,sampleView):
        assert sampleView.country.value == '061'

class TestSetFields:
    def testText(self, sampleView):
        assert sampleView.label == 'Label'
        assert sampleView[0]['label'].strvalue == 'Label'
        sampleView[0]['label'].strvalue = 'xLabel'
        assert sampleView[0]['label'].strvalue == 'xLabel'


    def testDateFld(self, sampleView):
        assert sampleView.date == datetime(16, 2, 1)
        assert sampleView[0]['date'].strvalue == ' 1/02/0016'
        #assert sampleView[0].date.strvalue == ' 1/02/0016'
        sampleView[0]['date'].strvalue = '02/03/2017'
        assert sampleView.date == date(2017, 3, 2)

class TestLoops:
    """ testing row structure supports looping through rows
        and within rows through fields"""
    def test_loop_row(self, sampleView):
        loopcount = 0
        for row in sampleView:
            assert row.label == 'Label'
            loopcount += 1
        assert loopcount == 1

    def test_loop_fields(self, sampleView):
        row=sampleView[0]
        names=[]
        values=[]
        for field in row:
            names.append(field.name)
            values.append(field.value)
        assert names == ['label','date','country']
        assert values == ['Label',datetime(16,2,1),
                type(row.country)('061')]

    def test_loop_fields_loop(self, sampleView):
        row = sampleView[0]
        names=[]
        for field in row.loop_(case=Case.allFields):
            names.append(field.name)
        assert names == ['sqlid','salt','label','date','country']

class TestIndexAttr:
    """ testings access to attributes ViewRow """
    def test_row_index(self, sampleView):
        row = sampleView[0]
        assert row['label'].value == 'Label'
        with pytest.raises(TypeError):
            row['label'] = 5

class TestView_idx_labelsList:
    def test_view_(self,sampleView):
        assert sampleView.view_ is sampleView
        assert sampleView[0].view_ is sampleView

    def test_idx_(self,sampleView):
        assert sampleView.idx_ == 0
        with pytest.raises(AttributeError):
            sampleView.idx_ = 5

    def test_idx_row(self,sampleView):
        assert sampleView[0].idx_ == 0
        with pytest.raises(AttributeError):
            sampleView[0].idx_ = 5

    def test_labelsList(self,sampleView):
        assert sampleView.labelsList_() == ['no labels']


@pytest.fixture
def memberView():
    return MemberView(dict(sqlid=8)) # ObjDict(memberID='ian')

@pytest.fixture
def membersView():
    return MemberView(dict()) # ObjDict(memberID='ian')

class TestMembers:
    def test_member(self,memberView):
        mv= memberView
        assert len(mv)==1
        assert mv.memberID=='ian'

    def test_view_form(self, memberView):
        mv=memberView
        names='memberID','quickName','nameType','plan'
        for nm,fld in zip(names,mv.fields_()):
            assert fld.name == nm

        assert fld.label == 'Shaker Type' #just testing last one

    def test_members_rows(self,membersView):
        mv= membersView
        assert len(mv)==3
        names ='ian','Michael',' default'
        for n,m in zip(names,mv.fields_.loopRows()):
            assert m.memberID == n
            assert mv != m



    def test_members_index(self,membersView):
        mv =membersView
        assert mv[1].memberID == 'Michael'

class TestFieldAccess:
    def test_members_fields(self,membersView):
        mv= membersView
        assert len(mv)==3
        names ='ian','Michael',' default'
        for n,m in zip(names,mv.fields_.loopRows()):
            its = m.fields_.items()
            key,value = list(its)[2]
            assert value.value == n

    def test_members_fields_row_fields_items(self,membersView):
        mv= membersView
        assert len(mv)==3
        names ='ian','Michael',' default'
        for n,m in zip(names,mv):
            its = m.fields_.items()
            key,value = list(its)[2]
            assert value.value == n
            assert value.name == 'memberID'

    def test_members_fields_new(self,membersView):
        mv= membersView
        assert len(mv)==3
        names ='ian','Michael',' default'
        for n,m in zip(names,mv):
            its = m.fields_.items()
            key,value = list(its)[2]
            assert value.value == n
            assert value.name == 'memberID'


class Student(BaseView):
    models_ = viewModelDB.default(viewModelDB.baseDB.db.Students)
    id = IdField(cases={}) # , name = '_id')
    name = TxtField()
    course = TxtField()
    course_year = IntField()

    def x__init__(self, *args, **kargs):
        import pdb; pdb.set_trace()
        super().__init__(*args, **kargs)
        
class TestTutorial:
    def test_init_db_tutversion(self):
        name = "Fred Smith"
        student = Student(models=viewModelDB.default('Student2s'))
        assert len(student)== 0
        student.insert_()
        with student:
            student.name = name
        assert student.name == name
        assert '_id' in student.dbRows_[0]['Student2s']

    def test_init_db(self):
        student = Student()
        name = "Fred Smith"
        assert len(student)== 0
        student.insert_()
        with student:
            student.name = name
        assert student.name == name

    def test_read_and_modify(self):
        student = Student({})
        assert len(student)==1
        assert student.course_year == None
        assert student.course == ''

        with student:
            student.course_year = 2
            student.course = 'Computing'

    def test_add_second(self):
        student = Student()
        assert len(student)==0
        student.insert_()
        with student:
            student.name = 'Jane'
            student.course_year = 3
            student.course = 'Computer Engineering'

    def test_read_multiple(self):
        students = Student({})
        assert len(students)==2
        student = students[1]
        assert student.course_year == 3
        with student:
            student.course_year = 2

    def test_read_multiple_dict(self):
        students = Student({'course_year':2})
        assert len(students)==2
        student = students[1]
        assert student.course_year == 2
        for student in students:
            assert student.course_year == 2

class TestComplexFieldsUsingCardData:
    def test_access_inside(self):
        cv=CardView(8)
        c2=cv[1]
        assert c2.membcard['sqlid'] == 96

    def test_change_inside(self):
        cv=CardView(8)
        c2=cv[1]
        with c2:
            vals = c2.membcard
            vals['sqlid'] = 97
            vals.id = c2.id 
            c2.membcard = vals
        assert c2.membcard['sqlid'] == 97
        assert c2.membcard['id'] == c2.id

    

class TestCards:
    def test_card_read(self):
        cv=CardView(8)
        c2=cv[1]
        assert c2.membcard['sqlid'] == 97
        assert c2.label == 'c1'
        with pytest.raises(AssertionError):
            c2.nameOnCard == 'ian'
        with c2: #restore id to enable fetch from card
            vals = c2.membcard
            vals['sqlid'] = 96
            c2.membcard = vals          
        assert c2.nameOnCard == 'ian'

    def test_card_update(self):
        cv=CardView(8)
        c2=cv[1]
        with c2:
            c2.nameOnCard = 'Fred'
        assert cv.dbRows_[1]['cards'].nameOnCard == 'Fred'
        #cv.update_()
        cv=CardView(8)
        assert cv[1].nameOnCard == 'Fred'

    def test_card_labelupdate(self):
        cv=CardView(8)
        c2=cv[1]
        with c2:
            c2.nameOnCard = 'Fred'
            c2.label = 'new label'
        assert cv.dbRows_[1]['cards'].nameOnCard == 'Fred'
        cv=CardView(8)
        assert cv[1].nameOnCard == 'Fred'
        assert cv[1].label == 'new label'

    def test_card_label_insert(self):
        cv = CardView(8)
        cnew =cv.insert_()
        with cnew:
            cnew.nameOnCard = 'Fred'
            cnew.label = 'new card'
        assert cv.dbRows_[3]['cards'].nameOnCard == 'Fred'
        assert cv.dbRows_[3]['members.cards'].label == 'new card'
        assert '_id' in cv.dbRows_[3]['cards']
        memb = cv.dbRows_[3]['members.cards']
        assert 'key' in memb

        with cnew:
            cnew.sqlid = cnew.id 

        cv=CardView(8)
        assert cv[3].nameOnCard == 'Fred'
        assert cv[3].label == 'new card'
        