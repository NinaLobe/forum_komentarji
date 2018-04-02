from google.appengine.api import users
from google.appengine.api import memcache
from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment
import uuid

class TopicAdd(BaseHandler):
    def get(self):
        csrf_token = str(uuid.uuid4())
        user = users.get_current_user()
        memcache.add(key=user.email(), value=csrf_token, time=600)
        params = {"token":csrf_token}
        return self.render_template("topic_add.html",params=params)

    def post(self):
        user = users.get_current_user()
        csrf_token = self.request.get("csrf_token")
        token = memcache.get( key=user.email())

        if not user:
            return self.write("Please login before you're allowed to post a topic.")


        if token!=csrf_token:
            return self.write("Nope, not allowed!")

        title = self.request.get("title")
        text = self.request.get("text")

        new_topic = Topic(title=title, content=text, author_email=user.email())
        new_topic.put()  # put() saves the object in Datastore

        return self.redirect_to("topic-details", topic_id=new_topic.key.id())


class TopicDetails(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        comment = Comment.query(Comment.deleted == False).fetch()
        #comment.sort();
        params = {"topic": topic,"comments": comment}
        return self.render_template("topic_details.html", params=params)
