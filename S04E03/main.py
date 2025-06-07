from dotenv import load_dotenv
import os
import requests
import openai
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

print("Starting the script...")
load_dotenv()

AIDEVS_KEY = os.getenv("AIDEVS_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBSITE_URL = "https://softo.ag3nts.org/"

CENTRALA_URL = f"https://centrala.ag3nts.org/data/{AIDEVS_KEY}/softo.json"

openai.api_key = OPENAI_API_KEY

all_discovered_links = set()

def get_questions():
    print("\nFetching questions from API...")
    response = requests.get(CENTRALA_URL)
    response.raise_for_status()
    questions = response.json()
    print("Received questions:")
    print(questions)
    return questions

def get_text_and_links(url):
    print(f"\nFetching content from URL: {url}")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    text = soup.get_text(separator=" ", strip=True)
    
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        link_text = a.get_text(strip=True)
        links.append({"href": href, "text": link_text})

    # Add newly found links to the global set (only the href)
    for link_data in links:
        all_discovered_links.add(link_data["href"])

    print(f"Found {len(links)} links on the page. Total unique links discovered: {len(all_discovered_links)}")
    print(f"Text preview: {text[:200]}...")
    return text, links

def ask_llm(question, text, links):
    print(f"\nAsking LLM about question: {question}")
    
    formatted_links_for_prompt = ""
    for link_data in links:
        formatted_links_for_prompt += f"- Text: {link_data.get('text', 'N/A')}, URL: {link_data.get('href', 'N/A')}\n"

    prompt = f"""
Pytanie: {question}

Oto tekst aktualnej strony:
{text[:2000]}...

Dostępne linki:
{formatted_links_for_prompt}

Na podstawie powyższego:
1. JEŻELI odpowiedź na pytanie znajduje się w 'Oto tekst aktualnej strony', zwróć odpowiedź w formacie JSON: {{\"answer\": \"Twoja odpowiedź tutaj\"}}. Odpowiedź powinna być zwięzła i zawierać tylko istotne informacje. Nie możesz zwrócić, że nie ma odpowiedzi na obecnej stronie. W takim przypadku musisz zwrócić jeden z dostepnych linków (patrz punkt nr 2).
2. JEŻELI odpowiedź NIE znajduje się w 'Oto tekst aktualnej strony', wskaż link z 'Dostępne linki' prowadzący do podstrony, która może zawierać odpowiedź. Nazwa podstrony nie zawsze będzie taka sama jak w pytaniu. Musisz odpowiednio dopasować link. Zwróć TYLKO jeden link w formacie JSON {{\"link\": \"/pelna/sciezka/do/linku\"}} (link powinien być zawsze bezwzględny, czyli zaczynać się od / lub http://). Jezeli nie ma odpowiedniego linku, spróbuj dopasować najbardziej prawdopodobną możliwość z podanych linków
"""
    print("Prompt: ", prompt)

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content.strip()
    print(f"LLM raw response: {result}")

    try:
        json_response = json.loads(result)
        if "answer" in json_response:
            print("LLM returned a direct answer.")
            return json_response
        elif "link" in json_response:
            print("LLM returned a suggested link in JSON format.")
            # Ensure the link value is a string, not another dictionary if LLM messes up
            if isinstance(json_response["link"], str):
                return json_response
            else:
                print(f"LLM returned 'link' value that is not a string: {json_response['link']}. Returning None.")
                return None
        else:
            print(f"LLM returned valid JSON but without 'answer' or 'link' key: {json_response}. Returning None.")
            return None
    except json.JSONDecodeError:
        if result.lower() == "none":
            print("LLM explicitly returned 'NONE'. Returning None.")
            return None
        else:
            print(f"LLM returned unexpected non-JSON string: {result}. Returning None.")
            return None

def recursive_search(question, url, visited=None, depth=0):
    if visited is None:
        visited = set()

    print(f"\nRecursive search - Depth: {depth}")
    print(f"Current URL: {url}")
    print(f"Visited URLs so far: {len(visited)}")
    
    # Condition to stop:
    # 1. If URL is None
    # 2. If max depth is reached
    # 3. If URL has been visited, UNLESS it's the WEBSITE_URL
    if url is None or depth > 5 or (url in visited and url != WEBSITE_URL):
        reason = ""
        if url is None:
            reason = "URL is None"
        elif depth > 5:
            reason = "Max depth reached"
        elif url in visited and url != WEBSITE_URL:
            reason = "URL already visited (and not WEBSITE_URL)"
        print(f"Stopping search - {reason}")
        return None

    visited.add(url)
    text, page_links = get_text_and_links(url)

    # heuristic: check if answer is on the page (can be removed if LLM handles this)
    # if question.lower().split()[0] in text.lower():
    #     print("Found potential answer on current page!")
    #     return text[:1000]  # or full match logic

    try:
        llm_response = ask_llm(question, text, page_links)
    except Exception as e:
        print(f"Error during LLM call: {e}")
        return None

    if isinstance(llm_response, dict) and "answer" in llm_response:
        # If LLM explicitly says no answer, force it to behave as if it returned {"link": "NONE"}
        if llm_response["answer"].strip().lower() == "none":
            print("LLM returned {\"answer\": \"NONE\"}. Forcing to {\"link\": \"NONE\"} for fallback processing.")
            llm_response = {"link": "NONE"}
        else:
            print("Returning direct answer from LLM.")
            return llm_response["answer"]

    # Determine the raw link value, if any, from LLM response
    raw_link_value = None
    if isinstance(llm_response, dict) and "link" in llm_response:
        raw_link_value = llm_response["link"]
    # If llm_response was None, raw_link_value remains None.

    next_link_for_recursion = None

    if raw_link_value and raw_link_value.lower() == "none":
        # Fallback strategy: if LLM says NONE, try the first *unvisited and non-root* available link
        fallback_link_found = False
        for link_data in page_links: 
            potential_link_href = link_data.get("href")
            # Convert potential_link_href to absolute first to check against visited correctly
            absolute_potential_link = urljoin(url, potential_link_href)

            if potential_link_href and potential_link_href != "/" and absolute_potential_link not in visited:
                next_link_for_recursion = absolute_potential_link # Store the absolute URL here
                print(f"LLM returned NONE. Falling back to the next unvisited, non-root link on the current page: {next_link_for_recursion}")
                fallback_link_found = True
                break
            
        if not fallback_link_found:
            print("LLM returned NONE and no suitable fallback links available on current page or all suitable links already visited. Stopping this recursive path.")
            return None
    elif raw_link_value: # LLM returned a specific link (not NONE)
        # If LLM returned a specific link, make sure it's absolute or root-relative before proceeding
        if not raw_link_value.startswith('http://') and not raw_link_value.startswith('https://') and not raw_link_value.startswith('/'):
            next_link_for_recursion = '/' + raw_link_value # Force it to be root-relative if it's just a segment
            print(f"LLM suggested a path-relative link: {raw_link_value}, converting to root-relative: {next_link_for_recursion}")
        else:
            next_link_for_recursion = raw_link_value # It's already absolute or root-relative
            print(f"LLM suggested a link in JSON format: {next_link_for_recursion}")
    else: # llm_response was not a dict with 'link' or 'answer', likely None from ask_llm
        print("LLM did not suggest a valid link or direct answer. Stopping this recursive path.")
        return None

    # This crucial step ensures next_link_for_recursion is always an absolute URL
    # no matter if it came from LLM as relative, absolute, or from fallback.
    # It handles cases where url is 'https://softo.ag3nts.org/' and next_link_for_recursion is '/uslugi' -> https://softo.ag3nts.org/uslugi
    # It handles cases where url is 'https://softo.ag3nts.org/uslugi' and next_link_for_recursion is '/portfolio' -> https://softo.ag3nts.org/portfolio
    final_next_link = urljoin(url, next_link_for_recursion)

    # NEW LOGIC: If the resolved link is already visited (and not the WEBSITE_URL),
    # attempt to find a different unvisited link from the current page's links.
    if final_next_link in visited and final_next_link != WEBSITE_URL:
        print(f"LLM suggested already visited link: {final_next_link}. Attempting to find next unvisited link from current page.")
        re_fallback_link_found = False
        for link_data in page_links:
            potential_re_fallback_href = link_data.get("href")
            absolute_re_fallback_link = urljoin(url, potential_re_fallback_href)

            if potential_re_fallback_href and potential_re_fallback_href != "/" and absolute_re_fallback_link not in visited:
                final_next_link = absolute_re_fallback_link # This is the new next link
                print(f"Falling back to next unvisited, non-root link on current page: {final_next_link}")
                re_fallback_link_found = True
                break
        
        if not re_fallback_link_found:
            print("LLM suggested already visited link and no suitable unvisited fallback links available. Stopping this recursive path.")
            return None

    print(f"Resolved next link for recursion: {final_next_link}")

    return recursive_search(question, final_next_link, visited, depth + 1)

questions = get_questions()
collected_answers = {}
for question_id, question_text in questions.items():
    print(f"\nProcessing question ID: {question_id} - Text: {question_text}")
    answer = recursive_search(question_text, WEBSITE_URL)
    print(f"\nAnswer for question [{question_id}]: {question_text}")
    print(answer)
    if answer: # Only add if an answer was found
        collected_answers[question_id] = answer

print("\nAll questions processed. Sending results to report endpoint...")

REPORT_URL = "https://c3ntrala.ag3nts.org/report"
report_payload = {
    "task": "softo",
    "apikey": AIDEVS_KEY, # Use AIDEVS_KEY as the API key
    "answer": collected_answers
}

print(f"Sending payload to {REPORT_URL}: {report_payload}")
try:
    report_response = requests.post(REPORT_URL, json=report_payload)
    report_response.raise_for_status() # Raise an exception for bad status codes
    print("Successfully sent report!")
    print("Report API response:", report_response.json())
except requests.exceptions.RequestException as e:
    print(f"Error sending report: {e}")





