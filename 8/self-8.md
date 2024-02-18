The commit we tagged for your submission is ee47d28f9c79357b718af602682b904ccb9b7701.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/tree/ee47d28f9c79357b718af602682b904ccb9b7701

## Self-Evaluation Form for Milestone 8

Indicate below each bullet which file/unit takes care of each task:

- concerning the modifications to the referee: 

  - is the referee programmed to the observer's interface
    or is it hardwired?
    
    The referee is hardwired to the observer. It now takes an optional observer in its constructor, and if one is passed, the referee will use the functions
    receive_a_state to pass the game state to the observer after each turn and receive_a_game_over to inform the observer that the game is over.
    https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/3308161ecdb914f062867903675c971842ef0ab0/Q/Referee/referee.py#L21-L68
  - if an observer is desired, is every state per player turn sent to
    the observer? Where? 
    
    Yes, in the referee's run_game method, the referee sends the game_state to the observer after every turn using recieve_a_state in line 65
    https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/3308161ecdb914f062867903675c971842ef0ab0/Q/Referee/referee.py#L45-L65
  - if an observer is not desired, how does the referee avoid calls to
    the observer?
    
  Before any calls to the observer, the referee checks if the observer was initially passed in.
  https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/3308161ecdb914f062867903675c971842ef0ab0/Q/Referee/referee.py#L65-L66
- concerning the implementation of the observer:

  - does the purpose statement explain how to program to the
    observer's interface? 
    
  The observer does not have its purpose statement.
  - does the purpose statement explain how a user would use the
    observer's view? Or is it explained elsewhere? 
    
  The observer does not have its purpose statement. <br>
The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.

