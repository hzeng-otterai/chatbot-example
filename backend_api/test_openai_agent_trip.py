import os
import random
from typing import Optional
from agents import Agent, Runner, function_tool


@function_tool
def get_weather(location: str, day: Optional[str] = None) -> str:
    """Get current weather for a given location."""
    # Mock weather API call
    # In a real implementation, you would call an actual weather API
    weather_conditions = ["Sunny", "Cloudy", "Rainy", "Partly cloudy"]
    day_str = f" on {day}" if day else ""
    result = f"Weather in {location}{day_str}: {random.choice(weather_conditions)}, 22°C"
    return result

@function_tool
def suggest_poi(location: str, preference: str, category: Optional[str] = None) -> str:
    """Suggest points of interest based on location and preferences."""
    # Sample POI suggestions based on city and preference
    city = location.split(',')[0].strip().lower()
    poi_by_city = {
        "paris": {
            "indoor": ["Louvre Museum", "Musée d'Orsay", "Notre-Dame Cathedral"],
            "outdoor": ["Eiffel Tower", "Seine River Cruise", "Champs-Élysées"]
        },
        "new york": {
            "indoor": ["Metropolitan Museum", "Museum of Modern Art", "Broadway Theater"],
            "outdoor": ["Central Park", "Statue of Liberty", "Brooklyn Bridge"]
        }
    }
    # Default POIs if city not recognized
    default_indoor = ["National Gallery", "Science Museum", "Shopping Mall"]
    default_outdoor = ["Golden Gate Bridge", "Beach Promenade", "City Park"]

    if city in poi_by_city:
        indoor_pois = poi_by_city[city]["indoor"]
        outdoor_pois = poi_by_city[city]["outdoor"]
    else:
        indoor_pois = default_indoor
        outdoor_pois = default_outdoor

    if preference == "indoor":
        suggestions = indoor_pois[:3]
    elif preference == "outdoor":
        suggestions = outdoor_pois[:3]
    else:  # both
        suggestions = indoor_pois[:2] + outdoor_pois[:2]
        
    result = f"Suggested POIs in {location} ({preference}): {', '.join(suggestions)}"
    return result

@function_tool
def buy_ticket(attraction: str, location: str, date: str, quantity: int) -> str:
    """Purchase tickets for attractions that require them."""
    # Simulate ticket purchase
    ticket_price = 25  # Mock price
    total_cost = ticket_price * quantity
    result = f"Successfully purchased {quantity} ticket(s) for {attraction} in {location} on {date}. Total cost: ${total_cost}"
    return result

async def trip_planner_agent_sdk(user_message: str) -> str:
    """Main trip planner function using OpenAI Agent SDK"""
    
    # Create the agent with tools
    agent = Agent(
        name="Trip Planner Agent",
        instructions="You are a helpful trip planning assistant. Help users plan their trips by checking weather, suggesting points of interest, and buying tickets when needed. Always be friendly and provide comprehensive travel advice.",
        model="gpt-4.1",
        tools=[get_weather, suggest_poi, buy_ticket]
    )
    
    # Run the agent
    result = await Runner.run(agent, user_message)
    
    return result.final_output

# Example usage
async def main():
    # Test cases for the trip planner
    test_queries = [
        "Plan a 3 days' trip to Paris?",
        "I want to plan a trip to New York. Can you check the weather and suggest some outdoor attractions?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*50}")
        print(f"TEST QUERY {i}: {query}")
        print('='*50)
        response = await trip_planner_agent_sdk(query)
        print("Assistant:", response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 