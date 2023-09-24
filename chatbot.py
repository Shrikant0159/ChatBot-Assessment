import requests
from bs4 import BeautifulSoup
import openai

# OpenAI API key
api_key = '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'

# Initialize
openai.api_key = api_key

# Step 1: Web Scraping

url = "https://brainlox.com/courses/category/technical"

# Send a request to the URL
response = requests.get(url)

# if status code 200
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the course listings on the page
    course_listings = soup.find_all("div", class_="courses-content")

    # Initialize a list to store course information
    courses = []

    # Loop extract course details
    for listing in course_listings:
        title = listing.find("h3").text.strip()
        description = listing.find("p").text.strip()
        course_url = listing.find("a", class_="BookDemo-btn")["href"]

        # store course information
        course_info = {
            "Title": title,
            "Description": description,
            "URL": course_url
        }

        # Append the course information
        courses.append(course_info)

    # Step 2: Data Structuring and Cleaning 

    # Handle missing data and remove duplicates
    unique_courses = []
    seen_titles = set()

    for course in courses:
        title = course["Title"]

        # Handle missing title, description, and URL
        if not title:
            course["Title"] = "No Title Available"

        if not course.get("Description"):
            course["Description"] = "No Description Available"

        if not course.get("URL"):
            course["URL"] = "No URL Available"

        # based on title Remove duplicates
        if title not in seen_titles:
            seen_titles.add(title)
            unique_courses.append(course)

    # Format data into a dictionary
    formatted_data = {course["Title"]: {"Description": course["Description"], "URL": course["URL"]} for course in courses}
    #print(formatted_data)

    #  chatbot 
    def generate_response(user_input):
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=user_input,
                max_tokens=50
            )
            return response.choices[0].text

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
    
    # Step 3: Final step 
    def chatbot():
        print("Chatbot: Hello! I'm here to help you find technical courses.")

        while True:
            user_input = input("You: ")

            if user_input.lower() in ['exit', 'quit']:
                print("Chatbot: Goodbye!")
                break

            elif user_input.lower():
                print("Chatbot: Sure, what topic are you interested in?")
                user_topic = input("You: ")

                print(f"Chatbot: Great! Let me find courses related to {user_topic}")
                user_courses = []
                for course in unique_courses:
                    if user_topic.lower() in course['Title'].lower() or user_topic.lower() in course['Description'].lower():
                        user_courses.append(course)

                if user_courses:
                    print("Chatbot: Here are some courses I found:")
                    for course in user_courses:
                        print(f"- Title: {course['Title']}")
                        print(f"  Description: {course['Description']}")
                        print(f"  URL: {course['URL']}")
                else:
                    print("Chatbot: I couldn't find any courses on that topic.")
            else:
                chatbot_response = generate_response(user_input)
                if chatbot_response:
                    print("Chatbot:", chatbot_response)
                else:
                    print("Chatbot: I'm not sure how to respond to that.")

    if __name__ == "__main__":
        chatbot()
else:
    print("Failed to retrieve data. Check the URL or your internet connection.")
