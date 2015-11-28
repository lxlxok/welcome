# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    log_id = auth.user_id
    return dict(log_id=log_id)


def load_board():
    log_id = auth.user_id
    rows = db(db.board.id>0).select(orderby=~db.board.id)
    d = [{'title':r.title, 'draft_id':r.draft_id,'created_by':r.created_by,'edit':False} for r in rows]
    return response.json(dict(board_list=d,log_id=log_id))


@auth.requires_signature()
def add_board():
    db.board.update_or_insert((db.board.draft_id == request.vars.draft_id),
            draft_id=request.vars.draft_id,
            title=request.vars.title,
            created_by=auth.user_id)
    return "ok"

@auth.requires_signature()
def add_post():
    db.post.update_or_insert((db.post.draft_id == request.vars.draft_id),
            board_id=request.vars.board_id,
            draft_id=request.vars.draft_id,
            created_by=auth.user_id,
            title=request.vars.title,
            body=request.vars.body)

    return "ok"

@auth.requires_signature()
def delete_post():
    db(db.post.draft_id == request.vars.draft_id).delete()
    return "ok"

def load_post():
    log_id = auth.user_id
    rows = db(db.post.board_id == request.vars.board_id).select(orderby=~db.post.id)
    d = [{'title':r.title,'body':r.body,'created_by':r.created_by,'draft_id':r.draft_id,'edit_t':False,'edit_b':False,'color':'#eee','delete':False, 'save_error':False} for r in rows]
    return response.json(dict(post_list=d,log_id=log_id))

def post():
    log_id = auth.user_id
    row = db(db.board.draft_id == request.args(0)).select().first()
    board_name = row.title
    board_id = row.id
    db.board(db.board.draft_id == board_id)
    return dict(log_id=log_id,board_id=board_id,board_name=board_name)



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


