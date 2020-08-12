from datadog_checks.checks import AgentCheck

import os

class RpiCheck(AgentCheck):

    def measure_temp(self):
            temp = os.popen("vcgencmd measure_temp").readline()
            try:
                return float(temp.replace("temp=","").replace("'C",""))
            except (ValueError, TypeError) as err:
                raise Exception(f"Invalid temperature reading: {temp} ({err})")

    def measure_clock(self):
        out = {}
        for k in ["arm", "core", "h264", "isp", "v3d", "uart", "pwm", "emmc", "pixel", "vec", "hdmi", "dpi"]:
            v = os.popen(f"vcgencmd measure_clock {k}").readline()
            try:
                v = float(v[v.find("=")+1:])
            except ValueError as err:
                raise Exception(f"Invalid clock speed: {v} ({err})")
            out.update({k: v})
        return out

    def check(self, instance):
        err_list = []

        try:
            self.gauge(f"rpi.temperature.soc", float(self.measure_temp()), tags=["cpu", "temperature"])
        except Exception as err:
            err_list.append(f"measure_temp:{err}")

        try:
            clocks = self.measure_clock()
            for k, v in clocks.items():
                self.gauge(f"rpi.clock.{k}", v, tags=["cpu", "frequency"])
        except Exception as err:
            err_list.append(f"measure_clock:{err}")

        if err_list:
            status = AgentCheck.CRITICAL
            msg = ','.join(err_list)
        else:
            status = AgentCheck.OK
            msg = 'Ok'

        self.service_check('rpi.check', status, message=msg)
