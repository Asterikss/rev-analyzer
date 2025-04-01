import streamlit as st
import wikipediaapi


# The generic format for user_agent is <client name>/<version> (<contact
# information>) <library/framework name>/<version> [<library name>/<version>
# ...]. Parts that are not applicable can be omitted.
# User-Agent: CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)
# generic-library/0.0
@st.cache_data
def get_wiki_api():
  return wikipediaapi.Wikipedia(user_agent="SimpleStreamlitAppBot/0.1", language="en")


def get_wikipedia_summary(query):
  wiki_api = get_wiki_api()
  page = wiki_api.page(query)
  if page.exists():
    return page.summary
  return "Page not found."
