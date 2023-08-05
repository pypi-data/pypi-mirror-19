##############################################################################
#
# Copyright (c) 2016, CloudAcademy.
# All Rights Reserved.
#
# Class used to parse HubSpot Webhook data
#
##############################################################################


class WorkflowDataParser(object):

    def __init__(self, raw_payload):
        self.raw_payload = raw_payload
        self.filtered_payload = None

    def get_payload(self, raw=False):
        """
        :param raw: Boolean True if you want the raw payload
        :return: the Hubspot payload
        """
        if not raw and self.filtered_payload:
            return self.filtered_payload
        return self.raw_payload

    def get_properties(self, properties_key):
        """
        :param properties_key: string of the name of the property key
        :return: the properties related to the searched key
        """
        try:
            if self.get_payload().get("properties").get(properties_key).get("value"):
                return self.get_payload().get("properties").get(properties_key).get("value")
        except AttributeError:
            return None

    def remove_properties(self, blacklist_keys=None):
        """
        :param blacklist_keys: list of keys
        :return: the Webhook object without the blacklist keys
        """
        if isinstance(blacklist_keys, basestring):
            blacklist_keys = [blacklist_keys]

        for key in blacklist_keys:
            self.get_payload()["properties"].pop(key, None)
        return self

    def filter(self, timestamp=0, search_round_seconds=0):
        """
        :param timestamp: unix timestamp
        :param search_round_seconds: seconds
        :return: the Webhook object filtered by timestamp
        """
        for key in self.get_payload()["properties"]:
            versions = self.get_payload()["properties"][key].get("versions")
            if versions:
                keep_version = {}
                if timestamp == 0:
                    keep_version = versions[0]
                else:
                    try:
                        lower_time = timestamp - search_round_seconds
                        upper_time = timestamp + search_round_seconds
                        for version in versions:
                            if lower_time <= int(version["timestamp"]) <= upper_time:
                                keep_version = version
                    except TypeError:
                        keep_version = versions[0]

                self.get_payload()["properties"][key] = keep_version
        return self
