---
id: jqcek
name: How to Add a PBA
file_version: 1.0.2
app_version: 0.8.6-0
file_blobs:
  monkey/infection_monkey/monkey.py: e31c62cadad86a0c124b7623a61079994790ab3e
  monkey/infection_monkey/post_breach/actions/hide_files.py: 5c0bda507836980677492d473079bf9271f27a53
  monkey/monkey_island/cc/services/config_schema/definitions/post_breach_actions.py: d6831ed63b17f327d719a05840d7e51202fa5ccb
  monkey/monkey_island/cc/services/config_schema/monkey.py: a9f9790f847d82fb7c2fc9433d4e70a12503649a
  vulture_allowlist.py: c8c1378d4b115e69baaf808f64ae756c2a9929aa
  monkey/infection_monkey/post_breach/pba.py: 0ef8e0ecb1e9f505efa00634949197e505a8adbb
  monkey/infection_monkey/post_breach/actions/communicate_as_backdoor_user.py: 627e67e5b633ba1ae9e7810b17c45e004d9efe25
  monkey/infection_monkey/post_breach/custom_pba/custom_pba.py: ce7dd64f211f366462f125a82d9d7f04fb40d162
  monkey/infection_monkey/post_breach/actions/discover_accounts.py: a153cf5b6185c9771414fc5ae49d441efc7294b6
  monkey/infection_monkey/post_breach/actions/timestomping.py: 3e7c61f59fbf35cebcb96812d3e416055d030939
---

A PBA is a major component in our system. This document will describe what it is and how to add a new one.

A PBA is fsda{Explain what a PBA is and its role in the system}

Some examples of `PBA`[<sup id="1yTwmK">↓</sup>](#f-1yTwmK)s are `CommunicateAsBackdoorUser`[<sup id="1T4FcD">↓</sup>](#f-1T4FcD), `CustomPBA`[<sup id="Cb2a9">↓</sup>](#f-Cb2a9), `AccountDiscovery`[<sup id="ZzyhBz">↓</sup>](#f-ZzyhBz), and `Timestomping`[<sup id="Z1Hvwio">↓</sup>](#f-Z1Hvwio).

<br/>

## TL;DR - How to Add a `PBA`[<sup id="1yTwmK">↓</sup>](#f-1yTwmK)

1. Create a new class inheriting from `PBA`[<sup id="1yTwmK">↓</sup>](#f-1yTwmK)&nbsp;
   - Place the file in one of the directories under [[sym:./monkey/infection_monkey/post_breach({"type":"path","text":"monkey/infection_monkey/post_breach","path":"monkey/infection_monkey/post_breach"})]],
     e.g. `HiddenFiles`[<sup id="Z2aIscA">↓</sup>](#f-Z2aIscA) is defined in [[sym:./monkey/infection_monkey/post_breach/actions/hide_files.py({"type":"path","text":"monkey/infection_monkey/post_breach/actions/hide_files.py","path":"monkey/infection_monkey/post_breach/actions/hide_files.py"})]].
2. Implement `__init__`[<sup id="dQOwA">↓</sup>](#f-dQOwA).
3. Update [[sym:./monkey/infection_monkey/monkey.py({"type":"path","text":"monkey/infection_monkey/monkey.py","path":"monkey/infection_monkey/monkey.py"})]].
3. Update [[sym:./monkey/monkey_island/cc/services/config_schema/definitions/post_breach_actions.py({"type":"path","text":"monkey/monkey_island/cc/services/config_schema/definitions/post_breach_actions.py","path":"monkey/monkey_island/cc/services/config_schema/definitions/post_breach_actions.py"})]].
3. Update [[sym:./monkey/monkey_island/cc/services/config_schema/monkey.py({"type":"path","text":"monkey/monkey_island/cc/services/config_schema/monkey.py","path":"monkey/monkey_island/cc/services/config_schema/monkey.py"})]].
4. **Profit** 💰

<br/>

## Example Walkthrough - `HiddenFiles`[<sup id="Z2aIscA">↓</sup>](#f-Z2aIscA)
We'll follow the implementation of `HiddenFiles`[<sup id="Z2aIscA">↓</sup>](#f-Z2aIscA) for this example.

A `HiddenFiles`[<sup id="Z2aIscA">↓</sup>](#f-Z2aIscA) is {Explain what HiddenFiles is and how it works with the PBA interface}

<br/>

### `HiddenFiles`[<sup id="Z2aIscA">↓</sup>](#f-Z2aIscA) Usage Example
For example, this is how `HiddenFiles`[<sup id="Z2aIscA">↓</sup>](#f-Z2aIscA) can be used:
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 monkey/infection_monkey/monkey.py
```python
⬜ 277                PluginType.POST_BREACH_ACTION,
⬜ 278            )
⬜ 279            puppet.load_plugin(
🟩 280                "HiddenFiles", HiddenFiles(self._telemetry_messenger), PluginType.POST_BREACH_ACTION
⬜ 281            )
⬜ 282            puppet.load_plugin(
⬜ 283                "TrapCommand",
```

<br/>

## Steps to Adding a new `PBA`[<sup id="1yTwmK">↓</sup>](#f-1yTwmK)

<br/>

### 1\. Inherit from `PBA`[<sup id="1yTwmK">↓</sup>](#f-1yTwmK).
All `PBA`[<sup id="1yTwmK">↓</sup>](#f-1yTwmK)s are defined under [[sym:./monkey/infection_monkey/post_breach({"type":"path","text":"monkey/infection_monkey/post_breach","path":"monkey/infection_monkey/post_breach"})]].

<br/>

We first need to define our class in the relevant file, and inherit from `PBA`[<sup id="1yTwmK">↓</sup>](#f-1yTwmK):
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 monkey/infection_monkey/post_breach/actions/hide_files.py
```python
⬜ 15     HIDDEN_FSO_CREATION_COMMANDS = [get_commands_to_hide_files, get_commands_to_hide_folders]
⬜ 16     
⬜ 17     
🟩 18     class HiddenFiles(PBA):
⬜ 19         """
⬜ 20         This PBA attempts to create hidden files and folders.
⬜ 21         """
```

<br/>

### 2\. Implement `__init__`[<sup id="dQOwA">↓</sup>](#f-dQOwA)

<br/>

Implement `__init__`[<sup id="dQOwA">↓</sup>](#f-dQOwA).

<br/>

This is how we implemented it for `HiddenFiles`[<sup id="Z2aIscA">↓</sup>](#f-Z2aIscA) {Explain what's happening in this implementation}
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 monkey/infection_monkey/post_breach/actions/hide_files.py
```python
⬜ 20         This PBA attempts to create hidden files and folders.
⬜ 21         """
⬜ 22     
🟩 23         def __init__(self, telemetry_messenger: ITelemetryMessenger):
🟩 24             super(HiddenFiles, self).__init__(telemetry_messenger, name=POST_BREACH_HIDDEN_FILES)
⬜ 25     
⬜ 26         def run(self, options: Dict):
⬜ 27             # create hidden files and folders
```

<br/>

## Update additional files with the new class
Every time we add a new `PBA`[<sup id="1yTwmK">↓</sup>](#f-1yTwmK), we reference it in a few locations.
We will still look at `HiddenFiles`[<sup id="Z2aIscA">↓</sup>](#f-Z2aIscA) as our example.

<br/>

3\. Add the new class to [[sym:./monkey/infection_monkey/monkey.py({"type":"path","text":"monkey/infection_monkey/monkey.py","path":"monkey/infection_monkey/monkey.py"})]], for example:
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 monkey/infection_monkey/monkey.py
```python
⬜ 277                PluginType.POST_BREACH_ACTION,
⬜ 278            )
⬜ 279            puppet.load_plugin(
🟩 280                "HiddenFiles", HiddenFiles(self._telemetry_messenger), PluginType.POST_BREACH_ACTION
⬜ 281            )
⬜ 282            puppet.load_plugin(
⬜ 283                "TrapCommand",
```

<br/>

4\. We modify  [[sym:./monkey/monkey_island/cc/services/config_schema/definitions/post_breach_actions.py({"type":"path","text":"monkey/monkey_island/cc/services/config_schema/definitions/post_breach_actions.py","path":"monkey/monkey_island/cc/services/config_schema/definitions/post_breach_actions.py"})]], like so:
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 monkey/monkey_island/cc/services/config_schema/definitions/post_breach_actions.py
```python
⬜ 27             },
⬜ 28             {
⬜ 29                 "type": "string",
🟩 30                 "enum": ["HiddenFiles"],
⬜ 31                 "title": "Hidden Files and Directories",
⬜ 32                 "safe": True,
⬜ 33                 "info": "Attempts to create a hidden file and remove it afterward.",
```

<br/>

5\. Update [[sym:./monkey/monkey_island/cc/services/config_schema/monkey.py({"type":"path","text":"monkey/monkey_island/cc/services/config_schema/monkey.py","path":"monkey/monkey_island/cc/services/config_schema/monkey.py"})]], as seen here:
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 monkey/monkey_island/cc/services/config_schema/monkey.py
```python
⬜ 62                         "default": [
⬜ 63                             "CommunicateAsBackdoorUser",
⬜ 64                             "ModifyShellStartupFiles",
🟩 65                             "HiddenFiles",
⬜ 66                             "TrapCommand",
⬜ 67                             "ChangeSetuidSetgid",
⬜ 68                             "ScheduleJobs",
```

<br/>

## Optionally, these snippets may be helpful

<br/>

Update [[sym:./vulture_allowlist.py({"type":"path","text":"vulture_allowlist.py","path":"vulture_allowlist.py"})]]
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 vulture_allowlist.py
```python
⬜ 84     MySQLFinger  # unused class (monkey/infection_monkey/network/mysqlfinger.py:13)
⬜ 85     SSHFinger  # unused class (monkey/infection_monkey/network/sshfinger.py:15)
⬜ 86     ClearCommandHistory  # unused class (monkey/infection_monkey/post_breach/actions/clear_command_history.py:11)
🟩 87     AccountDiscovery  # unused class (monkey/infection_monkey/post_breach/actions/discover_accounts.py:8)
⬜ 88     ModifyShellStartupFiles  # unused class (monkey/infection_monkey/post_breach/actions/modify_shell_startup_files.py:11)
⬜ 89     Timestomping  # unused class (monkey/infection_monkey/post_breach/actions/timestomping.py:6)
⬜ 90     SignedScriptProxyExecution  # unused class (monkey/infection_monkey/post_breach/actions/use_signed_scripts.py:15)
```

<br/>

<!-- THIS IS AN AUTOGENERATED SECTION. DO NOT EDIT THIS SECTION DIRECTLY -->
### Swimm Note

<span id="f-dQOwA">__init__</span>[^](#dQOwA) - "monkey/infection_monkey/post_breach/actions/hide_files.py" L23
```python
    def __init__(self, telemetry_messenger: ITelemetryMessenger):
```

<span id="f-ZzyhBz">AccountDiscovery</span>[^](#ZzyhBz) - "monkey/infection_monkey/post_breach/actions/discover_accounts.py" L9
```python
class AccountDiscovery(PBA):
```

<span id="f-1T4FcD">CommunicateAsBackdoorUser</span>[^](#1T4FcD) - "monkey/infection_monkey/post_breach/actions/communicate_as_backdoor_user.py" L30
```python
class CommunicateAsBackdoorUser(PBA):
```

<span id="f-Cb2a9">CustomPBA</span>[^](#Cb2a9) - "monkey/infection_monkey/post_breach/custom_pba/custom_pba.py" L23
```python
class CustomPBA(PBA):
```

<span id="f-Z2aIscA">HiddenFiles</span>[^](#Z2aIscA) - "monkey/infection_monkey/post_breach/actions/hide_files.py" L18
```python
class HiddenFiles(PBA):
```

<span id="f-1yTwmK">PBA</span>[^](#1yTwmK) - "monkey/infection_monkey/post_breach/pba.py" L15
```python
class PBA:
```

<span id="f-Z1Hvwio">Timestomping</span>[^](#Z1Hvwio) - "monkey/infection_monkey/post_breach/actions/timestomping.py" L7
```python
class Timestomping(PBA):
```

<br/>

This file was generated by Swimm. [Click here to view it in the app](http://localhost:5000/repos/Z2l0aHViJTNBJTNBbW9ua2V5MiUzQSUzQXNhYXItc3dpbW0=/docs/jqcek).