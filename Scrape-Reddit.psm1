function Scrape-Reddit() {
  param (
    [string]$Subreddit = "wallpaper"
  )
  python $PSScriptRoot\scrape_reddit.py -o "$HOME\Downloads\reddit-wallpapers" $Subreddit
}

Set-Alias reddit Scrape-Reddit
