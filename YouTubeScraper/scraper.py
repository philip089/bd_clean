#################################
# Import modules
#################################
import sys
import time
import os
import requests

#################################
# YouTube Sraper Class
#################################

class YouTubeScraper:

    def __init__(self):

        ####################################################################
        # Initialize output directory and retrieve API key and country codes
        ####################################################################

        self.output_dir = 'ScraperData/'
        self.api_key, self.country_codes = self.get_api_key_and_country_codes()

    
    def get_api_key_and_country_codes(self):

        ####################################################################
        # Read API key from a file and set default country codes
        ####################################################################
        
        with open("YouTubeScraper/api_key.txt", 'r') as file:
            api_key = file.readline().strip()

        country_codes = ["US", "DE"]
        return api_key, country_codes
    

    def get_data(self):

        ##############################################################################################
        # Iterate through country codes to fetch data for each country 
        # Country Codes are set in country_codes.txt
        # You can add other Codes like ENG, FR, etc. if you want to receive Data from these countries
        ##############################################################################################

        for country_code in self.country_codes:

            # Fetch data for the specified country
            country_data = YouTubeDataFetcher(self.api_key, country_code).fetch_all()
            # Write fetched data to a file
            self.write_to_file(country_code, country_data)


    def write_to_file(self, country_code, country_data):

        #############################################
        # Write country data to a CSV file
        #############################################

        print(f"Writing {country_code} data to file...")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Change to a+: If you want it all in one CSV-File like DE.csv   I use a+ to append
        # Change to w+: If you want to replace existing file or you choose to create different CSV-Files base on the day
            
        # CountryCode.csv
        with open(f"data/{self.output_dir}/{country_code}.csv", "a+", encoding='utf-8') as file:
            file.write('\n'.join(country_data))

        #Time_CountryCpde.csv    
        with open(f"{self.output_dir}/{time.strftime('%y.%d.%m')}_{country_code}.csv", "w+", encoding='utf-8') as file:
            file.write('\n'.join(country_data))




#################################
# YouTube Data Fetecher Class
#################################


class YouTubeDataFetcher:
    def __init__(self, api_key, country_code):

        #####################################
        # Initialize API key and country code
        #####################################

        self.api_key = api_key
        self.country_code = country_code


    def fetch_all(self):

        ############################################
        # Fetch all videos for the specified country
        ############################################


        # Initialize an empty list to store the country data
        country_data = [",".join(self.get_header())]
        next_page_token = "&"

        # Loop until there are no more pages to fetch
        while next_page_token is not None:

            # Fetch the next page of video data
            video_data_page = self.api_request(next_page_token)

            # Extract the next page token for pagination
            next_page_token = video_data_page.get("nextPageToken")

            # Construct the page token parameter for the next request
            next_page_token = f"&pageToken={next_page_token}&" if next_page_token else None

            # Extract the list of videos from the current page
            items = video_data_page.get('items', [])

            # Process the videos and append the extracted data to the country data list
            country_data += self.get_videos(items)

        return country_data

    def api_request(self, page_token):

        #########################################
        # Make an API request to fetch video data
        #########################################

        # Construct URL
        request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{page_token}chart=mostPopular&regionCode={self.country_code}&maxResults=30&key={self.api_key}"
        request = requests.get(request_url)

        # Check if the request status code indicates a temporary ban (status code 429)
        if request.status_code == 429:
            print("Temp-Banned due to excess requests, please wait and continue later")
            sys.exit()
            
        return request.json()

    def get_header(self):

        #################################
        # Set the Header for the CSV file
        #################################

        return ["video_id", "title", "publishedAt", "channelId", "channelTitle", "categoryId", "trending_date","tags", "view_count", "comment_count", "comments_disabled"]

    def get_videos(self, items):

        #######################
        # Get video information
        #######################

        lines = []

        # Iterate through each video in the list
        for video in items:

            
            comments_disabled = False

            # Skip to the next iteration if 'statistics' key is not present
            if "statistics" not in video:
                continue

            # Extract the video ID from the 'id' field of the video item and prepare it for writing
            video_id = self.prepare_feature(video['id'])

            # Extract the 'snippet' and 'statistics'
            snippet = video['snippet']
            statistics = video['statistics']

            # Extract important features from the 'snippet' object and prepare them for writing
            features = [self.prepare_feature(snippet.get(feature, "")) for feature in self.get_important_features()]

            # Get the current date and format it as 'yy.dd.mm' (year.day.month)
            trending_date = time.strftime("%y.%d.%m")

            # Extract tags from the 'snippet' object and prepare them for writing
            tags = self.get_tags(snippet.get("tags", ["[none]"]))

            # Extract the view count from the 'statistics' object, defaulting to 0 if not present
            view_count = statistics.get("viewCount", 0)

            # Check if 'commentCount' key is present in the 'statistics' object and extract it
            if 'commentCount' in statistics:
                comment_count = statistics['commentCount']
            else:
                # Set the flag to indicate that comments are disabled and set comment count to 0
                comments_disabled = True
                comment_count = 0
            
            # Prepare all the extracted data for writing and join them together as a CSV line
            line = [video_id] + features + [self.prepare_feature(x) for x in [trending_date, tags, view_count, comment_count, comments_disabled]]

            # Append the CSV line to the list of extracted video information
            lines.append(",".join(line))


        # Return the list of extracted video information
        return lines

    def get_important_features(self):

        ###################################
        # Sets the main Columns for the CSV
        ###################################

        return ["title", "publishedAt", "channelId", "channelTitle", "categoryId"]

    def prepare_feature(self, feature):

        # Define a list of unsafe characters that need to be removed from the feature
        unsafe_characters = ['\n', '"']

        # Create a translation table to map each unsafe character to None (indicating removal)
        # X : Replace Y: Replacement Z: Removed
        translation_table = str.maketrans("", "", "".join(unsafe_characters))

        # Convert the feature to a string and remove unsafe characters using the translation table
        feature = str(feature).translate(translation_table)

        return f'"{feature}"'

    def get_tags(self, tags_list):

        ##################################
        # Prepare tags for writing to file
        ##################################
        return self.prepare_feature("|".join(tags_list))

# Main function
if __name__ == "__main__":
    scraper = YouTubeScraper()
    scraper.get_data()


