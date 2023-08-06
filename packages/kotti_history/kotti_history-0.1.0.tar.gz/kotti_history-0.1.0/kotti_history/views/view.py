# -*- coding: utf-8 -*-

"""
Created on 2017-01-03
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from datetime import datetime, timedelta

from kotti import DBSession
from pyramid.view import view_config
from pyramid.view import view_defaults
from sqlalchemy.orm.exc import NoResultFound
from kotti_controlpanel.util import set_setting, get_setting, get_settings

from kotti_history import _, fanstatic
from kotti_history.resources import ViewHistory, SearchHistory
from kotti_history.views import BaseView
from kotti_history.decorators import (
    login_required
)



@view_config(
    name='history-recorder',
    renderer='kotti_history:templates/recorder.pt')
class RecorderView(BaseView):

    def __call__(self):
        return {
            "timeout": 5000
        }


class SearchHistoryView(BaseView):

    @view_config(name="save-search", root_only=True, permission="view",
                 decorator=(login_required), request_method="POST",
                 renderer="json")
    def save_search(self):
        term = self.request.params.get("term", "")
        if not term:
            return {
                "status": "Failed",
                "message": "No term sent"
            }
        SearchHistory.create(username=self.request.user.name, term=term)
        return dict(status="Success", message="{} has been added".format(term))

    @view_config(name="previous-searches", root_only=True, permission="view",
                 decorator=(login_required),
                 renderer="kotti_history:templates/searches.pt")
    def my_searches(self):
        searches = SearchHistory.find_by_username(self.request.user.name)
        return dict(
            searches=searches
        )


class DefaultView(BaseView):
    @view_config(name="all-history",
                 request_method="GET",
                 root_only=True,
                 renderer="kotti_history:templates/history.pt",
                 permission="admin")
    def view_history(self):
        history = ViewHistory.query.all()
        return {
            "history": history
        }



@view_defaults(name="history", context="kotti.resources.Content")
class Viewer(BaseView):

    @view_config(request_method="GET", renderer="kotti_history:templates/history.pt", permission="owner")
    def view_history(self):
        history = ViewHistory.find_by_content_id(self.context.id)
        return {
            "history": history
        }

    @view_config(request_method="POST", renderer="json", permission="view")
    def save_view_history(self):

        contenttypes = get_setting("track_contenttypes")
        if self.context.type_info.title not in contenttypes:
            return {
                "status": "failed",
                "message": "This content type is not being tracked"
            }

        try:
            history = ViewHistory.find(content_id=self.context.id,
                                       username=self.request.user.name).one()
            today = datetime.now()  - timedelta(days=1)
            if today > history.date_last_viewed:
                num_views = history.num_views + 1
                history.num_views = num_views
                DBSession.add(history)
            else:
                num_views = history.num_views
                return dict(status="success",
                            message="Already updated",
                            num_views=num_views)
        except NoResultFound as e:
            history = ViewHistory.create(content=self.context, user=self.request.user)
            num_views = history.num_views
            DBSession.add(history)
        return {
            "status": "success",
            "message": "View count has been changed to {}".format(num_views),
            "num_views": num_views
        }
