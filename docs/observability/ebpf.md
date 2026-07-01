# eBPF Observability

## Overview
Deep kernel?level monitoring of network traffic and performance without code changes.

## Metrics
- TCP connections and throughput
- HTTP latency and request rate
- System call tracing

## Access
- API: http://localhost:8014
- Metrics endpoint: /metrics/tcp, /metrics/http

## eBPF Programs
Stored in `services/ebpf-agent/ebpf/`. Compile with:
```bash
clang -O2 -target bpf -c tcp_trace.c -o tcp_trace.o
