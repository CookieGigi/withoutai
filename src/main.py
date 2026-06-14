from api import create_app
from containers import InfraContainer, AppContainer

infra = InfraContainer()

app_container = AppContainer(infra=infra)
app_container.wire(packages=["api"])

app = create_app()
