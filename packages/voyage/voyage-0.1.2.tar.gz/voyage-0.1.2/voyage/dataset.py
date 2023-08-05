import gzip
import cPickle

class DataSet(object):

  def __init__(self, path):
    file = gzip.open(path, 'rb')
    (self.X_train, self.y_train), (self.X_test, self.y_test) = cPickle.load(file)
    file.close()

  def train(self):
    return (self.X_train, self.y_train)

  def test(self):
    return (self.X_test, self.y_test)