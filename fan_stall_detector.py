import logging

TIMER = 1

class FanStallDetector:
    def __init__(self, config):
        # Config
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.name = config.get_name()

        self.pin = config.get("pin")
        self.threshold = int(config.get("threshold", 5))

        # State
        self.last_state = {}
        self.stall_count = 0
        self.timer = None

        # Pins
        buttons = self.printer.load_object(config, "buttons")
        buttons.register_buttons([self.pin], self.fan_stall_event)

        # Gcodes
        gcode_macro = self.printer.load_object(config, "gcode_macro")
        self.gcode_fail = gcode_macro.load_template(config, "gcode_fail", "")
        self.gcode_ok = gcode_macro.load_template(config, "gcode_ok", "")
        self.gcode_failing = gcode_macro.load_template(config, "gcode_failing", "")

        self.gcode = self.printer.lookup_object("gcode")
        self.gcode.register_command(
            "QUERY_FAN_STALL_STATUS",
            self.cmd_QUERY_FAN_STALL_STATUS,
            desc=self.cmd_QUERY_FAN_STALL_STATUS_help,
        )

        # Event Handlers
        self.printer.register_event_handler("klippy:ready", self.handle_ready)
        self.timer = self.reactor.register_timer(self.handle_timer)

    def handle_ready(self):
        self.reactor.update_timer(self.timer, self.reactor.NOW)

    def handle_timer(self, eventtime):
        if not self.last_state:
            return eventtime + TIMER

        template = None

        if self.stall_count == self.threshold:
            template = self.gcode_fail
        else:
            template = self.gcode_failing
            self.stall_count += 1
            self.gcode.run_script(f"M118 stall count is {self.stall_count}")

        if template:
            try:
                self.gcode.run_script(template.render())
            except:
                logging.exception("FAN_STALL_DETECTOR: template error")

        return eventtime + TIMER

    cmd_QUERY_FAN_STALL_STATUS_help = "report the state of the fan stall detector"

    def cmd_QUERY_FAN_STALL_STATUS(self, gcmd):
        gcmd.respond_info("FAN_STALL_STATUS: " + self.get_status()["state"])

    def fan_stall_event(self, eventtime, state):
        self.last_state = state
        template = None

        if not state:
            self.stall_count = 0
            template = self.gcode_ok

            try:
                self.gcode.run_script(template.render())
            except:
                logging.exception("FAN_STALL_DETECTOR: template error")

    def get_status(self, eventtime=None):
        if self.last_state:
            if self.stall_count < self.threshold:
                return {"state": "FAILING"}
            return {"state": "FAIL"}
        return {"state": "OK"}


def load_config_prefix(config):
    return FanStallDetector(config)
