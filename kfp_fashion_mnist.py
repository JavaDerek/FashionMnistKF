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

  vop = dsl.VolumeOp(
    name="create_pvc", 
    resource_name="my-pvc", 
    size="1Gi")

  # Step 1: download and store data in pipeline
  download = dsl.ContainerOp(
    name='download',
    # image needs to be a compile-time string
    image='docker.io/dotnetderek/download:vop',
    arguments=[
      download_and_preprocess
    ],
    file_outputs={
      'downloadOk':'/downloadOk.txt'
    },
    pvolumes={
      "/mnt": vop.volume
    }
  )

  # Step 2: normalize data between 0 and 1
  preprocess = dsl.ContainerOp(
    name='preprocess',
    # image needs to be a compile-time string
    image='docker.io/dotnetderek/preprocess:vop',
    arguments=[
      download_and_preprocess,
      download.outputs['downloadOk']
    ],
    file_outputs={
      'preprocessOk':'/preprocessOk.txt'
    },
    pvolumes={
      "/mnt": vop.volume
    }
  )

  # Step 3: train a model
  train = dsl.ContainerOp(
    name='train',
    # image needs to be a compile-time string
    image='docker.io/dotnetderek/train:vop',
    arguments=[
      preprocess.outputs['preprocessOk'],
      download.outputs['downloadOk']
    ],
    file_outputs={
      'tOk':'/trainOk.txt'
    },
    pvolumes={
      "/mnt": vop.volume
    }
  )

  # Step 4: evaluate model
  # evaluate = dsl.ContainerOp(
  #   name='evaluate',
  #   # image needs to be a compile-time string
  #   image='docker.io/dotnetderek/evaluate:vop',
  #   arguments=[
  #     preprocess.outputs['preprocessOk'],
  #     download.outputs['downloadOk'],
  #     train.outputs['trainOk']
  #   ],
  #   pvolumes={
  #     "/mnt": vop.volume
  #   }
  # )

if __name__ == '__main__':
  import kfp.compiler as compiler
  import sys
  if len(sys.argv) != 2:
    print("Usage: kfp_fashion_mnist  pipeline-output-name")
    sys.exit(-1)
  
  filename = sys.argv[1]
  compiler.Compiler().compile(train_and_deploy, filename)