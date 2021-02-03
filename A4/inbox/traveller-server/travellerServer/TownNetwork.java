package travellerServer;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.Predicate;
import java.util.function.Supplier;
import java.util.stream.Stream;

import javafx.util.Pair;

/**
 * A collection of towns in an RPG.
 */
class TownNetwork implements TownNetworkInterface {

  private List<Town> towns;
  private List<Pair<String, String>> roads;

  /**
   * Creates a travellerServer.TownNetwork with the given towns and roads.
   * @param towns the towns in this network
   * @param roads the roads connecting the towns
   * @throws IllegalArgumentException if the roads contain a town that is not in the network
   *   or if either roads or towns is null
   */
  TownNetwork(List<Town> towns, List<Pair<String, String>> roads) throws IllegalArgumentException {
    if (towns == null || roads == null) {
      // TODO: should this also throw for an empty list of towns or roads?
      throw new IllegalArgumentException("cannot make a town network with null towns or roads");
    }
    if (!TownNetwork.roadsConnectExistingTowns(towns, roads)) {
      throw new IllegalArgumentException("roads passed in contain a town not in this network");
    }

    this.towns = towns;
    this.roads = roads;
  }

  /**
   * Do the roads only connect already existing towns?
   * @param towns existing towns
   * @param roads the roads connecting them
   * @return roads only connect existing towns
   */
  private static boolean roadsConnectExistingTowns(List<Town> towns, List<Pair<String, String>> roads) {
    Predicate<Pair<String, String>> roadConnectsExistingTowns = pair -> {
      String key = pair.getKey();
      Predicate<Town> keyIsTown = town -> town.getName().equals(key);

      String value = pair.getValue();
      Predicate<Town> valueIsTown = town -> town.getName().equals(value);

      return towns.stream().anyMatch(keyIsTown) && towns.stream().anyMatch(valueIsTown);
    };
    return roads.stream().allMatch(roadConnectsExistingTowns);
  }

  /**
   * Adds the given character to the town.
   * @param character the character to add to the town
   * @param townName the town to add the given character to
   * @throws IllegalStateException when the town does not exist in this network
   */
  @Override
  public void addCharacterToTown(Character character, String townName)
      throws IllegalStateException {
    this.getTownWithTownName(townName).setCharacter(character);
  }

  /**
   * DFS for the destination town from the character's current town.
   * @param characterName the character name to calculate for
   * @param townName the town to reach
   * @return is the destination reachable without encountering any characters
   * @throws IllegalStateException if the character or town are not in this network
   */
  @Override
  public boolean reachableWithoutCollision(String characterName, String townName) throws IllegalStateException {
    Town charactersTown = this.getTownWithParam(town -> town.hasCharacterWithName(characterName),
        () -> new IllegalStateException("town network does not have character with name: " + characterName));
    String charactersTownName = charactersTown.getName();
    boolean characterIsAlreadyThere = charactersTownName.equals(townName);
    return characterIsAlreadyThere || this.isReachableForNextTown(charactersTownName, townName, new ArrayList<>());
  }

  /**
   * Helper to reachableWithoutCollision - DFS for the path to destination, making sure that there aren't loops.
   * @param currentTownName the town to search from currently
   * @param destinationTownName the target town
   * @param visited the names of the visited towns
   * @return whether the destination town is reachable from the current town without encountering another character
   * @throws IllegalStateException if the town is not in this network
   */
  private boolean isCurrentTownAndPathToDestinationEmpty(String currentTownName,
      String destinationTownName, List<String> visited) throws IllegalStateException {
    if (visited.contains(currentTownName)) return false;

    visited.add(currentTownName);

    // DESIGN DECISION: if the destination has a character, then there is no "safe" passage because
    // there is a character at that final destination
    Town currentTown = this.getTownWithTownName(currentTownName);
    boolean currentTownIsEmpty = !currentTown.hasCharacter();
    return currentTownIsEmpty &&
        this.isReachableForNextTown(currentTownName, destinationTownName, visited);
  }

  /**
   * Recursive helper in the search for the destinationTownName.
   * @param currentTownName current town
   * @param destinationTownName town we're looking for
   * @param visited visited towns
   * @return whether it is reachable or not
   * @throws IllegalStateException if the town is not in this network
   */
  private boolean isReachableForNextTown(String currentTownName, String destinationTownName, List<String> visited)
      throws IllegalStateException {
    return currentTownName.equals(destinationTownName) ||
        this.getReachableTownsFromTownName(currentTownName)
            .anyMatch(nextTown -> this.isCurrentTownAndPathToDestinationEmpty(nextTown, destinationTownName, visited));
  }

  // DESIGN DECISION: although it was not explicitly stated, this method is to resolve
  // the assumption that the pairs imply bidirectional reachability - e.g. the key can
  // reach the value and the value can reach the key
  /**
   * Gets any reachable towns in from the given town.
   * @param townName the town to find reachable destinations for
   * @return a stream of the reachable town names
   */
  private Stream<String> getReachableTownsFromTownName(String townName) {
    return this.roads.stream()
        .map(pair -> {
          if (pair.getValue().equals(townName)) return pair.getKey();
          if (pair.getKey().equals(townName)) return pair.getValue();
          return null;
        })
        .filter(reachable -> reachable != null);
  }

  /**
   * Finds the town in this network with the given name.
   * @param townName name of the town to look for
   * @return the town with the given name
   * @throws IllegalStateException if the town is not in this network
   */
  private Town getTownWithTownName(String townName) throws IllegalStateException {
    return this.getTownWithParam(town -> town.getName().equals(townName),
        () ->  new IllegalStateException("No town with name: " + townName));
  }

  /**
   * Gets the town in the network with the given name or the town the given character name is in.
   * @param questionToAsk the function to use to find the town
   * @param errorSupplier function to get the error to throw if town is not found
   * @return the travellerServer.Town
   */
  private Town getTownWithParam(Predicate<Town> questionToAsk, Supplier<IllegalStateException> errorSupplier) {
    // DESIGN DECISION: multiple towns may match the criteria of having the same name or having a given character.
    // if this is the case, our code will not throw an error and instead will just "choose" one as it was unspecified
    Optional<Town> maybeTown = this.towns.stream()
        .filter(questionToAsk)
        .findFirst();

    if (maybeTown.isPresent()) return maybeTown.get();
    else {
      throw errorSupplier.get();
    }
  }
}
