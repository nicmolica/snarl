package travellerServer;

/**
 * A character in the RPG.
 */
public class Character {

  private String name;

  /**
   * Makes a character with the given name.
   * @param name the name of the character
   */
  public Character(String name) {
    this.name = name;
  }

  /**
   * Does the character have the given name?
   * @param name the name to compare
   * @return whether the character has the given name
   */
  public boolean isNamed(String name) {
    return this.name.equals(name);
  }

}
