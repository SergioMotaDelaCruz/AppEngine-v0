import logging

from flask import Flask, render_template, request, jsonify
from google.appengine.ext import ndb
from google.appengine.api import memcache, namespace_manager


application = Flask(__name__)

class Version(ndb.Model):
   likes=ndb.FloatProperty()
   views=ndb.FloatProperty()


@application.route('/')
def home():
   namespace_manager.set_namespace('VER_2')
   v2=Version.get_by_id('v2')
   if not v2:
      v2=Version(likes=1,views=1,id='v2')
      v2_key=v2.put()
   #print '------'
   #print request.user_agent
   #print request.remote_addr
   #print request.headers
   #print '------'

   v2_last=Version.get_by_id('v2')
   v2_last.views+=1
   v2_last.put()
   return render_template('home.html')

@application.route('/sumav2', methods=['POST'])
def sumav2():
   namespace_manager.set_namespace('VER_2')
   v2_last=Version.get_by_id('v2')
   v2_last.likes+=1
   v2_last.put()
   return render_template('like-v2.html')

@application.route('/stats/v2', methods=['GET'])
def stats_v1():
   namespace_manager.set_namespace('VER_2')
   data={"version":namespace_manager.get_namespace(),"views":Version.get_by_id('v2').views,"likes":Version.get_by_id('v2').likes}
   return jsonify(data)

@application.errorhandler(500)
def server_error(e):
    logging.exception('Error during request. '+str(e))
    return 'An internal error occurred.', 500
