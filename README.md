</br></br><p align="center"><img src="https://cycls.com/static/assets/favicon.svg" alt="Cycls"></p></br>

<div align="center">
    <a href="https://pypi.org/project/cycls/" target="_blank" rel="noopener noreferrer">
        <img loading="lazy" src="https://img.shields.io/pypi/v/cycls.svg" alt="PyPI" class="img_ev3q" style="display: inline;">
    </a>
    <a href="https://discord.gg/BMnaMatDC7" target="_blank" rel="noopener noreferrer">
        <img loading="lazy" src="https://img.shields.io/discord/1175782747164389466" alt="Discord" class="img_ev3q" style="display: inline;">
    </a>
</div>

</br>

```sh
pip install cycls
```

# Apps
Instantly publish and share AI-native apps

```py
from cycls import Cycls

cycls = Cycls()

# app on https://cycls.com/@spark
@cycls("@spark")
def spark_app(message):
    return message.content + "from spark"

# publish
cycls.push()
```

Async app with history and session id
```py
from cycls import Cycls

cycls = Cycls()

# async app on https://cycls.com/@cake
@cycls("@cake")
async def cake_app(message):
    print("history", message.history)
    print("session id", message.id)
    return message.content + "from cake"

cycls.push()
```

Try it now
- https://cycls.com/@groq   | [groq.py](https://github.com/Cycls/examples/blob/main/groq.py)
- https://cycls.com/@openai | [openai.py](https://github.com/Cycls/examples/blob/main/openai.py)
 
# Agents
Apps in Cycls double as **agents**. Call agents from the Cycls universe.
```py
from cycls import Cycls

cycls = Cycls()

# agent/app on https://cycls.com/@sparkle
@cycls("@sparkle")
async def sparkle_app(message):
    return cycls.call("@groq", message.content)

cycls.push()
```
    
   
