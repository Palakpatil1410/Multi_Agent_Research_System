from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic : str) -> dict:

    state = {}

    # Step 1: Search Agent
    print("\n"+" ="*50)
    print("step 1  - search agent is working...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user",f"Find recent, reliable and detailed information about:{topic}")]

    })
    print("\nFULL SEARCH RESULT:")
    print(search_result)
    state['search_results'] = search_result['messages'][-1].content

    print("\n search result", state['search_results'])

    # Step 2: Reader Agent
    print("\n"+" ="*50)
    print("step 2  - reader agent is scraping top resources.....")
    print("="*50)
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"based on the following search resulte about '{topic}', "
            f"pick the most relevant URLs and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"

        )]
    })
    state['scrape_content'] = reader_result['messages'][-1].content

    print("\nscrape content\n", state["scrape_content"])

    # Step 3: Writer Chain
    print("\n"+" ="*50)
    print("step 3 - writer is draffting the report...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS: \n{state['search_results']}\n\n"
        f"DETAILED SCRAPE CONTENT:\n{state['scrape_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n Final report \n", state['report'])


    # Step 4: Critic Chain
    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report...")
    print("="*50)
    state["feedback"] = critic_chain.invoke({
        "report": state['report']
    })
    print("\n Critic Report \n",state['feedback'])
    
    return state  
if __name__ == "__main__":
    topic = input("\nEnter a topic to research: ")
    run_research_pipeline(topic)

