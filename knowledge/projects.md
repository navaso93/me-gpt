# Projects

## As a student
### Seeding Impact
Role: Co-Founder

Driven by his intention to make a good impact after his experience fundraising in Australia, and very early into his double masters degree, Marc proposed an idea to his master program peers, and found a co-founder to push it with.
The project grew and became 'Seeding Impact', a platform in charge of connecting educational ressources in the energy and sustainability tech ecosystem in Europe, with incubators and start-ups in developping countries.
After organizing several promotional events and hackathons with challenges proposed by KTH and also some real-world incubators, there were a few trips organized for summer 2017, financed by KTH and Seeding Impact (after being granted a fund).
Marc travelled to Ethiopia with a couple peers, and for a monthcontributed to defining the expansion strategy of a small start-up with the mission of providing sanitized water to rural areas in Ethiopia.
The two weeks internship included field trips to rural villages to inform locals of the plans and the infrastructure requirements for the works to be completed.

Technologies: Excel

## During career
### PV Dome
Role: Creator and full-stack developer.

PV Dome is an actively developed full-stack MVP for managing and modelling commercial and industrial solar PV portfolios. It centralizes technical, contractual, operational, and financial asset information that would otherwise be distributed across spreadsheets, contracts, and monitoring platforms. It is intended for solar asset managers, portfolio owners, analysts, and investors. The MVP is suitable for demonstrations and workflow validation, but it is not yet a production-ready SaaS product.

Users can sign in to an organization-scoped workspace; create assets containing one or more PV systems; manage locations, owners, counterparties, tariffs, foreign-exchange rates, client contracts, O&M, insurance, and financing; enter monthly energy, irradiance, and performance-ratio simulations; generate and save monthly energy and cash-flow scenarios; record actual operational and financial results; compare actuals with a selected projection; and monitor portfolio, operational-data, and asset-definition completeness.

Marc conceived the product, defined its domain and workflows, and developed the MVP from a notebook prototype into a full-stack application. His work includes database and domain modelling, projection calculations, financial cash flows, authentication, organization-level security, asset-management workflows, operational analysis, frontend development, testing, and deployment configuration.

Marc used AI-assisted development extensively, particularly for frontend work and unfamiliar technical areas. He remained responsible for requirements, architecture and product decisions, reviewing generated output, testing workflows, and resolving problems. This strengthened both his ability to use AI tools critically and his understanding of the complete architecture.

The architecture has three main parts: a Next.js and TypeScript web application; a Supabase/PostgreSQL database with authentication and organization-level Row Level Security; and a separate Python and pandas calculation engine for projections and financial cash flows. Supabase is the source of truth. Assets are the main business objects, each asset can contain multiple PV systems, technical simulations begin at PV-system level, and operational comparison occurs at asset-month level. Authorization is enforced in PostgreSQL rather than only in the interface.

Important challenges included translating a flexible spreadsheet-style workflow into a relational product, maintaining consistent units and currencies, preventing partially saved assets, modelling different financing structures, and securing organization access. Marc chose incremental development to avoid overengineering, while preserving the original Jupyter and Streamlit prototype as a reference.

Technologies: Next.js, React, TypeScript, Tailwind CSS, Python, pandas, SQLAlchemy, Supabase, PostgreSQL, Supabase Auth, Row Level Security, Vercel, GitHub, Streamlit, and Jupyter.

Repository: https://github.com/navaso93/pv_assets

### LIAR Political-Statement Classification Project
Role: Data Scientist in a group project.

Marc developed the data preprocessing pipeline and trained Naive Bayes and combined
Naive Bayes-XGBoost classification models. His responsibilities included combining and
cleaning LIAR and Politifact data, grouping six truthfulness labels into three
categories, evaluating models using accuracy, recall, and macro F1, and building
ChromaDB retrieval with Gemini explanations.

Technologies: Python, pandas, scikit-learn, XGBoost, RoBERTa, ChromaDB, Gemini, FastAPI,
natural language processing (NLP), retrieval-augmented generation (RAG).

Repository: https://github.com/navaso93/liar_project

### Marc GPT Online CV Project
Role: Creator and developer.

Marc GPT is a deliberately small portfolio project: a RAG-powered online CV where
recruiters ask questions and receive answers grounded only in Marc's public knowledge
base. The initial version uses structured Markdown, a Streamlit interface, lexical
retrieval, explicit source citations, and an optional OpenAI answer generator.

Technologies: Python, Streamlit, Markdown, retrieval-augmented generation (RAG), OpenAI.
