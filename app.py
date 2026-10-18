from pathlib import Path
from dataclasses import asdict
import os,json
import streamlit as st
from aave_analyst.cli import analyst_at
from aave_analyst.pipeline import MODES

ROOT=Path(os.getenv('AAVE_PROJECT_ROOT',Path(__file__).parent)).resolve()
st.set_page_config(page_title="Aave V3 có dẫn chứng",page_icon="📊",layout="wide")
st.title("Hỏi đáp Aave V3 có dẫn chứng")
st.caption("Dữ liệu lịch sử Ethereum · DAI, USDC, USDT, USDe, WETH · Thử nghiệm phục vụ học tập")
mode=st.sidebar.selectbox("Phiên bản",list(MODES),index=2)
st.sidebar.write("B0: trả trực tiếp · B1: tự rà soát · P: kiểm chứng có cấu trúc")
if not (ROOT/'data/processed/aave.duckdb').exists() or not (ROOT/'data/documents/chunks.json').exists():
    st.info("Chạy lệnh prepare và documents theo README trước khi hỏi đáp.");st.stop()
question=st.text_area("Câu hỏi",placeholder="Có bao nhiêu giao dịch thanh lý trong tháng 8/2026?",height=90)
if st.button("Trả lời",type="primary",disabled=not question.strip()):
    try:
        with st.spinner("Đang truy vấn và kiểm tra bằng chứng…"):
            result=analyst_at(ROOT).answer(question,mode)
        st.session_state['result']=asdict(result)
    except Exception as exc:st.error(f"Không thể xử lý: {type(exc).__name__}: {exc}")
if 'result' in st.session_state:
    r=st.session_state['result'];draft=r['draft']
    st.markdown(draft['answer'])
    if r['error']:st.error(r['error'])
    if r['status']=='unverified':
        st.warning("Một phần câu trả lời chưa vượt qua kiểm tra. Hãy xem các vấn đề và nguồn bên dưới.")
    elif r['status']=='checks_passed':st.caption("Đã vượt qua các kiểm tra của hệ thống; đây không phải bảo đảm đúng tuyệt đối.")
    else:st.caption("Phiên bản này không xác nhận câu trả lời đã được kiểm chứng.")
    if draft['query_result']:
        st.subheader("Kết quả truy vấn")
        st.dataframe(draft['query_result']['rows'],use_container_width=True)
        if draft['query_result']['truncated']:st.warning("Bảng hiển thị bị giới hạn 200 dòng; chưa hiển thị toàn bộ kết quả.")
    with st.expander("SQL và bằng chứng số liệu [SQL1]"):
        st.code(draft['sql'],language='sql');st.json(draft['spec'])
        st.caption("Nguồn: stablecoin-onchain-data, data-2026-09-15; xem data/processed/audit.json để kiểm tra độ phủ.")
    for doc in draft['documents']:
        with st.expander(doc['id']+' · '+doc['title']):
            st.markdown(f"[Mở nguồn]({doc['url']})");st.write(doc['text']);st.caption('Thu thập: '+doc['collected_at'])
    with st.expander("Kết quả kiểm tra và nhật ký sửa"):
        st.json({'status':r['status'],'issues':r['issues'],'repairs':r['repairs'],'trace':r['trace']})
    st.caption(f"Thời gian: {r['elapsed']:.1f}s · Số vòng sửa: {r['repairs']}")
    st.download_button("Tải kết quả và bằng chứng",json.dumps(r,ensure_ascii=False,indent=2),file_name="aave-answer.json",mime="application/json")
