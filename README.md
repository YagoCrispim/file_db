# FileDB

## About

- FileDB is an extension of the <a target="_blank" href="https://github.com/igoiglesias/chaozzDBPy">ChaozzDBPy implementation</a>.

- FileDB is a database that stores data into text files.

- The main pourpose of this project is to implement a noSQL DB with a simplified SQL syntax.

## Setup

- ### Create the virtualenv

  ```bash
  virtualenv -p 3.8 .venv
  ```

- ### Activate the virtualenv

  ```bash
  source .venv/bin/activate
  ```

- ### Install requirements

  ```bash
  pip install -r requirements.txt
  ```

## Usage

- ### INSERT

  ```python
      from FileDB import run

      run("insert into users (name, age, grade) values ('John Doe','35','5'), ('Foo Bar','40','10')")
  ```

- ### SELECT

  ```python
      from FileDB import run

      users = run("select * from users")
  ```

- ### UPDATE

  ```python
    from FileDB import run

    run("update users set name = 'John Foo' where id = 1")
  ```

- ### DELETE

  ```python
    from FileDB import run

    run("delete from users where id = 1")
  ```
