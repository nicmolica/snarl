# Combat Protocol

## Design and Implementation

To implement the hitpoint management system, we only needed to make changes in three places: the code that handles interactions between entities, the methods that handle informing a player of information about their surroundings and the state of the game, and the entity classes themselves.

For the interaction code, we modified the interaction that occurs when a `Player` and an `Adversary` are on the same time. When one moves onto the other, the `Adversary`'s damage is subtracted from the `Player`'s health points. The `Player` also receives knockback of 1 tile, partially because we thought that was cool and partially because it makes rendering in ASCII a bit easier to have only a single entity on a tile at any given time.

For the code that updates human players, we added information about health status to the JSON updates. This slight change allowed the server to send information about the `Player`'s health to the client, so that it could render it.

On the entity classes, we made very simple changes to give `Adversary` classes a field specifying the damage they do, and the `Character` class a field specifying its initial health points.

## Features

With the new health point system, players get to see a health bar at the top of the updates that are rendered to them by the client. This health bar decreases each time they are hit. They are hit whenever an `Adversary` jumps onto the same tile as them, or whenever they jump onto the same tile as an `Adversary`. If the `Adversary` is a `Zombie`, then they lose 1 HP. If it's a `Ghost`, then they lose 2 HP.

When they're hit, they are also thrown back one tile in a random direction. We opted to do a random direction because of cases where there are 2 `Adversary`s standing right in front of a doorway. This came up frequently in testing and was a bit of a hindrance to game progress, so we think that being thrown in a random direction will make it a little easier to progress through a room than if they were thrown right back through the doorway.

A `Player` starts with 5 health, and it decreases as they're hit. On each new level, the `Player`'s HP is reset to 5. This gives them a couple chances before they're killed by `Adversary`s.