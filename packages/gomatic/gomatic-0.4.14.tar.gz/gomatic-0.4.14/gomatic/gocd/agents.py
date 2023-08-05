from gomatic.gocd.generic import ThingWithResources


class Agent(object):
    def __init__(self, element):
        self._element = element
        self.__thing_with_resources = ThingWithResources(element)

    @property
    def hostname(self):
        return self._element.attrib['hostname']

    @property
    def resources(self):
        return self.__thing_with_resources.resources

    def ensure_resource(self, resource):
        self.__thing_with_resources.ensure_resource(resource)
