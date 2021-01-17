import json
import inflection

from orator import Model, accessor

class CaptureFilter(Model):
  DEFAULT_CAPTURE_FILTERS = {
    'hostList': [],
    'hostSetting': '',
    'pathList': [],
    'pathSetting': '',
    'extList': [],
    'extSetting': '',
    'navigationRequests': True
  }

  @classmethod
  def create_defaults(cls):
    capture_filter = CaptureFilter()
    capture_filter.id = 1
    capture_filter.filters = json.dumps(cls.DEFAULT_CAPTURE_FILTERS)
    capture_filter.save()

  @accessor
  def host_list(self):
    return self.parsed_filters('hostList')

  @accessor
  def host_setting(self):
    return self.parsed_filters('hostSetting')

  @accessor
  def path_list(self):
    return self.parsed_filters('pathList')

  @accessor
  def path_setting(self):
    return self.parsed_filters('pathSetting')

  @accessor
  def ext_list(self):
    return self.parsed_filters('extList')

  @accessor
  def ext_setting(self):
    return self.parsed_filters('extSetting')

  @accessor
  def navigation_requests(self):
    return self.parsed_filters('navigationRequests')

  def parsed_filters(self, value = None):
    parsed_filters = json.loads(self.filters)

    if (value == None):
      return parsed_filters
    else:
      return parsed_filters[value]

  def set_filters(self, filters):
    current_filters = self.parsed_filters()

    for key, value in filters.items():
      camel_case_key = inflection.camelize(key, False)
      current_filters[camel_case_key] = value

    self.filters = json.dumps(current_filters)

