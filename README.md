# django-discord-bot
Framework for creating Discord bots using Django

* Uses ASGI for high efficiency and modern features
* Allows using a single daemon for both HTTP and Discord, making for easy deployment
* Integrates into Django's model, allowing for highly modular applications

One of the assumptions is that if your bot is big enough to need horizontal 
scaling, you are a strong enough developer to figure out how to add it in.

## prior art

* https://pycord.dev/
* https://github.com/AdvocatesInc/django-channels-discord


## ASGI Messages


* -> `discord.disconnect`: The WebSocket connection was closed. This does not
  mean we're shutting down, though--the framework will attempt to reconnect and
  resume.
* -> `discord.*`: Discord DISPATCH events are dynamically mapped to message types
  Of interest is `discord.ready`, which is sent after authentication has happened
* <- `discord.*`: Sends a message to discord. `type` is mapped to the op code,
  and the rest is taken as the data to send.

## Deliverables

* Low-level ASGI stuff
  * [x] Discord gateway ASGI server (connects to the Discord Gateway API and connects it to an ASGI app)
  * [ ] Lifespan multiplexer (allow multiple apps to be connected to lifespan)
* Django-based ASGI app
  * [ ] Signals for events
  * [ ] Some kind of django-flavored command framework
* [ ] Opinions about an in-process cron thingy
* [ ] Utilities to make it easy to wire up everything
* [ ] Opinions about Discord API client
  * Should be sync/async (to match current Django)
  * Process-wide connection pool
  * Way to get a default client authenticated with a configured bot token
* [ ] Opinions about OAuth2 handling & user management
  * django-allauth + minimal user
* [ ] Template application to demonstrate the use of all of that
