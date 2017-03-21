import random
from datetime import datetime

from models import Robot
from copy import deepcopy


def get_resources_left(planet):
    resources_left = {
        'steel': 0,
        'fuel': 0
    }
    
    for resource in planet.discovered_resources:
        resources_left['steel'] += resource['steel']
        resources_left['fuel'] += resource['fuel']

    if resources_left['steel'] < 10 or resources_left['fuel'] < 10:
        print('Insufficient steel or fuel. Please discover new resources!')
    return resources_left


def check_if_enough_inventory_for_robots(action, robot_type, inventory):
    if action == 'build':
        for robot_id in range(len(Robot.TYPES_NAME)):
            if inventory['steel'] < Robot.TYPES_COST[robot_type]:
                raise Exception('Insufficient steel')
    elif action == 'upgrade':
        if inventory['steel'] < Robot.UPGRADE_COST:
            raise Exception('Insufficient steel')
    else:
        raise Exception('Unknown action')


def upgrade_robot(robot_id, robots):
    found = False
    for robot in robots:
        if robot.robot_id == robot_id:
            robot.upgrade()
            found = True
    if not found:
        raise Exception('Unknown robot. Upgrade could not be performed.')


def create_status_intervals(robots):
    for robot in robots:
        status = (robot.status, datetime.now(), robot.upgrade_level)
        robot.status_intervals.append(status)


def build_robot(robot_type, inventory):
    if inventory['steel'] >= Robot.TYPES_COST[robot_type]:
        inventory['steel'] -= Robot.TYPES_COST[robot_type]
        return Robot(robot_type)
    else:
        raise Exception('Insufficient steel to build a robot of this type (Existing: {}, Required: {})'.format(
            inventory['steel'], Robot.TYPES_COST[robot_type]))


def consume_robots_maintenance_fuel(inventory, robots):
    for robot in robots:
        if inventory['fuel'] >= Robot.TYPES_MAINTENANCE_COST[robot.robot_type]:
            robot.status = Robot.ACTIVE
            inventory['fuel'] -= Robot.TYPES_MAINTENANCE_COST[robot.robot_type]
        else:
            robot.status = Robot.INACTIVE
            print('Insufficient fuel. Robot {} (Class: {}) will be inactive from now on.'.format(
                robot.robot_id, Robot.TYPES_NAME[robot.robot_type]))


def update_inventory(inventory, robots, planet):
    extracted_steel_since_last_check = 0
    extracted_fuel_since_last_check = 0
    for robot in robots:
        if robot.robot_type == Robot.STEEL:
            extracted_steel_since_last_check += robot.extracted_since_last_update() 
        elif robot.robot_type == Robot.FUEL:
            extracted_fuel_since_last_check += robot.extracted_since_last_update()
    
    resources_left = get_resources_left(planet)
    
    if resources_left['steel'] < extracted_steel_since_last_check:
        inventory['steel'] += resources_left['steel']
        remove_resource_from_planet('steel', planet, resources_left['steel'])
    else:
        inventory['steel'] += extracted_steel_since_last_check
        remove_resource_from_planet('steel', planet, extracted_steel_since_last_check)
    if resources_left['fuel'] < extracted_fuel_since_last_check:
        inventory['fuel'] += resources_left['fuel']
        remove_resource_from_planet('fuel', planet, resources_left['fuel'])
    else:
        inventory['fuel'] += extracted_fuel_since_last_check
        remove_resource_from_planet('fuel', planet, extracted_steel_since_last_check)

    consume_robots_maintenance_fuel(inventory, robots)


def update_discovered_resources(inventory, robots, planet, news_channel):
    exploration_points = 0
    for robot in robots:
         if robot.robot_type == Robot.EXPLORER:
             exploration_points += robot.discovered_since_last_update()

    inventory['exploration_points'] += exploration_points
    new_resources = inventory['exploration_points'] // 100
    if new_resources > 0:
        for i in range(new_resources):
            resource = planet.uncover_resource()
            news_channel.append('New resource field discover!: {}'.format(resource))

def remove_resource_from_planet(material, planet, amount):
    amount_left = amount
    for resource in planet.discovered_resources:
        if material == 'steel':
            if resource['steel'] >= amount_left:
                resource['steel'] -= amount_left
                amount_left = 0
            else:
                amount_left -= resource['steel']
                resource['steel'] = 0

        elif material == 'fuel':
            if resource['fuel'] >= amount_left:
                resource['fuel'] -= amount_left
                amount_left = 0
            else:
                amount_left -= resource['fuel']
                resource['fuel'] = 0
