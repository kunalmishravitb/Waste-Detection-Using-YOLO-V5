import os, sys
import yaml
from wasteDetection.utils.main_utils import read_yaml_file
from wasteDetection.logger import logging
from wasteDetection.exception import AppException
from wasteDetection.entity.config_entity import ModelTrainerConfig
from wasteDetection.entity.artifacts_entity import ModelTrainerArtifact


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.model_trainer_config=model_trainer_config
    
    
    def initiate_model_trainer(self,) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            # Unzipping the data and then removing it
            logging.info("Unzipping data")
            os.system("unzip data.zip")
            os.system("rm data.zip")

            # Reading the yaml file and extracting the number of classes
            with open("data.yaml", "r") as stream:
                num_classes=str(yaml.safe_load(stream)['nc'])
            
            # Splitting the weight name and taking only the model name i.e. yolov5s
            model_config_file_name=self.model_trainer_config.weight_name.split(".")[0]
            print(model_config_file_name)

            config=read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")

            # Changing the number of classes from 18 to 13
            config['nc']=int(num_classes)

            with open(f'yolov5/models/custom_{model_config_file_name}.yaml', 'w') as f:
                yaml.dump(config, f)
            
            os.system(f"cd yolov5/ && python train.py --img 416 --batch {self.model_trainer_config.batch_size} --epochs {self.model_trainer_config.no_epochs} --data ../data.yaml --cfg ./models/custom_yolov5s.yaml --weights {self.model_trainer_config.weight_name} --name yolov5s_results --cache")
            # Copying the best.pt inside yolov5 model
            os.system("cp yolov5/runs/train/yolov5s_results/weights/best.pt yolov5/")
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            # Copying the best.pt inside model_trainer directory in artifacts folder
            os.system(f"cp yolov5/runs/train/yolov5s_results/weights/best.pt {self.model_trainer_config.model_trainer_dir}/")

            # Removing the below folders and files
            os.system("rm -rf yolov5/runs")
            os.system("rm -rf train")
            os.system("rm -rf valid")
            os.system("rm -rf data.yaml")

            model_trainer_artifact=ModelTrainerArtifact(
                trained_model_file_path="yolov5/best.pt",
            )
            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact
        except Exception as e:
            raise AppException(e, sys)
