from typing import Optional

from peek_plugin_base.client.PeekClientPlatformHookABC import PeekClientPlatformHookABC


class PeekClientPlatformHook(PeekClientPlatformHookABC):

    def getOtherPluginApi(self, pluginName:str) -> Optional[object]:
        return None
