To test this Q game, one can run the xtest script located in the main directory.

In this test file, we run the following files: test.py, test_points.py, and test_player_strategy.py

- Test.py runs tests for the rulebook and map.
- Test_points.py runs tests for the scoring system. 
- The test_player_strategy.py tests different player strategies.


To test the functionality of converting from json to our data representations, computing valid positions to place a tile, 
and converting the output back to json, run the xlegal test harness with input as one of n-in.json files.
xlegal calls the run_from_command_line.py file.
xscore callss the run_xscore.py file
