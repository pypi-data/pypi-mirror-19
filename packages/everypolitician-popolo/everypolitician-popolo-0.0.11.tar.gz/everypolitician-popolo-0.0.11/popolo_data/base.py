from datetime import date
import json
import re


from approx_dates.models import ApproxDate
from six.moves.urllib_parse import urlsplit
import six


class ObjectDoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


def _is_name_current_at(name_object, date_string):
    start_range = name_object.get('start_date') or '0001-01-01'
    end_range = name_object.get('end_date') or '9999-12-31'
    return date_string >= start_range and date_string <= end_range


def extract_twitter_username(username_or_url):
    split_url = urlsplit(username_or_url)
    if split_url.netloc == 'twitter.com':
        return re.sub(r'^/([^/]+).*', r'\1', split_url.path)
    return username_or_url.strip().lstrip('@')


def first(l):
    '''Return the first item of a list, or None if it's empty'''
    return l[0] if l else None


def unique_preserving_order(sequence):
    '''Return a list with only the unique elements, preserving order

    This is from http://stackoverflow.com/a/480227/223092'''
    seen = set()
    seen_add = seen.add
    return [x for x in sequence if not (x in seen or seen_add(x))]


class PopoloObject(object):

    def __init__(self, data, all_popolo):
        self.data = data
        self.all_popolo = all_popolo

    def get_date(self, attr, default):
        d = self.data.get(attr)
        if d:
            return ApproxDate.from_iso8601(d)
        return default

    def get_related_object_list(self, popolo_array):
        return self.data.get(popolo_array, [])

    def get_related_values(
            self, popolo_array, info_type_key, info_type, info_value_key):
        '''Get a value from one of the Popolo related objects

        For example, if you have a person with related links, like
        this:

            {
                "name": "Dale Cooper",
                "links": [
                    {
                        "note": "wikipedia",
                        "url": "https://en.wikipedia.org/wiki/Dale_Cooper"
                    }
                ]
            }

        When calling this method to get the Wikipedia URL, you would use:

            popolo_array='links'
            info_type_key='note'
            info_type='wikipedia'
            info_value_key='url'

        ... so the following would work:

            self.get_related_value('links', 'note', 'wikipedia', 'url')
            # => 'https://en.wikipedia.org/wiki/Dale_Cooper'
        '''
        return [
            o[info_value_key]
            for o in self.get_related_object_list(popolo_array)
            if o[info_type_key] == info_type]

    def identifier_values(self, scheme):
        return self.get_related_values(
            'identifiers', 'scheme', scheme, 'identifier')

    def identifier_value(self, scheme):
        return first(self.identifier_values(scheme))

    def link_values(self, note):
        return self.get_related_values('links', 'note', note, 'url')

    def link_value(self, note):
        return first(self.link_values(note))

    def contact_detail_values(self, contact_type):
        return self.get_related_values(
            'contact_details', 'type', contact_type, 'value')

    def contact_detail_value(self, contact_type):
        return first(self.contact_detail_values(contact_type))

    @property
    def key_for_hash(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.id != other.id
        return NotImplemented

    def __hash__(self):
        return hash(self.key_for_hash)

    def repr_helper(self, enclosed_text):
        fmt = str('<{0}: {1}>')
        class_name = type(self).__name__
        if six.PY2:
            return fmt.format(class_name, enclosed_text.encode('utf-8'))
        return fmt.format(class_name, enclosed_text)


class CurrentMixin(object):

    def current_at(self, when):
        return ApproxDate.possibly_between(
            self.start_date, when, self.end_date)

    @property
    def current(self):
        return self.current_at(date.today())


class Person(PopoloObject):

    class DoesNotExist(ObjectDoesNotExist):
        pass

    class MultipleObjectsReturned(MultipleObjectsReturned):
        pass

    @property
    def id(self):
        return self.data.get('id')

    @property
    def email(self):
        return self.data.get('email')

    @property
    def gender(self):
        return self.data.get('gender')

    @property
    def honorific_prefix(self):
        return self.data.get('honorific_prefix')

    @property
    def honorific_suffix(self):
        return self.data.get('honorific_suffix')

    @property
    def image(self):
        return self.data.get('image')

    @property
    def name(self):
        return self.data.get('name')

    @property
    def sort_name(self):
        return self.data.get('sort_name')

    @property
    def national_identity(self):
        return self.data.get('national_identity')

    @property
    def summary(self):
        return self.data.get('summary')

    @property
    def biography(self):
        return self.data.get('biography')

    @property
    def birth_date(self):
        return self.get_date('birth_date', None)

    @property
    def death_date(self):
        return self.get_date('death_date', None)

    @property
    def family_name(self):
        return self.data.get('family_name')

    @property
    def given_name(self):
        return self.data.get('given_name')

    @property
    def wikidata(self):
        return self.identifier_value('wikidata')

    @property
    def twitter(self):
        username_or_url = self.contact_detail_value('twitter') or \
            self.link_value('twitter')
        if username_or_url:
            return extract_twitter_username(username_or_url)
        return None

    @property
    def twitter_all(self):
        # The Twitter screen names in contact_details and links will
        # in most cases be the same, so remove duplicates:
        return unique_preserving_order(
            extract_twitter_username(v) for v in
            self.contact_detail_values('twitter') +
            self.link_values('twitter'))

    @property
    def phone(self):
        return self.contact_detail_value('phone')

    @property
    def phone_all(self):
        return self.contact_detail_values('phone')

    @property
    def facebook(self):
        return self.link_value('facebook')

    @property
    def facebook_all(self):
        return self.link_values('facebook')

    @property
    def fax(self):
        return self.contact_detail_value('fax')

    @property
    def fax_all(self):
        return self.contact_detail_values('fax')

    def __repr__(self):
        return self.repr_helper(self.name)

    def name_at(self, particular_date):
        historic_names = [n for n in self.other_names if n.get('end_date')]
        if not historic_names:
            return self.name
        names_at_date = [
            n for n in historic_names
            if _is_name_current_at(n, str(particular_date))
        ]
        if not names_at_date:
            return self.name
        if len(names_at_date) > 1:
            msg = "Multiple names for {0} found at date {1}"
            raise Exception(msg.format(self, particular_date))
        return names_at_date[0]['name']

    @property
    def links(self):
        return self.get_related_object_list('links')

    @property
    def contact_details(self):
        return self.get_related_object_list('contact_details')

    @property
    def identifiers(self):
        return self.get_related_object_list('identifiers')

    @property
    def images(self):
        return self.get_related_object_list('images')

    @property
    def other_names(self):
        return self.get_related_object_list('other_names')

    @property
    def sources(self):
        return self.get_related_object_list('sources')

    @property
    def memberships(self):
        memberships_list = [
            m.data for m in self.all_popolo.memberships
            if m.person_id == self.id
        ]
        return MembershipCollection(memberships_list, self.all_popolo)

    __hash__ = PopoloObject.__hash__


class Organization(PopoloObject):

    class DoesNotExist(ObjectDoesNotExist):
        pass

    class MultipleObjectsReturned(MultipleObjectsReturned):
        pass

    @property
    def id(self):
        return self.data.get('id')

    @property
    def name(self):
        return self.data.get('name')

    @property
    def wikidata(self):
        return self.identifier_value('wikidata')

    @property
    def classification(self):
        return self.data.get('classification')

    @property
    def image(self):
        return self.data.get('image')

    @property
    def founding_date(self):
        return self.get_date('founding_date', None)

    @property
    def dissolution_date(self):
        return self.get_date('dissolution_date', None)

    @property
    def seats(self):
        return self.data.get('seats')

    @property
    def other_names(self):
        return self.data.get('other_names', [])

    def __repr__(self):
        return self.repr_helper(self.name)

    @property
    def identifiers(self):
        return self.get_related_object_list('identifiers')

    @property
    def links(self):
        return self.get_related_object_list('links')


class Membership(CurrentMixin, PopoloObject):

    class DoesNotExist(ObjectDoesNotExist):
        pass

    class MultipleObjectsReturned(MultipleObjectsReturned):
        pass

    @property
    def role(self):
        return self.data.get('role')

    @property
    def person_id(self):
        return self.data.get('person_id')

    @property
    def person(self):
        return self.all_popolo.persons.lookup_from_key[self.person_id]

    @property
    def organization_id(self):
        return self.data.get('organization_id')

    @property
    def organization(self):
        collection = self.all_popolo.organizations
        return collection.lookup_from_key[self.organization_id]

    @property
    def area_id(self):
        return self.data.get('area_id')

    @property
    def area(self):
        return self.all_popolo.areas.lookup_from_key[self.area_id]

    @property
    def legislative_period_id(self):
        return self.data.get('legislative_period_id')

    @property
    def legislative_period(self):
        collection = self.all_popolo.events
        return collection.lookup_from_key[self.legislative_period_id]

    @property
    def on_behalf_of_id(self):
        return self.data.get('on_behalf_of_id')

    @property
    def on_behalf_of(self):
        collection = self.all_popolo.organizations
        return collection.lookup_from_key[self.on_behalf_of_id]

    @property
    def post_id(self):
        return self.data.get('post_id')

    @property
    def post(self):
        return self.all_popolo.posts.lookup_from_key[self.post_id]

    @property
    def start_date(self):
        return self.get_date('start_date', ApproxDate.PAST)

    @property
    def end_date(self):
        return self.get_date('end_date', ApproxDate.FUTURE)

    def __repr__(self):
        enclosed = u"'{0}' at '{1}'".format(
            self.person_id, self.organization_id)
        return self.repr_helper(enclosed)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.data == other.data
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.data != other.data
        return NotImplemented

    @property
    def key_for_hash(self):
        return json.dumps(self.data, sort_keys=True)

    def __hash__(self):
        return hash(self.key_for_hash)


class Area(PopoloObject):

    @property
    def id(self):
        return self.data.get('id')

    @property
    def name(self):
        return self.data.get('name')

    @property
    def type(self):
        return self.data.get('type')

    @property
    def identifiers(self):
        return self.get_related_object_list('identifiers')

    @property
    def other_names(self):
        return self.get_related_object_list('other_names')

    @property
    def wikidata(self):
        return self.identifier_value('wikidata')

    def __repr__(self):
        return self.repr_helper(self.name)


class Post(PopoloObject):

    @property
    def id(self):
        return self.data.get('id')

    @property
    def label(self):
        return self.data.get('label')

    @property
    def organization_id(self):
        return self.data.get('organization_id')

    @property
    def organization(self):
        collection = self.all_popolo.organizations
        return collection.lookup_from_key[self.organization_id]

    def __repr__(self):
        return self.repr_helper(self.label)


class Event(CurrentMixin, PopoloObject):

    @property
    def id(self):
        return self.data.get('id')

    @property
    def name(self):
        return self.data.get('name')

    @property
    def classification(self):
        return self.data.get('classification')

    @property
    def start_date(self):
        return self.get_date('start_date', ApproxDate.PAST)

    @property
    def end_date(self):
        return self.get_date('end_date', ApproxDate.FUTURE)

    @property
    def organization_id(self):
        return self.data.get('organization_id')

    @property
    def organization(self):
        collection = self.all_popolo.organizations
        return collection.lookup_from_key[self.organization_id]

    def __repr__(self):
        return self.repr_helper(self.name)

    @property
    def identifiers(self):
        return self.get_related_object_list('identifiers')

    @property
    def memberships(self):
        memberships_list = [
            m.data for m in self.all_popolo.memberships
            if m.legislative_period_id == self.id
        ]
        return MembershipCollection(memberships_list, self.all_popolo)


class PopoloCollection(object):

    def __init__(self, data_list, object_class, all_popolo):
        self.all_popolo = all_popolo
        self.object_class = object_class
        self.object_list = \
            [self.object_class(data, all_popolo) for data in data_list]
        self.lookup_from_key = {}
        for o in self.object_list:
            self.lookup_from_key[o.key_for_hash] = o

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        return self.object_list[index]

    @property
    def first(self):
        return first(self.object_list)

    def filter(self, **kwargs):
        filter_list = [
            o.data for o in self.object_list
            if all(getattr(o, k) == v for k, v in kwargs.items())
        ]
        return self.__class__(filter_list, self.all_popolo)

    def get(self, **kwargs):
        matches = self.filter(**kwargs)
        n = len(matches)
        if n == 0:
            msg = "No {0} found matching {1}"
            raise self.object_class.DoesNotExist(msg.format(
                self.object_class, kwargs))
        elif n > 1:
            msg = "Multiple {0} objects ({1}) found matching {2}"
            raise self.object_class.MultipleObjectsReturned(msg.format(
                self.object_class, n, kwargs))
        return matches[0]


class PersonCollection(PopoloCollection):

    def __init__(self, persons_data, all_popolo):
        super(PersonCollection, self).__init__(
            persons_data, Person, all_popolo)


class OrganizationCollection(PopoloCollection):

    def __init__(self, organizations_data, all_popolo):
        super(OrganizationCollection, self).__init__(
            organizations_data, Organization, all_popolo)


class MembershipCollection(PopoloCollection):

    def __init__(self, memberships_data, all_popolo):
        super(MembershipCollection, self).__init__(
            memberships_data, Membership, all_popolo)


class AreaCollection(PopoloCollection):

    def __init__(self, areas_data, all_popolo):
        super(AreaCollection, self).__init__(
            areas_data, Area, all_popolo)


class PostCollection(PopoloCollection):

    def __init__(self, posts_data, all_popolo):
        super(PostCollection, self).__init__(
            posts_data, Post, all_popolo)


class EventCollection(PopoloCollection):

    def __init__(self, events_data, all_popolo):
        super(EventCollection, self).__init__(
            events_data, Event, all_popolo)

    @property
    def elections(self):
        elections_list = self.filter(classification='general election')
        elections_data = [election.data for election in elections_list]
        return EventCollection(elections_data, self.all_popolo)

    @property
    def legislative_periods(self):
        lps_list = self.filter(classification='legislative period')
        legislative_periods_data = [lp.data for lp in lps_list]
        return EventCollection(legislative_periods_data, self.all_popolo)
