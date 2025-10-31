import pandas as pd

from .topk_indexer import TopkIndexer


class ColumnStandardizer(TopkIndexer):
    
    def run(self, query):
        results = super().run(query)
        
        qtoken_data = self.tokenizer.run(query)
        qdata = pd.DataFrame({
            'query_start_idx': qtoken_data.iloc[results.index.get_level_values('start')]['start_idx'].values,
            'query_end_idx': qtoken_data.iloc[results.index.get_level_values('end') - 1]['end_idx'].values,
        })
        
        db_data = pd.DataFrame([
            [
                db_index, 
                self._data.iloc[db_index]['text'],
                self._path_token_maps[db_index].iloc[db_start]['start_idx'],
                self._path_token_maps[db_index].iloc[db_end - 1]['end_idx'],
            ] 
            for db_index, db_start, db_end \
                in results[['db_index', 'db_start', 'db_end']].itertuples(index=False)
        ], columns=['data_index', 'original', 'original_start', 'original_end'])
        
        results = results[['matching_score', 'matched_len', 'coverage_score', 'harmonic_score']].reset_index(drop=True)
        updated_results = pd.concat([qdata, db_data, results], axis=1)\
                            .set_index(['query_start_idx', 'query_end_idx'])\
                                .rename(columns={'matching_score': 'substring_matching_score'})
        return updated_results
