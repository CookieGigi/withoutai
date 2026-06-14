from dependency_injector import containers, providers

from infra.ai_models.common.adapters import RegistryAdapter
from infra.ai_models.litellm import register as litellm_register

from collections.abc import Callable

default_register_hooks = [litellm_register]


def setup_registry(register_hooks: list[Callable[[RegistryAdapter], None]]):

    registry_adapter = RegistryAdapter()

    for hook in register_hooks or default_register_hooks:
        hook(registry_adapter)
    return registry_adapter


class InfraContainer(containers.DeclarativeContainer):
    register_hooks = providers.List()

    registry_adapter = providers.Singleton(
        setup_registry, register_hooks=register_hooks
    )
