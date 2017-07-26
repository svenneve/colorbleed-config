from collections import defaultdict

import maya.cmds as cmds

import pyblish.api
import colorbleed.api


class ValidateUniqueNodeIds(pyblish.api.InstancePlugin):
    """Validate nodes have colorbleed id attributes"""

    order = colorbleed.api.ValidatePipelineOrder
    families = ['colorbleed.model']
    hosts = ['maya']
    label = 'Unique Id Attributes'
    actions = [colorbleed.api.SelectInvalidAction,
               colorbleed.api.GenerateUUIDsOnInvalidAction]

    @staticmethod
    def get_invalid_dict(instance):
        """Return a dictionary mapping of id key to list of member nodes"""

        uuid_attr = "cbId"

        # Collect each id with their members
        ids = defaultdict(list)
        for member in instance:
            has_attr = cmds.attributeQuery(uuid_attr, node=member, exists=True)
            if not has_attr:
                continue
            mbid = cmds.getAttr("{}.{}".format(member, uuid_attr))
            ids[mbid].append(member)

        # Skip those without IDs (if everything should have an ID that should
        # be another validation)
        ids.pop(None, None)

        # Take only the ids with more than one member
        invalid = dict((id, members) for id, members in ids.iteritems() if
                       len(members) > 1)
        return invalid

    @classmethod
    def get_invalid(cls, instance):
        """Return the member nodes that are invalid"""

        invalid_dict = cls.get_invalid_dict(instance)

        # Take only the ids with more than one member
        invalid = list()
        for members in invalid_dict.itervalues():
            invalid.extend(members)

        return invalid

    def process(self, instance):
        """Process all meshes"""

        # Ensure all nodes have a cbId
        invalid = self.get_invalid_dict(instance)
        if invalid:
            raise RuntimeError("Nodes found with non-unique "
                               "asset IDs: {0}".format(invalid))