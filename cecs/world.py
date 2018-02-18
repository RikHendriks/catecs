class World:

    def __init__(self):
        # Entities
        self.current_entity_id = -1
        self.entities = {}
        # Components
        self.components = {}
        self.current_system_id = -1
        # Systems
        self.systems = {}
        self.category_systems = {}

    # Entity functions
    def create_entity(self):
        self.current_entity_id += 1
        self.entities[self.current_entity_id] = {}
        return self.current_entity_id

    # Component functions
    def add_component(self, entity_id, component_instance):
        if entity_id in self.entities:
            if type(component_instance) in self.components:
                self.components[type(component_instance)] += entity_id
            else:
                self.components[type(component_instance)] = set()
            self.entities[entity_id][type(component_instance)] = component_instance

    def has_component(self, entity_id, component_type):
        if entity_id in self.entities:
            if component_type in self.entities[entity_id]:
                return True
        return False

    # System functions
    def add_system(self, system_instance, category):
        self.current_system_id += 1
        if category in self.systems:
            self.category_systems[category] += self.current_system_id
        else:
            self.category_systems[category] = set()
        self.systems[self.current_system_id] = system_instance
        return self.current_system_id

    def process_system(self, system_id):
        if system_id in self.systems:
            self.systems[system_id].update()

    def process_category(self, category):
        if category in self.category_systems:
            for system_id in self.category_systems[category]:
                self.systems[system_id].update()

    def process_all(self):
        for system in self.systems.values():
            system.update()