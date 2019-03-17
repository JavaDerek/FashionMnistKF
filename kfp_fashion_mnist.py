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
    preprocess = dsl.ContainerOp(
      name='download',
      # image needs to be a compile-time string
      image='docker.io/dotnetderek/download:031619',
      arguments=[
      ],
      file_outputs={
        'trainImages':'/trainImagesObjectName.txt',
        'trainLabels':'/trainLabelsObjectName.txt',
        'testImages':'/testImagesObjectName.txt',
        'testLabels':'/testImagesObjectName.txt'
        }
    )
  else:
    preprocess = ObjectDict({
      'outputs': {
        'train_images':'trainimages',
        'train_labels':'trainlabels',
        'test_images':'testimages',
        'test_labels':'testlabels'
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