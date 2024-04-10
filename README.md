# Benchmark_Model_inference
Image Classification Models Supported by TensorRT Server (Triton Server)

The purpose of this project is to use the Triton server to be able to host model inferencing to test the run time of multiple batches and models.

This repo is to be run on AWS services: EC2 and S3 but can be modified to include Lambda and EFS

##Creating the Model Repository
The first thing is create the model repository that stores all the models that we will use. Here the mode_repository directory will be the models that we will use. model_repository_main holds possible models that can be used but for this project we won't be using all of them. The structure of the model_repository directory is important because that is how the Triton Server will be able to read the models. The structure of the [model repository](https://github.com/triton-inference-server/server/blob/main/docs/model_repository.md) can be read here.

###Models Supported by Triton
* resnet10/resnet18/resnet34/resnet50/resnet101
* vgg16/vgg19
* googlenet
* mobilenet_v1/mobilenet_v2
* squeezenet
* darknet19/darknet53
* efficientnet_b0
* cspdarknet19/cspdarknet53

Note that some of the models may require a GPU and preset the max batch size.

We will be hosting our models in an S3 bucket. This is because the models may be large and it also isolates them from the rest of the code. Here we will be hosting our models on s3://modelsyppatel

##Running the Triton Server
Due to the lack of resources our Triton Server will need to be hosted without a GPU.

We first need to create an EC2 instance that will host the Triton Server. Ideally, we use the EC2 marketplace and get the NVIDIA Triton Server AMI which contains a **p3.2large** ec2 instance with the following specifications:
1) One NVIDIA Tesla V100 GPU
2) High frequency Intel Xeon E5-2686 v4 processor 
3) 61 GiB memory
4) 16 GiB GPU memory

However, we can also host it without a GPU with an EC2 instance with these specifications
1) t2.2xlarge instance type
2) 32 GiB Memory
3) IAM policy with S3 Full Access
4) Key-Value Pair <-- necessary for file transfer

Now once we have our EC2 instance up and running we will proceed to pull Triton Inference server container in our instance using docker with the following command.

Now once we have our EC2 instance up and running we will proceed to pull Triton Inference server container in our instance using docker with the following command.

###Install docker
```
sudo yum install docker
```
```
sudo systemctl start docker
```

###Pull the Triton Server Docker Image
```
sudo docker pull nvcr.io/nvidia/tritonserver:22.03-py3
```

###Run the Docker Image without a GPU
```
sudo docker run --rm -p8000:8000 -p8001:8001 -p8002:8002 nvcr.io/nvidia/tritonserver:22.03-py3 tritonserver --model-repository=s3://modelsyppatel/model_repository
```

The Triton Server should be running at this point but you can check on running this command for status. Run this line on the same EC2 instance, may need a nsew session.
```commandline
curl -v localhost:8000/v2/health/ready
```

##Running the Triton Client

Now we need to run a client image to do the inferencing. We need this since it has the libraries that is needed for our script.

###Get Docker image
```commandline
docker pull nvcr.io/nvidia/tritonserver:22.03-py3-sdk
```

###Run the docker
```commandline
docker pull nvcr.io/nvidia/tritonserver:22.03-py3-sdk
```
Test to see if the inferencing works
```commandline
/workspace/install/bin/image_client -m inception_graphdef -c 3 -s INCEPTION /workspace/images/mug.jpg
```

###Install some python libraries
```commandline
pip3 install boto3
pip3 install pandas
```

###Moving the benchmarking file
Copy our benchmark.py file to the EC2 instance. We used Filezilla to do so.

Copy our benchmark.py file to /workspace/install/bin. Can be done by
```commandline
sudo docker container ls
```
Get the container ID. Note that the ID will only show if the container is running
```commandline
sudo docker cp benchmark.py <container-id>:/workspace/install/bin
```

###Running the benchmark file
```commandline
python3 benchmark.py -m <model_name> -c 3 -s INCEPTION -b <batch_size> image-for-benchmark
```
-m is the model name that is being hosted by the Triton Server
-c number of outputs of a single image request
-s Type of scaling to apply to image pixels.
-b number of images in one batch. Default is 1.
image-for-benchmark File name that will be used for the S3 bucket where we host the images

##Output
After running benchmark.py. Two csv files will be created with the file name being <model_name>_<batch_size>_Throughput.csv and <model_name>_<batch_size>_Time.csv
The Time csv has the elapsed time after every batch has completed. The rows are the number attempts or number of times we went through the entire dataset.
The Throughout csv is the elapsed time per batch / batch size. It is the rate of time it takes to inference one image.
The files would be moved to the Results directory
