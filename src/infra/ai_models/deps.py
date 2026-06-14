from .litellm import register
from .common.adapters.registry import RegistryAdapter

registry = RegistryAdapter()

register(registry)
