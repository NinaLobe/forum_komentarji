#!/usr/bin/env python
import webapp2
from handlers.base import MainHandler, CookieAlertHandler
from handlers.topics import TopicAdd, TopicDetails
from handlers.comments import TopicCommentHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set-cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/topic/add', TopicAdd, name="topic-add"),
    webapp2.Route('/topic/<topic_id:\d+>', TopicDetails, name="topic-details"),
    webapp2.Route('/topic/<topic_id:\d+>/comment/add', TopicCommentHandler, name="comment-add"),
], debug=True)
