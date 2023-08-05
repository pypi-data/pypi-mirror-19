import socket
import time
import requests
from operator import attrgetter, itemgetter
from random import randrange
from datetime import datetime
from dateutil.tz import tzutc
from utilofies.stdlib import canonicalized, lgroupby
from .. import settings
from ..utils.logger import logger
from ..models import Session, Entry


# In accordance with
# https://dev.twitter.com/docs/streaming-apis/connecting#Stalls
socket.setdefaulttimeout(90)

class UnchangedException(Exception):
    pass


class BaseEntryInterface(object):

    def __init__(self, fetcher, raw_entry):
        self.fetcher = fetcher
        self.raw_entry = raw_entry

    @property
    def id(self):
        pass

    @property
    def summary(self):
        pass

    @property
    def summary_type(self):
        pass

    @property
    def content(self):
        pass

    @property
    def content_type(self):
        pass

    @property
    def source(self):
        pass

    @property
    def title(self):
        pass

    @property
    def fetched(self):
        return datetime.utcnow()

    @property
    def updated(self):
        pass

    @property
    def published(self):
        pass

    @property
    def link(self):
        pass

    @property
    def author(self):
        pass

    @property
    def entry(self):
        summary, summary_type = self.summary, self.summary_type
        content, content_type = self.content, self.content_type
        if settings.INCLUDE_SOURCE:
            if content:
                content = '{}\n\n{}'.format(content, self.source)
                content_type = 'html'
            else:
                # It is recommended that summary be nonempty
                # if there is no content. This is also useful
                # for the separate content fetching.
                summary = '{}\n\n{}'.format(summary, self.source)
                summary_type = 'html'
        return Entry(
            id=self.id,
            title=self.title or self.fetcher.title,
            fetched=self.fetched,
            updated=self.updated or datetime.utcnow(),
            published=self.published,
            link=self.link or self.fetcher.link or self.fetcher.url,
            summary=summary,
            summary_type=summary_type,
            content=content,
            content_type=content_type,
            author=self.author or self.fetcher.author,
            source_id=self.fetcher.id,
            source_title=self.fetcher.title,
            source_link=self.fetcher.url)


class BaseFetcher(object):

    type_mapping = {
        'text/plain': 'text',
        'text/html': 'html',
        'application/xhtml+xml': 'xhtml'}
    EntryInterface = BaseEntryInterface

    def __init__(self, url, interval, default_tz=tzutc, defaults=None,
                 update_existing=False, **kwargs):
        self.defaults = defaults or {}
        self.url = url
        # Fuzziness to spread updates out more evenly
        self.interval = interval - randrange(interval // 10 + 1)
        self.last_check = time.time() + self.interval
        self.default_tz = default_tz
        self.update_existing = update_existing
        self.kwargs = kwargs
        self.kwargs.setdefault('headers', {})
        self.kwargs['headers'].setdefault('user-agent', settings.USER_AGENT)
        self.kwargs.setdefault('timeout', settings.TIMEOUT)
        self.response_headers = {}

    @property
    def id(self):
        pass

    @property
    def title(self):
        pass

    @property
    def subtitle(self):
        pass

    @property
    def link(self):
        pass

    @property
    def hub(self):
        pass

    @property
    def author(self):
        pass

    @property
    def generator(self):
        pass

    def __hash__(self):
        return hash(self.url)

    def retrieve(self):
        self.kwargs['headers'].update(canonicalized({
            'if-modified-since': self.response_headers.get('last-modified'),
            'if-none-match': self.response_headers.get('etag')}))
        response = requests.get(self.url, **self.kwargs)
        response.raise_for_status()
        if response.url != self.url:
            logger.info('Redirects to %s', response.url)
        self.response_headers = response.headers
        if response.status_code == 304:
            raise UnchangedException
        return response

    def parse(self, response):
        raise NotImplementedError()

    @property
    def needs_update(self):
        return self.next_check < time.time()

    @property
    def next_check(self):
        return self.last_check + self.interval

    def touch(self):
        self.last_check = time.time()

    def clean(self):
        self.source = None
        self.raw_entries = None

    def is_valid(self, entry):
        return True

    @property
    def entries(self):
        for raw_entry in self.raw_entries:
            entry = self.EntryInterface(
                fetcher=self, raw_entry=raw_entry)
            if self.is_valid(entry):
                entry = entry.entry  # From EntryInterface to models.Entry
                for key, value in self.defaults.items():
                    if not getattr(entry, key, None):
                        setattr(entry, key, value)
                yield entry

    def _nub(self, entries):
        """Remove internal duplicates"""
        nub = [(key, len(value), value[0])
               for key, value
               in lgroupby(entries, attrgetter('id'))]
        entries = list(zip(*nub))[2]
        for id_, count, entry in nub:
            if count > 1:
                logger.warn('Removed duplicate entry: %s', entry)
        return entries

    def _deduplicate(self, entries):
        """Remove known entries"""
        session = Session()
        existing_ids = set(map(
            itemgetter(0),
            session.query(Entry.id)
                .filter(Entry.id.in_(map(attrgetter('id'), entries)))))
        return [entry for entry in entries
                if entry.id not in existing_ids]

    def persist(self):
        entries = sorted(self.entries, key=attrgetter('id'))
        if not entries:
            logger.warn('Feed seems empty')
            return []
        session = Session()
        entries = self._nub(entries)
        fresh_entries = self._deduplicate(entries)
        if not self.update_existing:  # Don't update by default
            entries = fresh_entries
        try:
            for entry in entries:
                assert entry.fetched, 'fetched time missing'
                if self.update_existing:
                    session.merge(entry)
                else:
                    session.add(entry)
            session.commit()
        except:
            session.rollback()
            raise
        if fresh_entries:
            logger.info('%s new entries', len(fresh_entries))
        return fresh_entries
