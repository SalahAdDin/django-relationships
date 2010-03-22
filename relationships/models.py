from django.contrib.auth.models import User
from django.db import models
from relationships.constants import *

class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='from_users')
    to_user = models.ForeignKey(User, related_name='to_users')
    status = models.IntegerField(default=RELATIONSHIP_FOLLOWING, 
                                 choices=RELATIONSHIP_STATUSES)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('from_user', 'to_user', 'status'),)

    def __unicode__(self):
        return 'Relationship from %s to %s' % (from_user.username,
                                               to_user.username)

field = models.ManyToManyField(User, through=Relationship, 
                               symmetrical=False, related_name='related_to')

class UserRelationships(object):
    def add_relationship(self, user, status=RELATIONSHIP_FOLLOWING):
        relationship, created = Relationship.objects.get_or_create(
            from_user=self,
            to_user=user,
            status=status)
        return relationship
    
    def remove_relationship(self, user, status=RELATIONSHIP_FOLLOWING):
        Relationship.objects.filter(
            from_user=self, 
            to_user=user,
            status=status).delete()
        return
    
    def get_relationships(self, status):
        return self.relationships.filter(
            to_users__status=status, 
            to_users__from_user=self)
    
    def get_related_to(self, status):
        return self.related_to.filter(
            from_users__status=status, 
            from_users__to_user=self)
    
    def get_following(self):
        return self.get_relationships(RELATIONSHIP_FOLLOWING)
    
    def get_followers(self):
        return self.get_related_to(RELATIONSHIP_FOLLOWING)
    
    def get_friends(self):
        return self.relationships.filter(
            to_users__status=RELATIONSHIP_FOLLOWING, 
            to_users__from_user=self,
            from_users__status=RELATIONSHIP_FOLLOWING, 
            from_users__to_user=self)

#HACK
field.contribute_to_class(User, 'relationships')
for name, attr in UserRelationships.__dict__.items():
    if callable(attr):
        setattr(User, name, attr)