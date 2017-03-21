import random
import time
import sys

from models import Planet, Robot, Building
from utils import (
    update_inventory, update_discovered_resources, create_status_intervals,
    check_if_enough_inventory_for_robots, upgrade_robot, build_robot,
    construct_building, update_robots
)

def main():
    exit = False
    planet = Planet()
    robots = planet.robots
    buildings = planet.buildings
    news_channel = []

    inventory = {
        'fuel': 1000,
        'steel': 1000,
        'exploration_points': 0
    }

    print('Welcome Colonist.')
    print('You have been assigned to a {} distant planet known as: {}'.format(
        planet.TYPES_NAME[planet.planet_type], planet.planet_id))
    print('After carefull analysis, this is are the metrics that we could figure out... {}'.format(planet.properties))
    
    print('Hint: Robots use a certain amount of "Fuel" for each minute they are "in service"')
    print('########################## - MENU - ############################')
    print('ROBOTS:')
    print('1) Build robot to extract steel (Cost: {} steel)'.format(
        Robot.TYPES_COST[Robot.STEEL]))
    print('2) Build robot to extract fuel (Cost: {} steel)'.format(
        Robot.TYPES_COST[Robot.FUEL]))
    print('3) Build robot to find new resources (Cost: {} steel)'.format(
        Robot.TYPES_COST[Robot.EXPLORER]))
    print('4) Build robot to defend our installations (Cost: {} steel)'.format(
        Robot.TYPES_COST[Robot.DEFENSE]))
    print('5) Upgrade robot (Cost: {} steel)'.format(Robot.UPGRADE_COST))
    print('BUILDINGS & SPACESHIPS:')
    print('6) Construct Warehouse to store steel (Cost: {} steel)'.format(
        Building.TYPES_COST[Building.WAREHOUSE]))
    print('7) Construct Fuel Tank to store fuel (Cost: {} steel)'.format(
        Building.TYPES_COST[Building.FUEL_TANK]))
    print('8) Construct Factory to process steel (Cost: {} steel)'.format(
        Building.TYPES_COST[Building.FACTORY]))
    print('9) Construct Refinery to process full (Cost: {} steel)'.format(
        Building.TYPES_COST[Building.REFINERY]))
    print('STATUS:')
    print('10) Inventory')
    print('11) Discovered Resources')
    print('12) Robots')
    print('13) Buildings')
    print('14) Planets')
    print('15) News Channel')
    print('16) Exit')
    print('################################################################')
    print('Now is your turn, please select one of the listed actions:')
    while (not exit):
        action = input('--> ')
        try:
            update_discovered_resources(inventory, robots, planet, news_channel)
            update_inventory(inventory, robots, planet)
            update_robots(inventory, robots, planet)
            create_status_intervals(robots)
            if action == '1':
                print('INFO: Building robot to extract STEEL...')
                robot = build_robot(Robot.STEEL, inventory)
                robots.append(robot)
                print('INFO: Done. Robot {} created and in service.'.format(robot.robot_id))
            elif action == '2':
                print('INFO: Building robot to extract FUEL...')
                robot = build_robot(Robot.FUEL, inventory)
                robots.append(robot)
                print('INFO: Done. Robot {} created and in service.'.format(robot.robot_id))
            elif action == '3':
                print('INFO: Building robot to discover new resources...')
                robot = build_robot(Robot.EXPLORER, inventory)
                robots.append(robot)
                print('INFO: Done. Robot {} created and in service.'.format(robot.robot_id))
            elif action == '4':
                print('INFO: Building robot to defend our installations...')
                robot = build_robot(Robot.DEFENSE, inventory)
                robots.append(robot)
                print('INFO: Done. Robot {} created and in service.'.format(robot.robot_id))
            elif action == '5':
                robot_id = input('Upgrading robot. Please type the "Robot ID" (e.g RO1742): \n')
                upgrade_robot(robot_id, robots)
                print('INFO: Done. Robot {} Upgraded.'.format(robot_id))
            elif action == '6':
                print('INFO: Construct Warehouse to store steel...')
                building = construct_building(Building.WAREHOUSE, inventory)
                buildings.append(building)
                print('INFO: Done. Building {} created and operative.'.format(building.building_id))

            elif action == '10':
                print('INFO: Inspecting Inventory...')
                print(inventory)
            elif action == '11':
                print('INFO: Inspecting Discovered Resources...')
                for resource in planet.discovered_resources:
                    print('\t {}'.format(resource))
            elif action == '12':
                print('INFO: Inspecting Robots...')
                for robot in robots:
                    print(robot)
            elif action == '13':
                print('INFO: Inspecting Buildings...')
                for building in buildings:
                    print(building)
            elif action == '14':
                print('INFO: Inspecting Planets...')
                print(planet)           
            elif action == '15':
                print('INFO: Broadcasting from the News Channel...')
                for news in news_channel:
                    print('\t [N] {}'.format(news))
            elif action == '16':
                print('Exiting...')
                exit = True
            else:
                print('That\'s not a valid option!')
        except Exception as e:
            #print(str(e))
            raise e
            
if __name__ == '__main__':
    main()