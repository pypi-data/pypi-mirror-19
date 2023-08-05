Solve
=====

Challenge Solving Utilities

This module uses Agents to solve Challenges. Both are modular and any number of
them can be added. A Solver works by running every loaded Challenge and checking
if it returned any data. If it did, then every Solver is ran from least cost to
greatest until a result is found or a RuntimeError is raised indicating that the
Challenge could not be solved. Because of the way the Solver works, it is
imperative that every Challenge and Agent operate according to their
specifications. See the unit tests for this module for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### Solver(object)

Solves challenges in a Browser

**Args:**

|  Name   |  Type   |      Description       |
|---------|---------|------------------------|
| browser | Browser | The web browser to use |

**Raises:**

|   Name    |            Description             |
|-----------|------------------------------------|
| TypeError | The browser is not of type Browser |

#### solve(self)

Solves a Challenge

**Returns:**

|  Type  |       Description       |
|--------|-------------------------|
| String | The ID of the Challenge |

**Raises:**

|     Name     |            Description            |
|--------------|-----------------------------------|
| RuntimeError | The Challenge could not be solved |

#### add_challenge(self, challenge)

Adds a Challenge to the list of challenge types

**Args:**

|   Name    |   Type    |     Description      |
|-----------|-----------|----------------------|
| challenge | Challenge | The Challenge to add |

**Raises:**

|   Name    |              Description               |
|-----------|----------------------------------------|
| TypeError | The challenge is not of type Challenge |

#### add_agent(self, agent)

Adds an Agent to the list of available solving agents

**Args:**

| Name  | Type  |   Description    |
|-------|-------|------------------|
| agent | Agent | The Agent to add |

**Raises:**

|   Name    |          Description           |
|-----------|--------------------------------|
| TypeError | The agent is not of type Agent |

#### set_success(self, id)

Sets a Challenge as successful and handles it appropriately before
removing it from the list

**Args:**

| Name |  Type  |       Description       |
|------|--------|-------------------------|
| id   | String | The ID of the Challenge |

**Raises:**

|   Name   |     Description      |
|----------|----------------------|
| KeyError | The ID was not found |

#### set_fail(self, id)

Sets a Challenge as failed and handles it appropriately before removing
it from the list

**Args:**

| Name |  Type  |       Description       |
|------|--------|-------------------------|
| id   | String | The ID of the Challenge |

**Raises:**

|   Name   |     Description      |
|----------|----------------------|
| KeyError | The ID was not found |
