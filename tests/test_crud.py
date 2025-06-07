from uuid import uuid4


class TestClientCRUD:
    """Test Client CRUD operations"""

    def test_create_client(self, client):
        response = client.post("/clients", json={"name": "Test Client"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Client"
        assert "id" in data

    def test_create_client_duplicate_name(self, client):
        # Create first client
        client.post("/clients", json={"name": "Duplicate Client"})
        # Try to create second client with same name - should fail due to unique constraint
        response = client.post("/clients", json={"name": "Duplicate Client"})
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_get_clients_empty(self, client):
        response = client.get("/clients")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_clients(self, client):
        # Create some clients
        client.post("/clients", json={"name": "Client 1"})
        client.post("/clients", json={"name": "Client 2"})

        response = client.get("/clients")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(c["name"] == "Client 1" for c in data)
        assert any(c["name"] == "Client 2" for c in data)

    def test_get_client_by_id(self, client):
        # Create a client
        create_response = client.post("/clients", json={"name": "Test Client"})
        client_id = create_response.json()["id"]

        # Get the client by ID
        response = client.get(f"/clients/{client_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Client"
        assert data["id"] == client_id

    def test_get_client_not_found(self, client):
        response = client.get(f"/clients/{uuid4()}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Client not found"

    def test_update_client(self, client):
        # Create a client
        create_response = client.post("/clients", json={"name": "Original Name"})
        client_id = create_response.json()["id"]

        # Update the client
        response = client.put(f"/clients/{client_id}", json={"name": "Updated Name"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["id"] == client_id

    def test_update_client_not_found(self, client):
        response = client.put(f"/clients/{uuid4()}", json={"name": "Updated Name"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Client not found"

    def test_delete_client(self, client):
        # Create a client
        create_response = client.post("/clients", json={"name": "To Delete"})
        client_id = create_response.json()["id"]

        # Delete the client
        response = client.delete(f"/clients/{client_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Client deleted successfully"

        # Verify client is deleted
        get_response = client.get(f"/clients/{client_id}")
        assert get_response.status_code == 404

    def test_delete_client_not_found(self, client):
        response = client.delete(f"/clients/{uuid4()}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Client not found"


class TestNetworkCRUD:
    """Test Network CRUD operations"""

    def test_create_network(self, client):
        response = client.post("/networks", json={"ipv4": "192.168.1.0/24"})
        assert response.status_code == 200
        data = response.json()
        assert data["ipv4"] == "192.168.1.0/24"
        assert "id" in data

    def test_create_network_no_ipv4(self, client):
        response = client.post("/networks", json={})
        assert response.status_code == 200
        data = response.json()
        assert data["ipv4"] is None
        assert "id" in data

    def test_create_network_duplicate_ipv4(self, client):
        # Create first network
        client.post("/networks", json={"ipv4": "192.168.1.0/24"})
        # Try to create second network with same ipv4 - should fail due to unique constraint
        response = client.post("/networks", json={"ipv4": "192.168.1.0/24"})
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_get_networks_empty(self, client):
        response = client.get("/networks")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_networks(self, client):
        # Create some networks
        client.post("/networks", json={"ipv4": "192.168.1.0/24"})
        client.post("/networks", json={"ipv4": "10.0.0.0/8"})

        response = client.get("/networks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(n["ipv4"] == "192.168.1.0/24" for n in data)
        assert any(n["ipv4"] == "10.0.0.0/8" for n in data)

    def test_get_network_by_id(self, client):
        # Create a network
        create_response = client.post("/networks", json={"ipv4": "172.16.0.0/16"})
        network_id = create_response.json()["id"]

        # Get the network by ID
        response = client.get(f"/networks/{network_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["ipv4"] == "172.16.0.0/16"
        assert data["id"] == network_id

    def test_get_network_not_found(self, client):
        response = client.get("/networks/999999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Network not found"

    def test_update_network(self, client):
        # Create a network
        create_response = client.post("/networks", json={"ipv4": "192.168.1.0/24"})
        network_id = create_response.json()["id"]

        # Update the network
        response = client.put(f"/networks/{network_id}", json={"ipv4": "192.168.2.0/24"})
        assert response.status_code == 200
        data = response.json()
        assert data["ipv4"] == "192.168.2.0/24"
        assert data["id"] == network_id

    def test_update_network_not_found(self, client):
        response = client.put("/networks/999999", json={"ipv4": "192.168.2.0/24"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Network not found"

    def test_delete_network(self, client):
        # Create a network
        create_response = client.post("/networks", json={"ipv4": "192.168.1.0/24"})
        network_id = create_response.json()["id"]

        # Delete the network
        response = client.delete(f"/networks/{network_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Network deleted successfully"

        # Verify network is deleted
        get_response = client.get(f"/networks/{network_id}")
        assert get_response.status_code == 404

    def test_delete_network_not_found(self, client):
        response = client.delete("/networks/999999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Network not found"


class TestPagination:
    """Test pagination functionality"""

    def test_clients_pagination(self, client):
        # Create multiple clients
        for i in range(5):
            client.post("/clients", json={"name": f"Client {i}"})

        # Test with limit
        response = client.get("/clients?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

        # Test with skip
        response = client.get("/clients?skip=2&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_networks_pagination(self, client):
        # Create multiple networks
        for i in range(5):
            client.post("/networks", json={"ipv4": f"192.168.{i}.0/24"})

        # Test with limit
        response = client.get("/networks?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

        # Test with skip
        response = client.get("/networks?skip=2&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3