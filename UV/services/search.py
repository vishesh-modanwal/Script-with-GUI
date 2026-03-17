
import sys
from ddgs import DDGS
import asyncio
import json
import datetime


async def main():
    if len(sys.argv) < 2:
        print("Usage: Python search.py '<Query>'")
        return

    # Get the query from command line arguments
    query = sys.argv[1]

    # Number of results you want to fetch
    number_of_results = int(input("Enter the number of results you want to fetch: "))
    
    # just as a counter aside of the results
    count = 1
    
    try:
        #printing the results
        print("\t"+"-"*(len(query)+70))
        print(f"\t {"="*5} Searching for: {query} - Printing the titles and repective urls {"="*5}")
        print("\t"+"-"*(len(query)+70)+"\n")

        for ddgs in DDGS().text(query, max_results=number_of_results):
            print(f"| {count}: | {ddgs['title']} ---->\t {ddgs['href']}\n")
            count += 1


        # for videos and corresponding data
        print("\n\n\t"+"-"*(len(query)+60))
        print(f"\t {"="*5} Searching for: {query} - Printing the videos params {"="*5}")
        print("\t"+"-"*(len(query)+60))
        vid_result = DDGS().videos(
            query=query,
            region="us-en",
            safesearch="moderate",
            timelimit='w',
            resolution='high',
            duration="medium",
            max_results=number_of_results,
        )
        vid_data = json.dumps(vid_result, indent=4)
        print(vid_data)
        print("-"*(len(query)+60))


        inp = input("\n\nWant to save this videos data in a file? (y/n): ")
        if inp.lower() == 'y':
            with open("search_results.txt", "a") as f:
                f.write("\t"+"*"*(len(query)+len(str(datetime.datetime.now()))+30) + "\n")
                f.write(f"\t|  Search Results for: {query} at {datetime.datetime.now()}  |\n")
                f.write("\t"+"*"*(len(query)+len(str(datetime.datetime.now()))+30) + "\n")
                for item in vid_result:
                    f.write("-"*60 + "\n")
                    f.write(f"Title: {item['title']}\n")
                    f.write(f"Content: {item['content']}\n")
                    f.write(f"Description: {item['description']}\n")
                    f.write(f"Duration: {item['duration']}\n")
                    f.write(f"Embeded HTML: {item['embed_html']}\n")
                    f.write(f"Embeded URL: {item['embed_url']}\n")
                    f.write(f"Image Token: {item['image_token']}\n")
                    f.write(f"Images: {item['images']}\n")
                    f.write(f"Provider: {item['provider']}\n")
                    f.write(f"Published: {item['published']}\n")
                    f.write(f"Publisher: {item['publisher']}\n")
                    f.write(f"Statistics: {item['statistics']}\n")
                    f.write(f"Uploader: {item['uploader']}\n")
                    f.write("-"*60 + "\n")
                f.write("\n\n")
            print(f"| {"-"*10} Data saved to search_results.txt {"-"*10} |")
        else:
            print(f"| {"-"*10} Data not saved {"-"*10} |")
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    asyncio.run(main())



from ddgs import DDGS
import datetime


def search_duckduckgo(query, number_of_results=5):
    try:
        text_results = []
        video_results = []

        # TEXT SEARCH
        with DDGS() as ddgs:
            for result in ddgs.text(query, max_results=number_of_results):
                text_results.append({
                    "title": result.get("title"),
                    "url": result.get("href")
                })

        # VIDEO SEARCH
        with DDGS() as ddgs:
            vids = ddgs.videos(
                query=query,
                region="us-en",
                safesearch="moderate",
                timelimit="w",
                resolution="high",
                duration="medium",
                max_results=number_of_results,
            )

            for item in vids:
                video_results.append({
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "duration": item.get("duration"),
                    "published": item.get("published"),
                    "publisher": item.get("publisher")
                })

        return {
            "query": query,
            "timestamp": str(datetime.datetime.now()),
            "text_results": text_results,
            "video_results": video_results
        }

    except Exception as e:
        return {"error": str(e)}
