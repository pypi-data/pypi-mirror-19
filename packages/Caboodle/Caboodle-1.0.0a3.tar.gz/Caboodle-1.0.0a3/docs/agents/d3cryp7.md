d3cryp7
=======

d3cryp7 Challenge solving Agents

This module is an implementation of the Agent specification and solves a
Challenge using API calls to a d3cryp7 server. To use this Agent, create a new
instance of it and call the `solve()` function. See the unit tests for this
module for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### d3cryp7TextImageAgent(Agent)

An Agent to solve image based Challenges containing text using d3cryp7

**Args:**

|   Name   |  Type  |          Description          |
|----------|--------|-------------------------------|
| url      | String | The URL of the d3cryp7 API    |
| currency | String | The currency to calculate for |

The currency must be a three letter code like USD or EUR.

You must run a d3cryp7 server in order to use this Agent. You can find
instructions to do so here:

https://bitbucket.org/bkvaluemeal/d3cryp7.py

#### solve(self, data)

Solves a Challenge and stores the result

**Args:**

| Name |    Type    |      Description       |
|------|------------|------------------------|
| data | Dictionary | The Challenge to solve |

**Raises:**

|   Name    |            Description            |
|-----------|-----------------------------------|
| TypeError | The Challenge is not a dictionary |

#### get_cost(self)

Returns the cost of using this Agent

**Returns:**

| Type  |             Description             |
|-------|-------------------------------------|
| Float | The cost as a floating point number |

#### success(self, data)

Performs actions for a successful Challenge

**Args:**

| Name |    Type    |       Description        |
|------|------------|--------------------------|
| data | Dictionary | The successful Challenge |

#### fail(self, data)

Performs actions for a failed Challenge

**Args:**

| Name |    Type    |     Description      |
|------|------------|----------------------|
| data | Dictionary | The failed Challenge |


### d3cryp7TagImageGridAgent(Agent)

An Agent to solve image grid based Challenges using d3cryp7

**Args:**

|   Name   |  Type  |          Description          |
|----------|--------|-------------------------------|
| url      | String | The URL of the d3cryp7 API    |
| currency | String | The currency to calculate for |

The currency must be a three letter code like USD or EUR.

You must run a d3cryp7 server in order to use this Agent. You can find
instructions to do so here:

https://bitbucket.org/bkvaluemeal/d3cryp7.py

#### solve(self, data)

Solves a Challenge and stores the result

**Args:**

| Name |    Type    |      Description       |
|------|------------|------------------------|
| data | Dictionary | The Challenge to solve |

**Raises:**

|   Name    |            Description            |
|-----------|-----------------------------------|
| TypeError | The Challenge is not a dictionary |

#### get_cost(self)

Returns the cost of using this Agent

**Returns:**

| Type  |             Description             |
|-------|-------------------------------------|
| Float | The cost as a floating point number |

#### success(self, data)

Performs actions for a successful Challenge

**Args:**

| Name |    Type    |       Description        |
|------|------------|--------------------------|
| data | Dictionary | The successful Challenge |

#### fail(self, data)

Performs actions for a failed Challenge

**Args:**

| Name |    Type    |     Description      |
|------|------------|----------------------|
| data | Dictionary | The failed Challenge |
