// MongoDB initialization script
db = db.getSiblingDB('scaffold_forge');

// Create collections
db.createCollection('status_checks');
db.createCollection('projects');

// Create indexes for better performance
db.status_checks.createIndex({ "timestamp": 1 });
db.status_checks.createIndex({ "client_name": 1 });
db.projects.createIndex({ "github_username": 1 });
db.projects.createIndex({ "created_at": 1 });
db.projects.createIndex({ "language": 1 });

// Insert sample data (optional)
db.status_checks.insertOne({
  client_name: "docker-init",
  timestamp: new Date(),
  id: "init-" + new Date().getTime()
});

print("✅ MongoDB initialized successfully for Scaffold Forge");
print("📊 Collections created: status_checks, projects");
print("🔍 Indexes created for better performance");
