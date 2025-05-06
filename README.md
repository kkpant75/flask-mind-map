# Generate Mind Map for Any JSON Data

This is generic code to generate mind map for any Json Data 

# How To Execute 

- Clone the code as per below
```
git clone 
```
- Execute Application 

```
python mindmap.py
```

# Test With Dummy Data

Open Any Browser and Use the below URL
```
http://localhost:5000
```
# Test Code With Simple Google Web Book Serach

- Open Any Browser and Search Any Book of Your Choice
```
http://localhost:5000/getbook?q=nifi
http://localhost:5000/getbook?q=fiction
```


# Data With Your Choice Using PostMan (POST API)

```
POST http://127.0.0.1:5000/mindmap?root=HL BS
```

- Put Your Data in Body-Raw (Simple Json)
```
{
	"name": "kk2",
	"addressLine1": "26196 Rea Ave",
	"addressLine2": {
		"add1": "sample",
		"add2": {
			"lev1": "sample2",
			"lev3": {
				"lev3": "sample3"
			}
		}
	}
}
```
- or Json Array 
```
[
	{
		"name": "kk2",
		"addressLine1": "26196 Rea Ave",
		"addressLine2": {
			"add1": "sample",
			"add2": {
				"lev1": "sample2",
				"lev3": {
					"lev3": "sample3"
				}
			}
		}
	},
	{
		"volumeInfo": {
			"title": "The Definitive Guide to Power Query (M)",
			"subtitle": "Mastering complex data transformation with Power Query",
			"authors": [
				"Gregory Deckler",
				"Rick de Groot",
				"Melissa de Korte"
			],
			"publisher": "Packt Publishing Ltd",
			"publishedDate": "2024-03-29"
		}
	}
]
```