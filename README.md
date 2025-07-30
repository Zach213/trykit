# TryKit

This repo contains the **communication layer** from Extended's overlay (https://tryextended.com) - an in-browser IDE for building Chrome extensions using voice or code. TryKit is the dev-focused version that allows developers to send DOM context to their IDEs, and is designed to be frictionless: hot reloading of chrome extensions, and communication.


**This piece —** `send_to_ide.py` — handles communication between the browser UI and local environments. It lets you send messages from your local IDE to an overlay.

We're open-sourcing this layer for others build smoother coding workflows across local and browser surfaces & understand the mechanism by which it works. More to come.

---

## ✨ What it does

```python
from send_to_ide import send_command

send_command("inject_code", language="js", snippet="console.log('Hello, world!')")
