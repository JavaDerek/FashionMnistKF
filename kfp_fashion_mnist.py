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
    #project='cloud-training-demos',
    #bucket='cloud-training-demos-ml',
    #startYear='2000'
):
  """Pipeline to train Fashion MNIST model"""
  start_step = 1

  # Step 1: download and store data in pipeline
  if start_step <= 1:
    download = dsl.ContainerOp(
      name='download',
      # image needs to be a compile-time string
      image='docker.io/dotnetderek/download:latest',
      arguments=[
      ],
      file_outputs={
        'trainImages':'/trainImagesObjectName.txt',
        'trainLabels':'/trainLabelsObjectName.txt',
        'testImages':'/testImagesObjectName.txt',
        'testLabels':'/testLabelsObjectName.txt'
        }
    )
  else:
    download = ObjectDict({
      'outputs': {
        'trainImages':'trainimages',
        'trainLabels':'trainlabels',
        'testImages':'testimages',
        'testLabels':'testlabels'
      }
    })

  # Step 2: normalize data between 0 and 1
  if start_step <= 2:
    preprocess = dsl.ContainerOp(
      name='preprocess',
      # image needs to be a compile-time string
      image='docker.io/dotnetderek/preprocess:latest',
      arguments=[
        download.outputs['trainImages'],
        download.outputs['trainLabels'],
        download.outputs['testImages'],
        download.outputs['testLabels']
      ],
      file_outputs={
        'normalizedTrainImages':'/trainImagesObjectName.txt',
        'normalizedTestImages':'/testImagesObjectName.txt'
        }
    )
  else:
    preprocess = ObjectDict({
      'outputs': {
        'normalizedTrainImages':'normalizedtrainimages',
        'normalizedTestImages':'normalizedtestimages'
      }
    })

  # Step 3: train a model
  if start_step <= 3:
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
  else:
    train = ObjectDict({
      'outputs': {
        'trainedModelName':'trainedmodel'
      }
    })

  # Step 4: evaluate model
  if start_step <= 4:
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
  else:
    evaluate = ObjectDict({
      'outputs': {
      }
    })

  # Step 5: serve
  if start_step <= 5:
    evaluate = dsl.ContainerOp(
      name='serve',
      # image needs to be a compile-time string
      image='docker.io/dotnetderek/serve:latest',
      arguments=[
        train.outputs['trainedModelName']
      ],
      file_outputs={
        }
    )
  else:
    evaluate = ObjectDict({
      'outputs': {
      }
    })

if __name__ == '__main__':
  import kfp.compiler as compiler
  import sys
  if len(sys.argv) != 2:
    print("Usage: kfp_fashion_mnist  pipeline-output-name")
    sys.exit(-1)
  
  filename = sys.argv[1]
  compiler.Compiler().compile(train_and_deploy, filename)