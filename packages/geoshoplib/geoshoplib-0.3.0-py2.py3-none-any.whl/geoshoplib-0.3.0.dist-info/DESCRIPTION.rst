geoshoplib
===============================

Small library which provides api to contact to geoshop.

For reading all products:

- create a base_service
- create a user_service with user/password and base_service as service parameter
- read the products => get_products()

For reading a specific product definition:

- create a base_service
- create a product with a known product_id, user/password and base_service as parameter
- read the definition => get_definition()

Have fun!

0.2.0
---

- Use geoshop id for error handling now.


0.2.0
---

- Fix bug when fields are not set in geoshop, now it is printed out to the console but the lib keeps running


0.1.0
---

- Initial version.
- implements first views for connection data sets


