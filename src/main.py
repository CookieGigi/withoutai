from api import create_app
from dependencies import APIDependencies

apiDependencies = APIDependencies()

apiDependencies.models_service().initalize_from_litellm()

app = create_app(apiDependencies)
