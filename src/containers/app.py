from dependency_injector import containers, providers
from app.services.ai_models.models import ModelsService


class AppContainer(containers.DeclarativeContainer):
    infra = providers.DependenciesContainer()

    models_service = providers.Factory(ModelsService, registry=infra.registry_adapter)
