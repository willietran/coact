# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Classroom.api_key'
        db.delete_column(u'marketplace_classroom', 'api_key')


    def backwards(self, orm):
        # Adding field 'Classroom.api_key'
        db.add_column(u'marketplace_classroom', 'api_key',
                      self.gf('django.db.models.fields.CharField')(default='0000', max_length=100, null=True),
                      keep_default=False)


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
        u'marketplace.calendar': {
            'Meta': {'object_name': 'Calendar'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'calendar_slot'", 'symmetrical': 'False', 'to': u"orm['marketplace.Slot']"}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'calendar_teacher'", 'to': u"orm['marketplace.User']"})
        },
        u'marketplace.classroom': {
            'Meta': {'object_name': 'Classroom'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'screenshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
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
        u'marketplace.payment': {
            'Meta': {'object_name': 'Payment'},
            'charge_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'classroom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment_classroom'", 'to': u"orm['marketplace.Classroom']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment_student'", 'to': u"orm['marketplace.User']"})
        },
        u'marketplace.review': {
            'Meta': {'object_name': 'Review'},
            'classroom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classroom_review'", 'to': u"orm['marketplace.Classroom']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviewer_review'", 'to': u"orm['marketplace.User']"})
        },
        u'marketplace.slot': {
            'Meta': {'object_name': 'Slot'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'slot_calendar'", 'to': u"orm['marketplace.Calendar']"}),
            'day': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.IntegerField', [], {})
        },
        u'marketplace.stripekey': {
            'Meta': {'object_name': 'StripeKey'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stripe_key_user'", 'to': u"orm['marketplace.User']"})
        },
        u'marketplace.teacher': {
            'Meta': {'object_name': 'Teacher'},
            'hangout': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teacher_hangout'", 'to': u"orm['marketplace.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teacher_name'", 'to': u"orm['marketplace.User']"})
        },
        u'marketplace.user': {
            'Meta': {'object_name': 'User'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'hangout': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['marketplace']