Pair: quirky-armadillos \
Commit: [d30b95e9e9fb0ac78f5f2e2d8e513b398604ec1a](https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/tree/d30b95e9e9fb0ac78f5f2e2d8e513b398604ec1a) \
Self-eval: https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/ab2422af60f4129873b30fd83c50cbe14312c5dc/9/self-9.md \
Score: 158/210 \
Grader: Derek Leung

– [20/20] points, for accurate self eval

The first batch of inspections concerns Q/Server/player:

Q/Server/player must implement the same interface as Q/Player/mechanism, that is, accepting

[10/10] points for name calls and return the name sent by the client; 

[10/10] points for setup calls, turn them into JSON, get result ("void") in JSON;

[10/10] points for take-turn calls, turn them into JSON, receive a JSON ACTION, return it as an internal value;

[10/10] points for new-tiles calls, turn them into JSON, get result ("void") in JSON;

[10/10] points for win calls, turn them into JSON, get result ("void") in JSON;

[15/15] points for constructors (builders, factories) that receive handles for sending/receiving over some stream (so that TCP can be mocked);

[9/15] points for unit tests for Q/Clients/player -- 60% for saying you didn't do


The second batch of inspections is about Q/Clients/referee:

Q/Clients/referee must implement the same "context" (co) as Q/Player/referee, namely, receiving and making:

[10/10] points for setup calls

[10/10] points for take-turn calls

[10/10] points for new-tiles calls

[10/10] points for win calls

[15/15] points for constructor (builder, factory) must receive (1) a player and (2) handles for sending/receiving JSON over streams.

[9/15] points for unit tests for Q/Server/referee -- 60% for saying you didn't do

[0/20] points for synchronizing client start-ups with servers; -- if sock.connect errors, you don't catch the error or retry.

[0/20] points for abstracting over the “wait for two periods” property of the server. -- not done
