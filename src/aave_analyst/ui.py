"""Read-only Streamlit presentation for recorded research results.

No query execution, model calls, verdict assignment or mutation of results.
"""
import json
from pathlib import Path

import pandas as pd
import sqlglot
import streamlit as st


def answer_for_display(result):
    """Separate the backend's appended diagnostics without editing the record."""
    answer = result['draft'].get('answer', '')
    issues = result.get('issues', [])
    if result.get('status') == 'unverified' and issues:
        suffix = '\n\nChưa thể xác minh đầy đủ: ' + '; '.join(issue['message'] for issue in issues)
        if answer.endswith(suffix):
            return answer[:-len(suffix)]
    return answer


def render_evidence(draft, index, root):
    st.markdown('**Bằng chứng**')
    data_tab, documents_tab, claims_tab = st.tabs(['Dữ liệu & SQL', 'Tài liệu', 'Dẫn chứng'])
    with data_tab:
        spec = draft.get('spec') or {}
        scope = []
        if spec.get('assets'):
            scope.append('Tài sản: ' + ', '.join(spec['assets']))
        if spec.get('start') or spec.get('end'):
            scope.append(f"UTC: [{spec.get('start') or 'không nêu'}, {spec.get('end') or 'không nêu'})")
        if spec.get('unit'):
            scope.append('Đơn vị: ' + spec['unit'])
        if scope:
            st.caption('Phạm vi từ bước phân tích · ' + ' · '.join(scope))
        query = draft.get('query_result')
        if query is not None:
            rows = query.get('rows', [])
            st.caption(f"SQL1 · {len(rows):,} dòng hiển thị · {len(query.get('columns', []))} cột")
            if rows:
                st.dataframe(pd.DataFrame(rows), width='stretch', hide_index=True,
                             height=min(420, 38 + 35 * len(rows)), key=f'query_{index}')
            else:
                st.info('Truy vấn không trả về dòng dữ liệu. Kiểm tra tài sản và khoảng thời gian trong câu hỏi.')
            if query.get('truncated'):
                st.warning('Kết quả bị giới hạn: chỉ hiển thị một phần dữ liệu. Không suy ra tổng số dòng từ bảng này.')
            st.download_button('Tải bảng CSV', pd.DataFrame(rows, columns=query.get('columns') or None).to_csv(index=False),
                               file_name=f'aave-query-{index + 1}.csv', mime='text/csv',
                               key=f'query_csv_{index}', icon=':material/download:')
        else:
            st.caption('Chưa có kết quả SQL được ghi nhận cho lượt này.')
        if draft.get('sql'):
            st.caption('SQL được ghi nhận' + (' · SQL1' if query is not None else ' · chưa có kết quả thực thi'))
            sql = draft['sql']
            display_sql = str(sql)
            if isinstance(sql, str):
                try:
                    display_sql = sqlglot.transpile(sql, read='duckdb', write='duckdb', pretty=True)[0]
                except (sqlglot.errors.SqlglotError, ValueError):
                    pass
            else:
                st.caption('SQL không đúng định dạng văn bản. Xem bản gốc trong JSON tải về.')
            st.code(display_sql, language='sql')
            st.caption('SQL được định dạng để đọc. Bản gốc được giữ nguyên trong JSON tải về.')
            normalizations = (draft.get('planning') or {}).get('sql_normalizations', [])
            if normalizations:
                with st.expander('SQL model sinh trước khi điều chỉnh cú pháp ngày'):
                    st.caption('Chỉ đổi định danh có dạng ngày ISO thành chuỗi ngày ở phép so sánh thời gian. SQL thực thi hiển thị bên trên; không tự sửa phép đếm hoặc mốc ngày.')
                    for item in normalizations:
                        st.code(item['raw_sql'], language='sql')
            with st.expander('Nguồn dữ liệu', icon=':material/database:'):
                st.caption('Database cục bộ của workspace; kết quả lượt hỏi không lưu mã phiên bản tệp dữ liệu.')
                try:
                    manifest = json.loads((Path(root) / 'data/raw/manifest.json').read_text(encoding='utf-8'))
                except (OSError, ValueError):
                    manifest = {}
                if isinstance(manifest, dict) and manifest.get('release'):
                    st.caption(f"Dataset hiện tại: {manifest['release']} · Thu thập: {manifest.get('collected_at', 'không ghi nhận')}")
                    for label, field in [('URL nguồn', 'url'), ('SHA-256', 'sha256')]:
                        if manifest.get(field):
                            st.caption(f'{label}: {manifest[field]}')
                    st.caption('Đây là metadata workspace hiện tại, không phải snapshot của lượt hỏi.')
                else:
                    st.caption('Chưa có manifest nguồn đọc được; không suy đoán release dữ liệu.')
    with documents_tab:
        documents = draft.get('documents', [])
        st.caption(f'{len(documents)} đoạn tài liệu được truy xuất cho lượt này.')
        for doc in documents:
            st.markdown(f"**{doc['id']} · {doc['title']}**")
            st.markdown(f"[Đọc tài liệu nguồn]({doc['url']})")
            st.write(doc['text'])
            st.caption('Thu thập: ' + doc['collected_at'])
            if doc.get('source_sha256'):
                st.caption('SHA-256: ' + doc['source_sha256'])
            st.divider()
        if not documents:
            st.caption('Chưa có tài liệu văn bản được truy xuất cho lượt này.')
    with claims_tab:
        st.caption('Liên kết phát biểu do backend ghi nhận; có trích dẫn không đồng nghĩa đã được xác minh.')
        claims = draft.get('claims', [])
        if not isinstance(claims, list):
            st.caption('Danh sách phát biểu không đúng định dạng. Xem bản gốc trong JSON tải về.')
            claims = []
        for number, claim in enumerate(claims, 1):
            if not isinstance(claim, dict):
                st.caption(f'Phát biểu {number} không đúng định dạng. Xem bản gốc trong JSON tải về.')
                continue
            st.markdown(f"**{claim.get('text', '')}**")
            citations = claim.get('citations', [])
            if isinstance(citations, list) and all(isinstance(cite, str) for cite in citations):
                st.caption('Tham chiếu: ' + (', '.join(citations) or 'chưa có'))
            else:
                st.caption('Tham chiếu không đúng định dạng. Xem bản gốc trong JSON tải về.')
            numeric = claim.get('numeric')
            if isinstance(numeric, dict):
                st.caption(f"Ô dữ liệu: {numeric.get('evidence_id', 'không nêu')} · dòng {numeric.get('row', 'không nêu')} "
                           f"(từ 0) · cột {numeric.get('column', 'không nêu')}")
                st.json(numeric, expanded=False)
            elif numeric is not None:
                st.caption('Liên kết ô dữ liệu không đúng định dạng. Xem bản gốc trong JSON tải về.')
        if not claims:
            st.caption('Chưa có phát biểu kèm liên kết dẫn chứng được ghi nhận.')


def render_verification(result, issue_help):
    issues = result.get('issues', [])
    if issues:
        st.markdown('**Các điểm cần kiểm tra**')
        for number, issue in enumerate(issues, 1):
            title, explanation = issue_help.get(issue['code'], (
                'Điểm cần kiểm tra',
                'Bộ kiểm chứng ghi nhận một vấn đề cần đối chiếu. Xem thông báo gốc trong phần kỹ thuật bên dưới.',
            ))
            st.markdown(f'**{number}. {title}**')
            st.caption(explanation)
    with st.expander('Thông báo kỹ thuật', icon=':material/fact_check:'):
        st.caption('Kết quả kiểm tra tự động không bảo đảm câu trả lời đúng tuyệt đối.')
        for number, issue in enumerate(issues, 1):
            st.caption(f"{number}. {issue['code']} · {issue.get('action', 'answer')}")
            st.text(issue['message'])
        if not issues:
            st.caption('Không có vấn đề được ghi nhận. Xem trạng thái câu trả lời để biết phạm vi kiểm chứng.')
        events = {'verification': 'Kiểm tra', 'repair': 'Vòng sửa', 'error': 'Lỗi xử lý',
                  'unchanged_repair_stop': 'Dừng vì nội dung không thay đổi'}
        for event in result.get('trace', []):
            label = events.get(event.get('event'), event.get('event', 'Bước xử lý'))
            if event.get('repair') is not None:
                label += f" {event['repair']}"
            st.markdown(f'**{label}**')
            if 'issues' in event:
                st.caption(f"{len(event['issues'])} vấn đề được ghi nhận tại bước này.")
            if event.get('message'):
                st.write(event['message'])
        if not result.get('trace'):
            st.caption('Chưa có bước kiểm tra hoặc sửa được ghi lại trong trace.')
        draft = result['draft']
        st.caption('Nhật ký kỹ thuật đầy đủ')
        st.json({'requirements': draft.get('spec', {}), 'planning': draft.get('planning', {}),
                 'status': result['status'], 'issues': result.get('issues', []),
                 'repairs': result['repairs'], 'trace': result.get('trace', [])}, expanded=False)
