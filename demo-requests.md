# Demo Requests

Use these sample requests after `docker compose --env-file .env.example up --build`.

You can also demo everything from the gateway UI at `http://localhost:8000`.

## 1. Register publisher

```bash
curl -X POST http://localhost:8001/api/publishers/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"publisher@example.com\",\"first_name\":\"Pub\",\"last_name\":\"Owner\",\"password\":\"12345678\",\"certificate\":\"demo-cert.pdf\"}"
```

## 2. Register customer

```bash
curl -X POST http://localhost:8001/api/users/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"customer@example.com\",\"first_name\":\"Book\",\"last_name\":\"Buyer\",\"password\":\"12345678\",\"phone\":\"0123456789\"}"
```

## 3. Create author

```bash
curl -X POST http://localhost:8001/api/authors/ \
  -H "Content-Type: application/json" \
  -d "{\"first_name\":\"Jane\",\"last_name\":\"Austen\",\"biography\":\"Classic author\",\"publisher\":1}"
```

## 4. Create category

```bash
curl -X POST http://localhost:8002/api/categories/ \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Fiction\"}"
```

## 5. Create book

```bash
curl -X POST http://localhost:8002/api/books/ \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Demo Book\",\"isbn\":\"ISBN-001\",\"description\":\"Microservice demo book\",\"price\":\"19.99\",\"language\":\"English\",\"no_of_page\":220,\"year_of_publication\":\"2024-01-01\",\"total_number_of_book\":12,\"category\":1,\"author_id\":1,\"publisher_id\":1,\"front_img\":\"https://example.com/front.jpg\",\"back_img\":\"https://example.com/back.jpg\"}"
```

## 6. Add rating

```bash
curl -X POST http://localhost:8002/api/ratings/ \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":2,\"book\":1,\"review\":\"Nice demo\",\"rate\":5}"
```

## 7. Add item to cart

```bash
curl -X POST http://localhost:8003/api/carts/2/items/ \
  -H "Content-Type: application/json" \
  -d "{\"book_id\":1,\"quantity\":2}"
```

## 8. Create order

```bash
curl -X POST http://localhost:8003/api/orders/2/create/ \
  -H "Content-Type: application/json" \
  -d "{\"country\":\"Thailand\",\"city\":\"Bangkok\",\"street\":\"Demo Street\",\"phone\":\"0999999999\",\"card_number\":\"4242424242424242\",\"provider\":\"demo-card\"}"
```

## 9. Check orders

```bash
curl http://localhost:8003/api/orders/customer/2/
curl http://localhost:8003/api/orders/publisher/1/
```
