import pandas as pd
import typer
import logging

logger = logging.getLogger(__name__)

def build_merge(dfs, column_merge= 'deal_id'):

    if not dfs:
        raise typer.BadParameter("no dataframes found")
    
    elif len(dfs) == 1:
        logger.info("Only one dataframe found, no need to merge")
        
        df_merged = dfs[0]
    
    else:
        if any([column_merge not in df.columns for df in dfs]):
            raise typer.BadParameter("column " + column_merge + " not found in every dataframe")
    
        logger.info(f"{len(dfs)} dataframes found. Merging the dataframes")

        df1 = dfs[0] 
        df_merged = pd.merge(df1, build_merge(dfs[1:],column_merge=column_merge),how='inner',on=column_merge)
        
        logger.info("Dataframes successfully merged")

    return(df_merged)