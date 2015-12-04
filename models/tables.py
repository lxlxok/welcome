#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################


from datetime import datetime

auth.settings.profile_next=URL('default', 'index')
auth.messages.logged_in=None
auth.messages.logged_out=None
auth.messages.profile_updated=None


db.define_table('post_content',
                Field('user_id','reference auth_user'),
                Field('uiud_id'),
                Field('pos_title'),
                Field('pos_content','text'),
                Field('pos_time','datetime',default=datetime.utcnow())
                )

db.define_table('folllow_relation',
                Field('teacher_id'),
                Field('followed_by_id'))

db.define_table('post_search',
                Field('post_content_id','reference post_content'),
                Field('post_to_id'),
                Field('read_state','boolean',default=False),
                Field('auth_name'),
                Field('pos_title'),
                Field('pos_time','datetime',default=datetime.utcnow())
                )

db.define_table('job',
                Field('user_id','reference auth_user'),
                Field('uiud_id'),
                Field('job_name',default=''),
                Field('job_title',default=''),
                Field('job_state',default='apply'),
                Field('job_contact',default=''),
                Field('job_email',default=''),
                Field('job_important','boolean',default=False),
                Field('data_time','date',default=datetime.utcnow().date())
                )




