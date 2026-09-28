# Selenium Capstone - automationexercise.com

## Folder structure
```
selenium_capstone/
  tests/test_shopping.py     -> all test functions
  utils/helpers.py           -> small helper functions
  testdata/testdata.json     -> test data (dummy)
  screenshots/               -> screenshots come here
  reports/report.html        -> report comes here
  conftest.py                -> browser setup + report code
  create_account.py         -> run once to make the account
  pytest.ini
  requirements.txt
```

## How to run
1. Install Google Chrome and Python.
2. `pip install -r requirements.txt`
3. `python create_account.py`   (only first time)
4. `pytest`
5. Open `reports/report.html`

## Notes
- Ads are blocked when browser starts, and removed again by `remove_ads()` if they still show up.
- Clicks are done with JavaScript so ads cannot block them.
- The cart page of this website has no quantity box, so "update quantity" = remove item and add it again with new quantity from product page.
- Change data in `testdata/testdata.json` (search word, quantity etc).
