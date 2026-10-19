from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st
from rules import classify
st.set_page_config(page_title="Shipment Exception Manager",layout="wide")
st.title("Shipment Exception Manager")
st.warning("Portfolio simulation: fictional shipments and unvalidated rules. No carrier tickets or customer messages are sent. Changes last only in this browser session.")
NOW=datetime(2026,10,19,12)
st.caption("Frozen simulation clock: 19 October 2026, 12:00, demo-local time. All timestamps use this same clock.")
if "shipments" not in st.session_state:
    st.session_state.shipments=pd.read_csv(Path(__file__).parent/"shipments.csv").fillna("").to_dict("records")
    st.session_state.audit=[]
if st.button("Reset simulation"):
    del st.session_state["shipments"];st.session_state.audit=[];st.rerun()
exceptions=[]
for row in st.session_state.shipments:
    rule=classify(row,NOW)
    if rule: exceptions.append({**row,**rule})
df=pd.DataFrame(exceptions)
a,b,c=st.columns(3)
a.metric("Detected exceptions",len(df));b.metric("Unresolved",int((df.case_status!="Resolved").sum()) if len(df) else 0);c.metric("P1 unresolved",int(((df.priority=="P1")&(df.case_status!="Resolved")).sum()) if len(df) else 0)
priority=st.selectbox("Priority",["All","P1","P2"])
state=st.selectbox("Case status",["All","Open","In progress","Resolved"])
view=df.copy()
if priority!="All":view=view[view.priority==priority]
if state!="All":view=view[view.case_status==state]
st.dataframe(view,use_container_width=True,hide_index=True)
if len(view):
    sid=st.selectbox("Open shipment",view.shipment_id.tolist())
    row=next(x for x in st.session_state.shipments if x["shipment_id"]==sid)
    rule=classify(row,NOW)
    st.subheader(sid);st.json({**row,**rule})
    st.info(rule["action"])
    with st.form("case_update"):
        owner=st.selectbox("Assign owner",["Unassigned","Seller operations","Support review"],index=["Unassigned","Seller operations","Support review"].index(row["owner"]))
        status=st.selectbox("Resolution status",["Open","In progress","Resolved"],index=["Open","In progress","Resolved"].index(row["case_status"]))
        note=st.text_input("Action note (required for resolution)",max_chars=500)
        submit=st.form_submit_button("Save simulated action")
    if submit:
        if status=="Resolved" and not note.strip():st.error("Add a resolution note first.")
        else:
            st.session_state.audit.append({"shipment_id":sid,"previous_status":row["case_status"],"new_status":status,"owner":owner,"note":note,"simulated_at":NOW.isoformat()})
            row.update(owner=owner,case_status=status);st.rerun()
    st.subheader("Customer message draft — not sent")
    draft=f"Hello, we are reviewing an exception affecting shipment {sid}. We are checking the latest available information and will share a confirmed update. We cannot confirm a delivery date yet."
    st.text_area("Editable draft",draft,key="draft_"+sid)
    if st.button("Mark draft prepared"):
        row["communication_status"]="Draft prepared";st.rerun()
st.subheader("Session action log")
st.dataframe(st.session_state.audit)
st.download_button("Export action log",pd.DataFrame(st.session_state.audit).to_csv(index=False),"action_log.csv")
st.download_button("Export exception queue",df.to_csv(index=False),"exception_queue.csv")
