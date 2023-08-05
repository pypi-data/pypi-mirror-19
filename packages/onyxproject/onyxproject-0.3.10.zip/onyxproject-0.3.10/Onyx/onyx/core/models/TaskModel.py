"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.extensions import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idAccount = db.Column(db.String(64))
    idCalendar = db.Column(db.String(64))
    text = db.Column(db.String(64))
    date = db.Column(db.String(64))


    @property
    def is_active(self):
        return True

    def get_id_(self):
        try:
            return unicode(self.id)  
        except NameError:
            return str(self.id)  
