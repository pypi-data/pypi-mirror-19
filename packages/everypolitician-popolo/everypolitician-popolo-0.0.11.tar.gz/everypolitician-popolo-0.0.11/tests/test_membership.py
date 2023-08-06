from datetime import date
from unittest import TestCase

import pytest
from mock import patch

from .helpers import example_file

from popolo_data.importer import Popolo


EXAMPLE_SINGLE_MEMBERSHIP = b'''
{
    "persons": [
        {
            "id": "SP-937-215",
            "name": "Jean-Luc Picard"
        }
    ],
    "organizations": [
        {
            "id": "starfleet",
            "name": "Starfleet"
        }
    ],
    "memberships": [
        {
            "person_id": "SP-937-215",
            "organization_id": "starfleet",
            "role": "student",
            "start_date": "2327-12-01"
        }
    ]
}
'''

EXAMPLE_MEMBERSHIP_ALL_FIELDS = b'''
{
    "areas": [
        {
            "id": "dunny-on-the-wold",
            "name": "Dunny-on-the-Wold"
        }
    ],
    "events": [
        {
            "classification": "legislative period",
            "id": "pitt",
            "name": "Parliamentary Period",
            "start_date": "1783-12-19",
            "end_date": "1801-01-01"
        }
    ],
    "persons": [
        {
            "id": "1234",
            "name": "Edmund Blackadder"
        }
    ],
    "posts": [
        {
            "id": "dunny-on-the-wold-seat",
            "label": "Member of Parliament for Dunny-on-the-Wold"
        }
    ],
    "organizations": [
        {
            "id": "commons",
            "name": "House of Commons"
        },
        {
            "id": "adder",
            "name": "Adder Party",
            "classification": "party"
        }
    ],
    "memberships": [
        {
            "area_id": "dunny-on-the-wold",
            "end_date": "1784-05-23",
            "legislative_period_id": "pitt",
            "on_behalf_of_id": "adder",
            "organization_id": "commons",
            "person_id": "1234",
            "post_id": "dunny-on-the-wold-seat",
            "role": "candidates",
            "start_date": "1784-03-01"
        }
    ]
}
'''


class TestMemberships(TestCase):

    def test_empty_file_gives_no_memberships(self):
        with example_file(b'{}') as filename:
            popolo = Popolo.from_filename(filename)
            assert len(popolo.memberships) == 0

    def test_membership_should_not_have_name(self):
        with example_file(EXAMPLE_SINGLE_MEMBERSHIP) as fname:
            popolo = Popolo.from_filename(fname)
            assert len(popolo.memberships) == 1
            m = popolo.memberships[0]
            with pytest.raises(AttributeError):
                m.name

    def test_membership_has_person_id_and_organisation_id(self):
        with example_file(EXAMPLE_SINGLE_MEMBERSHIP) as fname:
            popolo = Popolo.from_filename(fname)
            assert len(popolo.memberships) == 1
            m = popolo.memberships[0]
            assert m.person_id == 'SP-937-215'
            assert m.organization_id == 'starfleet'

    def test_membership_has_role(self):
        with example_file(EXAMPLE_SINGLE_MEMBERSHIP) as fname:
            popolo = Popolo.from_filename(fname)
            assert len(popolo.memberships) == 1
            m = popolo.memberships[0]
            assert m.role == 'student'

    def test_membership_foreign_keys(self):
        with example_file(EXAMPLE_MEMBERSHIP_ALL_FIELDS) as fname:
            popolo = Popolo.from_filename(fname)
            assert len(popolo.memberships) == 1
            m = popolo.memberships[0]
            assert m.area_id == 'dunny-on-the-wold'
            assert m.on_behalf_of_id == 'adder'
            assert m.legislative_period_id == 'pitt'
            assert m.post_id == 'dunny-on-the-wold-seat'

    def test_get_organization_from_membership(self):
        with example_file(EXAMPLE_SINGLE_MEMBERSHIP) as fname:
            popolo = Popolo.from_filename(fname)
            assert len(popolo.memberships) == 1
            m = popolo.memberships[0]
            assert m.start_date == date(2327, 12, 1)

    def test_get_sentinel_end_date_from_membership(self):
        with example_file(EXAMPLE_SINGLE_MEMBERSHIP) as fname:
            popolo = Popolo.from_filename(fname)
            m = popolo.memberships[0]
            assert m.end_date.future

    def test_organization_repr(self):
        with example_file(EXAMPLE_SINGLE_MEMBERSHIP) as fname:
            popolo = Popolo.from_filename(fname)
            assert len(popolo.memberships) == 1
            m = popolo.memberships[0]
            assert repr(m) == "<Membership: 'SP-937-215' at 'starfleet'>"

    def test_equality_of_memberships(self):
        with example_file(EXAMPLE_SINGLE_MEMBERSHIP) as fname:
            # Create the same membership via two Popolo objects - they
            # should still be equal.
            popolo_a = Popolo.from_filename(fname)
            assert len(popolo_a.memberships) == 1
            m_a = popolo_a.memberships[0]
            popolo_b = Popolo.from_filename(fname)
            assert len(popolo_b.memberships) == 1
            m_b = popolo_b.memberships[0]
            assert m_a == m_b
            assert not (m_a != m_b)


EXAMPLE_MULTIPLE_MEMBERSHIPS = b'''
{
    "persons": [
        {
            "id": "SP-937-215",
            "name": "Jean-Luc Picard"
        },
        {
            "id": "SC-231-427",
            "name": "William Riker"
        }
    ],
    "organizations": [
        {
            "id": "starfleet",
            "name": "Starfleet"
        },
        {
            "id": "gardening-club",
            "name": "Boothby's Gardening Club"
        }
    ],
    "memberships": [
        {
            "person_id": "SP-937-215",
            "organization_id": "starfleet",
            "start_date": "2322",
            "end_date": "2322"
        },
        {
            "person_id": "SP-937-215",
            "organization_id": "starfleet",
            "start_date": "2323-12-01",
            "end_date": "2327-12-01"
        },
        {
            "person_id": "SP-937-215",
            "organization_id": "gardening-club",
            "start_date": "2323-01-01",
            "end_date": "2327-11-31"
        },
        {
            "person_id": "SC-231-427",
            "organization_id": "starfleet",
            "start_date": "2357-03-08"
        }
    ]
}
'''


class TestPersonMemberships(TestCase):

    def test_person_memberships_method(self):
        with example_file(EXAMPLE_MULTIPLE_MEMBERSHIPS) as fname:
            popolo = Popolo.from_filename(fname)
            person = popolo.persons.first
            person_memberships = person.memberships
            assert len(person_memberships) == 3
            assert popolo.memberships[0] == person_memberships[0]
            assert popolo.memberships[1] == person_memberships[1]
            assert popolo.memberships[2] == person_memberships[2]

    def test_membership_person_method(self):
        with example_file(EXAMPLE_MULTIPLE_MEMBERSHIPS) as fname:
            popolo = Popolo.from_filename(fname)
            person_picard = popolo.persons[0]
            m = popolo.memberships[0]
            assert m.person == person_picard

    def test_membership_organization_method(self):
        with example_file(EXAMPLE_MULTIPLE_MEMBERSHIPS) as fname:
            popolo = Popolo.from_filename(fname)
            org_starfleet = popolo.organizations.first
            m = popolo.memberships[0]
            assert m.organization == org_starfleet

    def test_membership_on_behalf_of_method(self):
        with example_file(EXAMPLE_MEMBERSHIP_ALL_FIELDS) as fname:
            popolo = Popolo.from_filename(fname)
            org_adder_party = popolo.organizations[1]
            m = popolo.memberships[0]
            assert m.on_behalf_of == org_adder_party

    def test_membership_area_method(self):
        with example_file(EXAMPLE_MEMBERSHIP_ALL_FIELDS) as fname:
            popolo = Popolo.from_filename(fname)
            area_dunny = popolo.areas[0]
            m = popolo.memberships[0]
            assert m.area == area_dunny

    def test_membership_post_method(self):
        with example_file(EXAMPLE_MEMBERSHIP_ALL_FIELDS) as fname:
            popolo = Popolo.from_filename(fname)
            post_dunny = popolo.posts[0]
            m = popolo.memberships[0]
            assert m.post == post_dunny

    def test_membership_legislative_period(self):
        with example_file(EXAMPLE_MEMBERSHIP_ALL_FIELDS) as fname:
            popolo = Popolo.from_filename(fname)
            event_pitt = popolo.events[0]
            m = popolo.memberships[0]
            assert m.legislative_period == event_pitt

    def test_membership_current_at_true(self):
        with example_file(EXAMPLE_MEMBERSHIP_ALL_FIELDS) as fname:
            popolo = Popolo.from_filename(fname)
            m = popolo.memberships[0]
            assert m.current_at(date(1784, 4, 30))

    def test_membership_current_at_false_before(self):
        with example_file(EXAMPLE_MEMBERSHIP_ALL_FIELDS) as fname:
            popolo = Popolo.from_filename(fname)
            m = popolo.memberships[0]
            assert not m.current_at(date(1600, 1, 1))

    def test_membership_current_at_false_after(self):
        with example_file(EXAMPLE_MEMBERSHIP_ALL_FIELDS) as fname:
            popolo = Popolo.from_filename(fname)
            m = popolo.memberships[0]
            assert not m.current_at(date(1800, 1, 1))

    @patch('popolo_data.base.date')
    def test_membership_current_true(self, mock_date):
        mock_date.today.return_value = date(1784, 4, 30)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        with example_file(EXAMPLE_MEMBERSHIP_ALL_FIELDS) as fname:
            popolo = Popolo.from_filename(fname)
            m = popolo.memberships[0]
            assert m.current

    def test_hash_magic_method(self):
        with example_file(EXAMPLE_MULTIPLE_MEMBERSHIPS) as fname:
            popolo_a = Popolo.from_filename(fname)
            popolo_b = Popolo.from_filename(fname)
            set_of_memberships = set()
            for m in popolo_a.memberships:
                set_of_memberships.add(m)
            for m in popolo_b.memberships:
                set_of_memberships.add(m)
            assert len(set_of_memberships) == 4

    def test_equality_and_inequality_not_implemented(self):
        with example_file(EXAMPLE_MULTIPLE_MEMBERSHIPS) as fname:
            popolo = Popolo.from_filename(fname)
            m = popolo.memberships.first
            assert not (m == "a string, not a person")
            assert (m != "a string not a person")

    def test_person_membership_filtering(self):
        with example_file(EXAMPLE_MULTIPLE_MEMBERSHIPS) as fname:
            popolo = Popolo.from_filename(fname)
            person = popolo.persons.first
            person_memberships = person.memberships
            starfleet_memberships = \
                person_memberships.filter(organization_id="starfleet")
            assert len(starfleet_memberships) == 2

    def test_person_membership_multiple_filtering(self):
        with example_file(EXAMPLE_MULTIPLE_MEMBERSHIPS) as fname:
            popolo = Popolo.from_filename(fname)
            person = popolo.persons.first
            person_memberships = person.memberships
            starfleet_memberships = \
                person_memberships.filter(organization_id="starfleet")
            latest_starfleet_membership = \
                starfleet_memberships.filter(start_date=date(2323, 12, 1))
            assert len(latest_starfleet_membership) == 1
