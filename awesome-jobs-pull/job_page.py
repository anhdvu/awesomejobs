#!/usr/bin/env python3

from data_pull import connect_db,  init_db, data_pull
from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route('/')
def job_page():
    init_db()
    data_pull()
    conn = connect_db()
    c = conn.cursor()
    c.execute('select * from jobs order by no desc')
    data = c.fetchall()

    jobs = [(job[1], job[2], job[3]) for job in data]
    li_tags = ['<li><a href="{}">{} - {}</a></li>'.format(url, str(no), title) for no, title, url in jobs]
    output_string = '''<h1>Awesome Jobs</h1>
                        <ul>{}</ul><br />
                        <div><p>Author: Duy Anh<br />For PyMi class</p></div>
                        '''.format(''.join(li_tags))
    return output_string

if __name__ == '__main__':
    app.run(debug=False)