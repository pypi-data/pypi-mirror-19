from typing import Optional

from peek_plugin_base.agent.PeekAgentPlatformHookABC import PeekAgentPlatformHookABC


class PeekAgentPlatformHook(PeekAgentPlatformHookABC):
    def getOtherPluginApi(self, pluginName: str) -> Optional[object]:
        return None
