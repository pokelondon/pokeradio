# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CredentialsModal'
        db.delete_table(u'pokeradio_credentialsmodal')

        # Deleting model 'FlowModal'
        db.delete_table(u'pokeradio_flowmodal')


    def backwards(self, orm):
        # Adding model 'CredentialsModal'
        db.create_table(u'pokeradio_credentialsmodal', (
            ('credential', self.gf('oauth2client.django_orm.CredentialsField')(null=True)),
            ('id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], primary_key=True)),
        ))
        db.send_create_signal(u'pokeradio', ['CredentialsModal'])

        # Adding model 'FlowModal'
        db.create_table(u'pokeradio_flowmodal', (
            ('flow', self.gf('oauth2client.django_orm.FlowField')(null=True)),
            ('id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], primary_key=True)),
        ))
        db.send_create_signal(u'pokeradio', ['FlowModal'])


    models = {
        
    }

    complete_apps = ['pokeradio']