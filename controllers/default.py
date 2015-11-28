# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

from datetime import datetime


def job_create():
    """
    create a new job information for the job table
    """

    form = SQLFORM(db.job)
    now = datetime.utcnow()
    form.vars.data_time=now.date()
    if form.process().accepted:
       redirect(URL('default','mainpage'))
    return dict(form=form)


def job_delete():
    return dict()

def job_edit():
    return dict()

def boot():
    return dict()



"""
require the user to login and identify their statues
"""
def index():
    """
    show the view for login
    """
    log_id = auth.user_id
    if auth.user_id is not None:
        r = db(db.auth_user.id == log_id).select().first()
        person_identity = r.statue

        """
        check if user identity is teacher
        """
        if person_identity == 'teacher':
            redirect(URL('default','mainpage_teacher',args=auth))
        else:
            redirect(URL('default','mainpage',args=auth))
    logger.info("visiting index without loging")
    return dict()



"""
define all the mainpage related with teacher
"""

def mainpage_teacher():
    return dict()

def load_mainpage_t():
    log_id = auth.user_id
    r = db(db.auth_user.id == log_id).select().first()
    last_name = r.last_name
    if last_name is None:
        last_name = 'teacher'
    return response.json(dict(last_name=last_name))

def add_post():
    """
    add the content to the post_content table
    """
    now = datetime.utcnow()
    db.post_content.update_or_insert((db.post_content.uiud_id == request.vars.uiud_id),
            user_id = auth.user_id,
            uiud_id= request.vars.uiud_id,
            pos_title=request.vars.title,
            pos_content= request.vars.content,
            pos_time = now)
    """
    renew the table post_search who followed the teacher

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
    """



    return "ok"



def load_post():

    rows = db(db.post_content.user_id==auth.user_id).select(orderby=~db.post_content.id)
    d=[{'title':r.pos_title,'content':r.pos_content,'uiud':r.uiud_id,'time':r.pos_time} for r in rows]
    return response.json(dict(post_list=d))



"""
define all the mainpage related with student
"""
@auth.requires_login()
def mainpage():

    """
    show the mainpage
    including the dashboard and job table
    :return: information about job board
    """
    job_list=db(db.job.id > 0).select()

    return dict(job_list=job_list)


def load_mainpage_s():
    log_id = auth.user_id
    r = db(db.auth_user.id == log_id).select().first()
    graduate_date = r.graduate

    """
    calculate how many days left for graduate
    """
    remain_day = 0
    if r.graduate is not None:
        now = datetime.utcnow().date()
        remain = graduate_date - now
        remain_day = remain.days
    """
    calculate how many post unreaded
    """
    unread_mess_num = db((db.post_search.post_to_id == log_id) & (db.post_search.read_state == False)).count()

    return response.json(dict(remain_day=remain.days,unread_mess_num=unread_mess_num))




def message():
    return "hello world"

def search_user():
    email_add = request._vars['para']
    r = db(db.auth_user.email == email_add).select().first()
    is_teacher = 0
    if r is not None:
        first_name = r.first_name
        last_name = r.last_name
        statue = r.statue
        email = r.email
        course = r.course
        office = r.address
        introduction = r.introduction
        if statue=='teacher':
            is_teacher = 1
        return dict(exit=1,is_teacher=is_teacher,email_add=email_add,statue=statue,first_name=first_name,last_name=last_name,email=email,course=course,office=office,introduction=introduction)
    return dict(exit=0,is_teacher=0,email_add=email_add)




@auth.requires_login()
def dashboard():
    return dict(message=T('Dashboard'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


