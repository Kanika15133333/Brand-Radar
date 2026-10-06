# BrandRadar

## Digital Risk Protection for Social Media & App Monitoring

BrandRadar is a Digital Risk Protection platform designed to help organizations identify potential social-media impersonation accounts, fake company pages, scam profiles, and suspicious mobile applications that imitate a legitimate brand.

## Problem

Organizations can be impersonated through fake social-media accounts and fraudulent mobile applications. These threats can deceive customers, distribute scams, damage brand reputation, and misuse company identity.

BrandRadar provides a single dashboard to identify and prioritize these potential threats.

## Key Features

### Brand Profile
Organizations can define:
- Brand name
- Official social-media accounts
- Official mobile applications

### Social Media Monitoring
BrandRadar identifies potential:
- Impersonation accounts
- Fake company pages
- Scam profiles
- Look-alike names

### App Store Monitoring
BrandRadar identifies suspicious applications using:
- Similar app names
- Brand identity signals
- Similar descriptions
- Different developers or publishers

### Explainable Risk Scoring
Each potential threat receives a risk score from 0–100.

The platform also explains why an asset was flagged, using signals such as:
- Name similarity
- Logo/brand similarity
- Verification status
- Suspicious language
- Publisher/developer mismatch

### Official Asset Exclusion
Known legitimate social accounts and applications are excluded from threat detection to reduce false positives.

## Technology

- Python
- Streamlit
- Pandas
- GitHub
- Streamlit Community Cloud

## Prototype

The hackathon prototype uses a controlled demonstration dataset so that the complete detection workflow can be reliably demonstrated.

In a production version, the data ingestion layer could connect to approved social-platform APIs, app-store data sources, and licensed threat-intelligence feeds.

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
