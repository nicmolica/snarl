# Traveler Implementation Review

## Organization
Overall, the organization of the code was very close to what we specified in our spec. There were classes for the `Character`, `Town` and `TownNetwork`, each of which contained the correct fields and methods. Within the `TownNetwork` class, the methods were all of reasonable sizes and were appropriately modular. The documentation was also consistently good throughout, with appropriate Javadoc comments for every field, constructor, method and structure.

## Adherence to Specification
The most glaring difference between the spec and the implementation is the language difference. Our spec required Python, while the implementation we recieved used Java. This also necessitated that the implementation use different libraries. We originally designed our spec to utilize Python's NetworkX module, which took care of the more difficult aspects of functionality for us. The main reason we suggested the use of this module is because it has an efficient built-in breadth-first search algorithm, so this would eliminate the necessity of manually implementing one. Even with these differences, the implementation accomplished everything it needed to.

Beyond the difference in language, the only other significant deviation from the spec was making the `createTownNetwork` method static. This is understandable, as it is a byproduct of using a statically typed language like Java.

Overall, these differences would not prevent us from being able to integrate this implementation with the client we wrote. There would be a bit of a hurdle because the two pieces of software are written in different languages. Beyond that, the integration would be seamless. The only real downside for this integration would be that the manual implementation of a BFS algorithm would probably slow down the program's performance on a large `TownNetwork`.

## Estimated Integration Effort 
