import kfp.dsl as dsl

class ObjectDict(dict):
  def __getattr__(self, name):
    if name in self:
      return self[name]
    else:
      raise AttributeError("No such attribute: " + name)


@dsl.pipeline(
  name='fashion mnist',
  description='Train and Deploy Fashion MNIST'
)
def train_and_deploy(
  download_and_preprocess="full"
):

  # Step 1: download and store data in pipeline
  download = dsl.ContainerOp(
    name='download',
    # image needs to be a compile-time string
    image='docker.io/dotnetderek/download:latest',
    arguments=[
      download_and_preprocess
    ],
    file_outputs={
      'trainImages':'/trainImagesObjectName.txt',
      'trainLabels':'/trainLabelsObjectName.txt',
      'testImages':'/testImagesObjectName.txt',
      'testLabels':'/testLabelsObjectName.txt'
    }
  )

  # Step 2: normalize data between 0 and 1
  preprocess = dsl.ContainerOp(
    name='preprocess',
    # image needs to be a compile-time string
    image='docker.io/dotnetderek/preprocess:latest',
    arguments=[
      download.outputs['trainImages'],
      download.outputs['trainLabels'],
      download.outputs['testImages'],
      download.outputs['testLabels'],
      download_and_preprocess
    ],
    file_outputs={
      'normalizedTrainImages':'/trainImagesObjectName.txt',
      'normalizedTestImages':'/testImagesObjectName.txt'
      }
  )

  # Step 3: train a model
  train = dsl.ContainerOp(
    name='train',
    # image needs to be a compile-time string
    image='docker.io/dotnetderek/train:latest',
    arguments=[
      preprocess.outputs['normalizedTrainImages'],
      download.outputs['trainLabels']
    ],
    file_outputs={
      'trainedModelName':'/trainedModelName.txt' 
      }
  )

  # Step 4: evaluate model
  evaluate = dsl.ContainerOp(
    name='evaluate',
    # image needs to be a compile-time string
    image='docker.io/dotnetderek/evaluate:latest',
    arguments=[
      preprocess.outputs['normalizedTestImages'],
      download.outputs['testLabels'],
      train.outputs['trainedModelName']
    ],
    file_outputs={
      }
  )

if __name__ == '__main__':
  import kfp.compiler as compiler
  import sys
  if len(sys.argv) != 2:
    print("Usage: kfp_fashion_mnist  pipeline-output-name")
    sys.exit(-1)
  
  filename = sys.argv[1]
  compiler.Compiler().compile(train_and_deploy, filename)