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
                Field('uiud_id'),
                Field('job_name',default=''),
                Field('job_title',default=''),
                Field('job_state',default='apply'),
                Field('job_contact',default=''),
                Field('job_email',default=''),
                Field('job_important','boolean',default=False),
                Field('data_time','date',default=datetime.utcnow().date())
                )

db.define_table('job_old',
                Field('job_name',requires=IS_NOT_EMPTY(error_message='please enter the name for company')),
                Field('job_title',default='SDE'),
                Field('job_state',default='apply',requires=IS_IN_SET(['apply','telephone','onsite','offer','refused'])),
                Field('job_way',default='recommend',requires=IS_IN_SET(['recommend','jobfair','internet'])),
                Field('job_contact',default=''),
                Field('job_email',default=''),
                Field('job_important','boolean',default=False),
                Field('job_address',default=''),
                Field('job_tips','text',default=''),
                Field('data_time','date',default=datetime.utcnow().date(),readable=False, writable=False)
                )


