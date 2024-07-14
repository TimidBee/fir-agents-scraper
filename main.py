import csv
import requests
import json
import pandas as pd
import time

url = 'https://www.fir.com/wp-admin/admin-ajax.php'
base_url = 'https://www.fir.com/agents'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://www.fir.com/agents',
    'X-Requested-With': 'XMLHttpRequest',
}


def load_more_agents(base_url, headers):
    all_agents = []
    page_num = 1
    loaded_agents = []  # Initialize a list to keep track of loaded agents

    while True:
        print(f"Fetching page {page_num}...")
        payload = {
            'action': 'get_agents',
            'loadedAgents': json.dumps(loaded_agents),
            'agentName': '',
            'languages': '',
            'office': 'office',
        }

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            try:
                data = response.json()
                agents = data  # Assign the response directly since it's a list

                if not agents:
                    break

                for agent in agents:
                    agent_id = agent.get('post_id')
                    if agent_id not in loaded_agents:
                        loaded_agents.append(agent_id)
                        all_agents.append({
                            'Name': agent.get('title'),
                            'Phone': agent.get('mobile'),
                            'Email': agent.get('email'),
                            'Languages': agent.get('languages'),
                            'Branch': agent.get('branch'),
                            'Office': agent.get('office'),
                            'Thumbnail': agent.get('thumbnail'),
                            'Permalink': agent.get('permalink')
                        })

                page_num += 1
                time.sleep(1)  # Add a short delay to avoid hitting the server too frequently

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {str(e)}")
                break

        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            break

    return all_agents


def save_to_csv(all_agents, filename):
    keys = all_agents[0].keys() if all_agents else []
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_agents)


all_agents = load_more_agents(base_url, headers)
save_to_csv(all_agents, 'agents_data.csv')

print(f"Total agents scraped: {len(all_agents)}")
