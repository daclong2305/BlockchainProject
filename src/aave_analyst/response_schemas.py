"""Role output contracts for llama.cpp schema-constrained decoding."""


def object_schema(properties, required=None):
    return {'type': 'object', 'properties': properties,
            'required': list(properties) if required is None else required, 'additionalProperties': False}


STRING = {'type': 'string'}
PLAN_FIELDS = {
    'kind': {'type': 'string', 'enum': ['data', 'mixed', 'docs', 'unanswerable']},
    'metric': {'type': 'string', 'enum': ['supplied_usd', 'borrowed_usd', 'events', 'transactions', 'liquidation_usd', 'other']},
    'assets': {'type': 'array', 'items': {'type': 'string', 'enum': ['DAI', 'USDC', 'USDT', 'USDe', 'WETH']}},
    'start': {'type': ['string', 'null']}, 'end': {'type': ['string', 'null']},
    'unit': {'type': 'string', 'enum': ['USD', 'count', 'other']},
    'aggregation': {'type': 'string', 'enum': ['snapshot', 'average', 'min', 'max', 'count', 'count_distinct', 'compare', 'sum']},
    'grain': {'type': 'string', 'enum': ['hour', 'day', 'month', 'quarter', 'none']},
    'retrieval_query': STRING, 'clarification': STRING,
}


def plan_variant(metrics, kinds):
    # Decode the metric first, then constrain routing consistently with it.
    # This contract contains no question-specific dates, SQL or reference answer.
    properties = {'metric': {'type': 'string', 'enum': metrics},
                  'kind': {'type': 'string', 'enum': kinds}}
    properties.update({key: value for key, value in PLAN_FIELDS.items() if key not in properties})
    return object_schema(properties)


PLAN = {'anyOf': [
    plan_variant(['supplied_usd', 'borrowed_usd', 'events', 'transactions', 'liquidation_usd'], ['data', 'mixed']),
    plan_variant(['other'], ['docs', 'unanswerable']),
]}
REVIEW = object_schema({'issues': {'type': 'array', 'items': object_schema({
    'code': STRING, 'message': STRING,
    'action': {'type': 'string', 'enum': ['sql', 'answer', 'retrieve', 'stop']},
})}})
NUMERIC = object_schema({'value': {'type': 'number'},
                         'unit': {'type': 'string', 'enum': ['USD', 'count', 'other']},
                         'evidence_id': STRING, 'row': {'type': 'integer', 'minimum': 0},
                         'column': STRING})
ANSWER = object_schema({'answer': STRING, 'refused': {'type': 'boolean'},
                        'claims': {'type': 'array', 'items': object_schema({
                            'text': STRING, 'citations': {'type': 'array', 'items': STRING},
                            'numeric': NUMERIC}, required=['text', 'citations'])}})
SCHEMAS = {'plan': PLAN, 'plan_review': PLAN, 'sql': object_schema({'sql': STRING}),
           'answer': ANSWER, 'repair': object_schema({'sql': STRING, 'retrieval_query': STRING}),
           'sql_review': REVIEW, 'claim_review': REVIEW, 'generic_review': REVIEW}
