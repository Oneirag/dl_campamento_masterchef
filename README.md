# Image downloader from campamento masterchef website

This is a helper tool to download pictures from campamento masterchef blog website.

The tool downloads all images at maximum resolution to the images subdirectory. In that directory, 
the tool creates a directory with the camp name, then a directory for the blog entry and places all images there.
Additionaly creates a txt file with the blog entry text.

### Configuration

This tool uses [ong_utils](https://github.com/Oneirag/ong_utils.git) for configuration. Therefore, user needs to configure a `campamento_masterchef.yaml` file like this:
```
campamento_masterchef:
   password: insert_here_the_blog_password
   url: insert_here_the_link_to_the_camp_and_date (e.g. https://blogs.campamentosmasterchef.com/sedano-1-1-2022/)
log: {}
```
