from quantx.factors.container import Container


class Pipeline:
    _containers = dict()

    def add(self, name, container):
        self._containers[name] = container

    def get(self, name) -> Container:
        container = self._containers[name]
        container.run()
        return container
