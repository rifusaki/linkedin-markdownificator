# ```linkedin-markdownificator```
As the name suggests, you can use this tool to export your LinkedIn profile to Markdown. Using Pandoc or similar you can also export it to PDF.

>[!IMPORTANT]
> This tool is currently incomplete, albeit functional. Check my to-do at the end of this text.

See [my CV](https://github.com/rifusaki/linkedin-markdownificator/blob/main/examples/example-default.md) as example.

## Usage
- Clone the repo
- Add your credentials to ```.env```
- Run ```main.py```

## FAQ
#### Just... why?
Mostly because updating both my LinkedIn profile and a separate CV sounds redundant. Tools like the now deprecated [LinkedIn2Md](https://github.com/fkztw/linkedin2md) only used the public profile which is quite incomplete. I wanted the full data.

#### Why not use the API?
The whole registration process sounds way too convluted for what is a rather simple thing. Also, I wanted to play with web scraping. However, the current implementation is quite finicky, so I would eventually like to try the API.

## To-Do
- [ ] Fix education section XPATH retrieving unnecesary data
- [ ] Fix about section not being retrieved
- [ ] Add skills section
- [ ] Add more templates
  - [ ] ... something prettier
- [ ] Look into more robust API implementation?