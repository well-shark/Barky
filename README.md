# Barky - Push notifications to your iPhone with Bark.

> Bark: https://github.com/Finb/Bark

# Installation

Binary installers for the latest released version are available on Pypi.

```
pip install Barky
```

# Usage

For the first initialization:

```python
from barky import Bark

'''You only need to specify the Server URL and Client Key once
''' 
bark = Bark('Your Key') # Use default server
# or
bark = Bark('Your Key', server='Server URL') # Use custom server

bark.send('Hello World')
```
Barky will store the parameters you first specified in `~/.bark/config.ini`.
Modifying this file or re-specifying parameters can adjust the configuration.

Then, for future initialization:

```python
from barky import Bark

bark = Bark() # Using stored configurations

bark.send('Hello World')
```

`send()` supports all official parameters, such as `title`, `group`, and so on.
For specific parameters, please refer to [Bark](https://bark.day.app/#/tutorial?id=%e8%af%b7%e6%b1%82%e5%8f%82%e6%95%b0).