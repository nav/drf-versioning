# API Versioning with Django Rest Framework

Demo of API Versioning with Django Rest Framework

## Diagram

```sh
                                        ┌────────────────────────────┐
                                        │   Versioning Middleware    │
┌────────────────────────────────┐      │                            │
│ GET /api/products              │      │  ┌────────────────────┐    │
│ X-API-Version: v1              │      │  │  Transformations   ├─┐  │
│                                │      │  │                    │ │  │
│            --- or ---          │      │  │ ┌────────────────┐ │ │  │   ┌─────────────────────┐
│                                │      │  │ │  Request Body  │ │ │  │   │   Request Handler   │
│ POST /api/products             │──────┼──┼▶│ Transformation │─┼─┼──┼──▶│ Current Version: v2 │
│ X-API-Version: v1              │      │  │ └────────────────┘ │ │  │   └─────────────────────┘
│ Content-Type: application/json │      │  │                    │ │  │              │
│                                │◀────┐│  │ ┌────────────────┐ │ │  │              │
│ {"sku": "some name"}           │     ││  │ │ Response Body  │ │ │  │              │
└────────────────────────────────┘     └┼──┼─│ Transformation │◀┼─┼──┼──────────────┘
                                        │  │ └────────────────┘ │ │  │
                                        │  │                    │ │  │
                                        │  └─┬──────────────────┘ │  │
                                        │    └────────────────────┘  │
                                        │                            │
                                        └────────────────────────────┘
```
