# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, invalid-name, import-error

from google.appengine.ext import ndb

def int_validator(prop, val):
	if(val):
		val = int(val)
		return val

class Professor(ndb.Model):
    nome = ndb.StringProperty(required=True)
    area = ndb.StringProperty(required=True)
    perfil = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    foto = ndb.BlobProperty()

class Cursos(ndb.Model):
	nome = ndb.StringProperty(required=True)
	periodo = ndb.StringProperty(required=True)
	semestral = ndb.StringProperty(required=True)
	disciplina = ndb.TextProperty(required=True)