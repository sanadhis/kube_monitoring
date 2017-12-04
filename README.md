# Django - Kubernetes Monitoring

This application aims to:
* Create trusted and reliable system to accurately monitor jobs' resource utilization (CPU,Memory,Storage,GPU) in each containers' across a Kubernetes cluster.
* Storing resource utilization data to database.
* Provide an interface between database and EPFL's SIFAC billing system. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To run, you need to install python and django

```
$ #check python version
$ python -V
$ #install django with pip
$ pip install Django
```

### Supported Metrics
* cpu/limit
* cpu/node_allocatable
* cpu/node_capacity
* cpu/node_reservation
* cpu/node_utilization
* cpu/request
* cpu/usage
* cpu/usage_rate
* filesystem/inodes
* filesystem/inodes_free
* filesystem/limit
* filesystem/usage
* memory/cache
* memory/limit
* memory/major_page_faults
* memory/major_page_faults_rate
* memory/node_allocatable
* memory/node_capacity
* memory/node_reservation
* memory/node_utilization
* memory/page_faults
* memory/page_faults_rate
* memory/request
* memory/rss
* memory/usage
* memory/working_set
* network/rx
* network/rx_errors
* network/rx_errors_rate
* network/rx_rate
* network/tx
* network/tx_errors
* network/tx_errors_rate
* network/tx_rate

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

