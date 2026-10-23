"""Aave V3 research chat with evidence for each answer."""
from dataclasses import asdict
import json
from pathlib import Path
import streamlit as st
from aave_analyst.cli import analyst_at
from aave_analyst.config import read_settings
from aave_analyst.pipeline import MODES

APP_DIR = Path(__file__).resolve().parent
ROOT = Path(read_settings().get('AAVE_PROJECT_ROOT') or APP_DIR).resolve()
MODE_LABELS = {'B0': 'B0 · Trả lời trực tiếp', 'B1': 'B1 · Tự rà soát',
               'P': 'P · Kiểm chứng có cấu trúc', 'P-SQL': 'P-SQL · Bỏ kiểm tra SQL',
               'P-Evidence': 'P-Evidence · Bỏ kiểm tra dẫn chứng', 'P-Repair': 'P-Repair · Không sửa tự động'}
MODE_HELP = {
    'B0': 'Trả lời từ dữ liệu truy xuất, không chạy bộ kiểm chứng hoặc sửa tự động.',
    'B1': 'Tự rà soát tổng quát và sửa câu trả lời khi phát hiện vấn đề.',
    'P': 'Kết hợp kiểm tra SQL, dẫn chứng và tối đa hai vòng sửa nội dung.',
    'P-SQL': 'Đối chiếu dẫn chứng và sửa nội dung; bỏ bước kiểm tra SQL chuyên biệt.',
    'P-Evidence': 'Kiểm tra SQL và sửa nội dung; bỏ bước kiểm tra dẫn chứng chuyên biệt.',
    'P-Repair': 'Kiểm tra SQL và dẫn chứng; không tự sửa khi phát hiện vấn đề.',
}
ISSUE_HELP = {
    'metric_unit_mismatch': ('Chỉ số và đơn vị chưa nhất quán', 'Ví dụ: yêu cầu đếm giao dịch nhưng phần phân tích lại chọn giá trị USD. Cần đối chiếu câu hỏi với SQL.'),
    'metric_aggregation_mismatch': ('Phép tính chưa khớp câu hỏi', 'Kiểm tra xem câu hỏi cần số lượng, tổng giá trị hay giá trị trung bình.'),
    'grain_event_vs_transaction': ('Cần phân biệt sự kiện và giao dịch', 'Một giao dịch có thể chứa nhiều sự kiện thanh lý; hai cách đếm có thể cho kết quả khác nhau.'),
    'semantic_correctness_unverified': ('Ý nghĩa kết quả chưa được xác minh', 'Truy vấn có thể chạy thành công nhưng chưa chứng minh được rằng kết quả trả lời đúng yêu cầu.'),
}
SUGGESTIONS = [
    ('01 / THANH LÝ', 'Theo dõi hoạt động thanh lý', 'Có bao nhiêu giao dịch thanh lý trong tháng 8 năm 2026?'),
    ('02 / TÀI SẢN CUNG CẤP', 'Khám phá dòng vốn cung cấp', 'Giá trị tài sản cung cấp trung bình của USDC trong tháng 8 năm 2026 là bao nhiêu USD?'),
    ('03 / DƯ NỢ', 'So sánh nhu cầu vay', 'So sánh dư nợ trung bình của USDC và USDT trong tháng 8 năm 2026.'),
    ('04 / KIẾN THỨC AAVE', 'Hiểu cơ chế của giao thức', 'Health factor là gì và khi nào một vị thế trên Aave có thể bị thanh lý?'),
]
st.set_page_config(page_title='Aave Lens · Trợ lý phân tích Aave V3', page_icon='◈', layout='wide')
st.markdown(f'<style>{(APP_DIR / "assets/chat.css").read_text(encoding="utf-8")}</style>', unsafe_allow_html=True)


def reset_chat():
    st.session_state.messages = []


def render_answer(result, index):
    draft = result['draft']
    if draft['answer']:
        st.markdown(draft['answer'])
    elif not result.get('error'):
        st.info('Chưa có nội dung trả lời cho câu hỏi này.')
    status = result['status']
    if result.get('error'):
        st.error(f"Chưa thể hoàn tất câu trả lời. {result['error']}")
    elif status == 'checks_passed':
        st.success('Đã vượt qua các bước kiểm tra của hệ thống.', icon=':material/verified:')
    elif status == 'unverified':
        st.warning('Chưa xác minh đầy đủ. Xem các điểm cần kiểm tra bên dưới.', icon=':material/fact_check:')
    elif draft.get('refused'):
        st.info('Cần làm rõ câu hỏi hoặc bổ sung dữ liệu để trả lời có căn cứ.')
    else:
        st.caption('Câu trả lời này chưa được xác nhận qua bộ kiểm chứng đầy đủ.')
    with st.expander('Bằng chứng & kết quả truy vấn', icon=':material/database:'):
        query = draft.get('query_result')
        if query:
            st.dataframe(query['rows'], width='stretch', hide_index=True)
            if query.get('truncated'):
                st.caption('Bảng đang hiển thị một phần kết quả (tối đa 200 dòng).')
        if draft.get('sql'):
            st.caption('SQL đã thực thi · [SQL1]')
            st.code(draft['sql'], language='sql')
            st.caption('Nguồn: stablecoin-onchain-data · release data-2026-09-15.')
        documents = draft.get('documents', [])
        for doc in documents:
            st.markdown(f"**{doc['id']} · {doc['title']}**")
            st.markdown(f"[Đọc tài liệu nguồn]({doc['url']})")
            st.write(doc['text'])
            st.caption('Thu thập: ' + doc['collected_at'])
        if not query and not documents:
            st.caption('Chưa có bảng kết quả hoặc tài liệu được truy xuất cho lượt này.')
    with st.expander('Chi tiết kiểm chứng', icon=':material/fact_check:'):
        st.caption('Kết quả kiểm tra tự động không bảo đảm câu trả lời đúng tuyệt đối.')
        for issue in result.get('issues', []):
            title, explanation = ISSUE_HELP.get(issue['code'], (issue['code'], issue['message']))
            st.markdown(f'**{title}**')
            st.write(explanation)
        if not result.get('issues'):
            st.caption('Không có vấn đề được ghi nhận trong lượt này. Xem trạng thái ở trên để biết các bước kiểm chứng đã được áp dụng.')
        st.caption('Nhật ký kỹ thuật đầy đủ')
        st.json({'requirements': draft['spec'], 'planning': draft.get('planning', {}), 'status': status, 'issues': result['issues'],
                 'repairs': result['repairs'], 'trace': result['trace']}, expanded=False)
    meta, download = st.columns([3, 2])
    with meta:
        st.caption(f"{result.get('mode', 'P')} · {result['elapsed']:.1f} giây · {result['repairs']} vòng sửa")
    with download:
        st.download_button('Tải câu trả lời', json.dumps(result, ensure_ascii=False, indent=2),
                           file_name=f'aave-answer-{index + 1}.json', mime='application/json',
                           key=f'download_{index}', icon=':material/download:', width='stretch')


if 'messages' not in st.session_state:
    st.session_state.messages = []
    previous = st.session_state.pop('result', None)
    if previous and previous.get('draft', {}).get('question'):
        st.session_state.messages = [{'role': 'user', 'content': previous['draft']['question']},
                                     {'role': 'assistant', 'result': previous}]
ready = (ROOT / 'data/processed/aave.duckdb').exists() and (ROOT / 'data/documents/chunks.json').exists()
with st.sidebar:
    st.markdown('''<div class="brand"><span class="brand-mark">◈</span><div><strong>Aave Lens</strong>
        <span>ON-CHAIN RESEARCH ASSISTANT</span></div></div>''', unsafe_allow_html=True)
    st.button('Cuộc trò chuyện mới', key='new_chat', icon=':material/add:',
              on_click=reset_chat, width='stretch', type='primary')
    st.download_button('Xuất hội thoại', json.dumps(st.session_state.messages, ensure_ascii=False, indent=2),
                       file_name='aave-conversation.json', mime='application/json', key='export_chat',
                       disabled=not st.session_state.messages, icon=':material/download:', width='stretch')
    if st.session_state.messages:
        count = sum(message['role'] == 'user' for message in st.session_state.messages)
        st.caption(f'{count} câu hỏi trong phiên hiện tại')
    st.markdown('<div class="sidebar-label">KHÔNG GIAN NGHIÊN CỨU</div>', unsafe_allow_html=True)
    st.markdown('**Aave V3 · Ethereum**')
    st.caption('Phân tích tài sản cung cấp, dư nợ và hoạt động thanh lý bằng dữ liệu có dẫn chứng.')
    st.markdown('<div class="asset-tags"><span>DAI</span><span>USDC</span><span>USDT</span><span>USDe</span><span>WETH</span></div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('**Phương pháp trả lời**')
    mode = st.selectbox('Chế độ phân tích', list(MODES), index=2, format_func=lambda value: MODE_LABELS[value],
                        key='analysis_mode', label_visibility='collapsed')
    st.caption(MODE_HELP[mode])
    with st.expander('Hướng dẫn đặt câu hỏi'):
        st.write('Ghi rõ tài sản, chỉ số và khoảng thời gian. Ví dụ: dư nợ trung bình của USDC trong tháng 8/2026.')
        st.write('Lịch sử được giữ trong phiên này. Mỗi câu hỏi được phân tích độc lập; hãy ghi lại thông tin cần thiết khi hỏi tiếp.')
        st.write('Thời gian được hiểu theo UTC. Dữ liệu lịch sử không phản ánh thị trường trực tiếp.')
    st.divider()
    st.caption('ĐỀ TÀI C.5 · BLOCKCHAIN & AI')
    st.caption('Chatbot Aave V3 có dẫn chứng. Phục vụ học tập và nghiên cứu; không phải khuyến nghị đầu tư.')
st.markdown('''<div class="workspace-bar"><span>WORKSPACE <b>/ AAVE V3</b></span>
    <span class="dataset-label"><i></i> Dữ liệu lịch sử · Ethereum</span></div>''', unsafe_allow_html=True)
if not ready:
    st.warning('Chưa có đủ dữ liệu để bắt đầu hội thoại. Chạy các lệnh prepare và documents theo README.')
suggested = None
if not st.session_state.messages:
    st.markdown('''<section class="welcome"><div class="welcome-symbol">◈</div>
        <div class="eyebrow">AAVE V3 INTELLIGENCE</div>
        <h1>Dữ liệu on-chain.<br><span>Câu trả lời có dẫn chứng.</span></h1>
        <p>Khám phá tài sản cung cấp, dư nợ và thanh lý trên Aave V3.<br>
        Đặt câu hỏi bằng tiếng Việt. Kiểm tra từng câu trả lời bằng dữ liệu.</p>
        <div class="capabilities"><span>✧ Phân tích bằng SQL</span><span>▤ Tài liệu Aave</span><span>✓ Kiểm chứng có cấu trúc</span></div>
        </section>''', unsafe_allow_html=True)
    st.markdown('<div class="suggestion-heading">BẮT ĐẦU TỪ MỘT CÂU HỎI</div>', unsafe_allow_html=True)
    for row in range(2):
        columns = st.columns(2)
        for column, index in zip(columns, range(row * 2, row * 2 + 2)):
            label, title, question = SUGGESTIONS[index]
            with column, st.container(border=True):
                st.caption(label)
                st.markdown(f'**{title}**')
                if st.button(question, key=f'suggestion_{index}', width='stretch', disabled=not ready):
                    suggested = question
else:
    st.markdown('### Hội thoại nghiên cứu')
    st.caption('Mở phần bằng chứng bên dưới mỗi câu trả lời để đối chiếu kết quả.')
for index, message in enumerate(st.session_state.messages):
    with st.chat_message(message['role'], avatar=':material/person:' if message['role'] == 'user' else ':material/insights:'):
        if message['role'] == 'user':
            st.markdown(message['content'])
        elif 'result' in message:
            render_answer(message['result'], index)
        else:
            st.error(message['error'])
typed = st.chat_input('Hỏi về Aave V3 — ghi rõ tài sản và khoảng thời gian…', disabled=not ready, key='question')
prompt = typed or suggested
if prompt and prompt.strip() and ready:
    prompt = prompt.strip()
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user', avatar=':material/person:'):
        st.markdown(prompt)
    with st.chat_message('assistant', avatar=':material/insights:'):
        try:
            with st.spinner('Đang phân tích câu hỏi, truy xuất dữ liệu và kiểm tra dẫn chứng…'):
                result = asdict(analyst_at(ROOT).answer(prompt, mode))
            st.session_state.messages.append({'role': 'assistant', 'result': result})
        except Exception as exc:
            st.session_state.messages.append({'role': 'assistant', 'error': f'Không thể xử lý câu hỏi: {type(exc).__name__}: {exc}'})
    st.rerun()
