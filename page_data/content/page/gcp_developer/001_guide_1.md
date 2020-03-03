

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


#### Infrastructure as a Service vs. Container as a Service vs. Platform as a Service (e.g., autoscaling implications)

##### Infrastructure as a Service (IaaS)

Infrastructure-as-a-Service, commonly referred to as simply “IaaS,” is a form of cloud computing that delivers fundamental compute, network, and storage resources to consumers on-demand, over the internet, and on a pay-as-you-go basis. IaaS enables end users to scale and shrink resources on an as-needed basis, reducing the need for high, up-front capital expenditures or unnecessary “owned” infrastructure, especially in the case of “spiky” workloads. In contrast to PaaS and SaaS (even newer computing models like containers and serverless), IaaS provides the lowest-level control of resources in the cloud.

IaaS emerged as a popular computing model in the early 2010s, and since that time, it has become the standard abstraction model for many types of workloads. However, with the advent of new technologies, such as containers and serverless, and the related rise of the microservices application pattern, IaaS remains foundational but is in a more crowded field than ever.

IaaS is made up of a collection of physical and virtualized resources that provide consumers with the basic building blocks needed to run applications and workloads in the cloud.

- Physical data centers: IaaS providers will manage large data centers, typically around the world, that contain the physical machines required to power the various layers of abstraction on top of them and that are made available to end users over the web. In most IaaS models, end users do not interact directly with the physical infrastructure, but it is provided as a service to them.
- Compute: IaaS is typically understood as virtualized compute resources, so for the purposes of this article, we will define IaaS compute as a virtual machine. Providers manage the hypervisors and end users can then programmatically provision virtual “instances” with desired amounts of compute and memory (and sometimes storage). Most providers offer both CPUs and GPUs for different types of workloads. Cloud compute also typically comes paired with supporting services like auto scaling and load balancing that provide the scale and performance characteristics that make cloud desirable in the first place.
- Network: Networking in the cloud is a form of Software Defined Networking in which traditional networking hardware, such as routers and switches, are made available programmatically, typically through APIs. More advanced networking use cases involve the construction of multi-zone regions and virtual private clouds, both of which will be discussed in more detail later.
- Storage: The three primary types of cloud storage are block storage, file storage, and object storage. Block and file storage are common in traditional data centers but can often struggle with scale, performance and distributed characteristics of cloud. Thus, of the three, object storage has thus become the most common mode of storage in the cloud given that it is highly distributed (and thus resilient), it leverages commodity hardware, data can be accessed easily over HTTP, and scale is not only essentially limitless but performance scales linearly as the cluster grows.  

Taken together, there are many reasons why someone would see cloud infrastructure as a potential fit:

- Pay-as-you-Go: Unlike traditional IT, IaaS does not require any upfront, capital expenditures, and end users are only billed for what they use.
- Speed: With IaaS, users can provision small or vast amounts of resources in a matter of minutes, testing new ideas quickly or scaling proven ones even quicker.
- Availability: Through things like multizone regions, the availability and resiliency of cloud applications can exceed traditional approaches.
- Scale: With seemingly limitless capacity and the ability to scale resources either automatically or with some supervision, it’s simple to go from one instance of an application or workload to many.
- Latency and performance: Given the broad geographic footprint of most IaaS providers, it’s easy to put apps and services closers to your users, reducing latency and improving performance.




##### Containers as a service (CaaS)

Containers as a service (CaaS) is a cloud service model that allows users to upload, organize, start, stop, scale and otherwise manage containers, applications and clusters. It enables these processes by using either a container-based virtualization, an application programming interface (API) or a web portal interface. CaaS helps users construct security-rich, scalable containerized applications through on-premises data centers or the cloud. Containers and clusters are used as a service with this model and are deployed in the cloud or in onsite data centers.  

In the spread of cloud computing services, CaaS is considered a subset of infrastructure as a service (IaaS) and is found between IaaS and platform as a service (PaaS). CaaS includes containers as its basic resource, counter to the virtual machines (VMs) and bare metal hardware host systems commonly used for IaaS environments.

An essential quality of CaaS technology is orchestration that automates key IT functions. Google Kubernetes and Docker Swarm are two examples of CaaS orchestration platforms. IBM, Amazon Web Services (AWS) and Google are a few examples of public cloud CaaS providers.

Here are several of the client benefits for using containers:

- Portability: When an application is created in a container, that completed app has everything it needs to run, including dependencies and configuration files. Having portability allows end users to reliably launch applications in different environments and public or private clouds. This portability also grants enterprises a large amount of flexibility, accelerating the development process and making it easier to switch to a different provider or cloud environment.
- Highly efficient and cost cutting: Because containers don’t need a separate operating system, they require less resources than a VM. A container often requires only a few dozen megabytes to run, allowing you to run several containers on a single server that would otherwise be used to run a VM. 

Containers don’t interact and are somewhat isolated from other containers on the same servers, although they do share the same resources. If an application crashes for one container, other containers can continue to use it without experiencing any technical issues.

- Security: The isolation that containers have from one another doubles as a risk-minimizing security feature. If one application is compromised, then its negative effects won’t spread to the other containers.

Also, because containers run application processes in isolation from the operating system and don’t need specific software to run applications, it’s simpler to manage your host system. This benefit allows you to speedily launch updates and security patches.    

- Speed: It only takes seconds to start a container, and to create, replicate or destroy a container, because containers don’t need an operating system book. This advantage also enables a quick development process, expedites the time to market and operational speed, and makes releasing new versions or software simple, quick and easier than before. 
- Scaling: Containers feature the capability for horizontal scaling, allowing end users to incorporate multiple identical containers within the same cluster to scale out. By using smart scaling and running only the containers that you need when you need them, you can dramatically cut costs and boost your return on investment. 
- Streamlined development: Having an effective and efficient development pipeline is an advantage of container-based infrastructure. Because containers allow applications to work and run as if built locally, environmental inconsistencies are eliminated. This removal bolsters testing and debugging, making them less complicated and time-consuming. This feature also doubles for updating applications, only requiring the developer to modify the configuration file, then generate new containers and delete the previous ones; a process that should only take moments.


##### Platform as a Service (PaaS)

PaaS, or Platform-as-a-Service, is a cloud computing model that provides customers a complete platform—hardware, software, and infrastructure—for developing, running, and managing applications without the cost, complexity, and inflexibility of building and maintaining that platform on-premises.

The PaaS provider hosts everything—servers, networks, storage, operating system software, databases—at their data center; the customer uses it all for a for a monthly fee based on usage and can purchase more resources on-demand as needed. In this way, PaaS lets your development teams to build, test, deploy, maintain, update, and scale applications (and to innovate in response to market opportunities and threats) much more quickly and less expensively than they could if you had to build out and manage your own on-premises platform.

The following are some specific advantages your organization can realize from utilizing PaaS:

- Faster time to market: With PaaS, there’s no need to purchase and install the hardware and software you’ll use to build and maintain your application development platform and no need for development teams to wait while you do this. You simply tap into the cloud service provider’s PaaS resources and begin developing immediately.
- Faster, easier, less-risky adoption of a wider range of resources: PaaS platforms typically include access to a greater variety of choices up and down the application development stack—operating systems, middleware, and databases, and tools such as code libraries and app components—than you can affordably or practically maintain on-premises. It also lets you test new operating systems, languages, and tools without risk—that is, without having to invest in the infrastructure required to run them.
- Easy, cost-effective scalability: If an application developed and hosted on-premises starts getting more traffic, you’ll need to purchase more computing, storage, and even network hardware to meet the demand, which you may not be able to do quickly enough and can be wasteful (since you typically purchase more than you need). With PaaS, you can scale on-demand by purchasing just the amount of additional capacity you need.
- Lower costs: Because there’s no infrastructure to build, your upfront costs are lower. Costs are also lower and more predictable because most PaaS providers charge customers based on usage.



##### PaaS, IaaS, and SaaS
PaaS (Platform-as-a-Service), IaaS (Infrastructure-as-a-Service), and SaaS (Software-as-a-Service) are the three most common models of cloud services, and it’s not uncommon for an organization to use all three. However, there is often confusion among the three and what’s included with each:

- With IaaS, your cloud provider offers access to ‘raw’ computing resources, such as servers, storage, and networking, but you’re responsible for the platform and application software.
- With PaaS, your provider delivers and manages the entire platform infrastructure; you are abstracted from the lower-level details of the environment, and you use the platform to develop and deploy your applications.
- SaaS is software you use via the cloud, as if it were installed on your computer (and parts of it may, in fact, be installed on your computer). SaaS applications reside on the cloud network, and users can store and analyze data and collaborate on projects thorough the application.
