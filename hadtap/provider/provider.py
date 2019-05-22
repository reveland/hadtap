from abc import ABCMeta, abstractmethod


class Provider(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_names(self):
        """Get names from tablazat"""
        pass

    @abstractmethod
    def get_user_ids(self):
        """Get userids from tablazat"""
        pass

    @abstractmethod
    def record_fogyasztas(self, user_name, value):
        """Record an user action."""
        pass

    @abstractmethod
    def get_value_for_item(self, item):
        """Record an user action."""
        pass

    @abstractmethod
    def get_name(self, user_id):
        """Record an user action."""
        pass
