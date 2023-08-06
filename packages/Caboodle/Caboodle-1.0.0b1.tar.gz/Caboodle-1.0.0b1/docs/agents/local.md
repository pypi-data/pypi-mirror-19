Local
=====

A local Challenge solving Agent

This module is an implementation of the Agent specification and solves a
Challenge using the `input()` function. To use this Agent, create a new instance
of it and call the `solve()` function. See the unit tests for this module for
more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### LocalAgent(Agent)

An Agent to solve Challenges with input from the user

This Agent uses the `input()` function and thus will block the execution of
your application until it receives input. The result is appended to the
dictionary with the key 'result' as per the guidelines. Because this Agent
relies on user input, it has a cost of zero.

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
