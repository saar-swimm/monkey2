---
id: uwdpa
name: Creating a Telem
file_version: 1.0.2
app_version: 0.8.6-0
file_blobs:
  monkey/infection_monkey/monkey.py: e31c62cadad86a0c124b7623a61079994790ab3e
  monkey/infection_monkey/telemetry/state_telem.py: 98aec3166688be7b8a8b6530144c46001f7691d2
  monkey/infection_monkey/telemetry/i_telem.py: faaa0a65e40219e55b24b5dbf8df3126723425bb
  monkey/infection_monkey/telemetry/base_telem.py: 2f8f68892afcb6692f6a31953ed42382b369ded0
  monkey/infection_monkey/telemetry/attack/t1105_telem.py: a3745a59f3e57b5f235db491f0c353a516985001
  monkey/infection_monkey/telemetry/credentials_telem.py: 4f5c43aa4b62c74354bb0423f8eb00eb17f02144
  monkey/infection_monkey/telemetry/exploit_telem.py: 62f5d728fb37ad4fc05c8b2b2bbb0c8048ad0d4f
  monkey/infection_monkey/telemetry/attack/t1107_telem.py: c3667289bb07c4757e10f839b729e63cf20b449c
  monkey/infection_monkey/telemetry/attack/attack_telem.py: cbb158bf4ca2e1d6c07ef8deac9416b12746b7a8
---

In this document, we will learn how to add a new Telem to the system.

A Telem is a{Explain what a Telem is and its role in the system}

When we create a new Telem, we create a class that inherits from `ITelem`[<sup id="ZSfQXe">↓</sup>](#f-ZSfQXe).

Some examples of `ITelem`[<sup id="ZSfQXe">↓</sup>](#f-ZSfQXe)s are `T1105Telem`[<sup id="25k0nX">↓</sup>](#f-25k0nX), `CredentialsTelem`[<sup id="1xNgsU">↓</sup>](#f-1xNgsU), `ExploitTelem`[<sup id="Z1cpAlO">↓</sup>](#f-Z1cpAlO), and `T1107Telem`[<sup id="2k7H5A">↓</sup>](#f-2k7H5A). Note: some of these examples inherit indirectly from `ITelem`[<sup id="ZSfQXe">↓</sup>](#f-ZSfQXe).

<br/>

## Inherit from `BaseTelem`[<sup id="Z1J6DnY">↓</sup>](#f-Z1J6DnY) or `AttackTelem`[<sup id="2llVd6">↓</sup>](#f-2llVd6)? 🤔


Instances of `ITelem`[<sup id="ZSfQXe">↓</sup>](#f-ZSfQXe) usually don't inherit from it directly. Rather, they inherit from `AttackTelem`[<sup id="2llVd6">↓</sup>](#f-2llVd6) when {When to inherit from AttackTelem?} or from `BaseTelem`[<sup id="Z1J6DnY">↓</sup>](#f-Z1J6DnY) when {When to inherit from BaseTelem?}.

In this document we demonstrate inheriting from `BaseTelem`[<sup id="Z1J6DnY">↓</sup>](#f-Z1J6DnY) as it is more common.

<br/>

## TL;DR - How to Add a `BaseTelem`[<sup id="Z1J6DnY">↓</sup>](#f-Z1J6DnY)

1. Create a new class inheriting from `BaseTelem`[<sup id="Z1J6DnY">↓</sup>](#f-Z1J6DnY)&nbsp;
   - Place the file under [[sym:./monkey/infection_monkey/telemetry({"type":"path","text":"monkey/infection_monkey/telemetry","path":"monkey/infection_monkey/telemetry"})]],
     e.g. `StateTelem`[<sup id="Z2s980C">↓</sup>](#f-Z2s980C) is defined in [[sym:./monkey/infection_monkey/telemetry/state_telem.py({"type":"path","text":"monkey/infection_monkey/telemetry/state_telem.py","path":"monkey/infection_monkey/telemetry/state_telem.py"})]].
2. Define `telem_category`[<sup id="EnaHS">↓</sup>](#f-EnaHS).
2. Implement `__init__`[<sup id="Z4Xy50">↓</sup>](#f-Z4Xy50) and `get_data`[<sup id="Z1q3POg">↓</sup>](#f-Z1q3POg).
4. **Profit** 💰

<br/>

## Example Walkthrough - `StateTelem`[<sup id="Z2s980C">↓</sup>](#f-Z2s980C)
We'll follow the implementation of `StateTelem`[<sup id="Z2s980C">↓</sup>](#f-Z2s980C) for this example.

A `StateTelem`[<sup id="Z2s980C">↓</sup>](#f-Z2s980C) is {Explain what StateTelem is and how it works with the Telem interface}

<br/>

### `StateTelem`[<sup id="Z2s980C">↓</sup>](#f-Z2s980C) Usage Example
For example, this is how `StateTelem`[<sup id="Z2s980C">↓</sup>](#f-Z2s980C) can be used:
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 monkey/infection_monkey/monkey.py
```python
⬜ 173            if self._monkey_inbound_tunnel and self._propagation_enabled():
⬜ 174                self._monkey_inbound_tunnel.start()
⬜ 175    
🟩 176            StateTelem(is_done=False, version=get_version()).send()
⬜ 177            TunnelTelem().send()
⬜ 178    
⬜ 179            self._build_master()
```

<br/>

## Steps to Adding a new `BaseTelem`[<sup id="Z1J6DnY">↓</sup>](#f-Z1J6DnY)

<br/>

### 1\. Inherit from `BaseTelem`[<sup id="Z1J6DnY">↓</sup>](#f-Z1J6DnY).
All `BaseTelem`[<sup id="Z1J6DnY">↓</sup>](#f-Z1J6DnY)s are defined in files under [[sym:./monkey/infection_monkey/telemetry({"type":"path","text":"monkey/infection_monkey/telemetry","path":"monkey/infection_monkey/telemetry"})]].

<br/>

We first need to define our class in the relevant file, and inherit from `BaseTelem`[<sup id="Z1J6DnY">↓</sup>](#f-Z1J6DnY):
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 monkey/infection_monkey/telemetry/state_telem.py
```python
⬜ 2      from infection_monkey.telemetry.base_telem import BaseTelem
⬜ 3      
⬜ 4      
🟩 5      class StateTelem(BaseTelem):
⬜ 6          def __init__(self, is_done, version="Unknown"):
⬜ 7              """
⬜ 8              Default state telemetry constructor
```

<br/>

### 2\. Define `telem_category`[<sup id="EnaHS">↓</sup>](#f-EnaHS)
Every `ITelem`[<sup id="ZSfQXe">↓</sup>](#f-ZSfQXe) should define this variable:
- `telem_category`[<sup id="EnaHS">↓</sup>](#f-EnaHS): {Explain what the value should be}

<br/>


<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 monkey/infection_monkey/telemetry/state_telem.py
```python
⬜ 12             self.is_done = is_done
⬜ 13             self.version = version
⬜ 14     
🟩 15         telem_category = TelemCategoryEnum.STATE
⬜ 16     
⬜ 17         def get_data(self):
⬜ 18             return {"done": self.is_done, "version": self.version}
```

<br/>

### 3\. Implement `__init__`[<sup id="Z4Xy50">↓</sup>](#f-Z4Xy50) and `get_data`[<sup id="Z1q3POg">↓</sup>](#f-Z1q3POg)

<br/>

Implement `__init__`[<sup id="Z4Xy50">↓</sup>](#f-Z4Xy50).

<br/>

This is how we implemented it for `StateTelem`[<sup id="Z2s980C">↓</sup>](#f-Z2s980C) {Explain what's happening in this implementation}
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 monkey/infection_monkey/telemetry/state_telem.py
```python
⬜ 3      
⬜ 4      
⬜ 5      class StateTelem(BaseTelem):
🟩 6          def __init__(self, is_done, version="Unknown"):
🟩 7              """
🟩 8              Default state telemetry constructor
🟩 9              :param is_done: Whether the state of monkey is done.
🟩 10             """
🟩 11             super(StateTelem, self).__init__()
🟩 12             self.is_done = is_done
🟩 13             self.version = version
⬜ 14     
⬜ 15         telem_category = TelemCategoryEnum.STATE
⬜ 16     
```

<br/>

The goal of `get_data`[<sup id="Z1q3POg">↓</sup>](#f-Z1q3POg) is to {Explain get_data's role}.

<br/>

This is how we implemented it for `StateTelem`[<sup id="Z2s980C">↓</sup>](#f-Z2s980C) {Explain what's happening in this implementation}
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 monkey/infection_monkey/telemetry/state_telem.py
```python
⬜ 14     
⬜ 15         telem_category = TelemCategoryEnum.STATE
⬜ 16     
🟩 17         def get_data(self):
🟩 18             return {"done": self.is_done, "version": self.version}
⬜ 19     
```

<br/>

<!-- THIS IS AN AUTOGENERATED SECTION. DO NOT EDIT THIS SECTION DIRECTLY -->
### Swimm Note

<span id="f-Z4Xy50">__init__</span>[^](#Z4Xy50) - "monkey/infection_monkey/telemetry/state_telem.py" L6
```python
    def __init__(self, is_done, version="Unknown"):
```

<span id="f-2llVd6">AttackTelem</span>[^](#2llVd6) - "monkey/infection_monkey/telemetry/attack/attack_telem.py" L5
```python
class AttackTelem(BaseTelem):
```

<span id="f-Z1J6DnY">BaseTelem</span>[^](#Z1J6DnY) - "monkey/infection_monkey/telemetry/base_telem.py" L26
```python
class BaseTelem(ITelem, metaclass=abc.ABCMeta):
```

<span id="f-1xNgsU">CredentialsTelem</span>[^](#1xNgsU) - "monkey/infection_monkey/telemetry/credentials_telem.py" L10
```python
class CredentialsTelem(BaseTelem):
```

<span id="f-Z1cpAlO">ExploitTelem</span>[^](#Z1cpAlO) - "monkey/infection_monkey/telemetry/exploit_telem.py" L9
```python
class ExploitTelem(BaseTelem):
```

<span id="f-Z1q3POg">get_data</span>[^](#Z1q3POg) - "monkey/infection_monkey/telemetry/state_telem.py" L17
```python
    def get_data(self):
```

<span id="f-ZSfQXe">ITelem</span>[^](#ZSfQXe) - "monkey/infection_monkey/telemetry/i_telem.py" L4
```python
class ITelem(metaclass=abc.ABCMeta):
```

<span id="f-Z2s980C">StateTelem</span>[^](#Z2s980C) - "monkey/infection_monkey/telemetry/state_telem.py" L5
```python
class StateTelem(BaseTelem):
```

<span id="f-25k0nX">T1105Telem</span>[^](#25k0nX) - "monkey/infection_monkey/telemetry/attack/t1105_telem.py" L8
```python
class T1105Telem(AttackTelem):
```

<span id="f-2k7H5A">T1107Telem</span>[^](#2k7H5A) - "monkey/infection_monkey/telemetry/attack/t1107_telem.py" L4
```python
class T1107Telem(AttackTelem):
```

<span id="f-EnaHS">telem_category</span>[^](#EnaHS) - "monkey/infection_monkey/telemetry/state_telem.py" L15
```python
    telem_category = TelemCategoryEnum.STATE
```

<br/>

This file was generated by Swimm. [Click here to view it in the app](http://localhost:5000/repos/Z2l0aHViJTNBJTNBbW9ua2V5MiUzQSUzQXNhYXItc3dpbW0=/docs/uwdpa).