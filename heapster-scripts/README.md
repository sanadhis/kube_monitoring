# Heapster Scripts 

## Background
By default, heapster is designed to send metrics to internal influxdb pod(s) in the kubernetes cluster. However since pods are designed to stateless, thus we need to deploy influxdb outside the kubernetes cluster. Influxdb itself may, by default, not implement user-authentication. Therefore, usually heapster is not using authentication as well.

## Purpose
The aim of this scripts is to provide automation for targeting Influxdb host, port, username, and password when deploying either heapster, grafana, or both pod(s).

## Running the scripts
You need to ensure that you do not have neither running heapster nor grafana in your kubernetes cluster.

### Prerequisites - Removing Heapster & Grafana Deployment

Remove heapster/grafana deployment only.

```
$ kubectl delete deployment heapster --namespace=kube-system
$ kubectl delete deployment monitoring-grafana --namespace=kube-system
```

### Installing

Deploy heapster/grafana with customized influxdb target

```
$ ./install-heapster [INFLUXDB_HOST] [INFLUXDB_PORT] [INFLUXDB_USERNAME] [INFLUXDB_PASSWORD]
$ ./install-grafana

```