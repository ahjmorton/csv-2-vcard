# CSV 2 VCard Converter

Small Python script to convert a [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) into [VCard](https://en.wikipedia.org/wiki/VCard)

## Usage
_All data here generated using the amazing [faker.js](https://fakerjs.dev/) library_

Say we have a CSV with the following data saved as `sample.csv`

```
First name,Last name,General mobile,General phone,General email
Roderick,Leannon,022 1260 5488,,Favian37@yahoo.com
Jeannie,,,0800 240 2624,,
Lauren,,024 0735 8784,0386 742 8782,
```
We can run the following:
```
python ./csv2vcard.py sample.csv
```
At present this will create / append to a file called `sample.csv.vcf` which will look like the following:
```
BEGIN:VCARD
VERSION:2.1
N:Leannon;Roderick;;;
FN:Roderick Leannon
TEL;VOICE;CELL:022 1260 5488
EMAIL;INTERNET:Favian37@yahoo.com
END:VCARD
BEGIN:VCARD
VERSION:2.1
N:;Jeannie;;;
FN:Jeannie
TEL;VOICE:0800 240 2624
END:VCARD
BEGIN:VCARD
VERSION:2.1
N:;Lauren;;;
FN:Lauren
TEL;VOICE:0386 742 8782
TEL;VOICE;CELL:024 0735 8784
END:VCARD
```

## Known Issues

Originally this was developed to convert a CSV export from a mobile phone to VCard for migration to a new device. The make / model of the original mobile phone is lost to time. As such it might have a number of rough edges / edge cases.

Below are list of known issues:
- Only UK home / mobile numbers are classified as such. All other formats will be classified as "other". 
- Redirection with stdin and stdout are not supported. 
- Other CSV formats are not handled. This includes other headers being used and other delimiters between fields.