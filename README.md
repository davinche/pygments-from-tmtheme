tmTheme to Pygment Styles (CSS)
===============================

Here is a stupid script that makes a "best attempt" at extracting 
textmate/sublime colour themes and converts them into a pygment style 
to be used with Jekyll and what-have-you.

Theme files that have been tested (a very limited selection) with this script
are ones that are found at:

<http://tmtheme-editor.herokuapp.com/>

##Usage##

Run `python tmTheme2pygment.py inputColourScheme.tmTheme ~/Desktop/output.css`
Replace the first argument with the location of the tmTheme file you downloaded from the link above.
Replace the second argument with where you want to output the css file.
