import numpy as np
from scipy.stats import rankdata

from scattertext.Scalers import percentile_min, percentile_ordinal
from scattertext.TermDocMatrixFilter import filter_bigrams_by_pmis, \
	filter_out_unigrams_that_only_occur_in_one_bigram


class NoWordMeetsTermFrequencyRequirementsError(Exception):
	pass




class ScatterChart:
	def __init__(self,
	             term_doc_matrix,
	             minimum_term_frequency=3,
	             jitter=0,
	             seed=0,
	             pmi_threshold_coefficient=3,
	             filter_unigrams=False):
		'''
		:param term_doc_matrix: TermDocMatrix
		:param minimum_term_frequency: int, minimum times an ngram has to be seen to be included
		:param jitter: float
		:param seed: float
		:param pmi_threshold_coefficient: float, the minimum threshold
		:param filter_unigrams: bool, default False, do we filter unigrams that only occur in one bigram
		:return dataframe, html
		'''
		self.term_doc_matrix = term_doc_matrix
		self.jitter = jitter
		self.minimum_term_frequency = minimum_term_frequency
		self.seed = seed
		self.pmi_threshold_coefficient = pmi_threshold_coefficient
		self.filter_unigrams = filter_unigrams
		np.random.seed(seed)

	def to_dict(self,
	            category,
	            category_name=None,
	            not_category_name=None,
	            scores=None,
	            transform=percentile_ordinal):
		'''
		Returns a dictionary that encodes the scatter chart
		information. The dictionary can be dumped as a json document, and
		used in scattertext.html

		:param category: Category to annotate
		:param category_name: Name of category which will appear on web site.
		:param not_category_name: Name of non-category axis which will appear on web site.
		:param scores: Scores to use.  Default to Scaled F-Score.
		:param transform: Defaults to percentile_ordinal
		:return: dictionary {info: {category_name: ..., not_category_name},
		                     data: {term:, x:frequency [0-1], y:frequency [0-1],
		                            s: score,
		                            cat25k: freq per 25k in category,
		                            ncat25k: freq per 25k in non-category}}
		'''
		all_categories, other_categories = self._get_category_names(category)
		df = self._term_rank_score_and_frequency_df(all_categories, category, scores)
		df['x'], df['y'] = self._get_coordinates_from_transform_and_jitter_frequencies \
			(category, df, other_categories, transform)
		df['not cat freq'] = df[[x for x in other_categories]].sum(axis=1)
		json_df = df[['x', 'y', 'term']]
		self._add_term_freq_to_json_df(json_df, df, category)
		json_df['s'] = percentile_min(df['color_scores'])
		category_terms = list(json_df.sort_values('s')['term'][:10])
		not_category_terms = list(json_df.sort_values('s')['term'][:10])
		if category_name is None:
			category_name = category
		if not_category_name is None:
			not_category_name = 'Not ' + category_name
		j = {'info': {'category_name': category_name.title(),
		              'not_category_name': not_category_name.title(),
		              'category_terms': category_terms,
		              'not_category_terms': not_category_terms}}
		j['data'] = json_df.sort_values(by=['x', 'y', 'term']).to_dict(orient='records')
		return j

	def _add_term_freq_to_json_df(self, json_df, term_freq_df, category):
		json_df['cat25k'] = ((term_freq_df[category + ' freq'] * 1.
		                      / term_freq_df[category + ' freq'].sum()) * 25000)
		json_df['ncat25k'] = ((term_freq_df['not cat freq'] * 1.
		                       / term_freq_df['not cat freq'].sum()) * 25000)
		json_df['cat25k'] = json_df['cat25k'].apply(np.round).astype(np.int)
		json_df['ncat25k'] = json_df['ncat25k'].apply(np.round).astype(np.int)

	def _get_category_names(self, category):
		other_categories = [val + ' freq' for _, val \
		                    in self.term_doc_matrix._category_idx_store.items() \
		                    if val != category]
		all_categories = other_categories + [category + ' freq']
		return all_categories, other_categories

	def draw(self,
	         category,
	         num_top_words_to_annotate=4,
	         words_to_annotate=[],
	         scores=None,
	         transform=percentile_ordinal):
		try:
			import matplotlib.pyplot as plt
		except:
			raise Exception("matplotlib and mpld3 need to be installed to use this function.")
		try:
			from mpld3 import plugins, fig_to_html
		except:
			raise Exception("mpld3 need to be installed to use this function.")
		all_categories, other_categories = self._get_category_names(category)
		df = self._term_rank_score_and_frequency_df(all_categories, category, scores)
		x_data, y_data = self._get_coordinates_from_transform_and_jitter_frequencies \
			(category, df, other_categories, transform)
		df_to_annotate = df[(df['not category score rank'] <= num_top_words_to_annotate)
		                    | (df['category score rank'] <= num_top_words_to_annotate)
		                    | df['term'].isin(words_to_annotate)]
		words = list(df['term'])

		font = {'family': 'sans-serif',
		        'color': 'black',
		        'weight': 'normal',
		        'size': 'large'}

		fig, ax = plt.subplots()
		plt.figure(figsize=(10, 10))
		plt.gcf().subplots_adjust(bottom=0.2)
		plt.gcf().subplots_adjust(right=0.2)

		points = ax.scatter(x_data,
		                    y_data,
		                    c=-df['color_scores'],
		                    cmap='seismic',
		                    s=10,
		                    edgecolors='none',
		                    alpha=0.9)
		tooltip = plugins.PointHTMLTooltip(points,
		                                   ['<span id=a>%s</span>' % w for w in words],
		                                   css='#a {background-color: white;}')
		plugins.connect(fig, tooltip)
		ax.set_ylim([-.2, 1.2])
		ax.set_xlim([-.2, 1.2])
		ax.xaxis.set_ticks([0., 0.5, 1.])
		ax.yaxis.set_ticks([0., 0.5, 1.])
		ax.set_ylabel(category.title() + ' Frequency Percentile', fontdict=font, labelpad=20)
		ax.set_xlabel('Not ' + category.title() + ' Frequency Percentile', fontdict=font, labelpad=20)

		for i, row in df_to_annotate.iterrows():
			# alignment_criteria = row['category score rank'] < row['not category score rank']
			alignment_criteria = i % 2 == 0
			horizontalalignment = 'right' if alignment_criteria else 'left'
			verticalalignment = 'bottom' if alignment_criteria else 'top'
			term = row['term']
			ax.annotate(term,
			            (x_data[i], y_data[i]),
			            size=15,
			            horizontalalignment=horizontalalignment,
			            verticalalignment=verticalalignment,
			            )
		# texts.append(
		# ax.text(row['dem freq scaled'], row['rep freq scaled'], row['word'])
		# )
		# adjust_text(texts, arrowprops=dict(arrowstyle="->", color='r', lw=0.5))
		plt.show()
		return df, fig_to_html(fig)

	def _get_coordinates_from_transform_and_jitter_frequencies(self,
	                                                           category,
	                                                           df,
	                                                           other_categories,
	                                                           transform):
		x_data_raw = transform(df[other_categories].sum(axis=1))
		y_data_raw = transform(df[category + ' freq'])
		x_data = self._add_jitter(x_data_raw)
		y_data = self._add_jitter(y_data_raw)
		return x_data, y_data

	def _add_jitter(self, vec):
		"""
		:param vec: array to jitter
		:return: array, jittered version of arrays
		"""
		if self.jitter == 0:
			return vec
		else:
			to_ret = vec + np.random.rand(1, len(vec))[0] * self.jitter
			return to_ret

	def _term_rank_score_and_frequency_df(self, all_categories, category, scores):
		df = self.term_doc_matrix.get_term_freq_df()
		np.array(self.term_doc_matrix.get_rudder_scores(category))
		df['category score'] = np.array(self.term_doc_matrix.get_rudder_scores(category))
		df['not category score'] = np.sqrt(2) - df['category score']
		df['color_scores'] = self._get_color_scores(category, scores)
		df = filter_bigrams_by_pmis(
			df[df[all_categories].sum(axis=1) > self.minimum_term_frequency],
			threshold_coef=self.pmi_threshold_coefficient
		)
		if self.filter_unigrams:
			df = filter_out_unigrams_that_only_occur_in_one_bigram(df)

		if len(df) == 0:
			raise NoWordMeetsTermFrequencyRequirementsError()
		df['category score rank'] = rankdata(df['category score'], method='ordinal')
		df['not category score rank'] = rankdata(df['not category score'], method='ordinal')
		df = df.reset_index()
		return df

	def _get_color_scores(self, category, scores):
		# type: (str, np.array) -> np.array
		if scores is None:
			return np.array(self.term_doc_matrix.get_scaled_f_scores(category))
		return scores



