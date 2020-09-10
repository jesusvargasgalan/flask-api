# Execution

```bash
docker-compose up
```

or if you want pdb

```bash
docker-compose run --rm --service-ports backend
```

# Init

Init the DB

```bash
docker-compose run --rm --service-ports backend poetry run python init.py
```
