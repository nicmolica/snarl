package travellerServer;

import java.util.List;

import javafx.util.Pair;

/**
 * A travellerServer.TownNetwork in the RPG.
 */
public interface TownNetworkInterface {

  // DESIGN DECISION: this method is static so that it can be on the interface and we don't need to expose a bogus
  // constructor. the specification provided to us did not explicitly ask for this to be static, but it also did not
  // provide an outline of a constructor, so this is meant to expose ONLY travellerServer.TownNetworkInterface (as travellerServer.TownNetwork can
  // now be package public and not externally exposed)
  /**
   * Makes a travellerServer.TownNetworkInterface with the given towns and roads
   * @param towns the towns to put in this network
   * @param roads the roads to connect the towns
   * @return a travellerServer.TownNetworkInterface with the given towns and roads
   * @throws IllegalArgumentException if the roads contain a town that is not in the network
   *   or if either roads or towns is null
   */
  static TownNetworkInterface createTownNetwork(List<Town> towns, List<Pair<String, String>> roads)
    throws IllegalArgumentException {
    return new TownNetwork(towns, roads);
  }

  /**
   * Adds the given character to the town with the given name
   * @param character
   * @param townName
   */
  void addCharacterToTown(Character character, String townName);

  /**
   * Is the given character able to reach the given town name without encountering another character?
   * @param characterName the character name to calculate for
   * @param townName the town to reach
   * @return whether it's possible or not
   */
  boolean reachableWithoutCollision(String characterName, String townName);
}

