# ```linkedin-markdownificator```
As the name suggests, you can use this tool to export your LinkedIn profile to Markdown. From there you can export it to PDF however you like.

>[!IMPORTANT]
> Without access to the API, this was developed using a ```selenium``` webdriver and manually downloading the source HTML for each page. This means that it can easily break if LinkedIn changes its interface.

See my CV as example in [Markdown](https://github.com/rifusaki/linkedin-markdownificator/blob/main/examples/example-default.md) or .

## Basic usage
- Clone the repo
- Add your credentials to ```.env```
- Run ```main.py```

### Templates
There are currently two templates: ```default_template.md``` and ```peppermint.md```. In order to switch between them go to ```markdownify()``` in [```processer.py```](https://github.com/rifusaki/linkedin-markdownificator/blob/main/utils/processer.py). These are some examples:

#### ```peppermint```
This template was designed with the usage of Jekyll in mind. I use [```minimal-mistakes```](https://github.com/mmistakes/minimal-mistakes) for the live version (which can also be saved to PDF):
- [Live](https://rifusaki.co/CV/)

And this is the result using only a basic PDF exporter:
- [Markdown](https://github.com/rifusaki/linkedin-markdownificator/blob/main/examples/example-peppermint.md)
- [PDF](https://github.com/rifusaki/linkedin-markdownificator/blob/main/examples/example-peppermint.pdf)

#### ```default_template```
- [Markdown](https://github.com/rifusaki/linkedin-markdownificator/blob/main/examples/example-default.md)
- [PDF](https://github.com/rifusaki/linkedin-markdownificator/blob/main/examples/example-default.pdf)

## FAQ
#### Just... why?
Mostly because updating both my LinkedIn profile and a separate CV sounds redundant. Tools like the now deprecated [LinkedIn2Md](https://github.com/fkztw/linkedin2md) only used the public profile which is quite incomplete. I wanted the full data.

#### Why not use the API?
Pretty much because, as far as I know, I can't. In order to get access to the Member Data Portability API, I need to have a legally registered company (see [the documentation](https://learn.microsoft.com/en-us/linkedin/dma/member-data-portability/member-data-portability-3rd-party/)). Or, as the access request form kindly puts it:

>  Please note that this product is only available for legal registered entities (e.g. LLC, Corporations, 501(c), etc.) and not individual developers.

## Known issues
- When projects are not associated with any experience or education, incorrect information is retrieved.
