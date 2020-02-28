

#### 1. Designing highly scalable, available, and reliable cloud-native applications

1. Designing performant applications and APIs. Considerations include:

- Infrastructure as a Service vs. Container as a Service vs. Platform as a Service (e.g., autoscaling implications)
- Portability vs. platform-specific design
- Evaluating different services and technologies
- Operating system versions and base runtimes of services
- Geographic distribution of Google Cloud services
- Microservices
- Defining a key structure for high write applications using Cloud Storage, Cloud Bigtable, Cloud Spanner, or Cloud SQL
- Session management
- Deploying and securing an API with cloud endpoints
- Loosely coupled applications using asynchronous Cloud Pub/Sub events
- Health checks
- Google-recommended practices and documentation

2. Designing secure applications. Considerations include:

- Applicable regulatory requirements and legislation
- Security mechanisms that protect services and resources
- Storing and rotating secrets
- IAM roles for users/groups/service accounts
- HTTPs certificates
- Google-recommended practices and documentation

3. Managing application data. Tasks include:

- Defining database schemas for Google-managed databases (e.g., Cloud Datastore, Cloud Spanner, Cloud Bigtable, BigQuery)
- Choosing data storage options based on use case considerations, such as:
- Cloud Storage signed URLs for user-uploaded content
- Using Cloud Storage to run a static website
- Structured vs. unstructured data
- ACID transactions vs. analytics processing
- Data volume
- Frequency of data access in Cloud Storage
- Working with data ingestion systems (e.g., Cloud Pub/Sub, Storage Transfer Service)
- Following Google-recommended practices and documentation

4. Re-architecting applications from local services to Google Cloud Platform. Tasks include:

- Using managed services
- Using the strangler pattern for migration
- Google-recommended practices and documentation
