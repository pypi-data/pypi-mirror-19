from __future__ import print_function

import scattertext.viz
from scattertext import Scalers, ScatterChart
from scattertext import termranking
from scattertext.CSRMatrixTools import CSRMatrixFactory
from scattertext.CorpusFromPandas import CorpusFromPandas
from scattertext.CorpusFromParsedDocuments import CorpusFromParsedDocuments
from scattertext.FastButCrapNLP import fast_but_crap_nlp
from scattertext.IndexStore import IndexStore
from scattertext.ParsedCorpus import ParsedCorpus
from scattertext.Scalers import percentile_ordinal
from scattertext.ScatterChart import ScatterChart
from scattertext.ScatterChartExplorer import ScatterChartExplorer
from scattertext.TermDocMatrix import TermDocMatrix
from scattertext.TermDocMatrixFactory import TermDocMatrixFactory, FeatsFromDoc
from scattertext.TermDocMatrixFilter import TermDocMatrixFilter, filter_bigrams_by_pmis
from scattertext.TermDocMatrixFromPandas import TermDocMatrixFromPandas
from scattertext.termscoring.ScaledFScore import InvalidScalerException
from scattertext.viz import VizDataAdapter, HTMLVisualizationAssembly


def produce_scattertext_html(term_doc_matrix,
                             category,
                             category_name,
                             not_category_name,
                             protocol='https',
                             pmi_filter_thresold=2,
                             minimum_term_frequency=3,
                             max_terms=None,
                             filter_unigrams=False,
                             height_in_pixels=None,
                             width_in_pixels=None,
                             term_ranker=termranking.AbsoluteFrequencyRanker):
	'''Returns html code of visualization.

	Parameters
	----------
	term_doc_matrix : TermDocMatrix
		Corpus to use
	category : str
		name of category column
	category_name: str
		name of category to mine for
	not_category_name: str
		name of everything that isn't in category
	protocol : str
		optional, used prototcol of , http or https
	filter_unigrams : bool
		default False, do we filter unigrams that only occur in one bigram
	width_in_pixels: int
		width of viz in pixels, if None, default to JS's choice
	height_in_pixels: int
		height of viz in pixels, if None, default to JS's choice
	term_ranker : TermRanker
			TermRanker class for determining term frequency ranks.

	Returns
	-------
		str, html of visualization
	'''
	scatter_chart_data = ScatterChart(term_doc_matrix=term_doc_matrix,
	                                  minimum_term_frequency=minimum_term_frequency,
	                                  pmi_threshold_coefficient=pmi_filter_thresold,
	                                  filter_unigrams=filter_unigrams,
	                                  max_terms=max_terms,
	                                  term_ranker=term_ranker) \
		.to_dict(category=category,
	           category_name=category_name,
	           not_category_name=not_category_name,
	           transform=percentile_ordinal)
	html = HTMLVisualizationAssembly(VizDataAdapter(scatter_chart_data),
	                                 width_in_pixels,
	                                 height_in_pixels).to_html(protocol=protocol)
	return html
from scattertext.termranking import OncePerDocFrequencyRanker

def produce_scattertext_explorer(corpus,
                                 category,
                                 category_name,
                                 not_category_name,
                                 protocol='https',
                                 pmi_filter_thresold=2,
                                 minimum_term_frequency=3,
                                 max_terms=None,
                                 filter_unigrams=False,
                                 height_in_pixels=None,
                                 width_in_pixels=None,
                                 max_snippets=None,
                                 max_docs_per_category=None,
                                 metadata=None,
                                 scores=None,
                                 singleScoreMode=False,
                                 use_full_doc=False,
                                 term_ranker=termranking.AbsoluteFrequencyRanker):
	'''Returns html code of visualization.

	Parameters
	----------
	corpus : Corpus
		Corpus to use.
	category : str
		Name of category column as it appears in original data frame.
	category_name : str
		Name of category to use.  E.g., "5-star reviews."
	not_category_name : str
		Name of everything that isn't in category.  E.g., "Below 5-star reviews".
	protocol : str, optional
		Protocol to use.  Either http or https.  Default is https.
	minimum_term_frequency : int, optional
		Minimum number of times word needs to appear to make it into visualization.
	max_terms : int, optional
		Maximum number of terms to include in visualization.
	filter_unigrams : bool
		Default False, do we filter unigrams that only occur in one bigram
	width_in_pixels : int
		Width of viz in pixels, if None, default to JS's choice
	height_in_pixels : int
		Height of viz in pixels, if None, default to JS's choice
  max_snippets : int
    Maximum number of snippets to show when term is clicked.  If None, all are shown.
  max_docs_per_category: None or int
    Maximum number of documents to store per category.  If None, all are stored.
	metadata : list, optional
		list of meta data strings that will be included for each document
	scores : np.array, optional
		Array of term scores or None.
	singleScoreMode : bool, optional
		Label terms based on score vs distance from corner.  Good for topic scores.
	use_full_doc : bool, optional
		Use the full document in snippets.  False by default.
	term_ranker : TermRanker
		TermRanker class for determining term frequency ranks.

	Returns
	-------
		str, html of visualization

	'''
	color = None
	sort_by_dist = True
	if singleScoreMode:
		color = 'd3.interpolatePurples'
		sort_by_dist = False

	scatter_chart_explorer = ScatterChartExplorer(corpus,
	                                              minimum_term_frequency=minimum_term_frequency,
	                                              pmi_threshold_coefficient=pmi_filter_thresold,
	                                              filter_unigrams=filter_unigrams,
	                                              max_terms=max_terms,
	                                              term_ranker=term_ranker)
	scatter_chart_data = scatter_chart_explorer.to_dict(category=category,
	                                                    category_name=category_name,
	                                                    not_category_name=not_category_name,
	                                                    transform=percentile_ordinal,
	                                                    scores=scores,
	                                                    max_docs_per_category=max_docs_per_category,
	                                                    metadata=metadata)
	return HTMLVisualizationAssembly(VizDataAdapter(scatter_chart_data),
	                                 width_in_pixels,
	                                 height_in_pixels,
	                                 max_snippets,
	                                 color,
	                                 sort_by_dist,
	                                 use_full_doc).to_html(protocol=protocol)
