import requests
from behave_web_api.utils import dereference_arguments, make_url
from behave_web_api.steps import *
from hamcrest import *

use_step_matcher("re")


@given(u'I set header "(?P<header_key>\w+)" with auth token "(?P<header_value>.*)"')
@dereference_arguments
def i_set_an_authenticated_header(context, header_key, header_value):
    """
    We want to set the Bearer authorization header
    """
    if not hasattr(context, 'request_headers'):
        context.request_headers = {}
    # grab the value from context.<somewhere> if that's what the value has
    if header_value.startswith('context.'):
        header_value = getattr(context, header_value[8:])
    context.request_headers[header_key] = 'Bearer ' + header_value


@when(u'I send a (?P<method>\w+) request to "(?P<endingpoint>.*)" authenticated with')
@dereference_arguments
def i_send_an_authenticated_request(context, method, endingpoint):
    """
    We want to set the auth arguments for HTTPBasicAuth
    """
    # we know that this is JUST auth=('username','password')
    context.auth = eval(context.text.split(u'=')[1])
    do_request(context, method, endingpoint)


@then(u'the "(?P<keyname>[\w\.]+)" key within (?P<is_each>each of )?"(?P<location>[\w\.]+)"'
      u' (?P<must_or_not_at_all>must|does not need to) (?P<match_or_contain>match|contain)'
      u'(?P<_one_of> one of)? "(?P<matchable>[\w+\.]+)"')
def the_key_in_json_must_match_or_contain(context, keyname, is_each, location,
                                          must_or_not_at_all, match_or_contain, _one_of, matchable):
    """
    We want to check on a specific asset belonging to the same as a matchable asset
     i.e. all users in a many-returned JSON to have the same client as me
    """
    import json
    # print keyname, is_each, location, must_or_not_at_all, match_or_contain, _one_of, matchable
    comparable = get_comparable(context, location, json.loads(context.response.text))
    # We know there are MANY returned in this instance
    if is_each:
        if _one_of: # may want to refactor this to capture the entirety of "match|contain one of"
            if must_or_not_at_all != "must":
                # build a SET of individual numbers (since we DON'T want them to be unique)
                all_things = set()

                for thing in comparable:
                    at_key = unpack_unicode_dict_at(keyname, thing['attributes'])
                    if is_primative(at_key):
                        all_things.add(at_key)
                    else:
                        for athing in thing['attributes'][keyname]:
                            all_things.add(athing['id'])
                assert_that(len(all_things), greater_than_or_equal_to(1))
            else:
                for thing in comparable:
                    at_key = unpack_unicode_dict_at(keyname, thing['attributes'])
                    # print thing

                    if is_primative(at_key):
                        assert_that([t.id for t in eval(matchable)], has_item(at_key))
                    else:
                        # assert that any ONE of many subthings match my matchable (i.e. groups in users)
                        for subthing in at_key:
                            if must_or_not_at_all == "must":
                                # print [t.id for t in eval(matchable) if t.id != int(subthing['id'])], subthing['id']
                                assert_that([t.id for t in eval(matchable)], has_item(int(subthing['id'])))
                            else:
                                # print [t.id for t in eval(matchable) if t.id != int(subthing['id'])], subthing['id']
                                for spec_id in [t.id for t in eval(matchable) if t.id != int(subthing['id'])]:
                                    assert_that(spec_id, not equal_to(int(subthing['id'])))
        else:
            if must_or_not_at_all == "must":
                for thing in comparable:
                    possible_dict = unpack_unicode_dict_at(keyname, thing['attributes'])
                    if dict_containing(possible_dict, 'id'):
                        assert_that(str(eval(matchable).id), equal_to(possible_dict['id']))
                    else:
                        # print eval(matchable).id, possible_dict
                        if isinstance(possible_dict, (unicode, str)):
                            matchable_value = str(eval(matchable).id)
                        else:
                            matchable_value = eval(matchable).id
                        assert_that(matchable_value, equal_to(possible_dict))
            else:
                # build a SET of individual numbers (since we DON'T want them to be unique)
                all_things = set()
                for thing in comparable:
                    possible_dict = unpack_unicode_dict_at(keyname, thing['attributes'])
                    if dict_containing(possible_dict, 'id'):
                        all_things.add(possible_dict['id'])
                    else:
                        all_things.add(possible_dict)

                assert_that(len(all_things), greater_than_or_equal_to(1))
    else:
        if must_or_not_at_all == "must":
            # print "COMPARABLE JSON:", comparable[keyname], "\nMY CLIENT", context.desired_user.client
            if dict_containing(comparable[keyname], 'id'):
                assert_that(str(eval(matchable).id), equal_to(comparable[keyname]['id']))
            else:
                assert_that(eval(matchable).id, equal_to(comparable[keyname]))

#     ----- HELPER METHODS -----     #


def dict_containing(d, key):
    return isinstance(d, dict) and key in d


def get_comparable(context, location, comparable):
    if '.' in location:
        # little hacky/cheaty way of getting at a namespaced part of a dict
        return unpack_unicode_dict_at(location, comparable)
    else:
        return json.loads(context.response.text)[location]


def unpack_unicode_dict_at(location, d):
    try:
        return eval('d' + ''.join(['.get("' + l + '")' for l in location.split('.')]))
    except AttributeError, e:
        if str(e) == "'unicode' object has no attribute 'get'":
            import json
            first_key, new_loc = location.split('.', 2)
            return unpack_unicode_dict_at(new_loc, json.loads(d.get(first_key)))


def do_request(context, method, endingpoint, body=None):
    fn = getattr(requests, method.lower())
    kwargs = {}

    if hasattr(context, 'request_headers'):
        kwargs['headers'] = context.request_headers

    if hasattr(context, 'auth'):
        kwargs['auth'] = context.auth

    if body:
        kwargs['data'] = body

    if hasattr(context, 'request_files'):
        kwargs['files'] = context.request_files

    context.response = fn(make_url(context, endingpoint), **kwargs)


def is_primative(var_to_check):
    """
    Check whether or not a variable is stricly "primative", defined as int, basestring, bool or FakeDateTime

    Returns True if it is deemed to be primative
    """
    from freezegun.api import FakeDatetime
    return isinstance(var_to_check, (int, basestring, bool, FakeDatetime))
