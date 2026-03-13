#!/bin/bash
# Setup PostgreSQL for the Real Estate application

echo "🐘 Setting up PostgreSQL..."

# Create postgres user
psql postgres -c "CREATE USER postgres WITH SUPERUSER CREATEDB PASSWORD 'password';" 2>&1 || echo "User may already exist"

# Create database
psql postgres -c "CREATE DATABASE real_estate_db OWNER postgres;" 2>&1 || echo "Database may already exist"

echo "✅ PostgreSQL setup complete!"
echo ""
echo "Database: real_estate_db"
echo "User: postgres"
echo "Password: password"
echo "Host: localhost:5432"
