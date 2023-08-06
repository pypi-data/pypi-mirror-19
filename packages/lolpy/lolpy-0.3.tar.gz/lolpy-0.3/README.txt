This is a python library for the league of legends api.

Quick Start:
Register for an api key at https://developer.riotgames.com/ .
Then import lolpy into a Python Session using:
    import lolpy
Next, create an instance of an APIClient and pass the api key as an argument:
    client = lolpy.APIClient("<insert key here>"[, Region])
Now, make calls to the API such as:
    client.champion_list(True)