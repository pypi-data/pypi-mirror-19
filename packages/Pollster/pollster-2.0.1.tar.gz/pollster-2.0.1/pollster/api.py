import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from collections import defaultdict

from .configuration import Configuration
from .api_client import ApiClient


class Api(object):
    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def charts_get(self, **kwargs):
        """
        Charts
        Returns a list of Charts, ordered by creation date (newest first).  A Chart is chosen by Pollster editors. One example is \"Obama job approval - Democrats\". It is always based upon a single Question.  Users should strongly consider basing their analysis on Questions instead. Charts are derived data; Pollster editors publish them and change them as editorial priorities change. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.charts_get(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str cursor: Special string to index into the Array
        :param str tags: Comma-separated list of tag slugs. Only Charts with one or more of these tags and Charts based on Questions with one or more of these tags will be returned.
        :param date election_date: Date of an election, in YYYY-MM-DD format. Only Charts based on Questions pertaining to an election on this date will be returned.
        :return: InlineResponse200
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.charts_get_with_http_info(**kwargs)
        else:
            (data) = self.charts_get_with_http_info(**kwargs)
            return data

    def charts_get_with_http_info(self, **kwargs):
        """
        Charts
        Returns a list of Charts, ordered by creation date (newest first).  A Chart is chosen by Pollster editors. One example is \"Obama job approval - Democrats\". It is always based upon a single Question.  Users should strongly consider basing their analysis on Questions instead. Charts are derived data; Pollster editors publish them and change them as editorial priorities change. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.charts_get_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str cursor: Special string to index into the Array
        :param str tags: Comma-separated list of tag slugs. Only Charts with one or more of these tags and Charts based on Questions with one or more of these tags will be returned.
        :param date election_date: Date of an election, in YYYY-MM-DD format. Only Charts based on Questions pertaining to an election on this date will be returned.
        :return: InlineResponse200
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cursor', 'tags', 'election_date']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method charts_get" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        resource_path = '/charts'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'cursor' in params:
            query_params['cursor'] = params['cursor']
        if 'tags' in params:
            query_params['tags'] = params['tags']
        if 'election_date' in params:
            query_params['election_date'] = params['election_date']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/xml'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='InlineResponse200',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            _request_timeout=params.get('_request_timeout'),
                                            collection_formats=collection_formats)

    def charts_slug_get(self, slug, **kwargs):
        """
        Chart
        A Chart is chosen by Pollster editors. One example is \"Obama job approval - Democrats\". It is always based upon a single Question.  Users should strongly consider basing their analysis on Questions instead. Charts are derived data; Pollster editors publish them and change them as editorial priorities change. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.charts_slug_get(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique identifier for a Chart (required)
        :return: Chart
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.charts_slug_get_with_http_info(slug, **kwargs)
        else:
            (data) = self.charts_slug_get_with_http_info(slug, **kwargs)
            return data

    def charts_slug_get_with_http_info(self, slug, **kwargs):
        """
        Chart
        A Chart is chosen by Pollster editors. One example is \"Obama job approval - Democrats\". It is always based upon a single Question.  Users should strongly consider basing their analysis on Questions instead. Charts are derived data; Pollster editors publish them and change them as editorial priorities change. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.charts_slug_get_with_http_info(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique identifier for a Chart (required)
        :return: Chart
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['slug']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method charts_slug_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'slug' is set
        if ('slug' not in params) or (params['slug'] is None):
            raise ValueError("Missing the required parameter `slug` when calling `charts_slug_get`")


        collection_formats = {}

        resource_path = '/charts/{slug}'.replace('{format}', 'json')
        path_params = {}
        if 'slug' in params:
            path_params['slug'] = params['slug']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/xml'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Chart',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            _request_timeout=params.get('_request_timeout'),
                                            collection_formats=collection_formats)

    def charts_slug_pollster_chart_poll_questions_tsv_get(self, slug, **kwargs):
        """
        One row per poll plotted on a Chart
        Derived data presented on a Pollster Chart.  Rules for which polls and responses are plotted on a chart can shift over time. Here are some examples of behaviors Pollster has used in the past:  * We've omitted \"Registered Voters\" from a chart when \"Likely Voters\"   responded to the same poll question. * We've omitted poll questions that asked about Gary Johnson on a   chart about Trump v Clinton. * We've omitted polls when their date ranges overlapped. * We've omitted labels (and their responses) for dark-horse   candidates.  In short: this endpoint is about Pollster, not the polls. For complete data, use a TSV from the Questions API.  The response follows the exact same format as `questions/{slug}/poll-responses-clean.tsv`, which you should strongly consider before settling on the Chart TSV. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.charts_slug_pollster_chart_poll_questions_tsv_get(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique Chart identifier. For example: `obama-job-approval` (required)
        :return: InlineResponse2001
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.charts_slug_pollster_chart_poll_questions_tsv_get_with_http_info(slug, **kwargs)
        else:
            (data) = self.charts_slug_pollster_chart_poll_questions_tsv_get_with_http_info(slug, **kwargs)
            return data

    def charts_slug_pollster_chart_poll_questions_tsv_get_with_http_info(self, slug, **kwargs):
        """
        One row per poll plotted on a Chart
        Derived data presented on a Pollster Chart.  Rules for which polls and responses are plotted on a chart can shift over time. Here are some examples of behaviors Pollster has used in the past:  * We've omitted \"Registered Voters\" from a chart when \"Likely Voters\"   responded to the same poll question. * We've omitted poll questions that asked about Gary Johnson on a   chart about Trump v Clinton. * We've omitted polls when their date ranges overlapped. * We've omitted labels (and their responses) for dark-horse   candidates.  In short: this endpoint is about Pollster, not the polls. For complete data, use a TSV from the Questions API.  The response follows the exact same format as `questions/{slug}/poll-responses-clean.tsv`, which you should strongly consider before settling on the Chart TSV. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.charts_slug_pollster_chart_poll_questions_tsv_get_with_http_info(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique Chart identifier. For example: `obama-job-approval` (required)
        :return: InlineResponse2001
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['slug']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method charts_slug_pollster_chart_poll_questions_tsv_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'slug' is set
        if ('slug' not in params) or (params['slug'] is None):
            raise ValueError("Missing the required parameter `slug` when calling `charts_slug_pollster_chart_poll_questions_tsv_get`")


        collection_formats = {}

        resource_path = '/charts/{slug}/pollster-chart-poll-questions.tsv'.replace('{format}', 'json')
        path_params = {}
        if 'slug' in params:
            path_params['slug'] = params['slug']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['text/tab-separated-values'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='InlineResponse2001',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            pandas_read_table_kwargs={
                                                'dtype': {
                                                    # float64 columns will be detected automatically
                                                    'poll_slug': 'str',
                                                    'survey_house': 'str',
                                                    'question_text': 'str',
                                                    'sample_subpopulation': 'str',
                                                    'observations': 'int',
                                                    'margin_of_error': 'float',
                                                    'mode': 'str',
                                                    'partisanship': 'str',
                                                    'partisan_affiliation': 'str'
                                                },
                                                'parse_dates': [ 'start_date', 'end_date' ]
                                            },
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            _request_timeout=params.get('_request_timeout'),
                                            collection_formats=collection_formats)

    def charts_slug_pollster_trendlines_tsv_get(self, slug, **kwargs):
        """
        Estimates of what the polls suggest about trends
        Derived data presented on a Pollster Chart.  The trendlines on a Pollster chart don't add up to 100: we calculate each label's trendline separately.  Use the `charts/{slug}` response's `chart.pollster_estimates[0].algorithm` to find the algorithm Pollster used to generate these estimates.  Pollster recalculates trendlines every time a new poll is entered. It also recalculates trendlines daily if they use the `bayesian-kallman` algorithm, because that algorithm's output changes depending on the end date. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.charts_slug_pollster_trendlines_tsv_get(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique Chart identifier. For example: `obama-job-approval` (required)
        :return: InlineResponse2002
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.charts_slug_pollster_trendlines_tsv_get_with_http_info(slug, **kwargs)
        else:
            (data) = self.charts_slug_pollster_trendlines_tsv_get_with_http_info(slug, **kwargs)
            return data

    def charts_slug_pollster_trendlines_tsv_get_with_http_info(self, slug, **kwargs):
        """
        Estimates of what the polls suggest about trends
        Derived data presented on a Pollster Chart.  The trendlines on a Pollster chart don't add up to 100: we calculate each label's trendline separately.  Use the `charts/{slug}` response's `chart.pollster_estimates[0].algorithm` to find the algorithm Pollster used to generate these estimates.  Pollster recalculates trendlines every time a new poll is entered. It also recalculates trendlines daily if they use the `bayesian-kallman` algorithm, because that algorithm's output changes depending on the end date. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.charts_slug_pollster_trendlines_tsv_get_with_http_info(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique Chart identifier. For example: `obama-job-approval` (required)
        :return: InlineResponse2002
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['slug']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method charts_slug_pollster_trendlines_tsv_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'slug' is set
        if ('slug' not in params) or (params['slug'] is None):
            raise ValueError("Missing the required parameter `slug` when calling `charts_slug_pollster_trendlines_tsv_get`")


        collection_formats = {}

        resource_path = '/charts/{slug}/pollster-trendlines.tsv'.replace('{format}', 'json')
        path_params = {}
        if 'slug' in params:
            path_params['slug'] = params['slug']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['text/tab-separated-values'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='InlineResponse2002',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            pandas_read_table_kwargs={
                                                'dtype': {
                                                    'label': 'str',
                                                    'value': 'float64',
                                                    'low': 'float64',
                                                    'high': 'float64',
                                                },
                                                'parse_dates': [ 'date' ],
                                            },
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            _request_timeout=params.get('_request_timeout'),
                                            collection_formats=collection_formats)

    def polls_get(self, **kwargs):
        """
        Polls
        A Poll on Pollster is a collection of questions and responses published by a reputable survey house. This endpoint provides raw data from the survey house, plus Pollster-provided metadata about each question.  Pollster editors don't include every question when they enter Polls, and they don't necessarily enter every subpopulation for the responses they _do_ enter. They make editorial decisions about which questions belong in the database.  The response will contain a maximum of 25 Poll objects, even if the database contains more than 25 polls. Use the `next_cursor` parameter to fetch the rest, 25 Polls at a time. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.polls_get(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str cursor: Special string to index into the Array
        :param str tags: Comma-separated list of Question tag names; only Polls containing Questions with any of the given tags will be returned.
        :param str question: Question slug; only Polls that ask that Question will be returned.
        :param str sort: If `updated_at`, sort the most recently updated Poll first. (This can cause race conditions when used with `cursor`.) Otherwise, sort by most recently _entered_ Poll first.
        :return: InlineResponse2003
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.polls_get_with_http_info(**kwargs)
        else:
            (data) = self.polls_get_with_http_info(**kwargs)
            return data

    def polls_get_with_http_info(self, **kwargs):
        """
        Polls
        A Poll on Pollster is a collection of questions and responses published by a reputable survey house. This endpoint provides raw data from the survey house, plus Pollster-provided metadata about each question.  Pollster editors don't include every question when they enter Polls, and they don't necessarily enter every subpopulation for the responses they _do_ enter. They make editorial decisions about which questions belong in the database.  The response will contain a maximum of 25 Poll objects, even if the database contains more than 25 polls. Use the `next_cursor` parameter to fetch the rest, 25 Polls at a time. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.polls_get_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str cursor: Special string to index into the Array
        :param str tags: Comma-separated list of Question tag names; only Polls containing Questions with any of the given tags will be returned.
        :param str question: Question slug; only Polls that ask that Question will be returned.
        :param str sort: If `updated_at`, sort the most recently updated Poll first. (This can cause race conditions when used with `cursor`.) Otherwise, sort by most recently _entered_ Poll first.
        :return: InlineResponse2003
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cursor', 'tags', 'question', 'sort']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method polls_get" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        resource_path = '/polls'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'cursor' in params:
            query_params['cursor'] = params['cursor']
        if 'tags' in params:
            query_params['tags'] = params['tags']
        if 'question' in params:
            query_params['question'] = params['question']
        if 'sort' in params:
            query_params['sort'] = params['sort']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/xml'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='InlineResponse2003',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            _request_timeout=params.get('_request_timeout'),
                                            collection_formats=collection_formats)

    def polls_slug_get(self, slug, **kwargs):
        """
        Poll
        A Poll on Pollster is a collection of questions and responses published by a reputable survey house. This endpoint provides raw data from the survey house, plus Pollster-provided metadata about each question.  Pollster editors don't include every question when they enter Polls, and they don't necessarily enter every subpopulation for the responses they _do_ enter. They make editorial decisions about which questions belong in the database. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.polls_slug_get(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique Poll identifier. For example: `gallup-26892`. (required)
        :return: Poll
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.polls_slug_get_with_http_info(slug, **kwargs)
        else:
            (data) = self.polls_slug_get_with_http_info(slug, **kwargs)
            return data

    def polls_slug_get_with_http_info(self, slug, **kwargs):
        """
        Poll
        A Poll on Pollster is a collection of questions and responses published by a reputable survey house. This endpoint provides raw data from the survey house, plus Pollster-provided metadata about each question.  Pollster editors don't include every question when they enter Polls, and they don't necessarily enter every subpopulation for the responses they _do_ enter. They make editorial decisions about which questions belong in the database. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.polls_slug_get_with_http_info(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique Poll identifier. For example: `gallup-26892`. (required)
        :return: Poll
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['slug']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method polls_slug_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'slug' is set
        if ('slug' not in params) or (params['slug'] is None):
            raise ValueError("Missing the required parameter `slug` when calling `polls_slug_get`")


        collection_formats = {}

        resource_path = '/polls/{slug}'.replace('{format}', 'json')
        path_params = {}
        if 'slug' in params:
            path_params['slug'] = params['slug']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/xml'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Poll',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            _request_timeout=params.get('_request_timeout'),
                                            collection_formats=collection_formats)

    def questions_get(self, **kwargs):
        """
        Questions
        Returns a list of Questions.  A Question is chosen by Pollster editors. One example is \"Obama job approval\".  Different survey houses may publish varying phrasings (\"Do you approve or disapprove\" vs \"What do you think of the job\") and prompt readers with varying responses (one poll might have \"Approve\" and \"Disapprove\"; another poll might have \"Strongly approve\" and \"Somewhat approve\"). Those variations do not appear in this API endpoint. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.questions_get(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str cursor: Special string to index into the Array
        :param str tags: Comma-separated list of Question tag names. Only Questions with one or more of these tags will be returned.
        :param date election_date: Date of an election, in YYYY-MM-DD format. Only Questions pertaining to an election on this date will be returned.
        :return: InlineResponse2004
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.questions_get_with_http_info(**kwargs)
        else:
            (data) = self.questions_get_with_http_info(**kwargs)
            return data

    def questions_get_with_http_info(self, **kwargs):
        """
        Questions
        Returns a list of Questions.  A Question is chosen by Pollster editors. One example is \"Obama job approval\".  Different survey houses may publish varying phrasings (\"Do you approve or disapprove\" vs \"What do you think of the job\") and prompt readers with varying responses (one poll might have \"Approve\" and \"Disapprove\"; another poll might have \"Strongly approve\" and \"Somewhat approve\"). Those variations do not appear in this API endpoint. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.questions_get_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str cursor: Special string to index into the Array
        :param str tags: Comma-separated list of Question tag names. Only Questions with one or more of these tags will be returned.
        :param date election_date: Date of an election, in YYYY-MM-DD format. Only Questions pertaining to an election on this date will be returned.
        :return: InlineResponse2004
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cursor', 'tags', 'election_date']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method questions_get" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        resource_path = '/questions'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'cursor' in params:
            query_params['cursor'] = params['cursor']
        if 'tags' in params:
            query_params['tags'] = params['tags']
        if 'election_date' in params:
            query_params['election_date'] = params['election_date']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/xml'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='InlineResponse2004',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            _request_timeout=params.get('_request_timeout'),
                                            collection_formats=collection_formats)

    def questions_slug_get(self, slug, **kwargs):
        """
        Question
        A Question is chosen by Pollster editors. One example is \"Obama job approval\".  Different survey houses may publish varying phrasings (\"Do you approve or disapprove\" vs \"What do you think of the job\") and prompt readers with varying responses (one poll might have \"Approve\" and \"Disapprove\"; another poll might have \"Strongly approve\" and \"Somewhat approve\"). Those variations do not appear in this API endpoint. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.questions_slug_get(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique Question identifier. For example: `00c -Pres (44) Obama - Job Approval - National`. (Remember to URL-encode this parameter when querying.) (required)
        :return: Question
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.questions_slug_get_with_http_info(slug, **kwargs)
        else:
            (data) = self.questions_slug_get_with_http_info(slug, **kwargs)
            return data

    def questions_slug_get_with_http_info(self, slug, **kwargs):
        """
        Question
        A Question is chosen by Pollster editors. One example is \"Obama job approval\".  Different survey houses may publish varying phrasings (\"Do you approve or disapprove\" vs \"What do you think of the job\") and prompt readers with varying responses (one poll might have \"Approve\" and \"Disapprove\"; another poll might have \"Strongly approve\" and \"Somewhat approve\"). Those variations do not appear in this API endpoint. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.questions_slug_get_with_http_info(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique Question identifier. For example: `00c -Pres (44) Obama - Job Approval - National`. (Remember to URL-encode this parameter when querying.) (required)
        :return: Question
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['slug']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method questions_slug_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'slug' is set
        if ('slug' not in params) or (params['slug'] is None):
            raise ValueError("Missing the required parameter `slug` when calling `questions_slug_get`")


        collection_formats = {}

        resource_path = '/questions/{slug}'.replace('{format}', 'json')
        path_params = {}
        if 'slug' in params:
            path_params['slug'] = params['slug']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/xml'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Question',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            _request_timeout=params.get('_request_timeout'),
                                            collection_formats=collection_formats)

    def questions_slug_poll_responses_clean_tsv_get(self, slug, **kwargs):
        """
        One row of response values per PollQuestion+Subpopulation concerning the given Question
        We include one TSV column per response label. See `questions/{slug}` for the Question's list of response labels, which are chosen by Pollster editors. Each row represents a single PollQuestion+Subpopulation. The value for each label column is the sum of the PollQuestion+Subpopulation responses that map to that `pollster_label`. For instance, on a hypothetical row, the `Approve` column might be the sum of that poll's `Strongly Approve` and `Somewhat Approve`. After the first TSV columns -- which are always response labels -- the next column will be `poll_slug`. `poll_slug` and subsequent columns are described in this API documentation. During the lifetime of a Question, Pollster editors may add, rename or reorder response labels. Such edits will change the TSV column headers. Column headers after `poll_slug` are never reordered or edited (but we may add new column headers). Sometimes a Poll may ask the same Question twice, leading to two similar rows with different values. Those rows will differ by `question_text` or by the set of response labels that have values.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.questions_slug_poll_responses_clean_tsv_get(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique Question identifier. For example: `00c -Pres (44) Obama - Job Approval - National`. (Remember to URL-encode this parameter when querying.) (required)
        :return: InlineResponse2001
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.questions_slug_poll_responses_clean_tsv_get_with_http_info(slug, **kwargs)
        else:
            (data) = self.questions_slug_poll_responses_clean_tsv_get_with_http_info(slug, **kwargs)
            return data

    def questions_slug_poll_responses_clean_tsv_get_with_http_info(self, slug, **kwargs):
        """
        One row of response values per PollQuestion+Subpopulation concerning the given Question
        We include one TSV column per response label. See `questions/{slug}` for the Question's list of response labels, which are chosen by Pollster editors. Each row represents a single PollQuestion+Subpopulation. The value for each label column is the sum of the PollQuestion+Subpopulation responses that map to that `pollster_label`. For instance, on a hypothetical row, the `Approve` column might be the sum of that poll's `Strongly Approve` and `Somewhat Approve`. After the first TSV columns -- which are always response labels -- the next column will be `poll_slug`. `poll_slug` and subsequent columns are described in this API documentation. During the lifetime of a Question, Pollster editors may add, rename or reorder response labels. Such edits will change the TSV column headers. Column headers after `poll_slug` are never reordered or edited (but we may add new column headers). Sometimes a Poll may ask the same Question twice, leading to two similar rows with different values. Those rows will differ by `question_text` or by the set of response labels that have values.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.questions_slug_poll_responses_clean_tsv_get_with_http_info(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique Question identifier. For example: `00c -Pres (44) Obama - Job Approval - National`. (Remember to URL-encode this parameter when querying.) (required)
        :return: InlineResponse2001
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['slug']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method questions_slug_poll_responses_clean_tsv_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'slug' is set
        if ('slug' not in params) or (params['slug'] is None):
            raise ValueError("Missing the required parameter `slug` when calling `questions_slug_poll_responses_clean_tsv_get`")


        collection_formats = {}

        resource_path = '/questions/{slug}/poll-responses-clean.tsv'.replace('{format}', 'json')
        path_params = {}
        if 'slug' in params:
            path_params['slug'] = params['slug']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['text/tab-separated-values'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='InlineResponse2001',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            pandas_read_table_kwargs={
                                                'dtype': {
                                                    # float64 columns will be detected automatically
                                                    'poll_slug': 'str',
                                                    'survey_house': 'str',
                                                    'question_text': 'str',
                                                    'sample_subpopulation': 'str',
                                                    'observations': 'int',
                                                    'margin_of_error': 'float',
                                                    'mode': 'str',
                                                    'partisanship': 'str',
                                                    'partisan_affiliation': 'str'
                                                },
                                                'parse_dates': [ 'start_date', 'end_date' ]
                                            },
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            _request_timeout=params.get('_request_timeout'),
                                            collection_formats=collection_formats)

    def questions_slug_poll_responses_raw_tsv_get(self, slug, **kwargs):
        """
        One row per PollQuestion+Subpopulation+Response concerning the given Question (Large)
        Raw data from which we derived `poll-responses-clean.tsv`.  Each row represents a single PollQuestion+Subpopulation+Response. See the Poll API for a description of these terms.  Group results by `(poll_slug, subpopulation, question_text)`: that's how the survey houses group them.  This response can be several megabytes large. We encourage you to consider `poll-responses-clean.tsv` instead. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.questions_slug_poll_responses_raw_tsv_get(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique Question identifier. For example: `00c -Pres (44) Obama - Job Approval - National`. (Remember to URL-encode this parameter when querying.) (required)
        :return: InlineResponse2005
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.questions_slug_poll_responses_raw_tsv_get_with_http_info(slug, **kwargs)
        else:
            (data) = self.questions_slug_poll_responses_raw_tsv_get_with_http_info(slug, **kwargs)
            return data

    def questions_slug_poll_responses_raw_tsv_get_with_http_info(self, slug, **kwargs):
        """
        One row per PollQuestion+Subpopulation+Response concerning the given Question (Large)
        Raw data from which we derived `poll-responses-clean.tsv`.  Each row represents a single PollQuestion+Subpopulation+Response. See the Poll API for a description of these terms.  Group results by `(poll_slug, subpopulation, question_text)`: that's how the survey houses group them.  This response can be several megabytes large. We encourage you to consider `poll-responses-clean.tsv` instead. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.questions_slug_poll_responses_raw_tsv_get_with_http_info(slug, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str slug: Unique Question identifier. For example: `00c -Pres (44) Obama - Job Approval - National`. (Remember to URL-encode this parameter when querying.) (required)
        :return: InlineResponse2005
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['slug']
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method questions_slug_poll_responses_raw_tsv_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'slug' is set
        if ('slug' not in params) or (params['slug'] is None):
            raise ValueError("Missing the required parameter `slug` when calling `questions_slug_poll_responses_raw_tsv_get`")


        collection_formats = {}

        resource_path = '/questions/{slug}/poll-responses-raw.tsv'.replace('{format}', 'json')
        path_params = {}
        if 'slug' in params:
            path_params['slug'] = params['slug']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['text/tab-separated-values'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='InlineResponse2005',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            pandas_read_table_kwargs={
                                                'dtype': {
                                                    'response_text': 'str',
                                                    'pollster_label': 'str',
                                                    'value': 'float64',
                                                    'poll_slug': 'str',
                                                    'survey_house': 'str',
                                                    'question_text': 'str',
                                                    'sample_subpopulation': 'str',
                                                    'observations': 'int',
                                                    'margin_of_error': 'float',
                                                    'mode': 'str',
                                                    'partisanship': 'str',
                                                    'partisan_affiliation': 'str'
                                                },
                                                'parse_dates': [ 'start_date', 'end_date' ]
                                            },
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            _request_timeout=params.get('_request_timeout'),
                                            collection_formats=collection_formats)

    def tags_get(self, **kwargs):
        """
        Tags
        Returns the list of Tags.  A Tag can apply to any number of Charts and Questions; Charts and Questions, in turn, can have any number of Tags.  Tags all look `like-this`: lowercase letters, numbers and hyphens. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.tags_get(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: list[Tag]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('callback'):
            return self.tags_get_with_http_info(**kwargs)
        else:
            (data) = self.tags_get_with_http_info(**kwargs)
            return data

    def tags_get_with_http_info(self, **kwargs):
        """
        Tags
        Returns the list of Tags.  A Tag can apply to any number of Charts and Questions; Charts and Questions, in turn, can have any number of Tags.  Tags all look `like-this`: lowercase letters, numbers and hyphens. 

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.tags_get_with_http_info(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: list[Tag]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []
        all_params.append('callback')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method tags_get" % key
                )
            params[key] = val
        del params['kwargs']


        collection_formats = {}

        resource_path = '/tags'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json', 'text/xml'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type([])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='list[Tag]',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'),
                                            _return_http_data_only=params.get('_return_http_data_only'),
                                            _preload_content=params.get('_preload_content', True),
                                            _request_timeout=params.get('_request_timeout'),
                                            collection_formats=collection_formats)

