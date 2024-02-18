The commit we tagged for your submission is d30b95e9e9fb0ac78f5f2e2d8e513b398604ec1a.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/tree/d30b95e9e9fb0ac78f5f2e2d8e513b398604ec1a

## Self-Evaluation Form for Milestone 9

Indicate below each bullet which file/unit takes care of each task.

For `Q/Server/player`,

- explain how it implements the exact same interface as `Q/Player/player`
It is a subclass of Q/Player/player.
https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/d30b95e9e9fb0ac78f5f2e2d8e513b398604ec1a/Q/Server/player.py#L14
- explain how it receives the TCP connection that enables it to communicate with a client
When signing up players, we store their name and connection in a dictionary. Once the game starts, we use that dictionary and pass in the connection to the init of the ProxyPlayer.
https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/d30b95e9e9fb0ac78f5f2e2d8e513b398604ec1a/Q/Server/server_callback.py#L12
- point to unit tests that check whether it writes (proper) JSON to a mock output device
We do not have a unit test for that check.
For `Q/Client/referee`,

- explain how it implements the same interface as `Q/Referee/referee`
The proxy referee listens for data on a main loop that runs until the game ends. However, it does not directly implement the interface for Q/Referee/referee.
- explain how it receives the TCP connection that enables it to communicate with a server
https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/d30b95e9e9fb0ac78f5f2e2d8e513b398604ec1a/Q/Client/run_client.py#L12-L13
We create a client and then pass it in to the initalizer of the ProxyRef.
- point to unit tests that check whether it reads (possibly broken) JSON from a mock input device
We do not have a check for this.
For `Q/Client/client`, explain what happens when the client is started _before_ the server is up and running:
It waits until the the server is up
- does it wait until the server is up (best solution) - yes.
- does it shut down gracefully (acceptable now, but switch to the first option for 10)

For `Q/Server/server`, explain how the code implements the two waiting periods. 
https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/d30b95e9e9fb0ac78f5f2e2d8e513b398604ec1a/Q/Server/server.py#L15-L38

We start two threads timers. One timer expires in 20 seconds and the other at 40 seconds. Both call the same function when the time expires and check if 2 or more players are in the player list. We add a boolean to the function paramters checking if we should close the server and the empty results are outputted. 
The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.

