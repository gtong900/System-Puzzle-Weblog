import datetime
import os
import psycopg2
import time

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def index():
    # Connect to database
    conn = psycopg2.connect(host='db', database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()

    # Get number of all GET requests
    sql_all = """SELECT COUNT(*) FROM weblogs;"""
    cur.execute(sql_all)
    all = cur.fetchone()[0]

    # Get number of all succesful requests
    sql_success = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\';"""
    cur.execute(sql_success)
    success = cur.fetchone()[0]

    # Get number of all remote requests
    sql_all_remote = """SELECT COUNT(*) FROM weblogs WHERE source = \'remote\';"""
    cur.execute(sql_all_remote)
    all_remote = cur.fetchone()[0]

    # Get number of all succesful remote requests
    sql_success_remote = """SELECT COUNT(*) FROM weblogs WHERE status LIKE \'2__\' AND source = \'remote\';"""
    cur.execute(sql_success_remote)
    success_remote = cur.fetchone()[0]

    # Calculate the number of all local requests and succesful local requests based on previous read from database
    all_local = all - all_remote
    success_local = success - success_remote

    # Determine rate if there was at least one request with respect to all, remote and local
    rate = "No entries yet!"
    rate_for_remote = "No entries yet!"
    rate_for_local = "No entries yet!"

    confirm = False
    if all != 0:
        rate = str(success /all) + "(" + str(round(success / all * 100,2)) + "%)"
        if all_remote != 0:
            rate_for_remote = str(success_remote / all_remote) + "(" + str(round(success_remote / all_remote * 100,2)) + "%)"
        if all_local != 0:
            rate_for_local = str(success_local / all_local) + "(" + str(round(success_local / all_local * 100,2)) + "%)"
        # Determine if all the data has been processed
        time.sleep(0.1)
        cur.execute(sql_all)
        confirm = (cur.fetchone()[0] == all)

    return render_template('index.html', rate = rate, all = all, success = success, fail = all - success,
                        status = confirm, rate_for_remote = rate_for_remote, rate_for_local = rate_for_local)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
