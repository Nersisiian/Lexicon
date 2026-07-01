#include <uapi/linux/ptrace.h>

BPF_HASH(connections, u32, u64);

int trace_connect(struct pt_regs *ctx) {
    u32 pid = bpf_get_current_pid_tgid();
    u64 ts = bpf_ktime_get_ns();
    connections.update(&pid, &ts);
    return 0;
}
