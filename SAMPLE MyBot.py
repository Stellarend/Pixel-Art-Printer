import hlt
import logging

# Point is a tuple, (x, y)
def distance_to_point(entity, point):
    return ((point[1] - entity.y)**2.0 + (point[0]-entity.x)**2.0)**0.5

# sqrddist doesnt sqrt the distance so its much faster
# Usefull for finding the closest point without caring exactly where
# Point is a tuple, (x, y)
def sqrddist_to_point(entity, point):
    return ((point[1] - entity.y)**2.0 + (point[0]-entity.x)**2.0)

def center_of_entities(entityList):
    # The length of the list, define it here so we don't have to keep recalculating
    listLen = float(len(entityList))
    # The x position of the closest entity to the left
    leftMargin = min(entityList, key=lambda entity: entity.x).x
    # The y position of the closest entity to the top
    topMargin = min(entityList, key=lambda entity: entity.y).y
    
    # Get sum of all positions
    xCenter = sum(map(lambda entity: entity.x, entityList))
    # Subtract to left bound*
    xCenter -= leftMargin * listLen
    # Devide by list len to get average
    xCenter /= listLen
    # Add left margin
    xCenter += leftMargin

    # Get sum of all positions
    yCenter = sum(map(lambda entity: entity.y, entityList))
    # Subtract to top bound*
    yCenter -= topMargin * listLen
    # Devide by list len to get average
    yCenter /= listLen
    # Add top margin
    yCenter += topMargin

    return (xCenter, yCenter)
        

# GAME START
game = hlt.Game("Stellarend")
logging.info("Stellarend initiated successfuly")

# dont loop through ships, loop through planets.

while True:
    # TURN START
    game_map = game.update_map()
    command_queue = []
    
    enemies = []
    for player in game_map.all_players():
        if player.id != game_map.my_id:
            enemies.append(player)

    unownedPlanets = []
    friendlyPlanets = []
    enemyPlanets = []
    
    for planet in game_map.all_planets():
        if planet.owner:
            if planet.owner.id == game_map.my_id: friendlyPlanets.append(planet)
            else: enemyPlanets.append(planet)
        else: unownedPlanets.append(planet)

    centerOfAllies = (0,0)
    if friendlyPlanets:
        centerOfAllies = center_of_entities(friendlyPlanets)
    

    # Sort enemy planets based on how close they are to the center of the hive
    enemyPlanets.sort(key=lambda planet: sqrddist_to_point(planet, centerOfAllies))
    # Create a list of firendly planets that can have more docked ships
    dockableFriendlyPlanets = list(filter(lambda planet: not planet.is_full(), friendlyPlanets))

    for ship in game_map.get_me().all_ships():
        # Only use undocked ships
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        # If there are unowned planets, go to the closest one
        if unownedPlanets:
            closestUPlanet = min(unownedPlanets, key = lambda planet: planet.calculate_distance_between(ship))
            unownedPlanets.remove(closestUPlanet)
            if ship.can_dock(closestUPlanet):
                command_queue.append(ship.dock(closestUPlanet))
            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(closestUPlanet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    max_corrections=18,
                    angular_step=5,
                    ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)
        # If there are dockable friendly planets, dock at the closest one
        elif dockableFriendlyPlanets:
            closestDPlanet = min(dockableFriendlyPlanets, key = lambda planet: planet.calculate_distance_between(ship))

            if ship.can_dock(closestDPlanet):
                command_queue.append(ship.dock(closestDPlanet))
            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(closestDPlanet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    max_corrections=18,
                    angular_step=5,
                    ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)
                    
        # Nothing to do, go attack the enemy planet that is closest to the cneter of allies
        elif enemyPlanets:
            # Since enemyPlanets is already sorted, enemyPlanets[0] can be done to get the closest
            closestEPlanet = enemyPlanets[0]
            navigate_command = ship.navigate(
                ship.closest_point_to(closestEPlanet.all_docked_ships()[0]),
                game_map,
                speed=int(hlt.constants.MAX_SPEED),
                max_corrections=6,
                angular_step=8,
                ignore_ships=False)
            if navigate_command:
                command_queue.append(navigate_command)

        # TODO: kill remaining enemy ships if no planets left
                
    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
