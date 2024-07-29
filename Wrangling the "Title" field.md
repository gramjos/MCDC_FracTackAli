---
tags: [MCDC, FracTracker, data]
---
#### Problem Statement
The field in question, `Title`, has valuable data stored in an unstructured way. 
#### Goal
Come up with enough rules to reliable retrieve specific data if it exists.
#### Hurdles
`Title` field contains ~2,700 records
#### Known Edge Cases
These records are not even close the schema that is loosely used.
- DSC_1344_HighRes 
- DSC_1220_HighRes 
- DJI_0250_HighRes
# Homework for Ted, fix these records!
## Can we have the demo the form to fix these column? Eddie
The below three the title is way off...
https://www.flickr.com/photos/fractracker/53183405100/in/album-72157715839488573
https://www.flickr.com/photos/fractracker/53183405215/in/album-72157715839488573
https://www.flickr.com/photos/fractracker/53399929386/in/album-72157715916543893

#### Data exclusion decisions
- The date is irrelevant because we already get that information in the `Date_taken` column
- The state or county information is irrelevant because it can be derived from the coordinates
**Note**, `Date_taken` is derived from the from coordinates. Meaning, photos with no coordinates will have no `Date_taken`. So the data exclusion decisions depend on (are only valid if) the API call disregards the photos with no coordinates. 

###### Records that have issue with month/season
[https://www.flickr.com/photos/fractracker/49728093488/in/album-72157713730887622](https://www.flickr.com/photos/fractracker/49728093488/in/album-72157713730887622) [https://www.flickr.com/photos/fractracker/49728093538/in/album-72157713730887622](https://www.flickr.com/photos/fractracker/49728093538/in/album-72157713730887622) [https://www.flickr.com/photos/fractracker/49728600276/in/album-72157713730887622](https://www.flickr.com/photos/fractracker/49728600276/in/album-72157713730887622) [https://www.flickr.com/photos/fractracker/49728601571/in/album-72157713730887622](https://www.flickr.com/photos/fractracker/49728601571/in/album-72157713730887622) [https://www.flickr.com/photos/fractracker/49785865077/in/album-72157715839488573](https://www.flickr.com/photos/fractracker/49785865077/in/album-72157715839488573)
