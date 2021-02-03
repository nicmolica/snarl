package travellerServer;

/**
 * A travellerServer.Town in the RPG.
 */
public class Town {
  private String name;
  private Character character;

  /**
   * Makes a town with the given name;
   * @param name
   */
  public Town(String name) {
    this.name = name;
  }

  /**
   * The name of this town.
   * @return the name of this town
   */
  public String getName() {
    return this.name;
  }

  /**
   * Is there a character in this town?
   * @return whether there is a character in this town
   */
  public boolean hasCharacter() {
    return this.character != null;
  }

  /**
   * Does the character in this town have the given name?
   * @param characterName the name to compare
   * @return whether there is a character in this town and it has the right name
   */
  public boolean hasCharacterWithName(String characterName) {
    return this.character != null && this.character.isNamed(characterName);
  }

  // DESIGN DECISION: unspecified what happens when a character is placed at a town where
  // another character already is. our code will just overwrite the previous character
  // without throwing an error
  /**
   * Sets this town's character
   * @param character the character to set
   */
  public void setCharacter(Character character) {
    if (character == null) throw new IllegalArgumentException("travellerServer.Character cannot be null");
    this.character = character;
  }

}
