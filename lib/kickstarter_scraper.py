from bs4 import BeautifulSoup
import json

def create_project_dict():
    with open('../fixtures/kickstarter.html', 'r', encoding='utf-8') as file:
        html = file.read()

    kickstarter = BeautifulSoup(html, 'html.parser')
    projects = {}

    for project in kickstarter.select("li.project.grid_4"):
        title = project.select_one("h2.bbcard_name strong a").text.strip()
        projects[title] = {
            'image_link': project.select_one("div.project-thumbnail a img")['src'],
            'description': project.select_one("p.bbcard_blurb").text.strip(),
            'location': project.select_one("ul.project-meta span.location-name").text.strip(),
            'percent_funded': project.select_one("ul.project-stats li.first.funded strong").text.strip("%")
        }
    return projects

if __name__ == "__main__":
    projects = create_project_dict()
    
    # Analysis
    total_projects = len(projects)
    successful = sum(1 for p in projects.values() if int(p['percent_funded']) >= 100)
    avg_funding = sum(int(p['percent_funded']) for p in projects.values()) / total_projects

    print(f"\nScraped {total_projects} projects:")
    print(f"- {successful} successfully funded ({successful/total_projects:.1%})")
    print(f"- Average funding: {avg_funding:.1f}%")
    
    # Save results
    with open('kickstarter_data.json', 'w') as f:
        json.dump(projects, f, indent=2)
    print("Data saved to kickstarter_data.json")