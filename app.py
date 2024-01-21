import streamlit as st
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import SequentialChain

# Create an instance of Ollama
llm = Ollama(model='openhermes')

# Define the first prompt
first_prompt = ChatPromptTemplate.from_template(
    "Using the Problem-Agitate-Solution (PAS) framework\
        create a compelling advertising headline for {product_service}. explain how this headline uses the PAS framework. return a headline."
)
chain_one = LLMChain(llm=llm, prompt=first_prompt, output_key="headline_idea")

# Define the second prompt
second_prompt = ChatPromptTemplate.from_template(
    "Write ad body copy which will influence the user to click or say yes. 30 words or less.\
        based on this previous headline idea. Return the headline and body copy. headline: {headline_idea}. "
)
chain_two = LLMChain(llm=llm, prompt=second_prompt, output_key="headline_body")

# Define the third prompt
third_prompt = ChatPromptTemplate.from_template(
    " using the {headline_body} generate 3 variations of the headline and body at a 6th grade reading level."
)
chain_three = LLMChain(llm=llm, prompt=third_prompt, output_key="headlines")

# Define the overall chain
overall_Chain = SequentialChain(
    chains=[chain_one, chain_two, chain_three],
    input_variables=["product_service"],
    output_variables=["headline_idea", "headline_body", "headlines"],
    verbose=True,
)

st.title('AdForge: The Ultimate Ad Generator')
st.subheader('Generate some cool ads using the Problem-Agitate-Solution framework')
# st.text('')
# Ask the user for the product service
product_service = st.text_input("Enter the product service", "")

if product_service != "":
    with st.spinner('Generating ... just wait!'):
        # Run the overall chain
        seqs = overall_Chain(product_service)
    
    # Display the results
    st.markdown("{}\n".format(seqs['headline_idea']))
    st.markdown("{}\n".format(seqs['headlines']))

