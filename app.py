"""Aave V3 research chat with evidence for each answer."""
from dataclasses import asdict
import json
from pathlib import Path
import streamlit as st
from aave_analyst.cli import analyst_at
from aave_analyst.config import read_settings
from aave_analyst.pipeline import MODES
from aave_analyst.ui import answer_for_display, render_evidence, render_verification

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
    'time_range': ('Cần đối chiếu khoảng thời gian', 'Kiểm tra mốc bắt đầu, kết thúc và thời gian quan sát trong dữ liệu.'),
    'coverage': ('Cần kiểm tra phạm vi dữ liệu', 'Đối chiếu khoảng thời gian và tài sản được hỏi với phạm vi dữ liệu đã nạp.'),
    'document_support': ('Cần đối chiếu tài liệu dẫn chứng', 'Kiểm tra tài liệu hoặc kết quả SQL có hỗ trợ phát biểu đang được dẫn hay không.'),
}
SUGGESTIONS = [
    ('01 / THANH LÝ', 'Theo dõi hoạt động thanh lý', 'Có bao nhiêu giao dịch thanh lý trong tháng 8 năm 2026?'),
    ('02 / TÀI SẢN CUNG CẤP', 'Khám phá dòng vốn cung cấp', 'Giá trị tài sản cung cấp trung bình của USDC trong tháng 8 năm 2026 là bao nhiêu USD?'),
    ('03 / DƯ NỢ', 'So sánh nhu cầu vay', 'So sánh dư nợ trung bình của USDC và USDT trong tháng 8 năm 2026.'),
    ('04 / KIẾN THỨC AAVE', 'Hiểu cơ chế của giao thức', 'Health factor là gì và khi nào một vị thế trên Aave có thể bị thanh lý?'),
]
st.set_page_config(page_title='Aave Lens · Nghiên cứu Aave V3', page_icon=':material/travel_explore:', layout='wide')
st.markdown(f'<style>{(APP_DIR / "assets/chat.css").read_text(encoding="utf-8")}</style>', unsafe_allow_html=True)


def reset_chat():
    st.session_state.messages = []
    st.session_state.pop('_pending_question', None)


def render_answer(result, index):
    with st.container(horizontal=True, gap='medium', key=f'answer_layout_{index}'):
        with st.container(width=640, key=f'answer_body_{index}'):
            st.caption('Aave Lens · ' + result.get('mode', 'P'))
            draft = result['draft']
            answer = answer_for_display(result)
            if answer:
                st.markdown(answer)
            elif not result.get('error'):
                st.info('Chưa có nội dung trả lời cho câu hỏi này.')
            status = result['status']
            if result.get('error'):
                st.error(f"Chưa thể hoàn tất câu trả lời. {result['error']}")
                st.caption('Gửi lại câu hỏi để thử lại hoặc thu hẹp khoảng thời gian. Ứng dụng không tự gửi lại yêu cầu.')
            elif status == 'checks_passed':
                st.success('Đã vượt qua các bước kiểm tra của hệ thống.', icon=':material/check_circle:')
                st.caption('Trạng thái kiểm tra tự động không khẳng định đáp án đúng tuyệt đối.')
            elif status == 'unverified':
                count = len(result.get('issues', []))
                detail = f'Có {count} điểm cần kiểm tra bên dưới.' if count else 'Xem thông báo kỹ thuật bên dưới.'
                st.warning(f'Chưa xác minh đầy đủ. {detail}', icon=':material/fact_check:')
            elif draft.get('refused'):
                st.info('Cần làm rõ câu hỏi hoặc bổ sung dữ liệu để trả lời có căn cứ.')
            else:
                st.caption('Câu trả lời này chưa được xác nhận qua bộ kiểm chứng đầy đủ.')
            st.caption(f"{result.get('mode', 'P')} · {result['elapsed']:.1f} giây · {result['repairs']} vòng sửa")
            if result.get('request_id'):
                st.caption(f"Mã tra log: `{result['request_id']}`")
            st.download_button('Tải câu trả lời', json.dumps(result, ensure_ascii=False, indent=2),
                               file_name=f'aave-answer-{index + 1}.json', mime='application/json',
                               key=f'download_{index}', icon=':material/download:')
            render_verification(result, ISSUE_HELP)
        with st.container(width=340, key=f'evidence_panel_{index}'):
            render_evidence(draft, index, ROOT)


if 'messages' not in st.session_state:
    st.session_state.messages = []
    previous = st.session_state.pop('result', None)
    if previous and previous.get('draft', {}).get('question'):
        st.session_state.messages = [{'role': 'user', 'content': previous['draft']['question']},
                                     {'role': 'assistant', 'result': previous}]
ready = (ROOT / 'data/processed/aave.duckdb').exists() and (ROOT / 'data/documents/chunks.json').exists()
with st.sidebar:
    st.markdown('''<div class="brand"><span class="brand-mark" aria-hidden="true">a.</span>
        <div><strong>Aave Lens</strong><span>Không gian nghiên cứu</span></div></div>''', unsafe_allow_html=True)
    st.button('Cuộc trò chuyện mới', key='new_chat', icon=':material/add:',
              on_click=reset_chat, width='stretch')
    st.caption('Phiên hiện tại')
    questions = [message['content'] for message in st.session_state.messages if message['role'] == 'user']
    with st.container(key='current_session'):
        st.write(questions[-1] if questions else 'Chưa có câu hỏi')
    if questions:
        st.caption(f'{len(questions)} câu hỏi trong phiên')
    mode = st.selectbox('Phương pháp trả lời', list(MODES), index=2,
                        format_func=lambda value: MODE_LABELS[value], key='analysis_mode',
                        disabled=bool(st.session_state.get('_pending_question')))
    st.caption(MODE_HELP[mode])
    st.divider()
    st.caption('Phạm vi dữ liệu')
    st.markdown('**Aave V3 · Ethereum**')
    st.caption('DAI · USDC · USDT · USDe · WETH')
    st.caption('Dữ liệu lịch sử · UTC')
    st.caption('Tệp dữ liệu cục bộ: ' + ('đã tìm thấy' if ready else 'chưa đầy đủ'))
    with st.expander('Hướng dẫn đặt câu hỏi'):
        st.write('Ghi rõ tài sản, chỉ số và khoảng thời gian. Ví dụ: dư nợ trung bình của USDC trong tháng 8/2026.')
        st.write('Lịch sử được giữ trong phiên này. Mỗi câu hỏi được phân tích độc lập; hãy ghi lại thông tin cần thiết khi hỏi tiếp.')
        st.write('Thời gian được hiểu theo UTC. Dữ liệu lịch sử không phản ánh thị trường trực tiếp.')
        st.caption('Tìm thấy tệp không xác nhận kết nối mô hình hay độ đầy đủ dữ liệu.')
    st.divider()
    st.download_button('Xuất hội thoại', json.dumps(st.session_state.messages, ensure_ascii=False, indent=2),
                       file_name='aave-conversation.json', mime='application/json', key='export_chat',
                       disabled=not st.session_state.messages, icon=':material/download:', width='stretch')
    st.caption('Phục vụ học tập và nghiên cứu; không phải khuyến nghị đầu tư.')

st.markdown('''<div class="workspace-bar"><span>Nghiên cứu / Aave V3</span>
    <span>Ethereum · Dữ liệu lịch sử · UTC</span></div>''', unsafe_allow_html=True)
suggested = None
typed = None
with st.container(key='research_sheet'):
    st.title('Hội thoại nghiên cứu')
    st.caption('Aave V3 Ethereum · Câu trả lời gắn với dữ liệu và tài liệu nguồn')
    if not ready:
        st.warning('Chưa có đủ dữ liệu để bắt đầu hội thoại. Chạy các lệnh prepare và documents theo README.')
    if not st.session_state.messages:
        with st.container(key='welcome_workspace'):
            st.header('Đi từ câu hỏi đến bằng chứng.')
            st.write('Hỏi về tài sản cung cấp, dư nợ và thanh lý trên Aave V3. Ghi rõ tài sản và khoảng thời gian bạn muốn phân tích.')
            with st.container(key='initial_composer'):
                st.caption('Câu hỏi nghiên cứu')
                typed = st.chat_input('Hỏi về Aave V3 — ghi rõ tài sản và khoảng thời gian…', disabled=not ready, key='question')
            st.caption('Một vài điểm bắt đầu')
            for index, (_, title, question) in enumerate(SUGGESTIONS):
                with st.container(key=f'starter_row_{index}'):
                    if st.button(f'**{title}**\n\n{question}', key=f'suggestion_{index}',
                                 width='stretch', disabled=not ready, icon=':material/north_east:'):
                        suggested = question
    for index, message in enumerate(st.session_state.messages):
        with st.chat_message(message['role'], avatar=':material/person:' if message['role'] == 'user' else ':material/scan:'):
            if message['role'] == 'user':
                st.caption('Bạn')
                st.markdown(message['content'])
            elif 'result' in message:
                render_answer(message['result'], index)
            else:
                st.error(message['error'])
                st.caption('Gửi lại câu hỏi để thử lại. Nếu lỗi tiếp diễn, kiểm tra kết nối và cấu hình mô hình.')
                if message.get('request_id'):
                    st.caption(f"Mã tra log: `{message['request_id']}`")
    processing_slot = st.empty()

if st.session_state.messages:
    typed = st.chat_input('Hỏi về Aave V3 — ghi rõ tài sản và khoảng thời gian…',
                          disabled=not ready or bool(st.session_state.get('_pending_question')), key='question')
prompt = typed or suggested
if prompt and prompt.strip() and ready:
    prompt = prompt.strip()
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    # Paint the conversation before starting a potentially slow request. The
    # inline welcome input has no bottom auto-scroll to reveal content below it.
    st.session_state['_pending_question'] = {'prompt': prompt, 'mode': mode}
    st.rerun()

pending = st.session_state.pop('_pending_question', None)
if pending and ready:
    with processing_slot.container(), st.chat_message('assistant', avatar=':material/scan:'):
        try:
            with st.status('Đang xử lý câu hỏi…', expanded=True) as progress:
                st.write('Đang phân tích và truy xuất bằng chứng theo chế độ đã chọn. Vui lòng chờ kết quả.')
                result = asdict(analyst_at(ROOT).answer(pending['prompt'], pending['mode']))
                progress.update(label='Đã nhận kết quả xử lý', state='complete', expanded=False)
            st.session_state.messages.append({'role': 'assistant', 'result': result})
        except Exception as exc:
            st.session_state.messages.append({'role': 'assistant', 'error': f'Không thể xử lý câu hỏi: {type(exc).__name__}: {exc}'})
    st.rerun()
