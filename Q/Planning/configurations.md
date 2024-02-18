Dear CEOS,<br>
From: Dilan Piscatello and Evan Chase<br>
CC: Matthias Felleisen<br>
Subject: Documenting the config changes<br>

## Configuration changes:


### RefereeStateConfig
<p> Inside the rulebook, the place where specific game logic is stored, we added a new initializer parameter called RefereeStateConfig.
This refereeStateConfig is a struct that contains the fbo and qbo scoring values. Now when we need to use the qbo and fbo values, 
we simply get them from the config. </p>

### RefereeConfig
<p> For the refereeConfig, we added a subclass to the referee called refereeWithConfig that takes in a config value and 
modifies any logic that is edited by the config values. </p>

### ServerConfig
<p> For the server config, we had to make a bunch of changes for things to work. We firstly needed to get ride of the 
way we use global variables and we moved the startup logic into a server class. This allowed us to more easily pass in a
serverConfig and didn't require us to use the keyword global. We also redid the server-tries logic because before
we had hardcoded two server-tries by making two threads.</p>
Thanks,

### Client Config
<p> We didn't have a way to make multiple clients before in one script. </p>

Thanks,
Dilan Piscatello and Evan Chase