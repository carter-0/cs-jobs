from flask import Flask, redirect, url_for, request, render_template, session, send_from_directory, jsonify, make_response
from time import gmtime, strftime, sleep
import models_pw as dbHandler
import jobDbHandler as db
import bcrypt
import time
import os
import re

### Main webserver using flask. managed by gunicorn for efficency ###

application = Flask(__name__) ##Various Configuration
application.config['SECRET_KEY'] = 'thisisaverysecretcode'
salt = bcrypt.gensalt()

html_template = """
      <div style="max-width:600px; margin-top: {}px;" class="front_job_details">   
        <h3>
            <a id="bttns" href="{}">
              {}
            </a>
        </h3>
      <strong><a id="loc" class="w3-btn w3-blue" class="btn apply_invert" data-toggle="tooltip" data-placement="bottom" top="" title="" href="/?jobs-at={}" data-original-title="Use company as filter">{}</a></strong>
      <strong><a id="loc" class="w3-btn w3-blue" class="btn apply_invert" data-toggle="tooltip" data-placement="bottom" top="" title="" href="/?jobs-in={}" data-original-title="Use location as filter">{}</a></strong>
      <span class="posted"><p>Posted: {}</p></span>
      <p>
        {}
      </p>
      </div>
"""

jobs_template = """
<div style="display: flex; flex-direction: row;" class="flex-container">
        <div style="flex: 1; border: 1px solid #808080; border-radius: 10px; max-width: 350px; margin-left: 32px; margin-top: 70px; padding: 25px; font-family: 'Open Sans', sans-serif; max-height: 325px;" class="shareBox">
            <div class="infoBox">
            <a style="color: #0c91f7" href="javascript:history.back()">< Back</a>
            <h5>Location:</h5>
                <h6>{}</h6>
            <br />
            <h5>Company:</h5>
                <h6>{}</h6>
                <br />
            <h5>Posted:</h5>
                <h6>{}</h6>            
            </div>
        </div>
        <div style="flex: 1; display: flex; margin-left: 64px; margin-top: 70px;" class="jobContainer">
            <div class="mainJob">
                <div style="color: #0c91f7; max-width: 1200px;" class="titles">
                    <h1>{}</h1>
                    <h3>{}</h3>
                </div>
                <br />
                <div style="max-width: 1200px;" class="description">
                    {}	
                </div>
                <div style="display: flex; justify-content: center; margin-top: 16px;" class="apply">
                    <button onclick="window.open('{}','_blank')" style="width: 200px; justify-content: center;" class="w3-btn w3-blue">Apply Now!</button>
                </div>
            </div>
        </div>
    </div>
"""

def lazyloader(counter, html_templates, posts, quantity):
    if counter == 0:
                    print("Returning posts 0 to {quantity}")
                    # Slice 0 -> quantity from the db
                    print(html_templates[0])
                    res = make_response(jsonify(html_templates[0: quantity]), 200)

    elif counter == posts:
        print("No more posts")
        res = make_response(jsonify({}), 200)

    else:
        print("Returning posts {counter} to {counter + quantity}")
        # Slice counter -> quantity from the db
        res = make_response(jsonify(html_templates[counter: counter + quantity]), 200)
    return res

@application.route('/', methods=['GET', 'POST']) ##Root of domain: return index.html
def root():
    if request.args.get('search') != None or request.args.get('jobs-at') != None or request.args.get('jobs-in') != None:
        if request.args.get('search') != None:
            allPosts = db.retrieve()
            jobNum = len(allPosts)
            title = []
            description = []
            results = []
            if request.args.get('jobs-at') == None and request.args.get('jobs-in') == None:
                for i in allPosts:
                    title.append(i[0])
                    description.append(i[9].lstrip())
                search = request.args.get('search').split()

                for i in search:
                    if i == "and":
                        search.remove(i)
                    if i == "or":
                        search.remove(i)
                    if i == "to":
                        search.remove(i)
                    if i == "out":
                        search.remove(i)
                    if i == "the":
                        search.remove(i)
                    if i == "more":
                        search.remove(i)
                    if i == "a":
                        search.remove(i)
                    if i == "b":
                        search.remove(i)
                    if i == "developer" and len(search) > 1:
                        search.remove(i)
                    if i == "engineer" and len(search) > 1:
                        search.remove(i)
                    if i == "manager" and len(search) > 2:
                        search.remove(i)

                for i in search:
                    for n in title:
                        if i.upper() in n.upper():
                            results.append(n)
                    for n in description:
                        if i.upper() in n.upper():
                            results.append(n)
                if session['logged_in']:
                    return render_template('basic/results_logged_in.html', value=len(results), searchTerm=request.args.get('search'))
                else:
                    return render_template('basic/results.html', value=len(results), searchTerm=request.args.get('search'))
            elif request.args.get('jobs-at') != None and request.args.get('jobs-in') != None:
                return render_template('basic/results_multi.html', reqType="all", searchTermData="{}:{}:{}".format(request.args.get('jobs-at'), request.args.get('jobs-in'), request.args.get('search')))
            elif request.args.get('jobs-in') != None and request.args.get('jobs-at') == None:
                return render_template('basic/results_multi.html', reqType="sand", searchTermData="{}:{}".format(request.args.get('jobs-in'), request.args.get('search')))
        elif request.args.get('jobs-at') != None:
            if request.args.get('jobs-in') != None:
                return render_template('basic/results_multi.html', reqType="both", searchTermData="{}:{}".format(request.args.get('jobs-at'), request.args.get('jobs-in')))
            else:
                return render_template('basic/results_multi.html', reqType="jobs-at", searchTermData="{}".format(request.args.get('jobs-at')))
        elif request.args.get('jobs-in') != None:
            return render_template('basic/results_multi.html', reqType="jobs-in", searchTermData="{}".format(request.args.get('jobs-in')))
    else:
        jobNum = len(db.retrieve())
        try:
            print(session['logged_in'])
            print(session['name'])
        except:
            session['logged_in'] = []
            session['name'] = []
        if session['logged_in'] == True:
            return render_template('rewrite/index.html', value=jobNum)
        else:
            return render_template('rewrite/index.html', value=jobNum)

@application.route('/signup', methods=['GET', 'POST']) ##Signup Handler
def signup():
    if request.method == 'GET':
        return render_template('basic/signup.html')
    elif request.method == 'POST':
        usr = str(request.form['user_name'])
        email = str(request.form['user_email'])
        passwrd = str(request.form['user_password'])

        if len(passwrd) < 8:
            return render_template('errors/signup_len_short.html')

        if len(passwrd) > 40:
            return render_template('errors/signup_len_long.html')

        allUsr = dbHandler.pwRetrieveNames()
        allEmail = dbHandler.pwRetrieveEmails()
        for i in allUsr:
            for q in i:
                if usr in q:
                    return render_template('errors/signup_usr_used.html', usr=usr)
        for i in allEmail:
            for q in i:
                if email in q:
                    return render_template('errors/signup_email_used.html', email=email)
        
        hashedPasswrd = bcrypt.hashpw(passwrd.encode(), salt)
        dbHandler.pwInsert(usr, email, hashedPasswrd)
        return redirect(url_for('login'))
        

@application.route('/login', methods=['GET', 'POST']) ##Login handler
def login():
    if request.method == 'GET':
        return render_template('basic/login.html')
    elif request.method == 'POST':
        completed = False
        usr = str(request.form['user_name'])
        passwrd = str(request.form['user_password'])

        allUsr = dbHandler.pwRetrieveNames()
 
        for i in allUsr:
            for q in i:
                if usr in q:
                    completed = True
                    break
                else:
                    continue
        
        if completed == False:
            return render_template('errors/login_no_usr.html')
        
        info = dbHandler.pwRetrieve()
        for i in info:
            for q in i:
                if i[0] == usr:
                    if bcrypt.hashpw(passwrd.encode(), i[2]) == i[2]:
                        session['logged_in'] = True
                        session['name'] = usr
                        return redirect(url_for('root'))
                    else:
                        return render_template('errors/login_incorrect.html')

@application.route('/account')
def account():
    if session['logged_in']:
        return 'Account'

@application.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        if session['logged_in']:
            return "I forgot to delete this part lol. ignore the 'messages' tab (this)"
        else:
            return redirect(url_for('login'))


@application.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@application.route('/scroll.js')
def scroll():
    return send_from_directory(os.path.join(application.root_path, 'static'),
                               'scroll.js')

@application.route('/jobs.js')
def jobsJs():
    return send_from_directory(os.path.join(application.root_path, 'static'),
                               'jobs.js')

@application.route('/scroll_multi.js')
def scroll_multi():
    return send_from_directory(os.path.join(application.root_path, 'static'),
                               'scroll_multi.js')

@application.route('/index.css')
def indexcss():
    return send_from_directory(os.path.join(application.root_path, 'static'), 'index.css')

@application.route('/load')
def load():
    if request.args.get('s') == None and request.args.get('company') == None and request.args.get('l') == None: ##Index.html
        #time.sleep(0.2)  # Used to simulate delay
        allPosts = db.retrieve()
        posts = len(allPosts)
        quantity = 20

        orderedDb = []
        x = 0
        for p in allPosts:
            if x == 0:
                orderedDb.append(html_template.format(240, "/jobs?id={}".format(p[12][-8:]), p[0], p[2], p[2], p[7], p[7], str(p[4]), p[8]))
                x = x + 1
            else:
                orderedDb.append(html_template.format(0, "/jobs?id={}".format(p[12][-8:]), p[0], p[2], p[2], p[7], p[7], str(p[4]), p[8]))
                x = x + 1

        if request.args:
            counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

            if counter == 0:
                print(f"Returning posts 0 to {quantity}")
                # Slice 0 -> quantity from the db
                res = make_response(jsonify(orderedDb[0: quantity]), 200)

            elif counter == posts:
                print("No more posts")
                res = make_response(jsonify({}), 200)

            else:
                print(f"Returning posts {counter} to {counter + quantity}")
                # Slice counter -> quantity from the db
                res = make_response(jsonify(orderedDb[counter: counter + quantity]), 200)

        return res
    else: ##Search Results
        if request.args.get('l'):
            location = request.args.get('l')
        else:
            location = None
        if request.args.get('company'):
            company = request.args.get('company').upper()
        else:
            company = None
        #time.sleep(0.2)  # Used to simulate delay
        allPosts = db.retrieve()
        posts = len(allPosts)
        quantity = 20

        orderedDb = []

        html_templates = []
        title = []
        description = []
        results = []
        maybeResults = []
        companyList = []
        locationList = []
        if request.args.get('s'):
            search_term = request.args.get('s')
            for i in allPosts:
                title.append(i[0])
                description.append(i[9].lstrip())
                companyList.append(i[2])
                locationList.append(i[7])
            search = search_term.split()
            for i in search:
                if i == "and":
                    search.remove(i)
                if i == "or":
                    search.remove(i)
                if i == "to":
                    search.remove(i)
                if i == "out":
                    search.remove(i)
                if i == "the":
                    search.remove(i)
                if i == "more":
                    search.remove(i)
                if i == "a":
                    search.remove(i)
                if i == "b":
                    search.remove(i)
                if i == "developer" and len(search) > 1:
                    search.remove(i)
                if i == "engineer" and len(search) > 1:
                    search.remove(i)
                if i == "manager" and len(search) > 2:
                    search.remove(i)
            if request.args.get('company') == None and request.args.get('l') == None:
                for i in search:
                    for n in title:
                        if i.upper() in n.upper():
                            results.append(n)
                    for n in description:
                        if i.upper() in n.upper():
                            results.append(n)
            if request.args.get('l') != None and request.args.get('company') == None:
                for i in search:
                    for n in title:
                        if i.upper() in n.upper():
                            maybeResults.append(n)
                    for n in description:
                        if i.upper() in n.upper():
                            maybeResults.append(n)
                for i in locationList:
                    if i.upper() in location.upper() and i in maybeResults:
                        results.append(i)
            if request.args.get('l') == None and request.args.get('company') != None:
                for i in search:
                    for n in title:
                        if i.upper() in n.upper():
                            maybeResults.append(n)
                    for n in description:
                        if i.upper() in n.upper():
                            maybeResults.append(n)
                for i in companyList:
                    if i.upper() in company.upper() and i in maybeResults:
                        results.append(i)
            if request.args.get('l') != None and request.args.get('company') != None:
                for i in search:
                    for n in title:
                        if i.upper() in n.upper():
                            maybeResults.append(n)
                    for n in description:
                        if i.upper() in n.upper():
                            maybeResults.append(n)
                for i in locationList:
                    if i.upper() in location.upper():
                        maybeResults.append(i)
                for i in companyList:
                    if i.upper() in company.upper() and i in maybeResults:
                        results.append(i)

            jobs = []
            html_templates = []
            #print(results)
            x = 0
            for i in results:
                for p in allPosts:
                    if i == p[0]:
                        jobs.append(p)
                        if x == 0:
                            html_templates.append(html_template.format(240, "/jobs?id={}".format(p[12][-8:]), p[0], p[2], p[2], p[7], p[7], str(p[4]), p[8]))
                        else:
                            html_templates.append(html_template.format(0, "/jobs?id={}".format(p[12][-8:]), p[0], p[2], p[2], p[7], p[7], str(p[4]), p[8]))
                x = x + 1
            if request.args: ##lazyloading for index.html
                counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

                if counter == 0:
                    print("Returning posts 0 to {quantity}")
                    # Slice 0 -> quantity from the db
                    res = make_response(jsonify(html_templates[0: quantity]), 200)

                elif counter == posts:
                    print("No more posts")
                    res = make_response(jsonify({}), 200)

                else:
                    print("Returning posts {counter} to {counter + quantity}")
                    # Slice counter -> quantity from the db
                    res = make_response(jsonify(html_templates[counter: counter + quantity]), 200)

            return res
        else:
            if location != None:
                if company != None:
                    for i in allPosts:
                        if company.upper() == i[2].upper() and location.upper() == i[7].upper():
                            orderedDb.append(i)
                    x = 0
                    for p in orderedDb:
                        if x == 0:
                            html_templates.append(html_template.format(240, "/jobs?id={}".format(p[12][-8:]), p[0], p[2], p[2], p[7], p[7], str(p[4]), p[8]))
                            x = x + 1
                        else:
                            html_templates.append(html_template.format(0, "/jobs?id={}".format(p[12][-8:]), p[0], p[2], p[2], p[7], p[7], str(p[4]), p[8]))
                            x = x + 1
                    return lazyloader(int(request.args.get('c')), html_templates, len(html_templates), 20)
                for i in allPosts:
                    #print(i[7])
                    if str(location.lower()) in str(i[7].lower()) or str(location.lower()) == str(i[7].lower()):
                        orderedDb.append(i)
                x = 0
                for p in orderedDb:
                    if x == 0:
                        html_templates.append(html_template.format(240, "/jobs?id={}".format(p[12][-8:]), p[0], p[2], p[2], p[7], p[7], str(p[4]), p[8]))
                        x = x + 1
                    else:
                        html_templates.append(html_template.format(0, "/jobs?id={}".format(p[12][-8:]), p[0], p[2], p[2], p[7], p[7], str(p[4]), p[8]))
                        x = x + 1
                return lazyloader(int(request.args.get('c')), html_templates, len(html_templates), 20)
            elif company != None:
                for i in allPosts:
                    if company.upper() == i[2].upper():
                        orderedDb.append(i)
                x = 0
                for p in orderedDb:
                    if x == 0:
                        html_templates.append(html_template.format(240, "/jobs?id={}".format(p[12][-8:]), p[0], p[2], p[2], p[7], p[7], str(p[4]), p[8]))
                        x = x + 1
                    else:
                        html_templates.append(html_template.format(0, "/jobs?id={}".format(p[12][-8:]), p[0], p[2], p[2], p[7], p[7], str(p[4]), p[8]))
                        x = x + 1
                return lazyloader(int(request.args.get('c')), html_templates, len(html_templates), 20)

@application.route('/jobs') ##Dynamically generate job overview on request by ID (sent by js)
def jobs():
    try:
        print(session['logged_in'])
    except:
        session['logged_in'] = False
    if request.args:
        if request.args.get('jid') != None:
            id = request.args.get('jid')
            links = []
            job = []
            newJob = []
            ref = db.retrieve()
            for i in ref:
                links.append(i[12])
            for i in links:
                #print(i[-8:])
                if str(id) == str(i[-8:]):
                    job.append(i)
            for i in ref:
                if i[12] == job[0]:
                    newJob.append(i)
            return jsonify([jobs_template.format(newJob[0][7], newJob[0][2], newJob[0][4], newJob[0][0], newJob[0][2], newJob[0][9], newJob[0][12]), ''], 200)
        else:
            id = request.args.get('id')
            if session['logged_in']:
                return render_template('rewrite/jobs.html', id=id)
            else:
                return render_template('rewrite/jobs.html', id=id)
    else:
        return redirect(url_for(root))

@application.route('/contact-us')
def contactus():
    try:
        print(session['logged_in'])
    except:
        session['logged_in'] = False
    if session['logged_in']:
        return render_template('basic/contactus_li.html')
    else:
        return render_template('basic/contactus.html')

@application.route('/testing')
def testing():
    return render_template('index.html')

if __name__ == '__main__': ##Starts server
    application.run(host='0.0.0.0', port=5000, debug=True)


