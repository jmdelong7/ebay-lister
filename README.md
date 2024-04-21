# ebay_lister

## Some important notes:

This is all personalized for my system, you can modify it and feel free to use whatever is in this project however you want. As of right now I do not plan on updating or maintaining this project.

The list.py script will look for exact name matches for templates on ebay using the excel column named  “category”. I do this for 2 reasons:

Firstly, it eliminates having to search for categories and have varying item specifics filled out. It is the quickest way to go to the listing page without having to look anything up. Overall, it improves reliability and repeatability. 

Secondly, I am able to have default values for different templates so when I or a virtual assistant goes through the listing they know what is already filled out and/or what needs to be added. The script is also tuned to take these default values into consideration. For instance, it skips changing the condition if the condition of the item is pre-owned since that is the default for all my templates.

I take a black photo after I’m done with photos for each listing. I put my phone face down on the table and snap a photo. The data.py script separates each set of item photos based on this photo. The scripts will not work unless there are black photos which separate item photo sets.

The shipping policy names I have set up are ground, padded, envelope, and priority.

The possible conditions are pre-owned, new with defects, new without tags, and new with tags. If an item is in the sports category, I have defaults in templates set to used and it will only change it if an item is new with tags.

The size, color, and materials will not be selected if they are not in the dropdown when they are searched for in the ebay listing. They must be separated by commas in each of their excel columns and for size and color it will always take the first value. All values are put in the main description. The ChatGPT tool takes care of separating them out by commas.

## Here is how I use these files:

Once all data is filled out in the Excel spreadsheet I open the change_me file and change the file paths so they match where the spreadsheet I just filled out is and where I want the new Excel spreadsheet with changes to be. 

That is, I change the excel_file variable to the location of the Excel spreadsheet I just filled out. And I change the excel_file_new variable to where I want the new Excel spreadsheet (with changes my script will make) to be. I just change the file paths in between the quotes.

I make sure the photos_folder location is the right path with all the photos I took for this session.

I open the data.py file and run it. If all goes well, there are no errors and a new file will be created and I can now run list.py.

Upon running it, I sign in manually and then press enter on the terminal next to where it says, “Press enter when logged in.” and away it goes. I leave the browser visible while it is running so google chrome or my computer doesn’t slow down since it is out of view.



