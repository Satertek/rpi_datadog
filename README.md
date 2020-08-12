# rpi_datadog
Raspberry Pi Custom Metrics for Datadog

Example Docker run:

<pre><code>
DOCKER_CONTENT_TRUST=1 docker run -d --name datadog \
        -v /var/run/docker.sock:/var/run/docker.sock:ro \
        -v /proc/:/host/proc/:ro \
        -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
        # Arguments below required to utilize vcgencmd
        --device=/dev/vchiq \
        --group-add video \
        -v /usr/bin/vcgencmd:/usr/bin/vcgencmd:ro \
        -v /usr/lib/aarch64-linux-gnu/:/usr/lib/aarch64-linux-gnu/:ro \
        -v /home/pi/rpi.py:/etc/datadog-agent/checks.d/rpi.py:ro \
        -v /home/pi/rpi.yaml:/etc/datadog-agent/conf.d/rpi.yaml \
        -e DD_API_KEY=[API KEY]
        -e DD_SITE="datadoghq.com" \
        datadog/agent:latest
</code></pre>
