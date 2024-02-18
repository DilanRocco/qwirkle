Dear CEOS,<br>
From: Dilan Piscatello and Evan Chase<br>
CC: Matthias Felleisen<br>
Subject: Planning the Remote Proxy Server<br>

### The proxy design:

There will be four classes that act in the proxy design.
-ProxyPlayer
-Player
-Referee
-ProxyReferee

Here is a basic look at what the player proxy will look like according to our current specs
![](images/player_referee_proxy.png?raw=true)

<p> The ProxyPlayer the place where data is converted from the Referee into JSON to be sent over TCP so the player can 
read this info over the wire. The Proxy Player will implement the Player interface. The ProxyPlayer will also accept Turn
info of the player when the player has submitted their turn. </p>

<p> The player class will be the class on the other side of the wire from the referee that does the logic to create a turn action on some 
given map and determine their move with some strategy of their choosing.</p>

<p> The Referee class will be the class that holds the logic for the game state and the current state. This would be on the server side.
The referee keeps track of all the players and can kick the players at any point.</p>

<p> The RefereeProxy will act on the client side where it will take in JSON and convert it to the player's implementation of the game. 
This will be the place where the data is received from the PlayerProxy. The proxy player is also the place where the player sends
the request over to the RefereeProxy saying they want to join the game.</p>


Thanks,
Dilan Piscatelo and Evan Chase