# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Teacher'
        db.create_table(u'marketplace_teacher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teacher_name', to=orm['marketplace.User'])),
            ('hangout', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teacher_hangout', to=orm['marketplace.User'])),
        ))
        db.send_create_signal(u'marketplace', ['Teacher'])

        # Removing M2M table for field classroom on 'Learner'
        db.delete_table(db.shorten_name(u'marketplace_learner_classroom'))

        # Adding M2M table for field student on 'Classroom'
        m2m_table_name = db.shorten_name(u'marketplace_classroom_student')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('classroom', models.ForeignKey(orm[u'marketplace.classroom'], null=False)),
            ('learner', models.ForeignKey(orm[u'marketplace.learner'], null=False))
        ))
        db.create_unique(m2m_table_name, ['classroom_id', 'learner_id'])


    def backwards(self, orm):
        # Deleting model 'Teacher'
        db.delete_table(u'marketplace_teacher')

        # Adding M2M table for field classroom on 'Learner'
        m2m_table_name = db.shorten_name(u'marketplace_learner_classroom')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('learner', models.ForeignKey(orm[u'marketplace.learner'], null=False)),
            ('classroom', models.ForeignKey(orm[u'marketplace.classroom'], null=False))
        ))
        db.create_unique(m2m_table_name, ['learner_id', 'classroom_id'])

        # Removing M2M table for field student on 'Classroom'
        db.delete_table(db.shorten_name(u'marketplace_classroom_student'))


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
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'classroom_learner'", 'symmetrical': 'False', 'to': u"orm['marketplace.Learner']"}),
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
            'hangout': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student_hangout'", 'to': u"orm['marketplace.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student_name'", 'to': u"orm['marketplace.User']"})
        },
        u'marketplace.teacher': {
            'Meta': {'object_name': 'Teacher'},
            'hangout': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teacher_hangout'", 'to': u"orm['marketplace.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teacher_name'", 'to': u"orm['marketplace.User']"})
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
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['marketplace']