"""Ground analysis in available sources and validate structured requirements."""
from copy import deepcopy
from datetime import datetime, timezone

from .data import DICTIONARY


def runtime_dictionary():
    dictionary = deepcopy(DICTIONARY)
    # Evaluation boundaries describe an experiment, not runtime data availability.
    dictionary['policy'] = {key: value for key, value in dictionary['policy'].items()
                            if not key.startswith('benchmark_')}
    return dictionary


def planning_context(db, retriever, question, remaining):
    dictionary = runtime_dictionary()
    markets = db.query('SELECT * FROM coverage', timeout=min(15, remaining())).rows
    events = db.query('SELECT MIN(time) AS first_event_utc, MAX(time) AS last_event_utc, '
                      'COUNT(*) AS event_rows FROM liquidation_events', timeout=min(15, remaining())).rows[0]
    candidates = retriever.search(question)
    return {
        'question': question,
        'dictionary': dictionary,
        'availability': {
            'market_hourly': markets,
            'liquidation_events': events,
            'interpretation': 'These are observed timestamp bounds, not guarantees of gap-free coverage. '
                              'The last event timestamp is not the collection cutoff. Do not infer '
                              'missing events or a partial month from an event timestamp alone. '
                              'Query the requested interval to report counts in the loaded dataset.',
        },
        'document_evidence': [{key: doc[key] for key in ('id', 'title', 'url', 'text')} for doc in candidates],
    }


def analysis_errors(spec):
    errors = []
    if not isinstance(spec.kind, str) or spec.kind not in {'docs', 'data', 'mixed', 'unanswerable'}:
        errors.append('kind must be docs, data, mixed or unanswerable')
    for key in ('metric', 'unit', 'aggregation', 'grain', 'retrieval_query', 'clarification'):
        if not isinstance(getattr(spec, key), str):
            errors.append(f'{key} must be a string')
    if not isinstance(spec.assets, list) or any(not isinstance(asset, str) for asset in spec.assets):
        errors.append('assets must be a list of strings')
    dates = {}
    for key in ('start', 'end'):
        value = getattr(spec, key)
        if value is None:
            continue
        try:
            dates[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
            if dates[key].tzinfo is None:
                dates[key] = dates[key].replace(tzinfo=timezone.utc)
        except (ValueError, TypeError, AttributeError):
            errors.append(f'{key} must be an ISO date or null')
    if len(dates) == 2 and dates['end'] <= dates['start']:
        errors.append('end must be later than start; intervals are [start, end)')
    if errors or spec.clarification or spec.kind not in {'data', 'mixed'}:
        return errors
    if spec.metric in {'transactions', 'events'} and spec.unit not in {'', 'count'}:
        errors.append('Transaction/event counts require unit=count, not USD')
    if spec.metric in {'supplied_usd', 'borrowed_usd', 'liquidation_usd'} and spec.unit not in {'', 'USD'}:
        errors.append('USD metrics cannot use unit=count; choose the metric from the original question')
    if spec.metric == 'transactions' and spec.aggregation not in {'', 'count_distinct', 'compare'}:
        errors.append('Transaction counts require distinct tx_hash aggregation')
    if spec.metric == 'events' and spec.aggregation not in {'', 'count', 'compare'}:
        errors.append('Event counts require event-row counting, not USD aggregation')
    return errors
