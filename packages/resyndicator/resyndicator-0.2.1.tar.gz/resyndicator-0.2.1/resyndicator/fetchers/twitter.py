import json
from datetime import datetime
from operator import attrgetter, itemgetter
from twython import Twython, TwythonStreamer
from dateutil.parser import parse as parse_date
from dateutil.tz import tzutc
from .. import settings
from utilofies.stdlib import sub_slices, itertimeout
from ..utils.logger import logger
from ..models import Session, Entry


class TweetInterface(object):

    def __init__(self, tweet):
        self.tweet = tweet

    @property
    def tweet_text(self):
        if self.tweet.has_key('retweeted_status'):
            tweet = self.tweet['retweeted_status']
            prefix = 'RT @{screen_name}: '.format(
                screen_name=tweet['user']['screen_name'])
        else:
            tweet = self.tweet
            prefix = ''
        replacements = {}
        for url in tweet['entities']['urls']:
            replacements[tuple(url['indices'])] = \
                url.get('display_url', url['expanded_url'])
        for medium in tweet['entities'].get('media', []):
            replacements[tuple(medium['indices'])] = \
                medium.get('display_url', medium['expanded_url'])
        # Purging possible None values
        replacements = dict((key, value)
                            for key, value in replacements.items()
                            if value)
        return prefix + sub_slices(tweet['text'], replacements)

    @property
    def tweet_html(self):
        # TODO: Embed replies
        if self.tweet.has_key('retweeted_status'):
            tweet = self.tweet['retweeted_status']
            prefix = (
                'RT <a href="https://twitter.com/{screen_name}"'
                ' title="{name}">@{screen_name}</a>: ').format(
                    screen_name=tweet['user']['screen_name'],
                    name=tweet['user']['name'])
        else:
            tweet = self.tweet
            prefix = ''
        images = []
        replacements = {}
        for url in tweet['entities']['urls']:
            replacements[tuple(url['indices'])] = (
                '<a href="{expanded_url}">{display_url}</a>'.format(
                    expanded_url=url['expanded_url'],
                    display_url=url.get('display_url',
                                        url['expanded_url'])))
            if any(map((url['expanded_url'] or '').endswith,
                       ('.png', '.jpg', '.jpeg', '.gif', '.svg'))):
                images.append(url['expanded_url'])
        for hashtag in tweet['entities']['hashtags']:
            replacements[tuple(hashtag['indices'])] = (
                ('<a href="https://twitter.com/#!/search/'
                 '?q=%23{hashtag}&src=hash">#{hashtag}</a>').format(
                    hashtag=hashtag['text']))
        for mention in tweet['entities']['user_mentions']:
            # Case insensitive
            verbatim = tweet['text'][slice(*mention['indices'])]
            replacements[tuple(mention['indices'])] = (
                ('<a href="https://twitter.com/{screen_name}" title="{name}">'
                 '{verbatim}</a>').format(
                    screen_name=mention['screen_name'],
                    name=mention['name'],
                    verbatim=verbatim))
        for medium in tweet['entities'].get('media', []):
            replacements[tuple(medium['indices'])] = (
                '<a href="{expanded_url}">{display_url}</a>'.format(
                    expanded_url=medium['expanded_url'],
                    display_url=medium.get('display_url',
                                           medium['expanded_url'])))
            if medium['type'] == 'photo':
                images.append(medium['media_url'])
        # Purging possible None values
        replacements = dict((key, value)
                            for key, value in replacements.items()
                            if value)
        text = prefix + sub_slices(tweet['text'], replacements)
        images = '<br />'.join('<img src="{url}" alt="" />'.format(url=url)
                               for url in images)
        return '<p>{text}</p><p>{images}</p>'.format(text=text, images=images)

    @property
    def id(self):
        return unicode(self.tweet['id'])

    @property
    def fetched(self):
        return datetime.utcnow()

    @property
    def updated(self):
        date = parse_date(self.tweet['created_at'])
        return date.astimezone(tzutc()).replace(tzinfo=None)

    @property
    def title(self):
        tweet_text = self.tweet_text
        if len(tweet_text) > settings.TWITTER_TITLE_LENGTH:
            return tweet_text[:settings.TWITTER_TITLE_LENGTH - 1] + '…'
        return tweet_text

    @property
    def author(self):
        return '{screen_name} ({name})'.format(
            screen_name=self.tweet['user']['screen_name'],
            name=self.tweet['user']['name'])

    @property
    def link(self):
        return 'https://twitter.com/{screen_name}/statuses/{id}'.format(
            screen_name=self.tweet['user']['screen_name'],
            id=self.tweet['id'])

    @property
    def content(self):
        return self.tweet_html

    @property
    def source_id(self):
        return 'urn:twitter:user:{id}'.format(id=self.tweet['user']['id'])

    @property
    def source_title(self):
        return '{author} on Twitter'.format(author=self.author)

    @property
    def source_link(self):
        return 'https://twitter.com/{screen_name}'.format(
            screen_name=self.tweet['user']['screen_name'])

    @property
    def entry(self):
        return Entry(
            id=self.id,
            title=self.title,
            fetched=self.fetched,
            updated=self.updated,
            published=self.updated,
            link=self.link,
            content=self.content,
            content_type='html',
            author=self.author,
            source_id=self.source_id,
            source_title=self.source_title,
            source_link=self.source_link)


class TwitterStreamer(object):

    def __init__(self, oauth_token, oauth_secret, timeout=0, **kwargs):
        self.oauth_token = oauth_token
        self.oauth_secret = oauth_secret
        self.timeout = timeout
        self.kwargs = kwargs
        self.friends = None

    def store(self, entries, new=False):
        session = Session()
        if not new:
            existing_ids = map(
                itemgetter(0),
                session.query(Entry.id)
                    .filter(Entry.id.in_(map(attrgetter('id'), entries))))
            entries = [entry for entry in entries
                       if entry.id not in existing_ids]
        try:
            for entry in entries:
                session.merge(entry)
            session.commit()
        except:
            session.rollback()
            raise
        return entries

    @property
    def stream(self):
        return TwythonStreamer(
            settings.CONSUMER_KEY,
            settings.CONSUMER_SECRET,
            self.oauth_token,
            self.oauth_secret,
            **self.kwargs)

    @property
    def rest(self):
        return Twython(
            settings.CONSUMER_KEY,
            settings.CONSUMER_SECRET,
            settings.OAUTH_TOKEN,
            settings.OAUTH_SECRET)

    def retrieve_home_timeline(self, count=200):
        return self.rest.get_home_timeline(
            count=count, exclude_replies=False, include_entities=True)

    def run(self):
        for i, tweet in enumerate(itertimeout(
                self.stream.user(**{'replies': 'all', 'with': 'followings'}),
                timeout=self.timeout)):
            fresh_entries = []
            if i % settings.TWITTER_STREAM_GET_INTERVAL == 0:
                # i == 0: Initial fetch in case we missed something
                # i != 0: Additional fetch in case the streaming API
                #         missed something.
                try:
                    get_tweets = self.retrieve_home_timeline()
                except Exception as excp:
                    logger.exception('Error during initial fetch: %r', excp)
                else:
                    entries = [TweetInterface(get_tweet).entry
                               for get_tweet in get_tweets]
                    fresh_entries = self.store(entries)
                    logger.info(
                        'Stored %s missed tweets by %s',
                        len(fresh_entries),
                        ', '.join(entry.author for entry in fresh_entries)
                            or 'everyone')
            logger.debug(json.dumps(tweet, indent=4))
            if tweet.has_key('id'):
                if tweet['user']['id'] in self.friends:
                    entry = TweetInterface(tweet).entry
                    self.store([entry], new=True)
                    logger.info('Stored tweet %s by %s',
                                tweet['id'], tweet['user']['screen_name'])
                    fresh_entries.append(entry)
                else:
                    # Unfortunately Twitter also streams replies to tweets by
                    # people we’re following regardless of whether we’re
                    # following the author.
                    logger.info('Skipping foreign tweet by %s',
                                tweet['user']['screen_name'])
            elif tweet.has_key('friends'):
                # Should be the first item to be streamed
                self.friends = tweet['friends']
                logger.info('Received list of %s friends',
                            len(tweet['friends']))
            elif tweet.get('event') == 'follow':
                self.friends.append(tweet['target']['id'])
                logger.info('Received follow event for %s',
                            tweet['target']['screen_name'])
            else:
                logger.info('Skipping weird object: %s', tweet)
            # Final yield
            if fresh_entries:
                yield fresh_entries
