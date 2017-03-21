import random
from datetime import datetime


class Building(object):
    # Types
    WAREHOUSE = 0
    FUEL_TANK = 1
    FACTORY = 2
    REFINERY = 3
    ARMERY = 4
    
    TYPES_NAME = ['Warehouse', 'Fuel Tank', 'Refinery', 'Armery']
    TYPES_CAPACITY = [1000, 1000, 0, 0]
    TYPES_COST = [220, 200, 150, 150]
    MAX_STORAGE = 1000

    def __init__(self, building_type):
        self.building_id = 'BU{}'.format(random.randrange(0, 5000))
        self.building_type = building_type
        self.current_storage = 0
    
    def get_space_left(self):
        return self.MAX_STORAGE - self.current_storage

    def store_resource(self, amount):
        if self.MAX_STORAGE < self.current_storage + amount:
            return -1
        else:
            self.current_storage += amount
        return self.current_storage

    def __str__(self):
        return '\t{} {} | Space available: {}/{}'.format(
            self.TYPES_NAME[self.building_type], self.building_id, self.current_storage, self.MAX_STORAGE)


class Robot(object):
    # Types
    STEEL = 0
    FUEL = 1
    EXPLORER = 2
    DEFENSE = 3

    # Statuses
    ACTIVE = 0
    INACTIVE = 1
    BROKEN = 2
    STATUS_NAME = ['Active', 'Inactive', 'Broken']

    TYPES_NAME = ['Steel', 'Fuel', 'Explorer', 'Defense']
    TYPES_COST = [60, 40, 20, 80]
    # Per second
    TYPES_EXTRACTION_RATE = [5, 4, 0, 0]
    TYPES_MAINTENANCE_COST = [3, 1, 1, 6]
    UPGRADE_COST = 100
    # 2 Upgrades available. First Upgrade improves performance 3x, second 6x.
    UPGRADE_MULTIPLIER = [1, 3, 6]
    
    def __init__(self, robot_type):
        self.robot_id = 'RO{}'.format(random.randrange(0, 5000))
        self.robot_type = robot_type
        self.created_at = datetime.now()
        # Change to technological_level
        self.upgrade_level = 0
        self.status = self.ACTIVE
        # (status, starting time, upgrade_level)
        self.status_intervals = []

    # Change to "get_num..."
    def num_seconds_active_per_interval(self):
        total_seconds_active_per_interval = []
        for idx, status in enumerate(self.status_intervals):
            if status[0] == self.ACTIVE:
                if idx < len(self.status_intervals) - 1:
                    next_status = self.status_intervals[idx + 1]
                    total_seconds_active_per_interval.append(int((next_status[1] - status[1]).total_seconds()))
                else:
                    total_seconds_active_per_interval.append(int((datetime.now() - status[1]).total_seconds()))
            else:
                total_seconds_active_per_interval.append(0)

        return total_seconds_active_per_interval
    
    def num_seconds_active(self):
        return sum(self.num_seconds_active_per_interval())
            
    def extracted_since_last_update(self):
        if self.status_intervals:
            return (self.num_seconds_active_per_interval()[-1] * 
                self.TYPES_EXTRACTION_RATE[self.robot_type] * self.UPGRADE_MULTIPLIER[self.upgrade_level])
        return 0

    def extracted_so_far(self):
        num_seconds_active_per_interval = self.num_seconds_active_per_interval()
        total_extracted = 0
        for idx, status in enumerate(self.status_intervals):
            if status[0] == self.ACTIVE:
                upgrade_level = status[2]
                total_extracted += (num_seconds_active_per_interval[idx] * 
                    self.TYPES_EXTRACTION_RATE[self.robot_type] * self.UPGRADE_MULTIPLIER[upgrade_level])
        return total_extracted

    def discovered_since_last_update(self):
        if self.status_intervals:
            return (self.num_seconds_active_per_interval()[-1] * self.UPGRADE_MULTIPLIER[self.upgrade_level])
        else:
            return 0

    def discovered_so_far(self):
        num_seconds_active_per_interval = self.num_seconds_active_per_interval()
        exploration_points = 0
        for idx, status in enumerate(self.status_intervals):
            if status[0] == self.ACTIVE:
                upgrade_level = status[2]
                exploration_points += num_seconds_active_per_interval[idx] * self.UPGRADE_MULTIPLIER[upgrade_level]

        return exploration_points
    
    def upgrade(self):
        self.upgrade_level += 1

    def __str__(self):
        if self.robot_type == self.STEEL or self.robot_type == self.FUEL: 
            res = '\t [R] {} [Class: {} | Upgrade Level: {}]: During {} seconds active ({} {} units extracted so far | {} units/sec)'.format(
                self.robot_id,
                self.TYPES_NAME[self.robot_type],
                self.upgrade_level,
                self.num_seconds_active(),
                self.extracted_so_far(),
                self.TYPES_NAME[self.robot_type],
                self.UPGRADE_MULTIPLIER[self.upgrade_level] * self.TYPES_EXTRACTION_RATE[self.robot_type],
                )
        else:
            res = '\t [R] {} [Class: {} | Upgrade Level: {}]: During {} seconds active'.format(
                self.robot_id,
                self.TYPES_NAME[self.robot_type],
                self.upgrade_level,
                self.num_seconds_active())
        return res + ' ({})'.format(self.STATUS_NAME[self.status])


class Planet(object):
    DESERT = 0
    JUNGLE = 1
    FROZEN = 2
    ROCKY = 3
    TYPES_NAME = ['Desert', 'Jungle', 'Frozen', 'Rocky']

    def __init__(self):
        self.planet_id = 'PL{}'.format(random.randrange(4000, 30000))
        self.planet_type = random.randrange(0, len(self.TYPES_NAME))
        self.properties = self.planet_factory()
        self.discovered_resources = []
        self.robots = []
        self.buildings = []
        # This is going to be the only resource uncove at the beginning.
        self.uncover_resource()
    
    def uncover_resource(self):
        fuel = self.properties['fuel']
        steel = self.properties['minerals']['steel']
        resource = {
            'fuel': random.randrange(fuel//2, fuel*2),
            'steel':random.randrange(steel//2, steel*2),
        }
        self.discovered_resources.append(resource)
        return resource

    def planet_factory(self):
        if self.planet_type == self.DESERT:
            oxigen = random.randrange(20, 40)
            fuel = random.randrange(600, 1000)
            water = random.randrange(5, 20)
            danger = random.randrange(15, 60)
            mineral_steel = random.randrange(300, 500)

        elif self.planet_type == self.JUNGLE:
            oxigen = random.randrange(80, 100)
            fuel = random.randrange(200, 600)
            water = random.randrange(60, 90)
            danger = random.randrange(60, 90)
            mineral_steel = random.randrange(150, 300)

        elif self.planet_type == self.FROZEN:
            oxigen = random.randrange(20, 40)
            fuel = random.randrange(600, 1000)
            water = random.randrange(50, 70)
            danger = random.randrange(15, 30)
            mineral_steel = random.randrange(300, 500)

        elif self.planet_type == self.ROCKY:
            oxigen = random.randrange(20, 40)
            fuel = random.randrange(400, 600)
            water = random.randrange(5, 20)
            danger = random.randrange(15, 30)
            mineral_steel = random.randrange(600, 900)

        return {
            # ADD Temperature
            'oxigen': oxigen,
            'fuel': fuel,
            'water': water,
            'danger': danger,
            'minerals': {
                'steel': mineral_steel
            }
        }
    
    def __str__(self):
        return '\tPlanet {} ({}) | Properties: {}'.format(
            self.planet_id, self.TYPES_NAME[self.planet_type], self.properties)