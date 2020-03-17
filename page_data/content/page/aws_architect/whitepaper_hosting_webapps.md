# Web Application Hosting in the AWS Cloud

[Official documentation](https://d0.awsstatic.com/whitepapers/aws-web-hosting-best-practices.pdf)  

[Back to main page](/page/aws_architect)

## An AWS Cloud Architecture for Web Hosting

The following figure provides another look at that classic web application architecture and how it can leverage the AWS Cloud computing infrastructure.

![An example of a web hosting architecture on AWS](/images/architect-web-apps-architecture.png)

1. Load Balancing with Elastic Load Balancing (ELB)/Application Load Balancer (ALB) – Allows you to spread load across multiple Availability Zones and Amazon EC2 Auto Scaling groups for redundancy and decoupling of services.
2. Firewalls with Security Groups –Moves security to the instance to provide a stateful, host-level firewall for both web and application servers.
3. Caching with Amazon ElastiCache – Provides caching services with Redis or Memcached to remove load from the app and database, and lower latency for frequent requests.
4. Managed Database with Amazon RDS – Creates a highly available, Multi-AZ database architecture with six possible DB engines.
5. DNS Services with Amazon Route 53 – Provides DNS services to simplify domain management.
6. Edge Caching with Amazon CloudFront – Edge caches high-volume content to decrease the latency to customers.
7. Edge Security for Amazon CloudFront with AWS WAF – Filters malicious traffic, including XSS and SQL injection via customer-defined rules.
8. DDoS Protection with AWS Shield – Safeguards your infrastructure against the most common network and transport layer DDoS attacks automatically.
9. Static Storage and Backups with Amazon S3 – Enables simple HTTP-based object storage for backups and static assets like images and video.

[Back to main page](/page/aws_architect)