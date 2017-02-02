#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import  cgi
import re
#user sign up

signup_form="""
<form method="post">

 <table>
    <tbody><tr>
                    <td><label>Username</label></td>
                    <td>
                        <input name="username" type="text" value="%(username)s" required>
                        <span class="error" style="color:red">%(username_error)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label>Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error" style="color:red">%(password_error)s </span>
                    </td>
                </tr>
                <tr>
                    <td><label>Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label>Email (optional)</label></td>
                    <td>
                        <input name="email" type="text" value="%(email)s">
                        <span class="error" style="color:red">%(email_error)s</span>
                    </td>
                </tr>
            </tbody></table>
            <input type="submit">
</form>
"""
Welcome_form="""
<!DOCTYPE html>

<html>
    <head>
        <title>Welcome page!</title>
    </head>

    <body>
        <h2>Welcome, %(username)s!</h2>

    </body>
</html>"""

header="<h1>Signup</h1>"

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile("^.{3,20}$")
def valid_password(password):
    return USER_RE.match(password)

EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)



class SignupHandler(webapp2.RequestHandler):
    #self.response.write(content)

    def write_form(self, username="",email="",username_error="",password_error="",email_error=""):
        self.response.write(signup_form % {"username":username,
                                    "email":email,
                                    "username_error":username_error,
                                    "password_error":password_error,
                                    "email_error":email_error})


        #username error form
    def get(self):
        self.response.write(header)
        self.write_form()



    def post(self):
        username_error=""
        password_error=""
        email_error=""
        username_keyin=self.request.get('username')
        password_keyin=self.request.get('password')
        email_keyin=self.request.get('email')
        verify_keyin=self.request.get('verify')

        username_good=valid_username(username_keyin)
        password_good=valid_password(password_keyin)
        email_good=valid_email(email_keyin)

        #if not(username_good and password_good and email_good):  #only works if the username is not (not good)--> True.
        #if submitting blank user form.
        if  not (username_good and email_good and password_good): #only works if one of the field has bad data,
            #including blank spaces. set everything here but do not writeanything
            #to the form. write everything after all ifs are executed.
            if not username_good:#find out whihc one is bad input or blankspaces
                username_error="That's not a valid username."
        if  not (username_good and email_good and password_good):
            if not password_good:#is this bad . find out whihc one is bad input or blankspaces
                password_error="That's not a valid password."
        if  not (username_good and email_good and password_good):
            if not email_good: #is this bad . find out whihc one is bad input or blankspaces
                if email_keyin !="":
                    email_error="That's not a valid email."
        if password_good: #repeat password check
            if password_keyin !=verify_keyin:
                password_error="That's not a valid password."
                        #self.write_form(username_keyin,email_keyin,username_error,password_error,email_error)

        if  username_good and email_good and password_good:
            self.redirect('/Welcome?username=' + username_keyin)

        self.response.write(header)
        self.write_form(username_keyin,email_keyin,username_error,password_error,email_error)
        self.response.write("<br>"+"email_error: "+email_error+"<br>")
        self.response.write("<br>"+"username_error: "+username_error+"<br>")
        self.response.write("<br>"+"password_error: "+password_error+"<br>")
        self.response.write("<br>"+"username_good listed below: "+"<br>")
        self.response.write(username_good)
        self.response.write("<br>"+"email_good listed below"+"<br>")
        self.response.write(email_good)
        self.response.write("<br>"+"email entered "+email_keyin+"<br>")
        self.response.write("<br>"+"password entered "+password_keyin+"<br>")
        self.response.write("<br>"+"verify entered "+verify_keyin+"<br>")

        #otherwise everything looks good and its a success

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username=self.request.get('username')
        if valid_username(username):
            self.response.write(Welcome_form % {"username":username})
        else:
            self.redirect('/signup')


app = webapp2.WSGIApplication([
    ('/signup', SignupHandler),('/Welcome', WelcomeHandler)
], debug=True)
