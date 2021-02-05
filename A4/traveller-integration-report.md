# Traveler Implementation Review

## Organization
Overall, the organization of the code was very close to what we specified in our spec. There were classes for the `Character`, `Town` and `TownNetwork`, each of which contained the correct fields and methods. Within the `TownNetwork` class, the methods were all of reasonable sizes and were appropriately modular. The documentation was also consistently good throughout, with appropriate Javadoc comments for every field, constructor, method and structure.

## Adherence to Specification
The most glaring difference between the spec and the implementation is the language difference. Our spec required Python, while the implementation we recieved used Java. This also necessitated that the implementation use different libraries and exception types. However, the implementation does a good job of mapping the Python features in our specification,
to their semantic correspondents in Java. 

Beyond the difference in language, the only other significant deviation from the spec was making the `createTownNetwork` method static. This is understandable, as it is a byproduct of using a statically typed language like Java. Even with the differences, the implementation accomplished everything that our specification required of it. Furthermore, design choices
resulting from a vaguely specified behavior are clearly denoted and explained in comments. 

## Estimated Integration Effort 
We estimate that integrating the provided implementation with our client would take about 1 hour. Python has packages that can interact with a JVM, such as `JPype1` or `Py4J`. Setting up our code to utilize the implementation this way would require a relatively small amount of effort. 

Overall, these differences would not prevent us from being able to integrate this implementation with the client we wrote. There would be a bit of a hurdle because the two pieces of software are written in different languages. Beyond that, the integration would be seamless. The only real downside for this integration would be that the aforementioned packages for 
using Java code in Python work by setting up a JVM instance, which would cause a performance hit. 

## Reflection on Specification Writing
Based on the artifact you received and the above two questions, how could you improve your specification to make it more amenable for implementation as you intended?

On reflection, our specification could have included more detail about interactions and edge cases, rather than requiring the implementation team to make a design choice. An example
of this is the `TODO` comment on line 29 of `TownNetwork.java`, which asks if an empty list of towns should be allowed. Our specification does not mention the case of an empty
network, but it could have, in order to reduce the chance that the delivered functionality was not what we wanted. 

It also appears that we did not properly specify the `TownNetwork` class; while that was partially intentional, in order to reduce the presence of implementation details in the
specification, we should have added some detail explaining the purpose and any desired contents of the class. 