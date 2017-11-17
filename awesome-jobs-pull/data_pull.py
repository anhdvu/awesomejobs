#!/usr/bin/env python3

import sqlite3
import requests

# from flask import Flask, url_for, render_template    

def connect_db():
    ''' Connect to database'''
    conn = sqlite3.connect('job_db.db')
    return conn

def init_db():
    '''Create a sqlite db with schema'''
    c = connect_db()
    c.cursor().execute('drop table if exists jobs')
    c.cursor().execute('create table jobs (id primary key, no, title, url, content)')
    c.commit()
    c.close()


def data_pull():  # used to scrape data into db
    # Scrape data from API of awesome-jobs/vietnam repo
    page = 1
    url = 'https://api.github.com/repos/awesome-jobs/vietnam/issues?page={}'.format(page)
    r = requests.get(url)
    jobs = r.json()

    _id = None
    _number = None
    _title = None
    _url = None
    _content = None

    # Insert job data into table 'jobs' in database
    c = connect_db()
    for job in jobs:
        _id = job['id']
        _number = job['number']
        _title = job['title']
        _url = job['html_url']
        _content = job['body']
        c.cursor().execute('insert into jobs values (?,?,?,?,?)', (_id, _number,_title, _url, _content))
    c.commit()
    c.close()

def main():
    data_pull()

if __name__ == '__main__':
    main()