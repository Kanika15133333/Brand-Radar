
import streamlit as st
import pandas as pd
from difflib import SequenceMatcher

st.set_page_config(page_title="BrandRadar", page_icon="🛡️", layout="wide")

# -----------------------------
# Demo data
# -----------------------------
SOCIAL = pd.DataFrame([
    {"platform":"Instagram","handle":"@acme_official","display_name":"ACME","followers":128000,"verified":True,"logo_match":True,"suspicious_words":0,"url":"https://instagram.com/acme_official","type":"Official"},
    {"platform":"Instagram","handle":"@acme_support_help","display_name":"ACME Support Help","followers":4200,"verified":False,"logo_match":True,"suspicious_words":2,"url":"https://instagram.com/acme_support_help","type":"Impersonation"},
    {"platform":"X","handle":"@acme_india_deals","display_name":"ACME India Deals","followers":1800,"verified":False,"logo_match":True,"suspicious_words":3,"url":"https://x.com/acme_india_deals","type":"Scam"},
    {"platform":"LinkedIn","handle":"ACME Technologies","display_name":"ACME Technologies","followers":9500,"verified":False,"logo_match":True,"suspicious_words":1,"url":"https://linkedin.com/company/acme-technologies","type":"Impersonation"},
    {"platform":"Facebook","handle":"ACME Careers","display_name":"ACME Careers","followers":760,"verified":False,"logo_match":False,"suspicious_words":1,"url":"https://facebook.com/acme.careers","type":"Lookalike"},
    {"platform":"Instagram","handle":"@acmestore","display_name":"ACME Store","followers":32000,"verified":False,"logo_match":False,"suspicious_words":2,"url":"https://instagram.com/acmestore","type":"Suspicious"},
    {"platform":"X","handle":"@acme","display_name":"ACME","followers":200000,"verified":True,"logo_match":True,"suspicious_words":0,"url":"https://x.com/acme","type":"Official"},
    {"platform":"Telegram","handle":"@acme_refund","display_name":"ACME Refund Desk","followers":540,"verified":False,"logo_match":True,"suspicious_words":3,"url":"https://t.me/acme_refund","type":"Scam"},
])

APPS = pd.DataFrame([
    {"store":"Google Play","app_name":"ACME","developer":"ACME Technologies Pvt Ltd","rating":4.6,"downloads":"1M+","logo_match":True,"description_match":True,"official":True,"url":"https://play.google.com/store/apps/details?id=com.acme"},
    {"store":"Google Play","app_name":"ACME Rewards & Cashback","developer":"Quick Rewards Ltd","rating":4.1,"downloads":"100K+","logo_match":True,"description_match":True,"official":False,"url":"https://play.google.com/store/apps/details?id=com.quick.acme"},
    {"store":"Google Play","app_name":"ACME Support","developer":"HelpDesk Solutions","rating":2.9,"downloads":"10K+","logo_match":True,"description_match":True,"official":False,"url":"https://play.google.com/store/apps/details?id=com.help.acme"},
    {"store":"App Store","app_name":"ACME India","developer":"ACME Technologies Pvt Ltd","rating":4.7,"downloads":"500K+","logo_match":True,"description_match":True,"official":True,"url":"https://apps.apple.com/app/acme-india"},
    {"store":"App Store","app_name":"ACME Banking Secure","developer":"Secure Finance Apps","rating":1.8,"downloads":"5K+","logo_match":True,"description_match":True,"official":False,"url":"https://apps.apple.com/app/acme-banking-secure"},
    {"store":"Google Play","app_name":"ACMEE","developer":"Mobile Studio 24","rating":3.2,"downloads":"1K+","logo_match":False,"description_match":True,"official":False,"url":"https://play.google.com/store/apps/details?id=com.mobile.acmee"},
    {"store":"Google Play","app_name":"ACME Careers","developer":"Jobs Fast","rating":2.5,"downloads":"5K+","logo_match":False,"description_match":True,"official":False,"url":"https://play.google.com/store/apps/details?id=com.jobs.acme"},
])

def similarity(a, b):
    a = ''.join(ch.lower() for ch in a if ch.isalnum())
    b = ''.join(ch.lower() for ch in b if ch.isalnum())
    return round(SequenceMatcher(None, a, b).ratio() * 100, 1)

def social_score(row, brand):
    name_sim = similarity(row["display_name"], brand)
    score = 0
    reasons = []
    if name_sim >= 80:
        score += 35; reasons.append(f"Name similarity {name_sim}%")
    elif name_sim >= 60:
        score += 20; reasons.append(f"Look-alike name {name_sim}%")
    if row["logo_match"]:
        score += 25; reasons.append("Brand logo detected")
    if not row["verified"]:
        score += 10; reasons.append("Not verified")
    if row["suspicious_words"] >= 2:
        score += 20; reasons.append("Scam/support/deal language")
    elif row["suspicious_words"] == 1:
        score += 10; reasons.append("Potentially misleading language")
    if row["followers"] < 5000:
        score += 5; reasons.append("Low-account footprint")
    return min(score, 100), "; ".join(reasons)

def app_score(row, brand):
    name_sim = similarity(row["app_name"], brand)
    score = 0
    reasons = []
    if name_sim >= 80:
        score += 35; reasons.append(f"Name similarity {name_sim}%")
    elif name_sim >= 60:
        score += 20; reasons.append(f"Look-alike name {name_sim}%")
    if row["logo_match"]:
        score += 25; reasons.append("Brand logo detected")
    if row["description_match"]:
        score += 20; reasons.append("Brand-like description")
    if not row["official"]:
        score += 20; reasons.append("Developer/publisher not official")
    return min(score, 100), "; ".join(reasons)

# -----------------------------
# Sidebar: Brand Profile
# -----------------------------
st.sidebar.title("🛡️ BrandRadar")
st.sidebar.caption("Digital Risk Protection — Social & App Monitoring")
brand = st.sidebar.text_input("Brand name", "ACME")
official_social = st.sidebar.text_area(
    "Official social handles (one per line)",
    "@acme_official\n@acme"
)
official_apps = st.sidebar.text_area(
    "Official app names (one per line)",
    "ACME\nACME India"
)
st.sidebar.markdown("---")
st.sidebar.info("Demo mode uses a safe sample dataset. In a production version, this layer connects to platform APIs / approved data feeds.")

social = SOCIAL.copy()
apps = APPS.copy()

official_handles = {x.strip().lower() for x in official_social.splitlines() if x.strip()}
official_app_names = {x.strip().lower() for x in official_apps.splitlines() if x.strip()}

social["Official"] = social["handle"].str.lower().isin(official_handles)
apps["Official"] = apps["app_name"].str.lower().isin(official_app_names) | apps["official"]

# Explicitly exclude legitimate assets before scoring.
social = social[~social["Official"]].copy()
apps = apps[~apps["Official"]].copy()

social[["Risk Score","Why flagged"]] = social.apply(
    lambda r: pd.Series(social_score(r, brand)), axis=1
)
apps[["Risk Score","Why flagged"]] = apps.apply(
    lambda r: pd.Series(app_score(r, brand)), axis=1
)

def level(score):
    if score >= 70: return "🔴 HIGH"
    if score >= 45: return "🟠 MEDIUM"
    return "🟢 LOW"

social["Risk"] = social["Risk Score"].apply(level)
apps["Risk"] = apps["Risk Score"].apply(level)

# -----------------------------
# Main dashboard
# -----------------------------
st.title("🛡️ BrandRadar")
st.subheader("Digital Risk Protection for Social Media & App Stores")
st.write("Find potential impersonation threats, explain *why* they were flagged, and prioritize the riskiest cases.")

c1,c2,c3,c4 = st.columns(4)
c1.metric("Social threats", len(social))
c2.metric("Suspicious apps", len(apps))
c3.metric("High-risk cases", int((social["Risk Score"]>=70).sum() + (apps["Risk Score"]>=70).sum()))
c4.metric("Official assets protected", len(official_handles) + len(official_app_names))

tabs = st.tabs(["🚨 Threat Dashboard", "📱 App Monitoring", "📣 Social Monitoring", "🧠 How Detection Works"])

with tabs[0]:
    st.markdown("### Priority queue")
    all_threats = pd.concat([
        social[["platform","handle","display_name","Risk Score","Risk","Why flagged","url"]].rename(columns={"platform":"Source","handle":"Asset","display_name":"Name"}),
        apps[["store","app_name","developer","Risk Score","Risk","Why flagged","url"]].rename(columns={"store":"Source","app_name":"Asset","developer":"Name"})
    ], ignore_index=True).sort_values("Risk Score", ascending=False)
    st.dataframe(all_threats, use_container_width=True, hide_index=True)
    st.caption("Risk scores are explainable heuristic scores for the prototype — not a claim that an account/app is definitely malicious.")

with tabs[1]:
    st.markdown("### Suspicious mobile applications")
    view = apps[["store","app_name","developer","rating","downloads","Risk Score","Risk","Why flagged","url"]].sort_values("Risk Score", ascending=False)
    st.dataframe(view, use_container_width=True, hide_index=True)
    st.markdown("**What matters:** similar name + logo/description + different developer = stronger signal.")

with tabs[2]:
    st.markdown("### Potential social impersonations")
    view = social[["platform","handle","display_name","followers","verified","logo_match","Risk Score","Risk","Why flagged","url"]].sort_values("Risk Score", ascending=False)
    st.dataframe(view, use_container_width=True, hide_index=True)
    st.markdown("**What matters:** name similarity + logo usage + suspicious language + lack of verification.")

with tabs[3]:
    st.markdown("### Explainable detection engine")
    st.markdown("""
**1. Official-asset exclusion**  
Exact official handles and app names are marked legitimate **before** scoring, reducing false positives.

**2. Look-alike name detection**  
We normalize names and calculate similarity, catching spacing changes, character changes and added words.

**3. Brand-identity signals**  
Logo match and brand-like descriptions increase confidence.

**4. Context signals**  
Unverified accounts, scam/support/deal language and non-official publishers increase risk.

**5. Priority score**  
Signals are combined into a 0–100 score so a security/brand team can investigate the most urgent cases first.

> Production upgrade: connect approved platform/app-store feeds, add image embeddings/OCR, historical behavior, and human analyst feedback.
""")
    st.success("Demo story: configure ACME → scan external assets → official accounts are excluded → fake accounts/apps rise to the top → analyst sees the evidence behind every score.")

st.markdown("---")
st.caption("BrandRadar • Hackathon prototype • Built for Digital Risk Protection — Social & App Monitoring")

