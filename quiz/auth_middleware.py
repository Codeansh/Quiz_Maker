from flask import Request, Response
class Middleware():
    def __init__(self,app):
        self.app = app
