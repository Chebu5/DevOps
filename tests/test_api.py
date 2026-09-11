import pytest


def test_create_user(client):
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@test.com",
        "full_name": "Test User",
        "age": 25
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_get_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_product(client):
    response = client.post("/products/", json={
        "name": "Laptop",
        "description": "Gaming Laptop",
        "price": 999.99,
        "stock": 10,
        "category": "Electronics"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"


def test_get_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_order(client):
    user = client.post("/users/", json={
        "username": "orderuser",
        "email": "order@test.com",
        "full_name": "Order User",
        "age": 30
    }).json()

    product = client.post("/products/", json={
        "name": "Phone",
        "description": "Smartphone",
        "price": 499.99,
        "stock": 5,
        "category": "Electronics"
    }).json()

    response = client.post("/orders/", json={
        "user_id": user["id"],
        "product_id": product["id"],
        "quantity": 2
    })
    assert response.status_code == 200
    assert response.json()["quantity"] == 2


def test_update_user(client):
    user = client.post("/users/", json={
        "username": "updateuser",
        "email": "update@test.com",
        "full_name": "Update User",
        "age": 28
    }).json()

    response = client.put(f"/users/{user['id']}", json={
        "full_name": "Updated Name",
        "age": 29
    })
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"


def test_delete_user(client):
    user = client.post("/users/", json={
        "username": "deleteuser",
        "email": "delete@test.com",
        "full_name": "Delete User",
        "age": 22
    }).json()

    response = client.delete(f"/users/{user['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"