# Python Utils
import os
import re
import logging
import boto3


def find_updated_files(directory, keyword, number):
    """
    This functions searchs filen in the 'directory' guided by the 'keyword'.
    'number' is the number of path returned
    """
    assert os.path.exists(directory), print(f"path '{directory}' doesn't exists")
    print(os.path.dirname(directory))
    list_files = []
    for f1le in os.listdir(directory):
        if re.search(keyword, f1le):
            list_files.append(f"{directory}/{f1le}")
    # organize files by modified date
    list_files = sorted(list_files, key=os.path.getmtime)
    if len(list_files) > 4:
        deleted_item = list_files.pop()
        os.remove(f"{directory}/{deleted_item}")
        logging.info("Too many files")
        logging.warning(f"file '{deleted_item}' deleted")

    # regresa un lista con los archivos más recientes
    path_update_file = list_files[-number:]
    return path_update_file


def list_files_in_folder_AWS(folder_path):
    """
    This function goes to a folder and list the files that contains
    """
    ak_id = "YOUR ACCESS KEY ID HERE"
    sa_key = "YOUR SECRET ACCESS KEY HERE"
    bucket_name = "YOU BUCKET NAME"

    s3_resource = boto3.resource("s3", aws_access_key_id=ak_id, aws_secret_access_key=sa_key)
    my_bucket = s3_resource.Bucket(bucket_name)

    files = [obj.key for obj in my_bucket.objects.filter(Prefix=folder_path)]

    return files


def upload_AWS(filename_path, destination_path):
    """
    This function tries to 1 upload a file in the destination in ingebau AWS
    Need to be improved to upload many files
    """
    ak_id = "YOUR ACCESS KEY ID HERE"
    sa_key = "YOUR SECRET ACCESS KEY HERE"
    bucket_name = "YOU BUCKET NAME"

    s3_resource = boto3.resource("s3", aws_access_key_id=ak_id, aws_secret_access_key=sa_key)
    my_bucket = s3_resource.Bucket(bucket_name)

    content = open(filename_path, "rb")  # Comprobamos que no esté vacio
    assert content.__sizeof__() != 0, "The file you want to upload doesn't exists"

    items1 = set(list_files_in_folder_AWS(destination_path))  # Initial things in the folder
    path_s3 = f"{destination_path}{filename_path}"
    if path_s3 in items1:
        print("File already exists in S3")

    response = my_bucket.put_object(Key=path_s3, Body=content)
    items2 = set(list_files_in_folder_AWS(destination_path))

    if list(items2.difference(items1))[0] == path_s3:  # Something changed?
        print("Successful upload to AWS ")
    else:
        raise ValueError("Error uploading file or file alreday exists in S3")


def download_AWS(s3_filename, s3_folder):
    """
    This function download the content in ' cloud_filepath', contained in s3 bucket of AWS
    If ' cloud_filepath' is a folder, all files it contains are downloaded
    """
    ak_id = "YOUR ACCESS KEY ID HERE"
    sa_key = "YOUR SECRET ACCESS KEY HERE"
    bucket_name = "YOU BUCKET NAME"

    s3_resource = boto3.resource("s3", aws_access_key_id=ak_id, aws_secret_access_key=sa_key)
    my_bucket = s3_resource.Bucket(bucket_name)

    items1 = set(os.listdir("."))
    s3_files = list_files_in_folder_AWS(s3_folder)
    for item in s3_files:
        try:
            address, filename = os.path.split(item)
            if filename == s3_filename:
                my_bucket.download_file(item, filename)
        except:
            print(f"{s3_filename} not found. Error downloading file from AWS")

    items2 = set(os.listdir("."))
    if list(items2.difference(items1))[0] == s3_filename:  # Something changed?
        print("Successfully downloaded from AWS ")
    else:
        raise ValueError("File not downloaded")


if __name__ == "__main__":
    # Cargar Archivos
    # upload_AWS(filename_path="ARCHIVO_PRUEBA.pdf", destination_path=found)

    # Descargar archivo
    download_AWS("Contratos MENTA.XLSX", found)
