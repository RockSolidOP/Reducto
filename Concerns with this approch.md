Concerns with this approch

Each page may need custom regex check for each page #maybe we can standardize this 

If there is the change in way the api responds it will be hard to maintain as the entire code block might have to be changed 

Just page 6 required several lines of code and regex change but if we find a good way to normalize for all types then it might be easier to maintain based in type checks

Sometime the checkboxes repond with key and value embeded in the key

Example of a row from detected table by Reducto

["", "No \u2611", ""]

0th Eliment is Index
1 is supposed to be key
2 is supposed to be Value 

But the value \u2611 which means the checkbox is selected is embedded within the key section of table



