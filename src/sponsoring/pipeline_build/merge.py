import pandas as pd
import typer
import logging

logger = logging.getLogger(__name__)

def build_merge(dfs, column_merge= 'deal_id'):
    if any([column_merge not in df.columns for df in dfs]):
        raise typer.BadParameter("column " + column_merge + " not found in both dataframes")
    
    logger.info("Merging the dataframes")

    df1, df2 = dfs[0], dfs[1]
    df_merged = pd.merge(df1,df2,how='inner',on=column_merge)
    
    logger.info("Dataframes successfully merged")

    return(df_merged)
