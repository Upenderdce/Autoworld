import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.conf import settings
from autoworld.models import Dimensions # Your model to store data
import re
from autoworld.models import YouTubeVideo, YouTubeComment
from textblob import TextBlob
def remove_alphabet_and_symbols(s):
    # Remove all non-numeric characters
    return re.sub(r'[^0-9.]', '', s)

class Command(BaseCommand):
    help = 'Scrape data from two different sources'
    
    def handle(self, *args, **kwargs):
        self.list=[]
        self.stdout.write("Starting scraping data...")
        self.nexa()
        self.arena()
        self.stdout.write("Finished scraping data.")

        self.stdout.write("Starting fetching data...")
        self.comments()
        self.stdout.write("Finished fetching data.")


    def nexa(self):
        urls = ['https://www.nexaexperience.com/fronx/specifications#element_submenu',
                'https://www.nexaexperience.com/invicto/specifications#element_submenu',
                'https://www.nexaexperience.com/jimny/specifications#element_submenu',
                'https://www.nexaexperience.com/grand-vitara/specifications#element_submenu',
                'https://www.nexaexperience.com/xl6/specifications#element_submenu',
                'https://www.nexaexperience.com/ignis/specifications#element_submenu',
                'https://www.nexaexperience.com/baleno/specifications#element_submenu',
                'https://www.nexaexperience.com/ciaz/specifications#element_submenu'
               ]

        for url in urls:
            response = requests.get(url)
        
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                Spec_tables = soup.find_all('div', class_='specTableComn')
                Length = Width = Height = Wheelbase = Boot_Space = Seating_Capacity = Turning_Radius = None
                name = url.split('/')
                self.list.append(name[3])
                for Spec_table in Spec_tables:
                    for table in Spec_table.find_all('table'):
                        for tab in table.find_all('tr'):
                            values = [td.text.strip() for td in tab.find_all('td')]
                            if values:
                                if 'Length' in values[0]:
                                    Length = values[1]
                                    if 'x' in Length:
                                        Length = Length.split('x')[0]
                                    Length = remove_alphabet_and_symbols(Length)
                                if 'Width' in values[0]:
                                    Width = values[1]
                                    if 'x' in Width:
                                        Width = Width.split('x')[1]
                                    Width = remove_alphabet_and_symbols(Width)
                                if 'Height' in values[0]:
                                    Height = values[1]
                                    if 'x' in Height:
                                        Height = Height.split('x')[2]
                                    Height = remove_alphabet_and_symbols(Height)
                                if 'Wheelbase' in values[0]:
                                    Wheelbase = values[1]
                                    Wheelbase = remove_alphabet_and_symbols(Wheelbase)
                                if 'Boot Space' in values[0]:
                                    Boot_Space = values[1]
                                    Boot_Space = remove_alphabet_and_symbols(Boot_Space)
                                if 'Seating Capacity' in values[0]:
                                    Seating_Capacity = values[1]
                                    Seating_Capacity = remove_alphabet_and_symbols(Seating_Capacity)
                                if 'Min. Turning Radius' in values[0]:
                                    Turning_Radius = values[1]
                                    Turning_Radius = remove_alphabet_and_symbols(Turning_Radius)

            Dimensions.objects.update_or_create(Modelname=name[3],
                                            defaults={
                                                'Length': Length,
                                                'Width': Width,
                                                'Height': Height,
                                                'Wheelbase': Wheelbase,
                                                'Boot_Space': Boot_Space,
                                                'Seating_Capacity': Seating_Capacity,
                                                'Turning_Radius': Turning_Radius
                                            }
                                        )
            
    def arena(self):
        arenas=['https://www.marutisuzuki.com/celerio',
                'https://www.marutisuzuki.com/wagonr',
                'https://www.marutisuzuki.com/s-presso',
                'https://www.marutisuzuki.com/ertiga',
                'https://www.marutisuzuki.com/alto-k10',
                'https://www.marutisuzuki.com/brezza',
                'https://www.marutisuzuki.com/eeco',
                'https://www.marutisuzuki.com/dzire'
                ]
        for arena in arenas:
            response = requests.get(arena)

            # Check if the request was successful
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                Spec_tables = soup.find_all('div', class_='display-cell')
                
                # Initialize variables to hold vehicle dimensions
                Length = Width = Height = Wheelbase = Boot_Space = Seating_Capacity = Turning_Radius = None
                name = arena.split('/')
                self.list.append(name[3])
                # Loop through each spec table
                for Spec_table in Spec_tables:
                    h4_tag = Spec_table.find('h4')
                    p_tag = Spec_table.find('p')

                    # Ensure both tags exist before accessing their text
                    if h4_tag and p_tag:
                        if 'Length' in h4_tag.text:
                            Length = p_tag.text.strip()
                            if 'x' in Length:
                                Length = Length.split('x')[0]
                            Length = remove_alphabet_and_symbols(Length)
                        elif 'Width' in h4_tag.text:
                            Width = p_tag.text.strip()
                            if 'x' in Width:
                                Width = Width.split('x')[1]
                            Width = remove_alphabet_and_symbols(Width)
                        elif 'Height' in h4_tag.text:
                            Height = p_tag.text.strip()
                            if 'x' in Height:
                                Height = Height.split('x')[2]
                            Height = remove_alphabet_and_symbols(Height)
                        elif 'Wheelbase' in h4_tag.text:
                            Wheelbase = p_tag.text.strip()
                            Wheelbase = remove_alphabet_and_symbols(Wheelbase)
                        elif 'Boot Space' in h4_tag.text:
                            Boot_Space = p_tag.text.strip()
                            Boot_Space = remove_alphabet_and_symbols(Boot_Space)
                        elif 'Seating Capacity' in h4_tag.text:
                            Seating_Capacity = p_tag.text.strip()
                            Seating_Capacity = remove_alphabet_and_symbols(Seating_Capacity)
                        elif 'Min. Turning Radius' in h4_tag.text:
                            Turning_Radius = p_tag.text.strip()
                            Turning_Radius = remove_alphabet_and_symbols(Turning_Radius)

            Dimensions.objects.update_or_create(Modelname=name[3],
                                                defaults={
                                                    'Length': Length,
                                                    'Width': Width,
                                                    'Height': Height,
                                                    'Wheelbase': Wheelbase,
                                                    'Boot_Space': Boot_Space,
                                                    'Seating_Capacity': Seating_Capacity,
                                                    'Turning_Radius': Turning_Radius
                                                })
            
    def comments(self):
        api_key = settings.YOUTUBE_API_KEY
        for search_term in self.list:
            # Step 1: Search for videos
            search_url = "https://www.googleapis.com/youtube/v3/search"
            search_params = {
                'part': 'id,snippet',
                'q': search_term,
                'type': 'video',
                'key': api_key,
                'maxResults': 50,
            }
            try:
                response = requests.get(search_url, params=search_params)
                response.raise_for_status()
                search_results = response.json()
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Error fetching search results for '{search_term}': {e}"))
                continue  # Skip to the next search term
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"Error parsing JSON response for '{search_term}': {e}"))
                continue

            for item in search_results.get('items', []):
                video_id = item['id'].get('videoId')
                title = item['snippet'].get('title')

                if video_id:
                    # Step 2: Get video statistics
                    video_info_url = "https://www.googleapis.com/youtube/v3/videos"
                    video_info_params = {
                        'part': 'statistics',
                        'id': video_id,
                        'key': api_key,
                    }

                    try:
                        video_info_response = requests.get(video_info_url, params=video_info_params)
                        video_info_response.raise_for_status()
                        video_info = video_info_response.json()
                    except requests.exceptions.RequestException as e:
                        self.stdout.write(self.style.ERROR(f"Error fetching video info for video '{video_id}': {e}"))
                        continue
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(f"Error parsing JSON response for video '{video_id}': {e}"))
                        continue

                    stats = video_info['items'][0].get('statistics', {})
                    view_count = int(stats.get('viewCount', 0))
                    like_count = int(stats.get('likeCount', 0))
                    comment_count = int(stats.get('commentCount', 0))

                    dimension_instance, created = Dimensions.objects.get_or_create(Modelname=search_term)

                    if view_count > 1_000_000:
                        # Save video data to the database if not already exists
                        video, created = YouTubeVideo.objects.update_or_create(
                            video_id=video_id,
                            defaults={
                                'model': dimension_instance,
                                'title': title,
                                'view_count': view_count,
                                'like_count': like_count,
                                'comment_count': comment_count,
                            }
                        )

                        # Step 3: Get comments
                        comments_url = "https://www.googleapis.com/youtube/v3/commentThreads"
                        comments_params = {
                            'part': 'snippet',
                            'videoId': video_id,
                            'key': api_key,
                            'maxResults': 100,  # Get up to 100 comments
                        }
                        comments_fetched = False
                        try:
                            comments_response = requests.get(comments_url, params=comments_params)
                            comments_response.raise_for_status()
                            comments_data = comments_response.json()
                        except requests.exceptions.RequestException as e:
                            self.stdout.write(self.style.ERROR(f"Error fetching comments for video '{video_id}': {e}"))
                            YouTubeVideo.objects.filter(video_id=video_id).delete()
                            continue
                        except ValueError as e:
                            self.stdout.write(self.style.ERROR(f"Error parsing JSON response for comments on video '{video_id}': {e}"))
                            continue

                        for comment_item in comments_data.get('items', []):
                            comment_snippet = comment_item.get('snippet', {}).get('topLevelComment', {}).get('snippet', {})
                            author = comment_snippet.get('authorDisplayName')
                            comment_text = comment_snippet.get('textDisplay')
                            like_count = comment_snippet.get('likeCount', 0)
                            category = 'general'
                            themes = {
                                'exterior': ['look', 'design', 'style', 'appearance', 'paint', 'color'],
                                'interior': ['seat', 'dashboard', 'interior', 'cabin', 'material'],
                                'comfort': ['comfort', 'ride', 'smooth', 'cushion', 'soft'],
                                'engine': ['engine', 'power', 'horsepower', 'torque'],
                                'suspension': ['suspension', 'shock', 'absorber', 'ride'],
                                'performance': ['performance', 'speed', 'handling', 'acceleration'],
                                'quality': ['build', 'rating', 'ncap', 'quality']
                            }

                            # Step 4: Sentiment analysis
                            if comment_text:
                                comments_fetched = True
                                sentiment_result = TextBlob(comment_text)
                                sentiment = 'Neutral'
                                if sentiment_result.sentiment.polarity > 0:
                                    sentiment = 'Positive'
                                elif sentiment_result.sentiment.polarity < 0:
                                    sentiment = 'Negative'
                                
                                comment = re.sub(r'[^a-zA-Z\s\W]', '', comment_text.lower())
                                for theme, keywords in themes.items():
                                    if any(keyword in comment for keyword in keywords):
                                        category = theme
                                        break

                                # Save comment data to the database if not already exists
                                print(category)
                                if category:
                                    YouTubeComment.objects.update_or_create(
                                        video=video,
                                        text=comment_text,
                                        defaults={
                                            'author': author,
                                            'like_count': like_count,
                                            'sentiment': sentiment,
                                            'category': category,
                                        }
                                    )
                            if not comments_fetched:
                            # Delete the video if no comments were fetched
                                video.delete()
                                self.stdout.write(self.style.WARNING(f"No comments fetched for video '{video_id}'. Video deleted."))

            self.stdout.write(self.style.SUCCESS('Data fetched successfully!'))
