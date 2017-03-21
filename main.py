import random

from models import Planet, Robot
from utils import (
    update_inventory, update_discovered_resources, create_status_intervals,
    check_if_enough_inventory_for_robots, upgrade_robot, build_robot
)

def main():
    exit = False
    planet = Planet()
    robots = []
    buildings = []
    news_channel = []

    inventory = {
        'fuel': 200,
        'steel': 500,
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
    print('6) Build factory to transform steel (Cost: 220 steel)')
    print('7) Build refinery to process fuel (Cost: 200 steel)')
    print('8) Build armery (Cost: 150 steel)')
    print('9) Build "colonizer" spaceship (Cost: 800 steel)')
    print('STATUS:')
    print('10) Inventory')
    print('11) Discovered Resources')
    print('12) Robots')
    print('13) Buildings')
    print('14) Planets')
    print('15) News Channel')
    print('16) Exit')
    print('################################################################')

    while (not exit):
        action = input('Now is your turn, please select one of the listed actions: \n')
        try:
            update_discovered_resources(inventory, robots, planet, news_channel)
            update_inventory(inventory, robots, planet)
            create_status_intervals(robots)
            if action == '1':
                check_if_enough_inventory_for_robots('build', Robot.STEEL, inventory)
                print('Building robot to extract STEEL...')
                robot = build_robot(Robot.STEEL, inventory)
                robots.append(robot)
                print('Done. Robot {} created and in service.'.format(robot.robot_id))
            elif action == '2':
                check_if_enough_inventory_for_robots('build', Robot.FUEL, inventory)
                print('Building robot to extract FUEL...')
                robot = build_robot(Robot.FUEL, inventory)
                robots.append(robot)
                print('Done. Robot {} created and in service.'.format(robot.robot_id))
            elif action == '3':
                check_if_enough_inventory_for_robots('build', Robot.EXPLORER, inventory)
                print('Building robot to discover new resources...')
                robot = build_robot(Robot.EXPLORER, inventory)
                robots.append(robot)
                print('Done. Robot {} created and in service.'.format(robot.robot_id))
            elif action == '4':
                check_if_enough_inventory_for_robots('build', Robot.DEFENSE, inventory)
                print('Building robot to defend our installations...')
                robot = build_robot(Robot.DEFENSE, inventory)
                robots.append(robot)
                print('Done. Robot {} created and in service.'.format(robot.robot_id))
            elif action == '5':
                check_if_enough_inventory_for_robots('upgrade', None, inventory)
                robot_id = input('Upgrading robot. Please type the "Robot ID" (e.g RO1742): \n')
                upgrade_robot(robot_id, robots)
                print('Done. Robot {} Upgraded.'.format(robot_id))
            elif action == '10':
                print('Inspecting Inventory...')
                print(inventory)
            elif action == '11':
                print('Inspecting Discovered Resources...')
                for resource in planet.discovered_resources:
                    print('\t {}'.format(resource))
            elif action == '12':
                print('Inspecting Robots...')
                for robot in robots:
                    print(robot)
            
            elif action == '15':
                print('Broadcasting from the News Channel...')
                for news in news_channel:
                    print('\t [N] {}'.format(news))
            elif action == '16':
                print('Exiting...')
                exit = True
        except Exception as e:
            print(str(e))
            
if __name__ == '__main__':
    main()