
# coding: utf-8

# # S3 FUNCTIONS TO READ AND WRITE

# In[61]:


# Import packages as required for the functions

import boto3
import botocore
import re
import os
import io
import pyarrow.parquet as pq
from fastparquet import write 
import os, sys
import pandas as pd
import yaml
from io import BytesIO
from pathlib import Path


# # READ FROM S3

# ## FUNCTION READ CSV into DF

# In[33]:


def readS3_csv(yaml_path, filepath, file):  #### The path must be the final directory to the file
    
    target = yaml.load(open(yaml_path))  ## can be adapted
  
    bucket = target['bucket']['name']
    zone = target['bucket']['zone']
    key = target['bucket']['key']
    secret = target['bucket']['secret'] ## can be adapted
    zone = 'eu-central-1'
    
    client = boto3.client('s3', 
                      aws_access_key_id=key,
                      aws_secret_access_key=secret, 
                      region_name=zone
                      )
   
    try:
        obj = client.get_object(Bucket = bucket, 
                         Key = filepath + file, 
                         )
        
        dataframe = pd.read_csv(io.BytesIO(obj['Body'].read()), sep = ',')

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    
    return dataframe

def readS3_csv_simple(yaml_path, my_key):  #### The path must be the final directory to the file
    
    target = yaml.load(open(yaml_path))  ## can be adapted
  
    bucket = target['bucket']['name']
    zone = target['bucket']['zone']
    key = target['bucket']['key']
    secret = target['bucket']['secret'] ## can be adapted
    zone = 'eu-central-1'
    
    client = boto3.client('s3', 
                      aws_access_key_id=key,
                      aws_secret_access_key=secret, 
                      region_name=zone
                      )   

    obj = client.get_object(Bucket = bucket, 
                     Key = my_key, 
                     )

    dataframe = pd.read_csv(io.BytesIO(obj['Body'].read()), sep = ',', error_bad_lines=False)
    
    return dataframe

def readS3_csv_multi(yaml_path, filepath):  #### The path must be the final directory to the file
    target = yaml.load(open(yaml_path))  ## can be adapted
  
    bucket = target['bucket']['name']
    zone = target['bucket']['zone']
    key = target['bucket']['key']
    secret = target['bucket']['secret'] ## can be adapted
    zone = 'eu-central-1'
    
    client = boto3.client('s3', 
                      aws_access_key_id=key,
                      aws_secret_access_key=secret, 
                      region_name=zone
                      )
    
    s3 = boto3.resource('s3', 
                      aws_access_key_id=key,
                      aws_secret_access_key=secret, 
                      region_name=zone)
    
    bucket = s3.Bucket(bucket)    
        

    try:

        if not filepath.endswith('/'):
            filepath = filepath + '/'  # Add '/' to the end

        s3_keys = [item.key for item in bucket.objects.filter(Prefix=filepath)
                   if item.key.endswith('.csv')]
        
        if not s3_keys:
            print('No csv found in', bucket, filepath)

        for p in s3_keys: 
                print(p)
        
        dfs = [readS3_csv_simple(yaml_path, key) 
               for key in s3_keys]
          
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
           raise
    
    return pd.concat(dfs, ignore_index=True)


# ## READ SINGLE PARQUET

# In[140]:


def readS3_parquet(yaml_path, filepath, file):  #### The path must be the final directory to the file
    target = yaml.load(open(yaml_path))  ## can be adapted
  
    bucket = target['bucket']['name']
    zone = target['bucket']['zone']
    key = target['bucket']['key']
    secret = target['bucket']['secret'] ## can be adapted
    zone = 'eu-central-1'
    
    client = boto3.client('s3', 
                      aws_access_key_id=key,
                      aws_secret_access_key=secret, 
                      region_name=zone
                      )
    
    try:
        
        if not filepath.endswith('/'):
            filepath = filepath + '/'  # Add '/' to the end
        
        obj = client.get_object(Bucket = bucket, 
                         Key = filepath + file, 
                         )
        
        parquet = pd.read_parquet(io.BytesIO(obj['Body'].read()))

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    
    return parquet


# ## READ MULTI PARQUET

# In[174]:


def pd_readS3_parquet_simple(yaml_path, my_key):
    target = yaml.load(open(yaml_path))  ## can be adapted
  
    bucket = target['bucket']['name']
    zone = target['bucket']['zone']
    access_key = target['bucket']['key']
    secret = target['bucket']['secret'] ## can be adapted
    zone = 'eu-central-1'
    
    client = boto3.client('s3', 
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret, 
                      region_name=zone
                      )
    
    obj = client.get_object(Bucket=bucket, Key=my_key)
    return pd.read_parquet(io.BytesIO(obj['Body'].read()))


# In[175]:


def readS3_parquet_multi(yaml_path, filepath):  #### The path must be the final directory to the file
    target = yaml.load(open(yaml_path))  ## can be adapted
  
    bucket = target['bucket']['name']
    zone = target['bucket']['zone']
    key = target['bucket']['key']
    secret = target['bucket']['secret'] ## can be adapted
    zone = 'eu-central-1'
    
    client = boto3.client('s3', 
                      aws_access_key_id=key,
                      aws_secret_access_key=secret, 
                      region_name=zone
                      )
    
    s3 = boto3.resource('s3', 
                      aws_access_key_id=key,
                      aws_secret_access_key=secret, 
                      region_name=zone)
    
    bucket = s3.Bucket(bucket)    
        

    try:

        if not filepath.endswith('/'):
            filepath = filepath + '/'  # Add '/' to the end

        s3_keys = [item.key for item in bucket.objects.filter(Prefix=filepath)
                   if item.key.endswith('.parquet')]
        
        if not s3_keys:
            print('No parquet found in', bucket, filepath)

        for p in s3_keys: 
                print(p)
        
        dfs = [pd_readS3_parquet_simple(yaml_path, key) 
               for key in s3_keys]
          
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
           raise
    
    return pd.concat(dfs, ignore_index=True)


# ### TEST READ CSV AND PARQUET INTO DATAFRAME

# In[177]:


yml_path = "blob_new.yml" 
filepath = "sandbox/jscher/"
file = 'CBK_MTBC.csv'

df = readS3_csv(yml_path, filepath, file)
df


# In[178]:


yml_path ="blob_new.yml"
filepath = "sandbox/jscher/"
file = "CBK_MIC_complete.parquet"

df = readS3_parquet('blob_new.yml',filepath,file)
df


# In[176]:


yml_path ="blob_new.yml"
filepath = "sandbox/jscher/test"

df = readS3_parquet_multi('blob_new.yml',filepath)
df


# # WRITE TO BLOB

# ## WRITE CSV

# In[9]:


def writeS3_csv(dataframe ,yaml_path, filepath, file):  #### The path must be the final directory to the file
    
    target = yaml.load(open(yaml_path))  ## can be adapted
  
    bucket = target['bucket']['name']
    zone = target['bucket']['zone']
    key = target['bucket']['key']
    secret = target['bucket']['secret'] ## can be adapted
    
    zone = 'eu-central-1'
    
    client = boto3.client('s3', 
                      aws_access_key_id=key,
                      aws_secret_access_key=secret, 
                      region_name=zone
                      )

    # Create buffer
    csv_buffer = StringIO()
    # Write dataframe to buffer
    dataframe.to_csv(csv_buffer, sep=";", index=False)
    # Create S3 object
    s3_resource = boto3.resource("s3",
                                  aws_access_key_id=key,
                                  aws_secret_access_key=secret, 
                                  region_name=zone)
    # Write buffer to S3 object
    s3_resource.Object(bucket, filepath + file).put(Body=csv_buffer.getvalue(), ServerSideEncryption='AES256')


# ## WRITE PARQUET

# In[180]:


def writeS3_parquet(dataframe ,yaml_path, filepath, file):  #### The path must be the final directory to the file
        
    target = yaml.load(open(yaml_path))  ## can be adapted
  
    bucket = target['bucket']['name']
    zone = target['bucket']['zone']
    key = target['bucket']['key']
    secret = target['bucket']['secret'] ## can be adapted
    
    zone = 'eu-central-1'
    
    client = boto3.client('s3', 
                      aws_access_key_id=key,
                      aws_secret_access_key=secret, 
                      region_name=zone
                      )

    # Create buffer
    #parquet_buffer = StringIO()
    # Write dataframe to buffer
    
    parquet_obj = BytesIO()
    df.to_parquet(parquet_obj, compression="gzip", engine="pyarrow")
    
    #write(parquet_buffer, dataframe)
    #print(dataframe)
    #print(parquet_buffer)
    # Create S3 object
    s3_resource = boto3.resource("s3",
                                  aws_access_key_id=key,
                                  aws_secret_access_key=secret, 
                                  region_name=zone)
    #Write buffer to S3 object
    s3_resource.Object(bucket, filepath + file).put(Body=parquet_obj.getvalue(), ServerSideEncryption='AES256')


# ## TEST WRITE FUNCTIONS

# In[10]:


yml_path ="blob_new.yml"
filepath = "sandbox/jscher/"
file = "CBK_MTBC.csv"
df = pd.read_csv('CBK_MIC_complete.csv')

writeS3_csv(df,yml_path,filepath,file)


# In[12]:


yml_path ="blob_new.yml" # CHOOSE YOUR S3 CREDENTIALS AND LOAD THEM USING .YML
filepath = "sandbox/jscher/"
file = "CBK_MIC_complete.parquet"
df = pd.read_csv('CBK_MIC_complete.csv')

writeS3_parquet(dataframe,yml_path,filepath, file)

