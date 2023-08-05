from .details import DetailsTinyIntError

class TinyIntError(Exception):
  def __init__(self, message = ''):
    self.message = message if message else 'El número no cuenta con las caractatisticas de un tinyint'
    self.detail = DetailsTinyIntError()

  def __str__(self):
    return self.message

  def get_detail_as_dict(self):
    return self.detail.__dict__
