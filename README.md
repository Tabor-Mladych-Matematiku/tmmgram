# tmmgram

Jednoduchý klon Instagramu pro hru na TMM 

## How to run

### Before first run

1. Install the requirements:
   ```shell
   py -m pip install -r requirements.txt
   ```
2. Rename `tmm_webinfo.example.yaml` to `tmm_webinfo.yaml` and fill in the details (for debugging using a local SQLite database, remove
   the `db` section).
Prepare the database:
    ```shell
    py create_db.py
    ```

### Run

```shell
py -m flask run 
```
