from magnet.llm.visual_llm import VisualLLM
from magnet.llm.visual_llm_registry import VisualLLMRegistry


@VisualLLMRegistry.register('mock')
class MockVisualLLM(VisualLLM):
    def gen(self, *args, **kwargs) -> str:
        return "Foo Bar Img Sync"

    def gen_video(self, *args, **kwargs) -> str:
        return "Foo Bar Video Sync"
