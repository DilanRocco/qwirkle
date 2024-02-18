# The Q Game

The Q game is a spinoff of the board game Qwirkle. The Q Game involves 2-4 players who try to earn as many points as possible by placing their tiles. Each tile placement earns points and potentially bonus points by placing in contigious sequences, completing a Q or placing the rest of the players tiles. The game ends when either a player places all their tiles, all players in a round pass or exchange, or all players are kicked because of invalid moves.

# Scoring

If the player requests a placement, the referee checks whether it is legal and constructs the extended map. Based on this new map, the referee assigns points for a turn as follows:
- A player receives one point per tile placed.

- A player receives one point per tile in a contiguous sequence of tiles (in a row or column) that contains at least one of its newly placed tiles extends.

- A player receives 6 bonus points for completing a Q, which is a contiguous sequence of tiles that contains all shapes or all colors and nothing else.

- A player also receives 6 bonus points for placing all tiles in its possession.

- The referee keeps track of the scores on a per turn basis and shares the scores of all players with the player to whom it grants a turn.
  
  
# Ending a Game

The game ends if one of the following condition holds:

- at the end of a round if all remaining players pass or replace their tiles;

- at the end of a turn if a player has placed all tiles in its possession; or

- there are no players left after a turn.


## Usage

To work on this project and run the program through a terminal one must use the command:
```
pip install -e .
```
This command allows for all of the dependices to reference each other, allowing the imports to work. 

There are a few scripts that one might wish to run to simulate some functionality during the game. <br>

- `xgames` in `/7` which simualtes a game with some players.
- `xgames-with-observer` in `/8` which simualtes a game with some players and an observer GUI if you wish by using the --show command.
- `xbaddies` in `/9` which simulates a game with some good behaving players and some not so nice players that attempt to cheat. 
- `xclients` and `xserver` in `/10` simulates a server client relationship over TCP between the referee and the players. 

<p> For all the scripts above, there is examples of input into the script in their respective /Tests/ folder. 

  
## Remote Proxy Static Class Diagram:

  
```
            +----------------------+                                                                                            
            |                      |                                       |                                                     
  config    |     run_xserver      |                                       |                                                    
--------->  ------------------------                                       |        +-----------------+                         
            |        main()        |                                       | config |                 |                         
            +----------------------+                                       |------->|   run_xclient   |                         
                        |                                                  |        -------------------                         
                        |                                                  |        |      main()     |                         
                        |                                                  |        +-----------------+                         
                        ◆                                                  |                  |                                  
            +----------------------+                                       |                  |                                 
            |                      |                                       |                  ◆                                 
            |        Server        |                                       |        +-----------------+                         
            ------------------------                                       |        |                 |                         
            |    serve_forever()   |                     +------------+    |        |   RefereeProxy  |          -              
            +----------------------+               +---->| PlayerAPI  |    |        -------------------                         
                        \                          |     +------------+    |        |    listen()     |                         
   -                    /                          |                       |        +--------|--------+                         
                        \                          |                       |                 |                                  
                        /                          |                       |                 ◆                                  
            +-----------------------+         +----|------------+          |         +---------------+                          
            |                       |         |                 |          |         |    Client     |                          
            |      Connection       |◆--------|   PlayerProxy   |          |         |               |                          
            -------------------------         -------------------          |         -----------------                          
            | get_latest_message()  |         |                 |          |         |     recv()    |                          
            |write_method(meth,args)|         +-----------------+          |         |     send()    |                          
            +-----------------------+                                      |         +---------------+             
                 |                                the wire                               |
                 |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
```
## Client Interactions
```
                                                                               
                                                                               
                                                                               
                                                                               
                                                                               
                                                                               
    run_xclient                      RefereeProxy          Client              
                                                                               
         |         init(host, port, name)|                     | 
         |---------------------------------------------------->|
         |    init(client, strategy)     |                     |                                 
         |------------------------------>|                     |               
         |                               |                     |              
         |                               |                     |               
         |             listen()          |                     |               
         |------------------------------>|                     |               
         |                               |     recv()          |               
         |                               |-------------------->|               
         |                               |                     |               
         |                               |      data           |               
         |                               | <-------------------|               
         |                               |                     |               
         |                               | ---+                |               
         |                               |    | process_data() |               
         |                               | ---+                |               
         |                               |                     |               
         |                               |     send(json)      |               
         |                               |-------------------->|               
         |                               |                     |  over the wire 
         |                               |                     |---------->     
         |                               |                     |               
         |                               |                     |               
         |                               |                     |               
         |                               |                     |               
```
## Server Interactions
```
                                                                                                                                              
 run_xserver                     Server                Connection                    ProxyPlayer               Referee                        
                                                                                                                                              
      | init(config, addr, port)   |                       |                             |                        |                           
      |--------------------------->|                       |                             |                        |                           
      |                            |                       |                             |                        |                           
      |      serve_forever()       |                       |                             |                        |                           
      |--------------------------> |                       |                             |                        |                           
      |                            |                       |                             |                        |                           
      |                            |                       |                             |                        |                           
      |                            |       add_name()      | handle(name)                |                        |         data                  
      |                            | <---------------------|----------------------------------------------------------------------------------
      |                 players    |                       |                             |                        |                           
      |                 init after |                       |           init(name, conn)  |                        |                           
      |                 timer or   |  -------------------------------------------------->|                        |                           
      |                 4 players  |                       |                             |                        |                           
      |                            |                       |        main()               |                        |                           
      |                            |----------------------------------------------------------------------------->                                              |                           |                       |                             |                        |
      |                            |                       |                             |                        |                           
      |                            |                       |                             |   PlayerAPI Method     |                           
      |                            |                       |                             |<-----------------------|                           
      |                            |                       |                             |                        |                           
      |                            |                       |                  send(data) |                        |                           
      |                            |                       | <---------------------------|                        |                           
      |                            |                       |                             |                        |                           
      |                            |                       |                             |---+                    |                           
      |                            |                       |                LOOPING      |   | listen()           |                           
      |                            |                       |                             |<---                    |                           
      |                            |                       |                             |                        |                           
      |                            |                       | handle(response)            |                        |          data           
      |                            |                +------|<-----------------------------------------------------|-------------------------  
      |                            |                |      |                             |                        |                           
      |                            |   set_latest() |      |                             |                        |                           
      |                            |                |      |                             |                        |                           
      |                            |                +----->|                             |                        |                           
      |                            |                       |           data              |                        |                           
      |                            |                       |---------------------------->|    deserialized data   |                           
      |                            |                       |                             |----------------------> |                           
      |                            |                       |                             |                        |                           
                      
``` 
## Player Interface Diagram
```                                                                                                                  
                                                                                                     
                                         +-------------------+                                       
                                         |                   |                                       
                                         |      Player       |                                       
                                         |                   |                                       
                                         +---------|---------+                                       
                                                   |                                                 
                                                   |                                                 
          |-------------------------|--------------------------|------------------------|            
          |                         |                          |                        |            
          |                         |                          |                        |            
          |                         |                          |                        |            
+-------------------+     +---------|---------+      +---------|---------+    +-------------------+  
|                   |     |                   |      |                   |    |                   |  
|    CheatPlayer    |     |     ExnPlayer     |      |     LoopPlayer    |    |   InHousePlayer   |  
|                   |     |                   |      |                   |    |                   |  
+-------------------+     +-------------------+      +-------------------+    +-------------------+
```
  
  
## Misc.
```
                                                                                                    
              +---------------------+                              +----------------------+        
              |                     |                              |                      |        
              |      Strategy       |                              |      PlayerState     |        
              |                     |                              |                      |        
              +----------|----------+                              +-----------|----------+        
                         |                                                     |                   
                         |                                                     |                   
                         |                                                     |                   
              |-----------------------                             +-----------|----------+        
              |                      |                             |                      |        
    +---------|--------+   +---------|--------+                    |   PublicPlayerData   |        
    |                  |   |                  |                    |                      |        
    |       Dag        |   |      Ldasg       |                    +----------------------+        
    |                  |   |                  |                                                    
    +------------------+   +------------------+                                                    
                                                                                                   
                                                                                                   
     +----------------------+                                                                      
     |                      |                                                                      
     |         Turn         |                                                                      
     |                      |                                                                      
     +-----------|----------+                                                                      
                 |                                                                                 
                 |                                                                                 
                 |                                                                                 
     +-----------|----------+                                                                      
     |                      |                                                                      
     |     TurnOutcome      |                                                                      
     |                      |      
     +----------------------+      
```
## Referee Interface Diagram
```
                                     +--------------------+                                       
                                     |                    |                                       
                                     |      Referee       <----------------------------           
                                     |                    |                           |           
                                     +----------|---------+                           |           
                                                |                          +--------------------+ 
                                                |                          |                    | 
                                                |                          | RefereeWithConfig  | 
                                                |                          |                    | 
                                                |                          +--------------------+ 
                                     +----------◆---------+                                       
                                     |                    |                                       
            |-------------------------      GameState     -----------------------------|          
            |                        |                    |                            |          
            |                        +---------|----------+                            |          
            |                                  |                                       |          
            ◆                                  ◆                                       ◆          
+--------------------+               +--------------------+                 +--------------------+
|                    |               |                    |                 |                    |
|      RuleBook      |               |         Map        |                 |   PlayerGameState  |
|                    |               |                    |                 |                    |
+----------|---------+               +--------------------+                 +--------------------+
           |                                                                                      
           |                                                                                      
           |                                                                                      
+----------◆---------+                                                                            
|                    |                                                                            
| RefereeStateConfig |                                                                            
|                    |                                                                            
+--------------------+                                                                            
