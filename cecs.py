"""The module that contains the cecs implementation."""


class World:
    """World class"""

    def __init__(self):
        """A World object keeps track of all Entities, Components and Systems.

        """
        # Entities
        self.current_entity_id = 0
        self.entities = {}
        self.dead_entities = set()
        # Components
        self.components = {}
        self.current_system_id = 0
        # Systems
        self.systems = {}
        self.category_systems = {}

    # Entity functions
    def create_entity(self, *components):
        """ Creates a new entity.

        This method creates a new entity in the world, this is just a plain integer.
        You can optionally pass components to be added to the entity.

        :param components: Optional components to be added to the entity.
        :return: The id of the created entity.
        """
        self.current_entity_id += 1
        self.entities[self.current_entity_id] = {}

        for component in components:
            self.add_component(self.current_entity_id, component)

        return self.current_entity_id

    def delete_entity(self, entity, immediate=False):
        if immediate:
            for component_type in self.entities[entity]:
                self.components[component_type].discard(entity)

                if not self.components[component_type]:
                    del self.components[component_type]

            del self.entities[entity]

        else:
            self.dead_entities.add(entity)

    def delete_dead_entities(self):
        if self.dead_entities:
            for entity in self.dead_entities:
                self.delete_entity(entity, immediate=True)
            self.dead_entities.clear()

    # Component functions
    def get_component_from_entity(self, entity, component_type):
        return self.entities[entity][component_type]

    def get_all_components_from_entity(self, entity):
        return tuple(self.entities[entity].values())

    def has_component(self, entity_id, component_type):
        if entity_id in self.entities:
            if component_type in self.entities[entity_id]:
                return True
        return False

    def add_component(self, entity_id, component_instance):
        if entity_id in self.entities:
            if type(component_instance) in self.components:
                self.components[type(component_instance)].add(entity_id)
            else:
                self.components[type(component_instance)] = set()
            self.entities[entity_id][type(component_instance)] = component_instance

    def remove_component(self, entity, component_type):
        self.components[component_type].discard(entity)

        if not self.components[component_type]:
            del self

        del self.entities[entity][component_type]

        if not self.entities[entity]:
            del self.entities[entity]

        return entity

    def get_component(self, component_type):
        entity_db = self.entities
        for entity in self.components.get(component_type, []):
            yield entity, entity_db[entity][component_type]

    def get_components(self, *component_types):
        entity_db = self.entities
        comp_db = self.components

        try:
            for entity in set.intersection(*[comp_db[ct] for ct in component_types]):
                yield entity, [entity_db[entity][ct] for ct in component_types]
        except KeyError:
            pass

    # System functions
    def add_system(self, system_instance, category=""):
        self.current_system_id += 1
        if category in self.systems:
            self.category_systems[category] += self.current_system_id
        else:
            self.category_systems[category] = set()
        self.systems[self.current_system_id] = system_instance
        system_instance.world = self
        return self.current_system_id

    def process_system(self, *systems):
        self.delete_dead_entities()

        for system in systems:
            if system in self.systems:
                self.systems[system].process()

    def process_system_category(self, *system_categories):
        self.delete_dead_entities()

        for system_category in system_categories:
            if system_category in self.category_systems:
                for system_id in self.category_systems[system_category]:
                    self.systems[system_id].update()

    def process_all(self):
        self.delete_dead_entities()

        for system in self.systems.values():
            system.update()


class System:
    """System class"""
    def __init__(self):
        self.world = None

    def process(self):
        pass