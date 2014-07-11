# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.past1'
        db.add_column(u'marketplace_user', 'past1',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=50),
                      keep_default=False)

        # Adding field 'User.past2'
        db.add_column(u'marketplace_user', 'past2',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=50),
                      keep_default=False)

        # Adding field 'User.past3'
        db.add_column(u'marketplace_user', 'past3',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=50),
                      keep_default=False)

        # Adding field 'User.skill1'
        db.add_column(u'marketplace_user', 'skill1',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=50),
                      keep_default=False)

        # Adding field 'User.skill2'
        db.add_column(u'marketplace_user', 'skill2',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=50),
                      keep_default=False)

        # Adding field 'User.skill3'
        db.add_column(u'marketplace_user', 'skill3',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'User.past1'
        db.delete_column(u'marketplace_user', 'past1')

        # Deleting field 'User.past2'
        db.delete_column(u'marketplace_user', 'past2')

        # Deleting field 'User.past3'
        db.delete_column(u'marketplace_user', 'past3')

        # Deleting field 'User.skill1'
        db.delete_column(u'marketplace_user', 'skill1')

        # Deleting field 'User.skill2'
        db.delete_column(u'marketplace_user', 'skill2')

        # Deleting field 'User.skill3'
        db.delete_column(u'marketplace_user', 'skill3')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'marketplace.classroom': {
            'Meta': {'object_name': 'Classroom'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classroom_teacher'", 'to': u"orm['marketplace.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'marketplace.emailsignup': {
            'Meta': {'object_name': 'EmailSignup'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'marketplace.learner': {
            'Meta': {'object_name': 'Learner'},
            'classroom': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'student_classroom'", 'symmetrical': 'False', 'to': u"orm['marketplace.Classroom']"}),
            'hangout': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student_hangout'", 'to': u"orm['marketplace.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student_name'", 'to': u"orm['marketplace.User']"})
        },
        u'marketplace.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'hangout': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'past1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'past2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'past3': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'skill1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'skill2': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'skill3': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['marketplace']