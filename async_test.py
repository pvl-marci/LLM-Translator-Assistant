import asyncio
import httpx

# The base URL of your FastAPI application
BASE_URL = "http://127.0.0.1:8000"  # Update if your FastAPI runs on a different port

# Sample texts to send to the grammar-check API
texts = [
    "He don’t like pizza very much, but sometimes he eat it with his friends at the weekend. They usually goes to a pizzeria near his house.",  # "eat" to "eats", "goes" to "go"
    "They was late to class because the traffic was bad and they miss the bus. When they finally arrived, the teacher had already start the lesson.",  # "was" to "were", "miss" to "missed", "start" to "started"
    "She walk to school every day even when the weather is bad. Sometimes she listens to music or chats with her friend while she walk.",  # "walk" to "walks", "friend" to "friends", "walk" to "walks"
    "I can plays the guitar quite well, and I often practice for hours. My friends says that I should perform at a local concert soon.",  # "plays" to "play", "says" to "say"
    "The cat sleep on the mat during the day and sometimes it also lay on the couch. At night, it usually move to my bed and curls up beside me.",  # "sleep" to "sleeps", "lay" to "lays", "move" to "moves"
    "He don't know how to cook very well, so he always ask his mom for help when he need to prepare a meal. She usually give him simple recipes.",  # "don’t" to "doesn't", "ask" to "asks", "need" to "needs", "give" to "gives"
    "The children was excited for the trip to the zoo, but it start raining and they had to go home early. They was disappointed but they promise to try again another day.",  # "was" to "were", "start" to "started", "was" to "were", "promise" to "promised"
    "She have been working at the company for three years, but she still don't feels comfortable with the new software. She hopes to get more training soon.",  # "have" to "has", "don't feels" to "doesn't feel"
    "I was going to the store yesterday, but I forgot my wallet at home and had to came back. By the time I returned, the store was already closed.",  # "had to came" to "had to come"
    "The movie we watched last night was very interesting, but it was also quite long and we didn’t got home until very late. We were all very tired today.",  # "got" to "get"
    "He usually don’t like to eat vegetables, but he ate them willingly because his doctor told him it’s important for him health. He even tried a new recipe for carrots.",  # "him health" to "his health"
    "They was planning a surprise party for their friend's birthday, but they didn't realized he was going to be out of town that weekend. They had to change their plans.",  # "was" to "were", "realized" to "realize"
    "She always forgets to bring her lunch to work, so she end up buying something from the café nearby. It’s getting quite expensive over times.",  # "end up" to "ends up", "over times" to "over time"
    "I had went to the bank to withdraw some money, but they told me that my account had been locked due to some security issues. I needs to visit the branch to resolve it.",  # "had went" to "went", "needs" to "need"
    "The dog loves to run in the park, but he often gets tired quickly and need to takes breaks. His owner always bring water and a blanket for him.",  # "need" to "needs", "takes" to "take", "bring" to "brings"
    "He don't understand why his computer keeps crashing during important meetings. He has tried everything, but the problem still persist and it's very frustrating.",  # "persist" to "persists"
    "The restaurant we went to last night was very nice, but the service was slow and the food was not as good as we expected. We might try another place next time.",  # Correct
    "She had been studying for the exam for weeks, but when she got the test, she found it was much harder than she thought. She hopes she did well.",  # Correct
    "They was excited to go on vacation, but when they arrived at the airport, they found out their flight had been delayed. They spend hours waiting in the terminal.",  # "was" to "were", "spend" to "spent"
    "He was always forgetting to turn off the lights when he leave the house, and his electricity bill was higher than he expected. He decided to set reminder.",  # "leave" to "leaves", "reminder" to "reminders"
    "The children was playing outside when it suddenly started to rain. They ran inside quickly, but some of them got wet and needed to change their cloth.",  # "was" to "were", "cloth" to "clothes"
    "She doesn’t likes to go to crowded places, so she prefers to do her shopping early in the morning or late at night when there’s fewer people around.",  # "likes" to "like"
    "I can’t believes how quickly time has flown by. It feels like just yesterday that we were starting this project, and now we’re almost finished with it.",  # "believes" to "believe"
    "The team was working on the presentation all week, but they didn’t have enough time to rehearse it properly. The presentation didn’t go as smooth as they hoped.",  # "smooth" to "smoothly"
    "He don’t have enough experience for the job he applied for, but he’s very enthusiastic and willing to learn. He hopes that his positive attitude will make up for his lacks of experience.",  # "don’t" to "doesn't", "lacks of experience" to "lack of experience"
    "They was trying to fix the car themselves, but they realized it was too complicated and decided to take it to a mechanic. The repair costed was quite high.",  # "was" to "were", "costed" to "cost"
    "She always buys groceries in bulk to save money, but sometimes she ends up with more food than she can use before it expire. She needs to plan better.",  # "expire" to "expires"
    "I went to the library to borrow some books, but I forgot to return the ones I had previously borrowed. Now, I have to paying a late fee before I can borrow new ones.",  # "paying" to "pay"
    "The kids was excited for the summer camp, but they forgot to pack some important items like sunscreens and hat. They ended up buying these items at the camp.",  # "was" to "were", "sunscreens" to "sunscreen", "hat" to "hats"
    "He had went to the gym every day for a month, but he didn’t see much progress and felt discouraged. He decided to consult a personal trainer for advices.",  # "had went" to "went", "advices" to "advice"
    "They was visiting their grandparents over the weekend, but the weather was so bad that they couldn’t go out for any activities. They spend most of the time indoors.",  # "was" to "were", "spend" to "spent"
    "She have a lot of books that she wants to read, but she never seems to find the time to sit down and enjoy them. Her work schedule are very demanding.",  # "have" to "has", "are" to "is"
    "I tried to bake a cake for my friend’s birthday, but I accidentally used salt instead of sugar. The cake tasted terrible, and I had to go buy one from a bakery.",  # Correct
    "The company was organizing a team-building event, but many employees couldn’t attend due to other commitments. The event was not as successful as they hoped.",  # Correct
    "He don’t understand why his phone battery drains so quickly. He has tried changing settings and closing apps, but the problem still persists.",  # Correct
    "They was looking forward to their weekend getaway, but the weather forecast predicted a storm. They had to cancel their plans and stay home instead.",  # Correct
    "She have a collection of vintage postcards, but she hasn’t had the chance to organize them yet. They are all kept in a box, and it’s hard to find specific one.",  # "one" to "ones"
    "I was planning to attend the conference, but I got sick the day before and had to stay home. I missed out on some important networking opportunities.",  # Correct
    "The cat was playing with a toy, but it accidentally knocked over a vase and broke it. The owner was upset, but they cleaned up the mess and bought a new vase.",  # Correct
    "He don’t know how to fix the leaky faucet in the kitchen, so he called a plumber for help. The plumber came and fix it, but it was quite expensive.",  # "don’t" to "doesn't", "fix" to "fixed"
    "They was trying to improve their diet, so they started cooking more meals at home. However, they sometimes forget to plan ahead and end up ordering takeouts.",  # "was" to "were", "takeouts" to "takeout"
    "She always forgets her keys when she leave the house, and she had to call a locksmith twice this month. She’s thinking of getting a key holder for door.",  # "leave" to "leaves", "for door" to "for the door"
    "I had went to the doctor for a check-up, but they told me I needed additional tests to determine what was causing my symptoms. It was a bit stressful waiting for the result.",  # "had went" to "went", "result" to "results"
    "The children was excited for their field trip to the museum, but they had to wait in line for a long time before they could enter. They enjoyed the exhibits once they inside.",  # "was" to "were", "they inside" to "they were inside"
    "He was planning a surprise dinner for his partner, but he didn’t realized they had a prior engagement. He had to reschedule the dinner and tell them about the surprise.",  # "realized" to "realize"
    "They was building a treehouse in their backyard, but they didn’t have all the necessary tools and material. They had to make several trips to the hardware store.",  # "was" to "were", "material" to "materials"
    "She don’t like to watch horror movies because they scare her, but she agreed to watch one with her friends. She ended up feeling very anxious during the films.",  # "don’t" to "doesn't", "films" to "film"
    "I was supposed to meet my friend for coffee, but I forgot about the appointment and went to a different café. My friend had to wait for me and was a bit annoyed.",  # Correct
    "The restaurant had a special offer on desserts, but I didn’t realize that it was only valid for a limited times. By the time I ordered, the offer had already ended.",  # "limited times" to "limited time"
    "He don’t enjoy doing household chores, so he tries to find ways to make them more enjoyable. He listen to music or podcasts while he cleans to make it less boring.",  # "don’t" to "doesn't", "listen" to "listens"
    "They was planning to go hiking, but they couldn’t find their trail map and had to cancel the trip. They decided to go for a walk in the park instead.",  # "was" to "were", "map" to "maps"
    "She have a lot of emails to respond to, but she finds it hard to keep up with all of them. She try to set aside specific times each day to manage her inbox.",  # "have" to "has", "try" to "tries"
    "I went to the gym early this morning, but I forgot to bring my water bottle. I had to buying one from the vending machine, which was more expensive than usual.",  # "buying" to "buy"
    "The movie theater was having a special screening of a classic film, but the tickets sold out quick. I couldn’t get one and had to find an alternative activity.",  # "quick" to "quickly"
    "He was excited about his new job, but he found out that the commute was much longer than he expected. He considering moving closer to work to save time.",  # "considering" to "is considering"
    "They was hosting a barbecue party, but it started raining heavily just before the guests arrived. They had to move everything inside and the party wasn’t as fun.",  # Correct
    "She don’t like taking public transportation, so she usually drives to work. However, parking has become more difficult and she’s considering alternative.",  # "don’t" to "doesn't", "alternative" to "alternatives"
    "I had planned to go for a run in the park, but I forgot to check the weather forecast. It was too windy and cold, so I had to exercise indoor instead.",  # "indoor" to "indoors"
    "The book I borrowed from the library was due yesterday, but I haven’t had time to return it yet. I hope they won’t charge me a late fees for the overdue book.",  # "fees" to "fee"
]


# Function to send a POST request to the grammar-check API
async def send_request(text):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/grammar-check-api",
                data={"text_to_rewrite": text},
                timeout=10.0,  # Timeout after 10 seconds
            )
            response.raise_for_status()  # Raise an error for HTTP response codes 4xx/5xx
            print(f"Response for text: {text}\nStatus Code: {response.status_code}")
            print(response.text)  # Print the response content (HTML or JSON)
        except httpx.ReadTimeout:
            print(f"Request timed out for text: {text}")
        except httpx.RequestError as exc:
            print(f"Request error for text '{text}': {exc}")
        except Exception as e:
            print(f"An unexpected error occurred for text '{text}': {e}")


# Main function to run multiple asynchronous requests
async def main():
    tasks = [send_request(text) for text in texts]  # Create a task for each text
    await asyncio.gather(*tasks)  # Run the tasks concurrently


# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
