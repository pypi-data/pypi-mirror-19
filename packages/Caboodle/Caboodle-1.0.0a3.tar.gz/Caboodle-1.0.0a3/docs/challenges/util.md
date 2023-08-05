Util
====

Utility Functions for Challenges

This module defines useful and frequently used functions for use in Challenges.
Import this module to use them.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Functions:**
--------------

#### get_element_image(element, browser)

Takes a screenshot and crops out the element

**Args:**

|  Name   |    Type    |      Description       |
|---------|------------|------------------------|
| element | WebElement | The element to crop    |
| browser | Browser    | The web browser to use |

**Returns:**

| Type  |         Description         |
|-------|-----------------------------|
| Bytes | A base64 encoded JPEG image |

#### get_image_src(element)

Downloads the source of an image

**Args:**

|  Name   |    Type    |       Description       |
|---------|------------|-------------------------|
| element | WebElement | The element to download |

**Returns:**

| Type  |      Description       |
|-------|------------------------|
| Bytes | A base64 encoded image |
