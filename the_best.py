
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: n10204458
#    Student name: Jackson Doring
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  The Best, Then and Now
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application that allows the user to preview and print lists of
#  top-ten rankings.  See the instruction sheet accompanying this
#  file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.  YOU MAY NOT USE
# ANY NON-STANDARD MODULES SUCH AS 'Beautiful Soup' OR 'Pillow'.  ONLY
# MODULES THAT COME WITH A STANDARD PYTHON 3 INSTALLATION MAY BE
# USED.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.)
from tkinter import *

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *
import webbrowser


#
#--------------------------------------------------------------------#



#-----Downloader Function--------------------------------------------#
#
# This is our function for downloading a web page's content and both
# saving it on a local file and returning its source code
# as a Unicode string. The function tries to produce a
# meaningful error message if the attempt fails.  WARNING: This
# function will silently overwrite the target file if it
# already exists!  NB: You should change the filename extension to
# "xhtml" when downloading an XML document.  (You do NOT need to use
# this function in your solution if you choose to call "urlopen"
# directly, but it is provided for your convenience.)
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html'):

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        web_page = urlopen(url)
    except ValueError:
        raise Exception("Download error - Cannot find document at URL '" + url + "'")
    except HTTPError:
        raise Exception("Download error - Access denied to document at URL '" + url + "'")
    except:
        raise Exception("Download error - Something went wrong when trying to download " + \
                        "the document at URL '" + url + "'")

    # Read its contents as a Unicode string
    try:
        web_page_contents = web_page.read().decode('UTF-8')
    except UnicodeDecodeError:
        raise Exception("Download error - Unable to decode document at URL '" + \
                        url + "' as Unicode text")

    # Write the contents to a local text file as Unicode
    # characters (overwriting the file if it
    # already exists!)
    try:
        text_file = open(target_filename + '.' + filename_extension,
                         'w', encoding = 'UTF-8')
        text_file.write(web_page_contents)
        text_file.close()
    except:
        raise Exception("Download error - Unable to write to file '" + \
                        target_file + "'")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

##### DEVELOP YOUR SOLUTION HERE #####

#Creating the Tk window for selecting lists
window = Tk()
#Naming the window
window.title('Then Best Then and Now')

#Storing all of the URLs for where data will be drawn from
Song_URL = 'https://en.wikipedia.org/wiki/List_of_most-streamed_songs_on_Spotify'
Movie_URL = 'https://www.imdb.com/chart/moviemeter'
TV_URL = 'https://www.imdb.com/chart/tvmeter'

TV_Image_URL = 'http://www.iconarchive.com/show/popcorn-icons-by-thvg/TV-Shows-icon.html'
Movie_Image_URL = 'https://www.deviantart.com/hazza42/art/Camera-Photoreel-162246316'
Song_Image_URL = 'https://library.lapeer.org/children/images/music.png/image_view_fullscreen'

#Storing the radio button selection as a string
Selection = StringVar()

#This function will run whenever the user presses the Preview button
def preview_lists():

    #Checking which radio button the user has selected
    selected_list = Selection.get()

    #Selecting the correct URL or file to open depending on the list the they chose and if they chose Live or Previous
    if selected_list == 'Current Most Played Songs':
        #Opening the URL that correlates to the selected list
        html_file = urlopen(Song_URL)
        #Reading the opened URL
        html_code = html_file.read().decode('UTF-8')
    elif selected_list == 'Current Most Watched Movies':
        html_file = urlopen(Movie_URL)
        html_code = html_file.read().decode('UTF-8')
    elif selected_list == 'Current Most Watched TV Shows':
        html_file = urlopen(TV_URL)
        html_code = html_file.read().decode('UTF-8')
    else:
        #Opening the static file for the list that user has selected
        html_file = 'Archive/' + selected_list +'.html'
        #Reading the file that was selected
        html_code = open(html_file, encoding = 'utf-8').read()


    #Selecting a different findall function depending on which list the user selected
    if selected_list in ('Previous Most Played Songs', 'Current Most Played Songs'):
        #Selecting only the list from the html file
        find_list = findall('.>([a-zA-Z]+.[a-zA-Z ].*)</a>.</td>', html_code)
    elif selected_list in ('Previous Most Watched Movies', 'Current Most Watched Movies'):
        #Selecting only the list from the html file
        find_list = findall('>([a-zA-Z ]+)</a>\s*<span', html_code)
    else:
        #Selecting only the list from the html file
        find_list = findall('.>([a-zA-Z. ]+)</a>\s+<span', html_code)

    #Creating a new window to display the preview list that the user has selected
    preview_window = Tk()
    #Naming the window as the list that was selected
    preview_window.title(selected_list)

    #Creating and placing the heading for the window
    window_header = Label(preview_window, bg = 'orange', fg = 'white', text = selected_list, font = ('Arial', 35))
    window_header.grid(row = 1, column = 1, sticky = EW)

    #Setting and placing the text that will be used to display the list
    list_text = Text(preview_window, font = ('Arial', 25))
    list_text.grid(row = 2, column = 1, sticky = E)

    #Outputting the list that was found using the finall function and placing it in the window
    numbering = 1
    for top_ten in find_list[0:10]:
        list_text.insert(END, str(numbering) + '. ' + top_ten + '\n')
        numbering = numbering + 1


#This function will run whenever the user presses the Export button
def export_lists():
    
    #Checking which radio button the user has selected
    selected_list = Selection.get()

    #Selecting the correct URL or file to open depending on the list the they chose and if they chose Live or Previous
    if selected_list == 'Current Most Played Songs':
        #Opening the URL that correlates to the selected list
        html_file = urlopen(Song_URL)
        #Reading the opened URL
        html_code = html_file.read().decode('UTF-8')
        #Storing the data from the website for later use
        data_source = Song_URL
        #Closing down the website
        html_file.close()
    elif selected_list == 'Current Most Watched Movies':
        html_file = urlopen(Movie_URL)
        html_code = html_file.read().decode('UTF-8')
        data_source = Movie_URL
        html_file.close()
    elif selected_list == 'Current Most Watched TV Shows':
        html_file = urlopen(TV_URL)
        html_code = html_file.read().decode('UTF-8')
        data_source = TV_URL
        html_file.close()
    else:
        #Opening the static file for the list that user has selected
        html_file = 'Archive/' + selected_list +'.html'
        #Reading the file that was selected
        html_code = open(html_file, encoding = 'utf-8').read()
        #Storing that data for later use
        data_source = html_file
        
   #Selecting a different findall function depending on which list the user selected
    if selected_list in ('Previous Most Played Songs', 'Current Most Played Songs'):
        #Selecting only the list from the html file
        find_list = findall('.>([a-zA-Z]+.[a-zA-Z ].*)</a>.</td>', html_code)
        #Finding the number of streams that the songs have 
        find_attribute = findall('center">([0-9,]+)</td>', html_code)
        #Finding the date of when the information was last updated
        find_date = findall('8pt;">([a-zA-z0-9, ]+)', html_code)
        find_date = find_date[0]

        #Opening the URL that contains the image
        image_file = urlopen(Song_Image_URL)
        #Reading the opened URL
        image_code = image_file.read().decode('UTF-8')
        #Finding the image on the website
        find_image = findall('<img.* src="([^"]+)"',image_code)
        #Closing down the website
        image_file.close()
        
    elif selected_list in ('Previous Most Watched Movies', 'Current Most Watched Movies'):
        #Selecting only the list from the html file
        find_list = findall('>([a-zA-Z. ]+.[a-zA-Z. ].*)</a>\s*<span', html_code)
        #Finding the cover images for the movies on the website
        find_attribute = findall('<img.* src="([^"]+)".* width="45".*>', html_code)
        #Setting the date for the Previous list as when the list was downloaded because IMDb doesn't state when lists are updated
        if selected_list == 'Previous Most Watched Movies':
            find_date = 'As of 25th September, 2018'
        #Setting the date for the Current list as the current date
        else:
            find_date = 'As of ' + datetime.date.today().strftime('%d/%m/%Y')

        #Opening the URL that contains the image
        image_file = urlopen(Movie_Image_URL)
        #Reading the opened URL
        image_code = image_file.read().decode('UTF-8')
        #Finding the image on the website, have to make the search very specific because there are a lot of similar images
        find_image = findall('<img collect_rid="1:162246316" src="(https://pre00.deviantart.net/be3f/th/pre/i/2010/118/f/a/camera_photoreel_by_hazza42.jpg)"',image_code)
        #Closing down the website
        image_file.close()
        
    else:
        #Selecting only the list from the html file
        find_list = findall('.>([a-zA-Z. ]+)</a>\s+<span', html_code)
        #Finding the IMDb rating for all of the TV shows on the website
        find_attribute = findall('ratings">([0-9.]+)</strong>', html_code)
        #Setting the date for the Previous list as when the list was downloaded because IMDb doesn't state when lists are updated
        if selected_list == 'Previous Most TV Shows':
            find_date = 'As of 25th September, 2018'
        #Setting the date for the Current list as the current date
        else:
            find_date = 'As of ' + datetime.date.today().strftime('%d/%m/%Y')

        #Opening the URL that contains the image
        image_file = urlopen(TV_Image_URL)
        #Reading the opened URL
        image_code = image_file.read().decode('UTF-8')
        #Finding the image on the website, searching for a specific URL because there are a lot of very similar URLs in the website
        find_image = findall('<img src="(http://icons.iconarchive.com/icons/thvg/popcorn/256/TV-Shows-icon.png)"',image_code)
        #Closing down the website
        image_file.close()

    #Creating a html file for the list to be viewed in
    webpage_file = selected_list + '.html'
    #Opening the html file so it can be written into
    live_html_file = open(webpage_file, 'w')

    #Setting variables for the table titles in the Exported lists
    column_title_one = ''
    column_title_two = ''
    column_title_three = ''

    #Changing what the titles of the table is going to be in the Exported list depending on the list the user has selected
    if selected_list in ('Previous Most Played Songs', 'Current Most Played Songs'):
        column_title_one = 'Rank'
        column_title_two = 'Song Title'
        column_title_three = 'Number of Streams on Spotify (Millions)'
    elif selected_list in ('Previous Most Watched Movies', 'Current Most Watched Movies'):
        column_title_one = 'Rank'
        column_title_two = 'Poster'
        column_title_three = 'Movie Title'
    else:
        column_title_one = 'Rank'
        column_title_two = 'TV Show Title'
        column_title_three = 'IMDb Rating'
        
    #Putting the html header into the file
    live_html_file.write('''<!DOCTYPE html>
<html>

    <head>
        <title>Title</title>
    </head>
    
    <body>
        <!-----------styling elements of the website------------------------>
        <style>
            tr{
                font-size: 30px;
            }
            table, td, th{
                border: 1px solid black;
                border-collapse: collapse;
                padding: 30px;
                text-align: center;
            }
            h1{
                text-align: center;
                font-size: 60px;
                padding: 20px;
            }
            p{
                text-align: center;
            }
            h2{
                text-align: center;
                font-size: 30px;
            }
            img{
                display: block;
                margin-left: auto;
                margin-right: auto;
                max-width: 40%;
                padding: 40px;
            }
        </style>

        <h1>Title</h1>

        <h2>Date</h2>

        <img src ="Image">

        <!--------------Creating the table where the information will be presented------------------------->
        <table align = 'center'>
            <tr>
                <th>One</th>
                <th>Two</th>
                <th>Three</th>
            <tr>
'''
    #Replacing titles, headings, and images from the html with the correct ones that should be displayed depending on the list the user has selected
    .replace('Title', 'Top 10 ' + selected_list).replace('One', column_title_one).replace('Two', column_title_two).replace('Three', column_title_three).replace('Date', str(find_date)).replace('Image', find_image[0]))

    #Only choosing the first 10 from the list and giving them the corresponding number
    numbering = 1
    for top_ten in find_list[0:10]:
        
        #Writting all of the lists, attributes, and dates of the selected list into the appropriate html file
        if selected_list in ('Previous Most Played Songs', 'Current Most Played Songs'): 
            live_html_file.write('\t\t\t<tr>\n\t\t\t\t<td>' + str(numbering) +  '. ' + '</td>\n\t\t\t\t<td>' + top_ten + '</td>\n\t\t\t\t<td>' + find_attribute[numbering - 1] + '</td>\n\t\t\t</tr>\n')  
            numbering = numbering + 1
            
        elif selected_list in ('Previous Most Watched Movies', 'Current Most Watched Movies'):
            live_html_file.write('\t\t\t<tr>\n\t\t\t\t<td>' + str(numbering) +  '. ' + '</td>\n\t\t\t\t<td>' + '<img src ="' + find_attribute[numbering - 1] + '" width="90" height="134">\t' + '</td>\n\t\t\t\t<td>' + top_ten + '</td>\n\t\t\t</tr>\n')  
            numbering = numbering + 1
            
        else:
            live_html_file.write('\t\t\t<tr>\n\t\t\t\t<td>' + str(numbering) +  '. ' + '</td>\n\t\t\t\t<td>' + top_ten + '</td>\n\t\t\t\t<td>' + find_attribute[numbering - 1] + '</td>\n\t\t\t</tr>\n')  
            numbering = numbering + 1

    #Ending the body and html tags in the file
    live_html_file.write('''
         </table>
         <p> The data provided is sourced from ''' + str(data_source) + ''' </p>
    </body>

</html>''')

    #Closing down the html file
    live_html_file.close()
    #Opening the html file for the user to see
    webbrowser.open(selected_list + '.html')
    
    
def save_lists():
    #Checking which radio button the user has selected
    selected_list = Selection.get()

    #Selecting the correct URL or file to open depending on the list the they chose and if they chose Live or Previous
    if selected_list == 'Current Most Played Songs':
        #Opening the URL that correlates to the selected list
        html_file = urlopen(Song_URL)
        #Reading the opened URL
        html_code = html_file.read().decode('UTF-8')
        #Storing the data from the website for later use
        data_source = Song_URL
        #Closing down the website
        html_file.close()
    elif selected_list == 'Current Most Watched Movies':
        html_file = urlopen(Movie_URL)
        html_code = html_file.read().decode('UTF-8')
        data_source = Movie_URL
        html_file.close()
    elif selected_list == 'Current Most Watched TV Shows':
        html_file = urlopen(TV_URL)
        html_code = html_file.read().decode('UTF-8')
        data_source = TV_URL
        html_file.close()
    else:
        #Opening the static file for the list that user has selected
        html_file = 'Archive/' + selected_list +'.html'
        #Reading the file that was selected
        html_code = open(html_file, encoding = 'utf-8').read()
        #Storing that data for later use
        data_source = html_file
        
   #Selecting a different findall function depending on which list the user selected
    if selected_list in ('Previous Most Played Songs', 'Current Most Played Songs'):
        #Selecting only the list from the html file
        find_list = findall('.>([a-zA-Z]+.[a-zA-Z ].*)</a>.</td>', html_code)
        #Finding the number of streams that the songs have 
        find_attribute = findall('center">([0-9,]+)</td>', html_code)
        #Finding the date of when the information was last updated
        find_date = findall('8pt;">([a-zA-z0-9, ]+)', html_code)
        find_date = find_date[0]

        #Opening the URL that contains the image
        image_file = urlopen(Song_Image_URL)
        #Reading the opened URL
        image_code = image_file.read().decode('UTF-8')
        #Finding the image on the website
        find_image = findall('<img.* src="([^"]+)"',image_code)
        #Closing down the website
        image_file.close()
        
    elif selected_list in ('Previous Most Watched Movies', 'Current Most Watched Movies'):
        #Selecting only the list from the html file
        find_list = findall('>([a-zA-Z. ]+.[a-zA-Z. ].*)</a>\s*<span', html_code)
        #Finding the cover images for the movies on the website
        find_attribute = findall('<img.* src="([^"]+)".* width="45".*>', html_code)
        #Setting the date for the Previous list as when the list was downloaded because IMDb doesn't state when lists are updated
        if selected_list == 'Previous Most Watched Movies':
            find_date = 'As of 25th September, 2018'
        #Setting the date for the Current list as the current date
        else:
            find_date = 'As of ' + datetime.date.today().strftime('%d/%m/%Y')

        #Opening the URL that contains the image
        image_file = urlopen(Movie_Image_URL)
        #Reading the opened URL
        image_code = image_file.read().decode('UTF-8')
        #Finding the image on the website, have to make the search very specific because there are a lot of similar images
        find_image = findall('<img collect_rid="1:162246316" src="(https://pre00.deviantart.net/be3f/th/pre/i/2010/118/f/a/camera_photoreel_by_hazza42.jpg)"',image_code)
        #Closing down the website
        image_file.close()
        
    else:
        #Selecting only the list from the html file
        find_list = findall('.>([a-zA-Z. ]+)</a>\s+<span', html_code)
        #Finding the IMDb rating for all of the TV shows on the website
        find_attribute = findall('ratings">([0-9.]+)</strong>', html_code)
        #Setting the date for the Previous list as when the list was downloaded because IMDb doesn't state when lists are updated
        if selected_list == 'Previous Most TV Shows':
            find_date = 'As of 25th September, 2018'
        #Setting the date for the Current list as the current date
        else:
            find_date = 'As of ' + datetime.date.today().strftime('%d/%m/%Y')
    
    connection = connect(database = 'top_ten.db')
    cursor = connection.cursor()

    numbering = 1
    for top_ten in find_list[0:10]:
        sql = "INSERT INTO top_ten VALUES('"+ str(find_date) +"', '" + str(numbering) + "', '" + top_ten + "', '" + find_attribute[numbering - 1] + "')"
        cursor.execute(sql)
        numbering = numbering + 1
        
    
    connection.commit()
    cursor.close()
    connection.close()

#Setting the GUI for all of the windows--------------------------------------------------------------------------------------------------------------
#Creating label frames to house the radio buttons
song_selection = LabelFrame(window, text = 'Most Played Songs')
movie_selection = LabelFrame(window, text = 'Most Watched Movies')
TV_selection = LabelFrame(window, text = 'Best Televsion Shows')

#Using Grid Geometry Manager to place the labels into the window
label_margin = 15
song_selection.grid(padx = label_margin, pady = label_margin, row = 2, column = 1, columnspan = 2)
movie_selection.grid(padx = label_margin, pady = label_margin, row = 3, column = 1, columnspan = 2)
TV_selection.grid(padx = label_margin, pady = label_margin, row = 4, column = 1, columnspan = 2)

#Creating the canvas for the images inside the windows
image_canvas = Canvas(width = 500, height = 500)
image_canvas.grid(row = 1, column = 3, rowspan = 6)
window_image = PhotoImage(file = 'Images/logo.gif')
image_canvas.create_image(150, 250, image = window_image)

#Creating the heading for the main window
heading = Label(window, text = 'The Best and Now')
heading.grid(row = 1, column = 2, pady = 20, padx = 80)
heading.config(font=("Arial", 44))

#Creating Radio Buttons for selecting which list the user wants
song_static_top10 = Radiobutton(song_selection, text = 'Previous', value = 'Previous Most Played Songs', variable = Selection)
song_live_top10 = Radiobutton(song_selection, text = 'Current', value = 'Current Most Played Songs', variable = Selection)
movie_static_top10 = Radiobutton(movie_selection, text = 'Previous', value = 'Previous Most Watched Movies', variable = Selection)
movie_live_top10 = Radiobutton(movie_selection, text = 'Current', value = 'Current Most Watched Movies', variable = Selection)
TV_static_top10 = Radiobutton(TV_selection, text = 'Previous', value = 'Previous Most Watched TV Shows', variable = Selection)
TV_live_top10 = Radiobutton(TV_selection, text = 'Current', value = 'Current Most Watched TV Shows', variable = Selection)

#Using Grid Geometry Manager to place the radio buttons into the frame
song_static_top10.grid(row = 1, column = 1)
song_static_top10.select()
song_live_top10.grid(row = 1, column = 2)
movie_static_top10.grid(row = 1, column = 1)
movie_live_top10.grid(row = 1, column = 2)
TV_static_top10.grid(row = 1, column = 1)
TV_live_top10.grid(row = 1, column = 2)

#Creating the 'Export' and 'Preview' buttons
preview_button = Button(window, text = 'Preview', width = 18, height = 2, command = preview_lists)
export_button = Button(window, text = 'Export', width = 18, height = 2, command = export_lists)
save_button = Button(window, text = 'Save', width = 18, height = 2, command = save_lists)

#Using Geometry Manager to place 'Export' and 'Preview' buttons in the window
button_margin = 10
preview_button.grid(pady = button_margin, row = 5, column = 1, columnspan = 2)
export_button.grid(pady = button_margin, row = 6, column = 1, columnspan = 2)
save_button.grid(pady = button_margin, row = 7, column = 1, columnspan = 2)





