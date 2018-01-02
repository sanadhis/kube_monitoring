# Kube-App: Monitoring Kubernetes Metrics

## Overview
This application consists of two sub-applications; **REST API** and **Web UI**, which both are exposed on the same port.
* REST API: HTTP API of application backend. Accessed via `/api` path.
* Web UI: Web application to display main metrics/measurements of kubernetes. Accessed via `/web` path

## Purposes
This application aims to:
* Create trusted and reliable system to accurately monitor jobs' resource utilization (CPU,Memory,GPU) in each containers' across a Kubernetes cluster.
* Provide an interface between metrics database and EPFL's SIFAC billing system. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Development - Prerequisites

To run the application for development, you need to install minimum dependencies, listed on `requirements.txt` file. To install, execute:

```
$ ./install-dependencies
```

### Supported Metrics for API
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

### Supported Metrics for Web
| Metric Name | Description |
|------------|-------------|
| cpu/node_capacity | Cpu capacity of a node. |
| cpu/usage | Cumulative CPU usage on all cores. |
| cpu/usage_rate | CPU usage on all cores in millicores. |
| gpu/usage | The usage on all gpus in Megabytes |
| memory/node_capacity | Memory capacity of a node. |
| memory/usage | Total memory usage. |
| memory/cache | Cache memory usage. |
| memory/rss | RSS memory usage. |
| network/rx | Cumulative number of bytes received over the network. |
| network/rx_rate | Number of bytes received over the network per second. |
| network/tx | Cumulative number of bytes sent over the network |
| network/tx_rate | Number of bytes sent over the network per second. |
| uptime  | Number of milliseconds since the container was started. |

### Avoid Committing YAML with Credentials

git update-index --assume-unchanged kube-monitoring.yaml

### Installing

A step by step series of examples that tell you have to get a development env running

TBD

```
TBD
```

And repeat

```
until finished
```

TBD

## Running the tests

TBD

### Break down into end to end tests

TBD

```
TBD
```

### And coding style tests

TBD

```
TBD
```

## Deployment

TBD

## Built With

* [Django](https://docs.djangoproject.com/en/1.11/releases/1.11.5) - The web framework used

## Contributing

TBD

## Versioning

TBD

## Authors

* **Sanadhi Sutandi** [@sanadhis](https://github.com/sanadhis)

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* EPFL's VLSC

