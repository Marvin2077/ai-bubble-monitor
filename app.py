import streamlit as st, yaml, pandas as pd
from src.storage.database import get_connection, init_db
from src.storage.repository import bulk_upsert_observations
from src.ingestion.csv_importer import import_csv_to_db
from src.scoring.indicator_scoring import score_indicator
from src.scoring.category_scoring import score_category
from src.scoring.scenario_scoring import select_scenario
from src.reporting.markdown_report import generate_monthly_report, save_report
from src.collectors.fred_collector import collect_fred_latest_observation
from src.collectors.sec_companyfacts_collector import collect_sec_latest_observation
from src.collectors.manual_stub_collector import collect_manual_registry
from src.ui.pages import header
from src.ui.charts import line_chart

header()
inds=yaml.safe_load(open('configs/indicators.yaml', encoding='utf-8'))
thresholds=yaml.safe_load(open('configs/thresholds.yaml', encoding='utf-8'))
cat_weights=yaml.safe_load(open('configs/category_weights.yaml', encoding='utf-8'))
indicator_map={i['id']:i for i in inds}
conn=get_connection('data/ai_bubble_monitor.db'); init_db(conn)

st.subheader('Data ingestion')
if st.button('Import sample CSV'):
    c,e=import_csv_to_db('data/sample_observations.csv',set(indicator_map),conn)
    st.success(f'imported {c} rows'); [st.error(x) for x in e]

if st.button('Auto-collect public data (optional)'):
    auto_obs = []
    auto_obs.extend(collect_manual_registry('data/manual_evidence_registry.csv'))
    # Public macro examples that match current indicators
    hy = collect_fred_latest_observation('US_HIGH_YIELD_SPREAD', 'BAMLH0A0HYM2')
    elec = collect_fred_latest_observation('US_ELECTRICITY_PRICE_INDEX', 'CUSR0000SEHF01')
    if hy: auto_obs.append(hy)
    if elec: auto_obs.append(elec)
    # SEC example (NVIDIA revenues in USD). Mapping to proxy indicator requires analyst judgement.
    sec_obs = collect_sec_latest_observation('NVDA_DC_REVENUE_YOY', '1045810', 'us-gaap', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'USD')
    if sec_obs: auto_obs.append(sec_obs)
    n = bulk_upsert_observations(conn, [o for o in auto_obs if o.indicator_id in indicator_map])
    st.success(f'auto-collected {n} observations from public sources')

obs=pd.read_sql_query('select * from observations', conn)
if obs.empty:
    st.info('Please import sample CSV first or run auto-collect.'); st.stop()
month=st.selectbox('Select month', sorted(obs['date'].unique()))
cur=obs[obs.date==month]
scores={}
for _,r in cur.iterrows():
    if r['indicator_id'] not in thresholds:
        continue
    s,_=score_indicator(r['value'],thresholds[r['indicator_id']], history=[])
    scores[r['indicator_id']]=s
cat_scores={}
for c in cat_weights:
    ids=[i['id'] for i in inds if i['category']==c and i['id'] in scores]
    if ids: cat_scores[c]=score_category({i:scores[i] for i in ids}, indicator_map)[0]
total=sum(cat_scores[c]*cat_weights[c] for c in cat_scores) if cat_scores else 0.0
sc=select_scenario(month,total,cat_scores or {k:0 for k in cat_weights})
st.subheader('Overview')
st.write({'selected_month':month,'total_score':round(total,2),'scenario_label':sc.final_label})
st.write(cat_scores)

st.subheader('Indicator table')
tbl=cur[['indicator_id','value','confidence','source_url','notes','input_type']].copy(); tbl['score']=tbl['indicator_id'].map(scores); st.dataframe(tbl)
st.subheader('Trend charts')
trend=obs.groupby('date',as_index=False)['value'].mean(); st.plotly_chart(line_chart(trend,'date','value',title='Average indicator value over time'))
st.subheader('Evidence library'); st.dataframe(cur[['indicator_id','source_url','notes','input_type']])
st.subheader('Monthly report generator')
if st.button('Generate report'):
    text=generate_monthly_report(month, sc.final_label,total,cat_scores, sorted(scores.items(), key=lambda x:x[1], reverse=True)[:5], [], list(cur['notes'].dropna().head(5)), ['Track financing stress','Review capex guidance'])
    path=save_report(text, month)
    st.success(f'Report saved: {path}')
    st.download_button('Download report', text, file_name=path.split('/')[-1])
