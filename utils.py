import random
import time

from datetime import datetime

from models import Robot, Building
from copy import deepcopy


def store_resource(buildings, resource, amount):
    amount_left = amount
    for building in buildings:
        if resource == 'steel' or resource == 'fuel':
            if building.get_space_left() >= amount_left:
                building.store_resource(amount_left)
            else:
                amount_left -= building.get_space_left()
                building.store_resource(building.get_space_left())


def get_space_available(buildings):
    space_available = {
        'fuel': 0,
        'steel': 0
    }
    for building in buildings:
        if building.building_type == Building.WAREHOUSE:
            space_available['steel'] += building.get_space_left()
        if building.building_type == Building.FUEL_TANK:
            space_available['fuel'] += building.get_space_left()
    return space_available


def get_resources_left(planet):
    resources_left = {
        'steel': 0,
        'fuel': 0
    }
    
    for resource in planet.discovered_resources:
        resources_left['steel'] += resource['steel']
        resources_left['fuel'] += resource['fuel']

    if resources_left['steel'] < 10 or resources_left['fuel'] < 10:
        print('WARNING: Low level of steel and/or fuel. Please discover new resources!')
    return resources_left


def check_if_enough_inventory_for_robots(action, robot_type, inventory):
    if action == 'build':
        if inventory['steel'] < Robot.TYPES_COST[robot_type]:
            raise Exception('ERROR: Insufficient steel to build a robot of this type (Existing: {}, Required: {})'.format(
        inventory['steel'], Robot.TYPES_COST[robot_type]))
    elif action == 'upgrade':
        if inventory['steel'] < Robot.UPGRADE_COST:
            raise Exception('ERROR: Insufficient steel to upgrade a robot of this type (Existing: {}, Required: {})'.format(
            inventory['steel'], Robot.TYPES_COST[robot_type]))
    else:
        raise Exception('ERROR: Unknown action')


def check_if_enough_inventory_for_buildings(action, building_type, inventory):
    if action == 'construct':
        if inventory['steel'] < Building.TYPES_COST[building_type]:
            raise Exception('ERROR: Insufficient steel to construct a building of this type (Existing: {}, Required: {})'.format(
        inventory['steel'], Building.TYPES_COST[building_type]))
    elif action == 'upgrade':
        if inventory['steel'] < Building.UPGRADE_COST:
            raise Exception('ERROR: Insufficient steel to upgrade a building of this type (Existing: {}, Required: {})'.format(
            inventory['steel'], Building.TYPES_COST[building_type]))
    else:
        raise Exception('ERROR: Unknown action')


def upgrade_robot(robot_id, robots, inventory):
    check_if_enough_inventory_for_robots('upgrade', None, inventory)
    found = False
    for robot in robots:
        if robot.robot_id == robot_id:
            if robot.status != Robot.ACTIVE:
                raise Exception('ERROR: You cannot Upgrade a robot with status: {}'.format(Robot.STATUS_NAME[robot.status]))
            elif robot.upgrade_level >= len(Robot.UPGRADE_MULTIPLIER) - 1:
                raise Exception('ERROR: Max Upgrade level reached.')
            else:
                robot.upgrade()
                found = True
    if not found:
        raise Exception('ERROR: Unknown robot. Upgrade could not be performed.')


def create_status_intervals(robots):
    for robot in robots:
        status = (robot.status, datetime.now(), robot.upgrade_level)
        robot.status_intervals.append(status)


def build_robot(robot_type, inventory):
    check_if_enough_inventory_for_robots('build', robot_type, inventory)
    inventory['steel'] -= Robot.TYPES_COST[robot_type]
    return Robot(robot_type)


def construct_building(building_type, inventory):
    check_if_enough_inventory_for_buildings('construct', building_type, inventory)
    inventory['steel'] -= Building.TYPES_COST[building_type]
    return Building(building_type)


def update_robots(inventory, robots, planet):
    def _check_if_enough_resources_for_robots(material, robot, resources_left):
        if resources_left[material] > 0:
            return True
        else:
            return False
    
    def _check_if_enough_fuel_to_run_engines(inventory, robot):
        if inventory['fuel'] >= Robot.TYPES_MAINTENANCE_COST[robot.robot_type]:
            return True
        else:
            return False
    
    def _set_robot_status(material, inventory, robot, resources_left):
        if not _check_if_enough_fuel_to_run_engines(inventory, robot) or not _check_if_enough_resources_for_robots(material, robot, resources_left):
            robot.status = Robot.INACTIVE
            print('WARNING: Insufficient steel/fuel. Robot {} (Class: {}) will be inactive from now on.'.format(
                robot.robot_id, Robot.TYPES_NAME[robot.robot_type]))
        else:
            robot.status = Robot.ACTIVE

    resources_left = get_resources_left(planet)
    for robot in robots:
        if robot.robot_type == Robot.STEEL:
            _set_robot_status('steel', inventory, robot, resources_left)
                
        elif robot.robot_type == Robot.FUEL:
            _set_robot_status('fuel', inventory, robot, resources_left)


def update_inventory(inventory, robots, planet):
    extracted_resources_since_last_update = {
        'steel': 0,
        'fuel': 0,
    }

    for robot in robots:
        if robot.robot_type == Robot.STEEL:
            extracted_resources_since_last_update['steel'] += robot.extracted_since_last_update() 
        elif robot.robot_type == Robot.FUEL:
            extracted_resources_since_last_update['fuel'] += robot.extracted_since_last_update()


    def _store_resources(resource, extracted_resources_since_last_update):
        resources_left = get_resources_left(planet)
        space_available = get_space_available(planet.buildings)

        if resources_left[resource] < extracted_resources_since_last_update[resource]:
            # Because we cannot extract more than what we have already discovered.
            amount_to_store = resources_left[resource]
        else:
            # Because we can store everything we extracted.
            amount_to_store = extracted_resources_since_last_update[resource]
    
        if not space_available[resource] or space_available[resource] < amount_to_store:
            # This is the case when the extracted doesn't fit in the warehouse/fuel tank we have.
            print('WARNING: Insufficent storage for {}. Please construct a Warehouse (steel) or Fuel Tank (fuel)'.format(resource))
            amount_to_store = space_available[resource]
            inventory[resource] += amount_to_store
            store_resource(planet.buildings, resource, amount_to_store)
        else:
            # This is the case when the extracted fit in the warehouse/fuel tank we have.
            inventory[resource] += amount_to_store
            store_resource(planet.buildings, resource, amount_to_store)
    
        remove_resource_from_planet(resource, planet, extracted_resources_since_last_update[resource])
    
    _store_resources('steel', extracted_resources_since_last_update)
    _store_resources('fuel', extracted_resources_since_last_update)


def update_discovered_resources(inventory, robots, planet, news_channel):
    exploration_points = 0
    for robot in robots:
         if robot.robot_type == Robot.EXPLORER:
             exploration_points += robot.discovered_since_last_update()

    inventory['exploration_points'] += exploration_points
    new_resources = inventory['exploration_points'] // 200
    if new_resources > 0:
        for i in range(new_resources):
            resource = planet.uncover_resource()
            news_channel.append('New resource field discover!: {}'.format(resource))
        inventory['exploration_points'] = 0

def remove_resource_from_planet(material, planet, amount):
    amount_left = amount
    for resource in planet.discovered_resources:
        if resource[material] >= amount_left:
            resource[material] -= amount_left
            amount_left = 0
        else:
            amount_left -= resource[material]
            resource[material] = 0
