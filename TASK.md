# Template-Python-Challenge

## Mandatory requirements

- Django 2.0+
- Python 3.6+
- [petl](https://petl.readthedocs.io/en/stable/intro.html)

### Recommended

- [requests](https://requests.readthedocs.io/en/master/)

## Scope

- For the sake of simplicity everything should be running in the Django development server (no task queues or similar)
- Interface does not have to be fancy (you can use plain HTML/CSS, Bootstrap, ...)
- Keep things simple, additional comments on how your app can be further improved and
  optimized are welcome

## Objective

Build a simple app which allows you to collect, resolve and inspect information about characters in the Star Wars universe from the [SWAPI](https://swapi.co/).<br/>
The entry endpoint for data retrieval is: [https://swapi.co/api/people/](https://swapi.co/api/people/).<br/>
_If the API should be inaccessible for some reason you can host your [own version](https://github.com/phalt/swapi) of it._

### Data retrieval and storage

The user should have a way to download the latest _complete_ dataset of characters from the API by clicking on a button, the collected and transformed data should be stored as a CSV file in the file system. Metadata for downloaded datasets (e.g. filename, date, etc.) should be stored inside the database. Fetching and transformations should be implemented _efficiently_, minimize the amount of requests, your app should be able to process _large amounts of data_.

![Star Wars Explorer](https://user-images.githubusercontent.com/640755/75017565-2ec0eb00-5485-11ea-913c-0b15ba62bf48.png)

### Transformations

- Add a _date_ column (%Y-%m-%d) based on _edited_ date
- Resolve the _homeworld_ field into the homeworld's name (_/planets/1/ -> Tatooine_)
- Fields referencing different resources and date fields other than _date/birth_year_ can be dropped

## Data representation

The user should be able to inspect all previously downloaded datasets, as well as do simple exploratory operations on it.

![Data representation](https://user-images.githubusercontent.com/640755/74833466-6ad33f00-5311-11ea-8e3c-03c814dd863f.png)

### Functionality

#### Load more

By default the table should only show the first 10 rows of the dataset, by clicking on a button _“Load more”_ additionally 10 rows should be shown - reloading the page is fine.

#### Value Count

Provide the functionality to count the occurrences of values (combination of values) for columns. For example when selecting the columns _date_ and _homeworld_ the table should show the counts as follows:

| homeworld | birth_year | Count |
| --------- | ---------- | ----- |
| Tatooine  | 19BBY      | 1     |
| Tatooine  | 112BBY     | 1     |
| Naboo     | 33BBY      | 1     |
| Tatooine  | 41.9BBY    | 2     |
| Alderaan  | 19BBY      | 1     |
| ..        | ..         | ..    |

![Value Count](https://user-images.githubusercontent.com/640755/74833446-5ee77d00-5311-11ea-95d8-ce1b2bb13404.png)

#### Scope

- _“Value Count”_ does not have to support _“Load more”_
