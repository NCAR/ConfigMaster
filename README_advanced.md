# Advanced ConfigMaster usage

In an effort to keep the primary configmaster README as short and easy to use as possible,
more advanced topics will be put on this page.

# Configuration Override
Sometimes it is useful to have a cmd line option cause a cascading effect which
overrides other configuration options.  

Example 5 shows how to override additional options based on cmd line parameters.  Normally 
the config file is parsed first, then the command line, so if you have this configuration:
```
model = "GFS3" # GFS4 also ok.
filesize = 1e+6

if model == "GFS3":
  filesize = 1e+6
else if model == "GFS4":
  filesize = 5e+6
```
and you pass --model GFS4, it will not set filesize based on your new model.

Instead you do it like this:
```
model = "GFS3" # GFS4 also ok.
filesize = 1e+6

_config_override["model"]["GFS4"]["filesize"] = 5e+6
```

_config_override is only triggered via the command line, so you can modify the config file values and not worry about what _config_override is set to.

[Example5.py Source](https://raw.githubusercontent.com/NCAR/ConfigMaster/master/example5/example5.py)

