
import datetime
import time


def to_datetime(timestamp):
    """ Converts timestamp (str) in datetime object. """
    return datetime.datetime(*time.strptime(timestamp[:19], '%Y-%m-%dT%H:%M:%S')[:6])


def _fields(isu):
    """Returns field names of Issue object."""
    no_method = lambda x: not callable(getattr(isu.fields, x))
    no_magic = lambda x: not x.startswith('_')
    no_constant = lambda x: not x[0].isupper()
    return filter(lambda x: no_magic(x) and no_method(x) and no_constant(x), dir(isu.fields))


def copy_resource(rsc):
    """
    Creates copy of resource object.

    :param rsc: Jira resource object
    :type resource: jira.resources.Resource
    """
    kls = type(rsc)
    obj = kls(rsc._options, rsc._session, rsc.raw)
    return obj


class Changelog(object):

    """
    Changelog handling made easy::

        >>> issue = jira.issue('JIRA-2204')
        >>> add_history(issue)
        >>> issue.history
        <Changelog 3 entries>

        >>> one_week_ago = datetime.timedelta(datetime.datetime.now(), days=-7)
        >>> issue.history.at(one_week_ago)
        {'resolution': <Resolution Closed>, ...}

    """

    def __init__(self, resource):
        """
        Initiates a Changelog object from a resource.

        :type resource: jira.resources.Resource
        """
        self._resource = resource
        self.changes = [Change(item) for item in resource.changelog.histories]

    @classmethod
    def _clone_resource(cls, rsc, fields=None):
        """
        Returns resource values as dict.

        :param rsc: Jira resource object
        :type resource: jira.resources.Resource
        :param fields: list of fields to be copied
        :type fields: list
        """
        fields = fields or _fields(rsc)
        return {field: getattr(rsc.fields, field) for field in fields}

    @staticmethod
    def rollback(change, values):
        """
        Rolls back a particular set of changes to restore values to what they
        were before the change was applied.

        ATTENTION: This will not change the raw data nor will it reload resource
        objects!

        :param change: change to be rolled back
        :type change: Change
        :param values: values change will be applied to
        :type values: dict
        """
        for item in change.items:
            key = item.field
            if key in values:
                # create a copy of original Jira object
                if hasattr(values[key], 'raw'):
                    values[key] = copy_resource(values[key])
                values[key].id = getattr(item, 'from')
                values[key].name = item.fromString

    def at(self, dt):
        """
        Returns values for resource at a certain time

        :param dt: point in time for which values should be recovered
        :type dt: datetime.datetime
        """
        # apply all changes in reverse succession
        changes = sorted(self.changes, key=lambda ch: ch.created, reverse=True)
        values = self._clone_resource(self._resource)

        # return values directly if no changes were made since creation
        if not changes:
            return values

        # return values if next change was applied before dt
        # otherwise rollback all changes
        while changes:
            next_change = changes.pop(0)
            if next_change.created < dt:
                return values
            self.rollback(next_change, values)

        # all changes have been rolled back
        # return virgin values
        return values


class Change(object):

    """
    Convenience class for handling change information.
    """

    def __init__(self, raw):
        self.id = raw.id
        self.created = to_datetime(raw.created)
        self.author = raw.author
        self.items = raw.items


def add_history(resource):
    """
    Injects a Changelog instance into a resource object.

    :param rsc: Jira resource object
    :type resource: jira.resources.Resource
    """
    assert hasattr(resource, 'changelog')
    changelog = Changelog(resource)
    resource.history = changelog
