from config import config
from flags import flags
from registry import registry

def control():
  if registry.sensor_reading < config['pressure_lower_bound'] or registry.sensor_reading > config['pressure_upper_bound']:
    flags.send_warning = True
