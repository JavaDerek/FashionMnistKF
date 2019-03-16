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
      image='preprocess',
      arguments=[
      ],
      file_outputs={
        'train_images':'/train_images',
        'train_labels':'/train_labels',
        'test_images':'/test_images',
        'test_labels':'/test_labels'}
    )
  else:
    preprocess = ObjectDict({
      'outputs': {
        'bucket': bucket
      }
    })

  # Step 2: Do hyperparameter tuning of the model on Cloud ML Engine
  if start_step <= 2:
    hparam_train = dsl.ContainerOp(
      name='hypertrain',
      # image needs to be a compile-time string
      image='gcr.io/cloud-training-demos/babyweight-pipeline-hypertrain:latest',
      arguments=[
        preprocess.outputs['bucket']
      ],
      file_outputs={'jobname': '/output.txt'}
    )
  else:
    hparam_train = ObjectDict({
      'outputs': {
        'jobname': 'babyweight_181008_210829'
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