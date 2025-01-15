import sys
import os

# Add the 'src' folder to the Python path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from src.myapi.models import Category

def test_create_category(client):
    response = client.post('/api/categories', json={
        'name': 'Test Category',
        'description': 'Test Description',
        'slug': 'test-category',
        'icon': 'fa-test'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test Category'
    assert data['description'] == 'Test Description'

def test_get_category(client):
    category = Category(name='Test Category', description='Test Description', slug='test-category', icon='fa-test')
    db.session.add(category)
    db.session.commit()
    response = client.get(f'/api/categories/{category.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Test Category'
    assert data['description'] == 'Test Description'

def test_update_category(client):
    category = Category(name='Test Category', description='Test Description', slug='test-category', icon='fa-test')
    db.session.add(category)
    db.session.commit()
    response = client.put(f'/api/categories/{category.id}', json={
        'name': 'Updated Category',
        'description': 'Updated Description'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Category'
    assert data['description'] == 'Updated Description'

def test_delete_category(client):
    category = Category(name='Test Category', description='Test Description', slug='test-category', icon='fa-test')
    db.session.add(category)
    db.session.commit()
    response = client.delete(f'/api/categories/{category.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Category deleted successfully'