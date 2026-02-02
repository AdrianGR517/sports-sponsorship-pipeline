from azure.storage.blob import ContainerClient
import pandas as pd
import os
import typer
import logging

logger = logging.getLogger(__name__)

os.makedirs('out',exist_ok=True)

def build_load(route: str, source: str = 'folder'):
    if source == 'folder':
        logger.info(f"Loading from folder {route}")
        dfs = list()
        for file in os.listdir(route):
            path = route + '/' + file
            file_extension = file.split('.')[-1]
            if file_extension == 'parquet':
                dfs.append(pd.read_parquet(path,engine='pyarrow'))
            elif file_extension == 'csv':
                dfs.append(pd.read_csv(path,engine='pyarrow'))
        if not dfs:
            raise typer.BadParameter("no files found in .parquet or .csv format")
        logger.info("Data successfully loaded")
        return(dfs)
    
    elif source == 'blob':
        destination = 'out/.raw_cache'
        os.makedirs(destination,exist_ok=True)

        container = ContainerClient.from_container_url(route)
        logger.info(f"Downloading from {route}")

        for blob in container.list_blobs():
            print(f"Downloading: {blob.name}")

            blob_client = container.get_blob_client(blob)
            local_path = os.path.join(destination, blob.name)

            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            with open(local_path, "wb") as f:
                stream = blob_client.download_blob()
                for chunk in stream.chunks():
                    f.write(chunk)
        logger.info("Data downloaded from blob")
        return(build_load(route=destination))
    
    else:
        raise typer.BadParameter("source must be 'folder' or 'blob'. Default value is 'folder'")