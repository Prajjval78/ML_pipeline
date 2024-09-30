import sys
import os

#importing exception and logging module
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

#importing components
from networksecurity.components.data_ingestion import DataIngestion




#importing configuration entity
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.entity.config_entity import DataIngestionConfig
    

#importing artifact entity
from networksecurity.entity.artifact_entity import DataIngestionArtifact




class TrainingPipeline:
    is_pipeline_running = False
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        # called from config_entity for entire training pipeline
        
    
    def start_data_ingestion(self):
        """_summary_
        """
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            #  called from config_entity.py the data_ingestion
            logging.info("Starting data ingestion")

            # it is component of dataIngestion that will collect data from Sources and create test_train split
            # are calling DataIngestionComponent
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)

            # this function is a part of DataIngestionComponent

            # after doing all task it will return data_ingestion_artifact which will be used by next component
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
        
    def run_pipeline(self):
        try:
            TrainingPipeline.is_pipeline_running = True
            
            data_ingestion_artifact:DataIngestionArtifact=self.start_data_ingestion()

            
        except Exception as e:
            #self.sync_artifact_dir_to_s3()
            #TrainingPipeline.is_pipeline_running=False
            raise NetworkSecurityException(e, sys)