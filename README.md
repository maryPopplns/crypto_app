# Crypto tracking app

Application to view crytpo news and track potential gains/losses.

## Tech Stack

**API:** Flask, PostgreSQL, JWT for auth.

<br>

## Environment Variables

| Variable     | Description |
| :----------- | :---------- |
| `PULSE_HOST` | api url     |

| Variable    | Description |
| :---------- | :---------- |
| `PULSE_KEY` | api key     |

| Variable        | Description |
| :-------------- | :---------- |
| `MINEABLE_HOST` | api url     |

| Variable       | Description |
| :------------- | :---------- |
| `MINEABLE_KEY` | api key     |

| Variable       | Description  |
| :------------- | :----------- |
| `DATABASE_URL` | database url |

| Variable     | Description    |
| :----------- | :------------- |
| `SECRET_KEY` | jwt secret key |

<br>

## API Reference

<br>

#### add coin to user

```http
  PUT /addcoin
```

#### remove coin from user

```http
  PUT /removecoin
```

#### get user coins

```http
  GET /usercoins
```

#### register user

```http
  POST /register
```

#### user login

```http
  POST /login
```

#### news headlines

```http
  GET /headlines
```

#### get top coins

```http
  GET /topcoins
```

#### get coin

```http
  GET /coin
```
