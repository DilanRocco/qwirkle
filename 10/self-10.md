The commit we tagged for your submission is 427143d433d1f08474be536dd4e1fb24ba5ad0a9.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/tree/427143d433d1f08474be536dd4e1fb24ba5ad0a9

## Self-Evaluation Form for Milestone 10

Indicate below each bullet which file/unit takes care of each task.

The data representation of configurations clearly needs the following
pieces of functionality. Explain how your chosen data representation 

- implements creation within programs _and_ from JSON specs 
- https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/427143d433d1f08474be536dd4e1fb24ba5ad0a9/Q/Util/util.py#L36-L64
Our Util class converts the json specs into our data representation.

- enforces that each configuration specifies a fixed set of properties (no more, no less)

https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/427143d433d1f08474be536dd4e1fb24ba5ad0a9/Q/Server/server_config.py#L5-L13

https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/427143d433d1f08474be536dd4e1fb24ba5ad0a9/Q/Referee/referee_config.py#L7-L13

https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/427143d433d1f08474be536dd4e1fb24ba5ad0a9/Q/Common/referee_state_config.py#L4-L7

Each configuration is represented by a struct so that it has a fixed set of properties.
- supports the retrieval of properties 

https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/427143d433d1f08474be536dd4e1fb24ba5ad0a9/Q/Referee/ref_with_config.py#L9-L10

The abstracted functionalities take the configurations as input, such the example of the abstracted referee above. The abstracted referee then can retrieve the
properties when it needs to.

- sets properties (what happens when the property shouldn't exist?) 

The configuration does not have default values to set when the property shouldn't exist

- unit tests for these pieces of functionality

We do not have unit tests for these functionality.

Explain how the server, referee, and scoring functionalities are abstracted
over their respective configurations.

https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/427143d433d1f08474be536dd4e1fb24ba5ad0a9/Q/Referee/ref_with_config.py#L9-L10

Abstracted classes implement their parent classes. The abstract classes take the configurations as input. Methods are overwritten using the configurations as 
needed.

Does the server touch the referee or scoring configuration, other than
passing it on?

https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/427143d433d1f08474be536dd4e1fb24ba5ad0a9/Q/Server/server.py#L43

No it does not. The server only passes the ref_config to its start game method to initialize the Referee for the game.

Does the referee touch the scoring configuration, other than passing
it on?

https://github.khoury.northeastern.edu/CS4500-F23/quirky-armadillos/blob/427143d433d1f08474be536dd4e1fb24ba5ad0a9/Q/Referee/ref_with_config.py#L15-L16

No it does not. The abstracted referee passes the game_state, which contains the scoring configuration to the parent class in the method start_from_state.

The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.

