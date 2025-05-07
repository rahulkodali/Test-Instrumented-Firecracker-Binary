import time
import subprocess
from pathlib import Path
import re
import pytest


def test_clippy_tracing_instrumentation(uvm_plain):
    """
    Test Firecracker with Clippy linting and tracing instrumentation enabled.
    """

    vm = uvm_plain
    vm.spawn(log_file=None)
    vm.basic_config(boot_args="log-level=Trace")

    log_path = Path(vm.path) / "log"
    log_path.touch()
    vm.api.logger.put(
        log_path=vm.create_jailed_resource(log_path),
        level="Trace",
        show_level=True,
        show_log_origin=True,
    )
    vm.log_file = log_path
    vm.time_api_requests = False

    vm.add_net_iface()

    vm.start()
    time.sleep(10) 

    logs = log_path.read_text()
    print("Tracing Logs:")
    print(logs)

    ping_result = vm.ssh.run("ping -c 4 8.8.8.8")

    assert ">>" in logs, "Expected tracing markers not found in logs"
    vm.kill()