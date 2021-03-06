from collections import OrderedDict

import avalon.maya
from colorbleed.maya import lib


class CreateYetiCache(avalon.maya.Creator):
    """Output for procedural plugin nodes of Yeti """

    name = "yetiDefault"
    label = "Yeti Cache"
    family = "colorbleed.yeticache"
    icon = "pagelines"

    def __init__(self, *args, **kwargs):
        super(CreateYetiCache, self).__init__(*args, **kwargs)

        data = OrderedDict(self.data)
        data["peroll"] = 0

        anim_data = lib.collect_animation_data()
        data.update({"startFrame": anim_data["startFrame"],
                     "endFrame": anim_data["endFrame"]})

        self.data = data
