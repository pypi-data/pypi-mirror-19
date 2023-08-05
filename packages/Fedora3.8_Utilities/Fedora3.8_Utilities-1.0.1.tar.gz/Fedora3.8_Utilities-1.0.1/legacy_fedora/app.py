"""
 mod:`urls` Fedora Batch App URL rourting
"""
__author__ = "Jeremy Nelson"

import json
import threading

from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, redirect, Response
from flask import jsonify
from flask_socketio import SocketIO
from forms import AddFedoraObjectFromTemplate, IndexRepositoryForm
from forms import MODSReplacementForm, MODSSearchForm 
from helpers import create_mods, generate_stubs
from indexer import Indexer
from repairer import update_multiple

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
socketio = SocketIO(app)


ACTIVE_MSGS = []
BACKEND_THREAD = None

class IndexerThread(threading.Thread):

    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.indexer = Indexer(app=app, 
            elasticsearch=kwargs.get('elasticsearch'))
        self.job = kwargs.get("job")
        self.pid = kwargs.get("pid")
        
    def run(self):
        if self.job.lower().startswith("full"):
            self.indexer.reset()
            self.indexer.index_collection(self.pid)
        return 

class RepairerThread(threading.Thread):

    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.pid_listing = kwargs.get('pid_listing')
        self.xpath = kwargs.get('xpath')
        self.old_value = kwargs.get('old_value')
        self.new_value = kwargs.get('new_value')
        
    def run(self):
        
        return

@app.route("/")
def default():
    return render_template('fedora_utilities/app.html')

@app.route("/about")
def about():
    return render_template("fedora_utilities/about.html")

@app.route("/add_stub", methods=["GET", "POST"])
def add_stub():
    ingest_form = AddFedoraObjectFromTemplate(csrf_enabled=False)
    if ingest_form.validate_on_submit():
        mods_xml = create_mods(request.form)
        return jsonify(generate_stubs(
            config=app.config,
            mods_xml=mods_xml,
            title=request.form.get('title'),
            parent_pid=request.form.get('collection_pid'),
            num_objects=request.form.get('number_objects'),
            content_model=request.form.get('content_models')))
    return render_template('fedora_utilities/batch-ingest.html',
        ingest_form=ingest_form)


@app.route("/index/status")
def indexing_status():
    if len(BACKEND_THREAD.indexer.messages) > 0:
        msg = BACKEND_THREAD.indexer.messages.pop(0)
    else:
        msg = "Finished"
    socketio.emit('status event', {"message": msg})

@app.route("/index/pid", methods=["POST"])
def index_pid():
    pid = request.args.get("pid")
    return jsonify({"message": "Indexed PID"})

@app.route("/index", methods=["POST", "GET"])
def index_repository():
    global BACKEND_THREAD
    index_form = IndexRepositoryForm(csrf_enabled=False)
    if index_form.validate_on_submit():
        if index_form.index_choice.data.startswith("0"):
            return jsonify({"message": "Started Incremental Indexing"})
        elif index_form.index_choice.data.startswith("1"):
            elastic_host = index_form.indices.data
            BACKEND_THREAD = IndexerThread(
                elasticsearch=elastic_host,
                job="full", 
                pid="coccc:root")
            BACKEND_THREAD.start()
            return jsonify({"message": "Started Full Indexing"})
        else:
            return jsonify({"message": "Unknown Indexing option"})
 
    return render_template('fedora_utilities/index-repository.html',
        index_form=index_form)


@app.route("/mods-replacement", methods=["POST", "GET"])
def mods_replacement():
    global BACKEND_THREAD
    replace_form = MODSReplacementForm(csrf_enabled=False)
    search_form = MODSSearchForm(csrf_enabled=False)
    if replace_form.validate_on_submit():
        pid_listing = replace_form.pid_listing.data.split(",")
        xpath = replace_form.select_xpath.data
        old_value = replace_form.old_value.data
        new_value = replace_form.new_value.data
            
        return "Submitted {}".format(pid_list)
    return render_template('fedora_utilities/mods-replacement.html',
        replace_form=replace_form,
        search_form=search_form)

@app.route("/search", methods=["POST", "GET"])
def search_pids():
    search_form = MODSSearchForm(csrf_enabled=False)
    if search_form.validate_on_submit():
        es_host = search_form.indices.data
        es = Elasticsearch(hosts=[es_host])
        found_pids = []
        query = search_form.query.data
        facet = search_form.facet.data
        if facet.startswith("none"):
            search_results = es.search(q=query, 
                index='repository',
                fields=['pid',],
                size=50)
        else:
            dsl = {
                "query": {
                    "term": { facet: query }
                }
            }
            search_results = es.search(body=dsl,
                index='repository', 
                fields=['pid',],
                size=50)
        for hit in search_results.get('hits', {})\
            .get('hits', []):
            pid = hit.get('fields', {}).get('pid')
            found_pids.append(pid)
        return jsonify({
            "pids": found_pids, 
            "total": search_results.get('hits', {}).get('total', 0)})
    return jsonify({"pids": []})
    

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=9455)
    #app.run(host='0.0.0.0', debug=True, port=9455)
