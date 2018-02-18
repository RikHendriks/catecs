import cecs
import pytest


# Fixtures
@pytest.fixture
def world():
    return cecs.World()


@pytest.fixture
def populate_world():
    pop_world = world()


# Tests
def test_world_instantiation(world):
    assert type(world) is cecs.World
    assert type(world.current_entity_id) is int
    assert type(world.current_system_id) is int
    assert type(world.entities) is dict
    assert type(world.dead_entities) is set
    assert type(world.components) is dict
    assert type(world.systems) is dict
    assert type(world.category_systems) is dict


def test_create_entity(world):
    entity1 = world.create_entity()
    entity2 = world.create_entity()
    assert type(entity1) and type(entity2) is int
    assert entity1 < entity2


def test_create_entity_with_component(world):
    entity1 = world.create_entity(ComponentA())
    entity2 = world.create_entity(ComponentB())
    assert world.has_component(entity1, ComponentA) is True
    assert world.has_component(entity1, ComponentB) is False
    assert world.has_component(entity2, ComponentA) is False
    assert world.has_component(entity2, ComponentB) is True


def test_delete_entity_immediate(world):
    entity1 = world.create_entity()
    world.add_component(entity1, ComponentA())
    entity2 = world.create_entity()
    world.add_component(entity2, ComponentB())
    entity3 = world.create_entity()
    # Entity 2 with components
    assert entity2 is 2
    world.delete_entity(entity2, immediate=True)
    with pytest.raises(KeyError):
        world.get_all_components_from_entity(entity2)
    # Entity 3 without components
    assert entity3 is 3
    world.delete_entity(entity3, immediate=True)
    with pytest.raises(KeyError):
        world.get_all_components_from_entity(entity3)
    # Delete an entity that doesn't exist
    with pytest.raises(KeyError):
        world.delete_entity(999, immediate=True)


def test_delete_entity_not_immediate(world):
    entity1 = world.create_entity()
    world.add_component(entity1, ComponentA())
    entity2 = world.create_entity()
    world.add_component(entity2, ComponentA())
    entity3 = world.create_entity()
    world.add_component(entity3, ComponentA())
    # Process all
    assert entity1 is 1
    world.delete_entity(entity1)
    world.process_all()
    with pytest.raises(KeyError):
        world.get_all_components_from_entity(entity1)
    # Process_system
    assert entity2 is 2
    world.delete_entity(entity2)
    system1 = world.add_system(SystemA())
    world.process_system(system1)
    with pytest.raises(KeyError):
        world.get_all_components_from_entity(entity2)
    # Process_system_category
    assert entity3 is 3
    world.delete_entity(entity3)
    world.process_system_category("")
    with pytest.raises(KeyError):
        world.get_all_components_from_entity(entity3)


def test_get_component_from_entity(world):
    entity = world.create_entity()
    world.add_component(entity, ComponentA())
    assert isinstance(world.get_component_from_entity(entity, ComponentA), ComponentA)
    with pytest.raises(KeyError):
        world.get_component_from_entity(entity, ComponentB)


def get_all_components_from_entity(world):
    entity = world.create_entity()
    world.add_component(entity, ComponentA())
    world.add_component(entity, ComponentB())
    world.add_component(entity, ComponentC())
    all_components = world.get_all_components_from_entity(entity)
    assert type(all_components) is tuple
    assert len(all_components) is 3
    with pytest.raises(KeyError):
        world.get_all_components_from_entity(999)


def test_has_component(world):
    entity1 = world.create_entity()
    entity2 = world.create_entity()
    world.add_component(entity1, ComponentA())
    world.add_component(entity2, ComponentB())
    assert world.has_component(entity1, ComponentA) is True
    assert world.has_component(entity1, ComponentB) is False
    assert world.has_component(entity2, ComponentA) is False
    assert world.has_component(entity2, ComponentB) is True


def test_get_component(world):
    assert False
    # TODO implement the test


def test_get_two_components(world):
    assert False
    # TODO implement the test


def test_get_three_components(world):
    assert False
    # TODO implement the test


def add_system(world):
    assert len(world.systems)
    system_a = SystemA()
    assert isinstance(system_a, cecs.System)
    world.add_system(system_a)
    assert len(world.systems) is 1
    assert isinstance(world.systems[0], cecs.System)
    # TODO test the system categories


def test_remove_processor(world):
    assert False
    # TODO implement this function and the test


def test_get_system(world):
    assert False
    # TODO implement this function and the test


# Helper classes and functions
class ComponentA:
    def __init__(self):
        self.a = -1.0
        self.b = 2.0


class ComponentB:
    def __init__(self):
        self.a = True
        self.b = False


class ComponentC:
    def __init__(self):
        self.a = True
        self.b = 0.5


class SystemA(cecs.System):
    def __init__(self):
        super().__init__()

    def process(self):
        pass