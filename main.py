# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, invalid-name, import-error

import os
import jinja2
import webapp2

from google.appengine.api import images
from google.appengine.ext import ndb

from model import Professor
from model import Cursos

from time import sleep

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        professor_key = ndb.Key(urlsafe=self.request.get('img_id'))
        professor = professor_key.get()
        if professor.foto:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(professor.foto)
        else:
            self.response.out.write('No image')

class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        curso_key = ndb.Key(urlsafe=self.request.get('curso_id'))
        curso_key.delete()
        sleep(.1)
        self.redirect('/cursos')

class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        curso_key = ndb.Key(urlsafe=self.request.get('curso_id'))
        curso = curso_key.get()
        sleep(.1)
        self.redirect('/cursos')

class MainHandler(Handler):
    def get(self):
        self.render("index.html")

class ProfessorHandler(Handler):
    def get(self):
        professores = Professor.query()

        self.render("professor.html", professores=professores)

    def post(self):
        nome   = self.request.get("nome")
        area   = self.request.get("area")
        perfil = self.request.get("perfil")
        email  = self.request.get("email")
        foto   = self.request.get("img")

        professor = Professor(nome=nome, area=area, perfil=perfil,
                              email=email, foto=foto)
        professor.put()

class CursoHandler(Handler):
	def get(self):
		cursos = Cursos.query().order(Cursos.nome)

		self.render("cursos.html", cursos=cursos)

	def post(self):
		nome 	   = self.request.get("nome")
		periodo    = self.request.get("periodo")
		semestral  = self.request.get("semestral")
		disciplina = self.request.get("disciplinas")

		curso = Cursos(nome=nome, periodo=periodo, semestral=semestral, 
					    disciplina=disciplina)
		curso.put()
		sleep(.1)
		return self.redirect('/cursos')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/professor', ProfessorHandler),
    ('/img', ImageHandler),
    ('/cursos', CursoHandler),
    ('/delete', DeleteHandler),
    ('/update', UpdateHandler)
], debug=True)
