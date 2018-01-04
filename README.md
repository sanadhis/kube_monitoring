# Kube-App: Monitoring Kubernetes Metrics

## Overview
This application consists of two sub-applications; **REST API** and **Web UI**, which both are exposed on the same port.
* REST API: HTTP API of application backend. Accessed via `/api` in path.
* Web UI: Web application to display main metrics/measurements of kubernetes. Accessed via `/web` in path.

## Purposes
This application aims to:
* Create trusted and reliable system to accurately monitor jobs' resource utilization (CPU,Memory,GPU) in each containers' across a Kubernetes cluster.
* Provide an interface between metrics database and EPFL's SIFAC billing system. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### 1. Dependencies

To run the application for development, you need to install minimum dependencies, listed on `requirements.txt` file. To install, execute:

```
./install-dependencies
```

### 2. Environment Variables

Export several environment variables before running the application:

```
# Configurations to connect and read to and from influxdb instance
export INFLUXDB_HOST="<your_influxdb_instance_hostname>"
export INFLUXDB_PORT="<your_influxdb_instance_port>"
export INFLUXDB_USER="<your_influxdb_account_username>"
export INFLUXDB_PASS="<your_influxdb_account_password>"
export INFLUXDB_DB="<your_influxdb_db_name>"

# Configurations for API authentication
export API_USERNAME="<username>"
export API_PASSWORD="<password>"
```

### 3. Logging

Create the default logging directory of the application and make it writable for user program.
```
sudo mkdir -p /logs/kube-monitoring
sudo chown $(id -u):$(id -g) /logs/kube-monitoring
```

### 4. Starting Application

To run, simply execute the start script to start the application and pass the desired port number as an argument.

```
# Example
./start-server 8000
```

## Metrics
**Note** that there are **main metrics** and **available metrics**.
* *Main metrics* : Metrics/measurement that count for accounting utilization (usage) by pods. Basically, the utilization/usage rate of compute resources will be measured based on these metrics.
* *Available metrics*: Metrics/measurement that available for query both in API and Web.

### Main Metrics for API & Web
| Metric Name | Description |
|------------|-------------|
| cpu/usage_rate | CPU usage on all cores in millicores. |
| gpu/usage | The usage of all gpus in megabytes. |
| memory/usage | Total memory usage in bytes. |

### Available Metrics for API and Web
| Metric Name | Description |
|------------|-------------|
| cpu/limit | CPU hard limit in millicores. |
| cpu/node_capacity | Cpu capacity of a node. |
| cpu/node_allocatable | Cpu allocatable of a node. |
| cpu/node_reservation | Share of cpu that is reserved on the node allocatable. |
| cpu/node_utilization | CPU utilization as a share of node allocatable. |
| cpu/request | CPU request (the guaranteed amount of resources) in millicores. |
| cpu/usage | Cumulative CPU usage on all cores. |
| cpu/usage_rate | CPU usage on all cores in millicores. |
| filesystem/usage | Total number of bytes consumed on a filesystem. |
| filesystem/limit | The total size of filesystem in bytes. |
| filesystem/available | The number of available bytes remaining in a the filesystem |
| filesystem/inodes | The number of available inodes in a the filesystem |
| filesystem/inodes_free | The number of free inodes remaining in a the filesystem |
| gpu/usage | The usage on all gpus in Megabytes |
| memory/limit | Memory hard limit in bytes. |
| memory/major_page_faults | Number of major page faults. |
| memory/major_page_faults_rate | Number of major page faults per second. |
| memory/node_capacity | Memory capacity of a node. |
| memory/node_allocatable | Memory allocatable of a node. |
| memory/node_reservation | Share of memory that is reserved on the node allocatable. |
| memory/node_utilization | Memory utilization as a share of memory allocatable. |
| memory/page_faults | Number of page faults. |
| memory/page_faults_rate | Number of page faults per second. |
| memory/request | Memory request (the guaranteed amount of resources) in bytes. |
| memory/usage | Total memory usage. |
| memory/cache | Cache memory usage. |
| memory/rss | RSS memory usage. |
| memory/working_set | Total working set usage. Working set is the memory being used and not easily dropped by the kernel. |
| network/rx | Cumulative number of bytes received over the network. |
| network/rx_errors | Cumulative number of errors while receiving over the network. |
| network/rx_errors_rate | Number of errors while receiving over the network per second. |
| network/rx_rate | Number of bytes received over the network per second. |
| network/tx | Cumulative number of bytes sent over the network |
| network/tx_errors | Cumulative number of errors while sending over the network |
| network/tx_errors_rate | Number of errors while sending over the network |
| network/tx_rate | Number of bytes sent over the network per second. |
| uptime  | Number of milliseconds since the container was started. |

# The Application
For both API and WEB, it is possible to discover all **available metrics** by specifying which metric in **URL path** for each request. However, you have to type manually in the web application as non-main kubernetes metrics are not really concerned in this project.

## Project Structure
------------
    ├── app
    │   ├── api             : Directory containing all views, and urls settings for API.
    │   ├── kube-monitoring : Directory containing Django project main settings, urls configuration, custom logging spec.
    │   ├── web             : Directory containing All methods, views, and urls settings for Web.
    │   ├── manage.py       : Script to manage administrative settings of the project.
    
------------

## Logging
For both API and web, the application will write its logging to **info.log** and **errors.log** in `/logs/kube-monitoring`. To trace either debug, info or error in application:
```
tail -f /logs/kube-monitoring/info.log
# or
tail -f /logs/kube-monitoring/errors.log
```

## API
The API service is available in `/api/[metrics]` path and works only with **HTTP POST**. Any other HTTP method will be rejected.
Alongside the HTTP request, **X-USERNAME** and **X-PASSWORD** must be presented in HTTP request headers. The contents of these headers should match **API_USERNAME** and **API_PASSWORD** that are exported in environment.  

The details of HTTP requests:
* HTTP Method: `POST`
* HTTP Path: `/api/[metrics]`, for example `/api/cpu/usage_rate`
* HTTP Headers:
    * `X-USERNAME` : username for the HTTP request
    * `X-PASSWORD` : password for the HTTP request
* Request body:
    * `namespace` : the specific namespace (virtual cluster) in kubernetes cluster. *Default is "default" namespace*
    * `limit` : the desired number of how much the datapoints should be returned to client. *Default is 100 datapoints*
    * `agg`   : the type of aggregation needed. *Default is None*, options are: `pod-by-namespace`, `all-namespace`, `all-pod`.
    * `timeBeginInterval` : The starting time range (inclusive) of query. *Default is 60 minutes from the current time of query*
    * `timeEndInterval`   : The ending time range (inclusive) of query. *Default is the current time of query*

### Using the API
There are four ways of using the HTTP API according to provided aggregation schemes:
1. Without aggregation
<br> To perform request without aggegration, simply set `agg` in HTTP request body into other values or left it empty.
2. Aggregation by pods per namespace
<br> Set `agg` in HTTP request body into `pod-by-namespace`. `Limit` will be ignored.
3. Aggegation by namespace
<br> Set `agg` in HTTP request body into `all-namespace`. `Limit` and `namespace` will be ignored.
4. Aggeration by pods
<br> Set `agg` in HTTP request body into `all-pod`. `Limit` and `namespace` will be ignored.

#### Example using curl
```
curl -X POST \
  http://<app_hostname>:<app_port>/api/cpu/usage_rate \
  -H 'x-password: <password>' \
  -H 'x-username: <username>' \
  -d '{
  "agg":"pod-by-namespace",
  "timeBeginInterval": "2017-12-01",
  "timeEndInterval": "2017-12-31"
}'
```

## Web
It is pretty straightforward to use the web. Login into the web and navigate using the main left sidebar to view main metrics of kubernetes monitoring.

### Advanced Usage - Filter by namespace on the Web
However, it is possible to filter metrics based on namespace. To do so add `/[namespace]` at the end of `/web/stats/[metrics]`. For example if you want to highlight namespace "cluster-3" for its cpu/usage_rate, simply hit on browser url the following: `<hostname>:<port>/web/stats/gpu/usage_rate/cluster-3`

### Creating User for the Web
To add user account for accessing the web, execute the following in the terminal:
```
python app/manage.py createuser --username=<username> --email=<email>
```
**Note** that you will be prompted the password afterwards.

## Deployment into Production
It is encouraged to deploy the application in the Kubernetes cluster as well, as the application is stateless and act only as an interface into influxdb instance.

### Building Docker Image
Build the image using make command:
```
make build IMAGE_NAME="<image_name>" VERSION="<version>"
```
Push to dockerhub:
```
make push IMAGE_NAME="<image_name>" VERSION="<version>"
```
Or build and push at once. For example:
```
# Example build and push command with default image name and version
make all IMAGE_NAME=sanadhis/kube-monitoring VERSION=0.1
```

### Deploying to Kubernetes
First, fill in the environment variables in `kube-monitoring.yaml`; **INFLUXDB_HOST**, **INFLUXDB_PORT**, **INFLUXDB_USER**, **INFLUXDB_PASS**, **INFLUXDB_DB**, **API_USERNAME**, **API_PASSWORD**. 

Ensure that you use the corresponding image name and version in `kube-monitoring.yaml`. Then, simply execute:
```
kubectl create -f kube-monitoring.yaml
```

### Avoid Committing YAML with Credentials
To avoid accidental commit of your account credentials information, ignore `kube-monitoring.yaml` by executing:
```
git update-index --assume-unchanged kube-monitoring.yaml
```

### Accessing Services
If you look closely, the **kube-monitoring** deployment comes with **Grafana v4.4.3**. Thus you can access the grafana and the application itself once you successfully deployed the YAML file.

To find the port of application (default by NodePort):
```
kubectl get svc | grep kube-monitoring
```
Test the application or grafana:
```
curl <hostname>:<application_port>/api
curl <hostname>:<application_port>/web
curl <hostname>:<grafana_port>
```

## Miscellaneous
### Built With

* [Django](https://docs.djangoproject.com/en/1.11/releases/1.11.5) - The web framework used

### Versioning

* Version 1.0 : 1st January 2018

### Authors

* **Sanadhi Sutandi** [@sanadhis](https://github.com/sanadhis)

### License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details

### Acknowledgments

* [EPFL VLSC](https://vlsc.epfl.ch/)
* [EPFL SIFAC](https://github.com/EPFL-IC)

