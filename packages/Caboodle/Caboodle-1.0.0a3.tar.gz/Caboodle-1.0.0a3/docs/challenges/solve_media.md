Solve Media
===========

Solve Media CAPTCHA Challenges

This module is an implementation of the Challenge specification and collects
data to solve Solve Media CAPTCHAs. To use these Challenges, create a new
instance of them and call the `get_data()` function. Then, process the data
using an Agent and submit it by calling the `submit_data()` function. See the
unit tests for this module for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### SolveMediaTextChallenge(Challenge)

A Challenge for Solve Media Text CAPTCHAs

A text CAPTCHA is the traditional type of CAPTCHA with obfuscated squiggly
text. This Challenge will locate it if it exists and add a base64 encoded
image of the CAPTCHA to the dictionary with the key 'image'. In addition to
the CAPTCHA, the form to enter the result and the reload button to get a new
CAPTCHA are added to the dictionary with the keys 'form' and 'reload'
respectively.

#### get_data(self, browser)

Collects data needed to solve the Challenge

**Args:**

|  Name   |  Type   |      Description       |
|---------|---------|------------------------|
| browser | Browser | The web browser to use |

**Returns:**

|    Type    |          Description           |
|------------|--------------------------------|
| Dictionary | A dictionary of collected data |

**Raises:**

|   Name    |            Description             |
|-----------|------------------------------------|
| TypeError | The browser is not of type Browser |

#### submit_data(self, data)

Submits the processed data and solves the Challenge

**Args:**

| Name |    Type    |       Description       |
|------|------------|-------------------------|
| data | Dictionary | The Challenge to submit |

**Raises:**

|   Name    |         Description          |
|-----------|------------------------------|
| TypeError | The data is not a dictionary |
