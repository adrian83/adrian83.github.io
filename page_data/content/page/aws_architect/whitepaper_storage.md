# AWS Storage Services Overview

[Back to main page](/page/aws_architect)

## A Look at Storage Services Offered by AWS


Amazon Web Services (AWS) provides low-cost data storage with high durability
and availability. AWS offers storage choices for backup, archiving, and disaster
recovery use cases and provides block, file, and object storage. In this whitepaper,
we examine the following AWS Cloud storage services and features.  


| Type                                         | Description                                                                      |
| -------------------------------------------- | -------------------------------------------------------------------------------- |
| Amazon Simple Storage Service (Amazon S3)    | A service that provides scalable and highly durable object storage in the cloud. |
| Amazon Glacier                               | A service that provides low-cost highly durable archive storage in the cloud.    |
| Amazon Elastic File System (Amazon EFS)      | A service that provides scalable network file storage for Amazon EC2 instances.  |
| Amazon Elastic Block Store (Amazon EBS)      | A service that provides block storage volumes for Amazon EC2 instances.          |
| Amazon EC2 Instance Storage                  | Temporary block storage volumes for Amazon EC2 instances.                        |
| AWS Storage Gateway                          | An on-premises storage appliance that integrates with cloud storage.             |
| AWS Snowball                                 | A service that transports large amounts of data to and from the cloud.           |
| Amazon CloudFront                            | A service that provides a global content delivery network (CDN).                 |



### S3 (Simple Storage Service)

Amazon Simple Storage Service (Amazon S3) provides developers and IT teams secure, durable, highly scalable object storage at a very low cost.1 You can store and retrieve any amount of data, at any time, from anywhere on the web through a simple web service interface. You can write, read, and delete objects containing from zero to 5 TB of data. Amazon S3 is highly scalable, allowing concurrent read or write access to data by many separate clients or application threads. Amazon S3 offers a range of storage classes designed for different use cases including the following:

- Amazon S3 Standard, for general-purpose storage of frequently accessed data
- Amazon S3 Standard-Infrequent Access (Standard-IA), for long-lived, but less frequently accessed data
- Amazon Glacier, for low-cost archival data

##### Use Patterns

1. Amazon S3 is used to store and distribute static web content and media.
2. Amazon S3 is used to host entire static websites. Amazon S3 provides a low-cost, highly available, and highly scalable solution, including storage for static HTML files, images, videos, and client-side scripts in formats such as JavaScript.
3. Amazon S3 is used as a data store for computation and large-scale analytics, such as financial transaction analysis, clickstream analytics, and media transcoding.
4. Amazon S3 is often used as a highly durable, scalable, and secure solution for backup and archiving of critical data. 

The following table presents some storage needs for which you should consider other AWS storage options.  


| Storage Need | Solution | AWS Services      |
| ------------ | -------- | ----------------- |
| File system            | Amazon S3 uses a flat namespace and isn’t meant to serve as a standalone, POSIX-compliant file system. Instead, consider using Amazon EFS as a file system.       | [EFS](http://aws.amazon.com/efs/)       |
| Structured data with query | Amazon S3 doesn’t offer query capabilities to retrieve specific objects. When you use Amazon S3 you need to know the exact bucket name and key for the files you want to retrieve from the service. Amazon S3 can’t be used as a database or search engine by itself. Instead, you can pair Amazon S3 with Amazon DynamoDB, Amazon CloudSearch, or Amazon Relational Database Service (Amazon RDS) to index and query metadata about Amazon S3 buckets and objects. | [DynamoDB](http://aws.amazon.com/dynamodb/), [RDS](http://aws.amazon.com/rds/), [CloudSearch](http://aws.amazon.com/cloudsearch/) |
| Rapidly changing data | Data that must be updated very frequently might be better served by storage solutions that take into account read and write latencies, such as Amazon EBS volumes, Amazon RDS, Amazon DynamoDB, Amazon EFS, or relational databases running on Amazon EC2. | [EBS](https://aws.amazon.com/ebs/), [EFS](http://aws.amazon.com/efs/), [DynamoDB](http://aws.amazon.com/dynamodb/), [RDS](http://aws.amazon.com/rds/) |
| Archival data | Data that requires encrypted archival storage with infrequent read access with a long recovery time objective (RTO) can be stored in Amazon Glacier more cost-effectively. | [Glacier](http://aws.amazon.com/glacier/) |
| Dynamic website hosting | Although Amazon S3 is ideal for static content websites, dynamic websites that depend on database interaction or use server-side scripting should be hosted on Amazon EC2 or Amazon EFS. | [EC2](http://aws.amazon.com/ec2/), [EFS](http://aws.amazon.com/efs/) |
| Rapidly changing data | Data that must be updated very frequently might be better served by a storage solution with lower read/write latencies, such as Amazon EBS, Amazon RDS, Amazon EFS, Amazon DynamoDB, or relational databases running on Amazon EC2. | [EBS](https://aws.amazon.com/ebs/), [RDS](http://aws.amazon.com/rds/), [EFS](http://aws.amazon.com/efs/), [DynamoDB](http://aws.amazon.com/dynamodb/), [EC2](http://aws.amazon.com/ec2/) | 
| Immediate access | Data stored in Amazon Glacier is not available immediately. Retrieval jobs typically require 3–5 hours to complete, so if you need immediate access to your object data, Amazon S3 is a better choice | [S3](http://aws.amazon.com/s3/) |

##### Performence 

In scenarios where you use Amazon S3 from the same Region, access to Amazon S3 from Amazon EC2 is designed to be fast.  

If you access Amazon S3 using multiple threads, multiple applications, or multiple clients concurrently, total Amazon S3 aggregate throughput typically scales to rates that far exceed what any single server can generate or consume.  

To improve the upload performance of large objects (typically over 100 MB), Amazon S3 offers a multipart upload command to upload a single object as a set of parts. After all parts of your object are uploaded, Amazon S3 assembles these parts and creates the object. Using multipart upload, you can get improved throughput and quick recovery from any network issues. Another benefit of using multipart upload is that you can upload multiple parts of a single object in parallel and restart the upload of smaller parts instead of restarting the upload of the entire large object.  

Amazon S3 Transfer Acceleration enables fast, easy, and secure transfer of files over long distances between your client and your Amazon S3 bucket. It leverages Amazon CloudFront globally distributed edge locations to route traffic to your Amazon S3 bucket over an Amazon-optimized network path. To get started with Amazon S3 Transfer Acceleration you first must enable it on an Amazon S3 bucket. Then modify your Amazon S3 PUT and GET requests to use the s3-accelerate endpoint domain name (< bucketname >.s3-accelerate.amazonaws.com). The Amazon S3 bucket can still be accessed using the regular endpoint. Some customers have measured performance improvements in excess of 500 percent when performing intercontinental uploads. 

##### Durability and Availability

Amazon S3 Standard storage and Standard-IA storage provide high levels of data durability and availability by automatically and synchronously storing your data across both multiple devices and multiple facilities within your selected geographical region. Error correction is built-in, and there are no single points of failure. Amazon S3 is designed to sustain the concurrent loss of data in two facilities, making it very well suited to serve as the primary data storage for mission-critical data. In fact, Amazon S3 is designed for 99.999999999 percent (11 nines) durability per object and 99.99 percent availability over a one-year period.  

Additionally, you have a choice of enabling cross-region replication on each Amazon S3 bucket. Once enabled, cross-region replication automatically copies objects across buckets in different AWS Regions asynchronously, providing 11 nines of durability and 4 nines of availability on both the source and destination Amazon S3 objects.

##### Security 

You can manage access to Amazon S3 by granting other AWS accounts and users permission to perform the resource operations by writing an access policy.

You can protect Amazon S3 data at rest by using server-side encryption, in which you request Amazon S3 to encrypt your object before it’s written to disks in data centers and decrypt it when you download the object or by using client-side encryption, in which you encrypt your data on the client side and upload the encrypted data to Amazon S3. You can protect the data in transit by using Secure Sockets Layer (SSL) or client-side encryption.

You can use versioning to preserve, retrieve, and restore every version of every object stored in your Amazon S3 bucket. With versioning, you can easily recover from both unintended user actions and application failures. Additionally, you can add an optional layer of security by enabling Multi-Factor Authentication (MFA) Delete for a bucket.7 With this option enabled for a bucket, two forms of authentication are required to change the versioning state of the bucket or to permanently delete an object version: valid AWS account credentials plus a sixdigit code (a single-use, time-based password) from a physical or virtual token device.  

To track requests for access to your bucket, you can enable access logging. Each access log record provides details about a single access request, such as the requester, bucket name, request time, request action, response status, and error code, if any. Access log information can be useful in security and access audits. It can also help you learn about your customer base and understand your Amazon S3 bill.

##### Interfaces

Amazon S3 provides:  

1. Standards-based REST web service application program interfaces (APIs) for both management and data operations.
2. Higher-level toolkit or software development kit (SDK) that wraps the underlying REST API.
3. Integrated AWS Command Line Interface (AWS CLI) also provides a set of high-level, Linux-like Amazon S3 file commands for common operations, such as ls, cp, mv, sync, and so on

Additionally, you can use the Amazon S3 notification feature to receive notifications when certain events happen in your bucket. Currently, Amazon S3 can publish events when an object is uploaded or when an object is deleted.  

Notifications can be issued to Amazon Simple Notification Service (SNS) topics, Amazon Simple Queue Service (SQS) queues, and AWS Lambda functions.

##### Cost Model

With Amazon S3, you pay only for the storage you actually use. Amazon S3 Standard has three pricing components: storage (per GB per month), data transfer in or out (per GB per month), and requests (per thousand requests per month). There are Data Transfer IN and OUT fees if you enable Amazon S3 Transfer Acceleration on a bucket and the transfer performance is faster than regular Amazon S3 transfer.

[Back to main page](/page/aws_architect)


### Amazon Glacier

Amazon Glacier is an extremely low-cost storage service that provides highly secure, durable, and flexible storage for data archiving and online backup.14 With Amazon Glacier, you can reliably store your data for as little as $0.007 per gigabyte per month. Amazon Glacier enables you to offload the administrative burdens of operating and scaling storage to AWS so that you don’t have to worry about capacity planning, hardware provisioning, data replication, hardware failure detection and repair, or time-consuming hardware migrations.

You store data in Amazon Glacier as archives. An archive can represent a single file, or you can combine several files to be uploaded as a single archive.

Retrieving archives from Amazon Glacier requires the initiation of a job. You organize your archives in vaults.

Amazon Glacier is designed for use with other Amazon web services. You can seamlessly move data between Amazon Glacier and Amazon S3 using S3 data lifecycle policies.


##### Use Patterns

Organizations are using Amazon Glacier to support a number of use cases. These use cases include archiving offsite enterprise information, media assets, and research and scientific data, and also performing digital preservation and magnetic tape replacement.

Amazon Glacier doesn’t suit all storage situations. The following table presents a few storage needs for which you should consider other AWS storage options.

| Storage Need | Solution | AWS Services      |
| ------------ | -------- | ----------------- |
| Rapidly changing data | Data that must be updated very frequently might be better served by a storage solution with lower read/write latencies, such as Amazon EBS, Amazon RDS, Amazon EFS, Amazon DynamoDB, or relational databases running on Amazon EC2. | [EBS](https://aws.amazon.com/ebs/), [RDS](http://aws.amazon.com/rds/), [EFS](http://aws.amazon.com/efs/), [DynamoDB](http://aws.amazon.com/dynamodb/), [EC2](http://aws.amazon.com/ec2/) | 
| Immediate access | Data stored in Amazon Glacier is not available immediately. Retrieval jobs typically require 3–5 hours to complete, so if you need immediate access to your object data, Amazon S3 is a better choice | [S3](http://aws.amazon.com/s3/) |


##### Performance

Amazon Glacier is a low-cost storage service designed to store data that is infrequently accessed and long-lived. Amazon Glacier retrieval jobs typically complete in 3 to 5 hours.

You can improve the upload experience for larger archives by using multipart upload for archives up to about 40 TB (the single archive limit). You can upload separate parts of a large archive independently, in any order and in parallel, to improve the upload experience for larger archives. You can even perform range retrievals on archives stored in Amazon Glacier by specifying a range or portion of the archive. Specifying a range of bytes for a retrieval can help control bandwidth costs, manage your data downloads, and retrieve a targeted part of a large archive.

