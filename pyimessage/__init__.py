import os

from pyimessage.tools.dotenv import set_env_file as _set_env


_set_env(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '.env'))