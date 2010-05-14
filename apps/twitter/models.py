# -*- coding: utf-8 -*-
import json
import tweepy

from django.db import models

class TweetManager(models.Manager):
    def search(query='#openparty', limit=5, since=None, page=1):
        tweets = tweepy.api.search(q=query, rpp=limit, since_id=since, page=page)
        return [self.model(tweet=tweet) for tweet in tweets]

# Create your models here.
class Tweet(models.Model):
    """(A model represent the tweets of twitter.com)"""
    tweet_id = models.PositiveIntegerField(blank=True, null=True)
    profile_image = models.CharField(blank=True, max_length=255)
    text = models.CharField(blank=True, max_length=512)
    language = models.CharField(blank=True, max_length=16)
    geo = models.CharField(blank=True, max_length=80)
    tweet_user_id = models.PositiveIntegerField(blank=True, null=True)
    tweet_user_name = models.CharField(blank=True, max_length=128)
    craeted_at = models.DateField(blank=False, null=False)
    source = models.CharField(blank=True, max_length=80)
    dump = models.TextField(blank=True)
    
    objects = TweetManager()
    
    def __init__(self, *args, **kwargs):
        super(Tweet, self).__init__(*args, **kwargs)
        if 'tweet' in kwargs:
            tweet = kwargs['tweet']
            self.tweet_id = tweet.id
            self.profile_image = tweet.profile_image_url
            self.text = tweet.text
            self.language = tweet.iso_language_code
            self.geo = tweet.geo
            self.tweet_user_id = tweet.from_user_id
            self.tweet_user_name = tweet.from_user
            self.created_at = tweet.created_at
            self.source = tweet.source
            self.dump = json.dumps(tweet.__dict__)

    class Meta:
        ordering = []
        verbose_name, verbose_name_plural = "Tweet", "s"

    def __unicode__(self):
        return u"Tweet"

    @models.permalink
    def get_absolute_url(self):
        return ('Tweet', [self.id])